#!/usr/bin/python3
"""Conservative AST/shell reachability, without importing or running traced code.

Unknown conditions select both branches. Only literal evaluation or a structurally
verified fail-closed guard excludes a branch. Filesystem reads always reset facts.
Paths are finite witnesses; recursion is an explicit unresolved cycle, not an
assertion that infinitely many concrete executions have been enumerated.
"""
import argparse
import ast
import builtins
import functools
import hashlib
import json
import math
import operator
from pathlib import Path
import re
import shlex
import sys

UNKNOWN = object()
PRIMITIVES = {'subprocess.' + x for x in ('run','Popen','call','check_call','check_output')}
PRIMITIVES |= {'os.system','os.popen','os.fork','os.forkpty','os.posix_spawn','os.posix_spawnp'}
PRIMITIVES |= {'os.' + x for x in ('execl','execle','execlp','execlpe','execv','execve','execvp','execvpe','spawnl','spawnle','spawnlp','spawnlpe','spawnv','spawnve','spawnvp','spawnvpe')}
LOAD_METHODS = {'read','readline','readlines','read_text','read_bytes','exists','is_file','is_dir','glob','rglob','iterdir','listdir','walk'}
ENGINE = {'memit','rome','util'}


class Value:
    def __init__(self, value=UNKNOWN, symbol='unknown', reasons=()):
        self.value, self.symbol, self.reasons = value, symbol, tuple(dict.fromkeys(reasons))

    def json(self):
        if self.value is UNKNOWN:
            return {'loaded_data': self.symbol, 'reasons': list(self.reasons)}
        if isinstance(self.value, list): return [x.json() for x in self.value]
        if isinstance(self.value, dict): return {str(k):v.json() for k,v in self.value.items()}
        return self.value


def reasons(values):
    return tuple(dict.fromkeys(r for v in values for r in v.reasons))


def wrap(value, symbol='literal', why=()):
    if isinstance(value, Value): return value
    if isinstance(value, (tuple,list)): value = [wrap(x, symbol, why) for x in value]
    if isinstance(value, dict): value = {k:wrap(v, symbol, why) for k,v in value.items()}
    return Value(value, symbol, why)


def raw(v):
    if v.value is UNKNOWN: raise ValueError('abstract unknown')
    if isinstance(v.value,list): return [raw(x) for x in v.value]
    if isinstance(v.value,dict): return {k:raw(x) for k,x in v.value.items()}
    return v.value


def join(values, symbol='join'):
    if not values: return Value(symbol=symbol)
    if all(v.json() == values[0].json() for v in values): return values[0]
    return Value(symbol=symbol, reasons=reasons(values))


class Module:
    def __init__(self, path, root):
        self.path, self.file = path, str(path.relative_to(root))
        self.source_bytes = path.read_bytes()
        self.source = self.source_bytes.decode('utf-8')
        self.sha256 = hashlib.sha256(self.source_bytes).hexdigest()
        self.tree = ast.parse(self.source, filename=self.file)
        self.aliases, self.functions, self.constants = {}, {}, {}
        self.parents = {}
        def collect(body, parent=''):
            for n in body:
                if isinstance(n, (ast.FunctionDef,ast.AsyncFunctionDef)):
                    key = parent+n.name
                    self.functions[key] = n
                    for x in ast.walk(n): self.parents[id(x)] = key
                elif isinstance(n,ast.ClassDef): collect(n.body,n.name+'.')
        collect(self.tree.body)


class Tracer:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.modules, self.sites, self.paths = {}, {}, []
        self.unresolved, self.boundaries = {}, {}
        self.active, self.chain, self.loops, self.taints = [], [], [], []
        self.argv, self.current_root = [], ''
        self.initialized = set()
        self.loaded_functions, self.source_snapshots = {}, {}
        self.may_start, self.edges = set(), {}
        self.stdlib = set(getattr(sys,'stdlib_module_names',())) | {'argparse','ast','os','sys','json','pathlib','subprocess','hashlib','math','time','datetime','tempfile','contextlib','resource','random','re','copy','unittest','importlib','difflib','collections','itertools','typing','__future__'}

    def location(self,m,n): return m.file+':'+str(getattr(n,'lineno',1))

    def unresolved_at(self,m,n,why):
        key = (m.file,getattr(n,'lineno',1),why)
        self.unresolved[key] = {'file':key[0],'line':key[1],'reason':why}

    @functools.lru_cache(maxsize=None)
    def find_module(self,name,base):
        if not re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*', name): return None
        rel = Path(*name.split('.'))
        for directory in (base,self.root,self.root/'experiments/track_c',self.root/'tools'):
            for p in (directory/rel.with_suffix('.py'),directory/rel/'__init__.py'):
                if p.is_file() and p.resolve().is_relative_to(self.root): return p.resolve()
        return None

    def load(self,path):
        path=Path(path).resolve()
        if path in self.modules: return self.modules[path]
        m=Module(path,self.root);self.modules[path]=m
        for n in ast.walk(m.tree):
            if isinstance(n,ast.Import):
                for a in n.names: m.aliases[a.asname or a.name.split('.')[0]]=(a.name,None)
            elif isinstance(n,ast.ImportFrom):
                for a in n.names:
                    if a.name=='*': self.unresolved_at(m,n,'star import '+str(n.module))
                    elif n.module: m.aliases[a.asname or a.name]=(n.module,a.name)
                    else: m.aliases[a.asname or a.name]=(a.name,None)
                if n.level>1:self.unresolved_at(m,n,'relative import level '+str(n.level))
        for name,attribute in list(m.aliases.values()):
            if attribute:
                submodule=self.find_module(name+'.'+attribute,path.parent)
                if submodule is not None:self.load(submodule)
            if name.split('.')[0] in ENGINE:
                self.boundaries[(name,m.file)]={'name':name,'file':m.file,'reason':'engine boundary; internals not qualified'}
                continue
            p=self.find_module(name,path.parent)
            if p is not None and name.split('.')[0] not in self.stdlib: self.load(p)
            elif name.split('.')[0] not in self.stdlib:
                self.boundaries[(name,m.file)]={'name':name,'file':m.file,'reason':'out-of-repo library'}
            elif p is None:
                self.boundaries[(name,m.file)]={'name':name,'file':m.file,'reason':'stdlib boundary; only explicit abstract semantics modeled'}
        for n in m.tree.body:
            if isinstance(n,(ast.Assign,ast.AnnAssign)):
                env=dict(m.constants)
                v=self.expr(m,n.value,env,{},False)
                for t in n.targets if isinstance(n,ast.Assign) else [n.target]: self.assign(t,v,m.constants,m)
        for n in ast.walk(m.tree):
            if isinstance(n,ast.Call):
                q=self.qualified(m,n.func)
                if q in PRIMITIVES:
                    s=self.location(m,n);key=s+':'+str(n.col_offset)
                    self.sites[key]={'site':s,'site_id':key,'primitive':q,'expression':ast.unparse(n),'family':m.parents.get(id(n),'<module>')}
                elif self.resolve(m,n.func) is None and not self.safe_call(m,n.func):
                    self.unresolved_at(m,n,'unresolved callee '+ast.unparse(n.func))
        return m

    def qualified(self,m,node):
        if isinstance(node,ast.Name):
            alias=m.aliases.get(node.id)
            return (alias[0]+('.'+alias[1] if alias[1] else '')) if alias else node.id
        if isinstance(node,ast.Attribute): return self.qualified(m,node.value)+'.'+node.attr
        return ast.unparse(node)

    def resolve(self,m,node):
        q=self.qualified(m,node)
        if q in m.functions: return m,q
        parts=q.split('.')
        for i in range(len(parts)-1,0,-1):
            name='.'.join(parts[:i]);fn='.'.join(parts[i:])
            if name.split('.')[0] in ENGINE or name.split('.')[0] in self.stdlib: continue
            p=self.find_module(name,m.path.parent)
            if p in self.modules and fn in self.modules[p].functions: return self.modules[p],fn
        return None

    def safe_call(self,m,node):
        q=self.qualified(m,node)
        pure={'str','int','float','bool','len','abs','min','max','sum','all','any','enumerate','zip','tuple','list','dict','set','sorted','range','round','isinstance','issubclass','print','object','type','repr'}
        if isinstance(node,ast.Name) and q in pure:return True
        if q in {'pathlib.Path','json.load','json.loads','json.dumps','sys.exit','os.getenv','os.environ.get'}:return True
        return False

    def build_graph(self):
        for m in list(self.modules.values()):
            for name,n in m.functions.items():
                key=(m.path,name); edges=set()
                for c in ast.walk(n):
                    if not isinstance(c,ast.Call):continue
                    if self.qualified(m,c.func) in PRIMITIVES: self.may_start.add(key)
                    target=self.resolve(m,c.func)
                    if target: edges.add((target[0].path,target[1]))
                for imported in ast.walk(n):
                    if isinstance(imported,(ast.Import,ast.ImportFrom)):
                        names=[a.name for a in imported.names] if isinstance(imported,ast.Import) else [imported.module or a.name for a in imported.names]
                        for imported_name in names:
                            p=self.find_module(imported_name,m.path.parent)
                            if p in self.modules and any(site['site'].startswith(self.modules[p].file+':') for site in self.sites.values()):self.may_start.add(key)
                self.edges[key]=edges
                loaded=set()
                for read in ast.walk(n):
                    if isinstance(read,ast.Call) and ((isinstance(read.func,ast.Attribute) and read.func.attr in LOAD_METHODS) or self.qualified(m,read.func) in ('json.load','json.loads','os.getenv','input')):
                        loaded.add('loaded '+self.location(m,read)+' '+ast.unparse(read))
                    elif isinstance(read,ast.Attribute) and self.qualified(m,read) in ('os.environ','sys.stdin'):
                        loaded.add('loaded '+self.location(m,read)+' '+ast.unparse(read))
                self.loaded_functions[key]=loaded
        while True:
            extra={key for key,edges in self.edges.items() if edges & self.may_start}
            if extra<=self.may_start:break
            self.may_start |= extra
        while True:
            changed=False
            for key,edges in self.edges.items():
                combined=set(self.loaded_functions[key])
                for edge in edges:combined.update(self.loaded_functions.get(edge,set()))
                if combined!=self.loaded_functions[key]:self.loaded_functions[key]=combined;changed=True
            if not changed:break

    def assign(self,target,value,env,m):
        if isinstance(target,ast.Name): env[target.id]=value
        elif isinstance(target,(ast.Tuple,ast.List)):
            for i,t in enumerate(target.elts):
                v=value.value[i] if isinstance(value.value,list) and i<len(value.value) else Value(symbol=value.symbol+'['+str(i)+']',reasons=value.reasons)
                self.assign(t,v,env,m)
        elif isinstance(target,(ast.Attribute,ast.Subscript)):
            # Mutation never makes a previously unknown object literal/pinned.
            env[ast.unparse(target)]=value
            if isinstance(target,ast.Attribute) and not target.attr.startswith('_'):
                self.unresolved_at(m,target,'attribute mutation '+ast.unparse(target))

    def subvalue(self,v,key,loc):
        try:
            k=raw(key)
            if isinstance(v.value,list) and isinstance(k,slice): return wrap(v.value[k],v.symbol+str(k),v.reasons)
            if isinstance(v.value,(list,dict)): return v.value[k]
            if v.value is not UNKNOWN:return wrap(v.value[k])
        except (ValueError,KeyError,IndexError,TypeError): pass
        return Value(symbol=v.symbol+'['+repr(key.value if key.value is not UNKNOWN else key.symbol)+']',reasons=v.reasons+key.reasons)

    def expr(self,m,n,env,facts,act=True):
        if n is None:return wrap(None)
        loc=self.location(m,n)
        if isinstance(n,ast.Constant):return wrap(n.value,repr(n.value)+'@'+loc)
        if isinstance(n,ast.Name):
            if n.id=='__file__':return wrap(str(m.path))
            if n.id=='__name__':return env.get('__name__',wrap(m.path.stem))
            return env.get(n.id,m.constants.get(n.id,Value(symbol=n.id)))
        if isinstance(n,ast.Starred):return self.expr(m,n.value,env,facts,act)
        if isinstance(n,ast.Slice):
            vs=[self.expr(m,x,env,facts,act) for x in (n.lower,n.upper,n.step)]
            try:return wrap(slice(*(raw(x) for x in vs)))
            except ValueError:return Value(symbol=ast.unparse(n),reasons=reasons(vs))
        if isinstance(n,(ast.List,ast.Tuple,ast.Set)):
            values=[]
            for x in n.elts:
                v=self.expr(m,x,env,facts,act)
                values.extend(v.value if isinstance(x,ast.Starred) and isinstance(v.value,list) else [v])
            return Value(values,ast.unparse(n),reasons(values))
        if isinstance(n,ast.Dict):
            vs=[self.expr(m,x,env,facts,act) for x in n.values]
            try:return Value({raw(self.expr(m,k,env,facts,act)):v for k,v in zip(n.keys,vs) if k is not None},ast.unparse(n),reasons(vs))
            except (ValueError,TypeError):return Value(symbol=ast.unparse(n),reasons=reasons(vs))
        if isinstance(n,ast.Attribute):
            q=self.qualified(m,n)
            if q=='sys.argv':return Value([wrap(m.file)]+self.argv,'argv',('argv supplied by entrypoint',))
            if q=='os.environ':return Value(symbol='os.environ',reasons=('os.environ',))
            if q=='sys.stdin':return Value(symbol='stdin',reasons=('stdin loaded data',))
            if q.endswith('.parents'):
                v=self.expr(m,n.value,env,facts,act)
                try:return wrap([str(p) for p in Path(raw(v)).parents])
                except (ValueError,TypeError):return Value(symbol=q,reasons=v.reasons)
            if q.endswith('.parent'):
                v=self.expr(m,n.value,env,facts,act)
                try:return wrap(str(Path(raw(v)).parent))
                except (ValueError,TypeError):return Value(symbol=q,reasons=v.reasons)
            parts=q.rsplit('.',1)
            if len(parts)==2:
                p=self.find_module(parts[0],m.path.parent)
                if p in self.modules and parts[1] in self.modules[p].constants:return self.modules[p].constants[parts[1]]
            v=self.expr(m,n.value,env,facts,act)
            if isinstance(v.value,dict) and n.attr in v.value:return v.value[n.attr]
            return Value(symbol=v.symbol+'.'+n.attr,reasons=v.reasons)
        if isinstance(n,ast.Subscript):
            v=self.subvalue(self.expr(m,n.value,env,facts,act),self.expr(m,n.slice,env,facts,act),loc)
            return facts.get(v.symbol,v)
        if isinstance(n,ast.UnaryOp):
            v=self.expr(m,n.operand,env,facts,act)
            try:return wrap({ast.Not:operator.not_,ast.USub:operator.neg,ast.UAdd:operator.pos,ast.Invert:operator.invert}[type(n.op)](raw(v)))
            except (ValueError,TypeError,KeyError):return Value(symbol=ast.unparse(n),reasons=v.reasons)
        if isinstance(n,ast.BinOp):
            a,b=[self.expr(m,x,env,facts,act) for x in (n.left,n.right)]
            try:
                if isinstance(n.op,ast.Div) and isinstance(raw(a),str):return wrap(str(Path(raw(a))/raw(b)))
                fn={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.FloorDiv:operator.floordiv,ast.Mod:operator.mod,ast.Pow:operator.pow}.get(type(n.op))
                return wrap(fn(raw(a),raw(b))) if fn else Value(symbol=ast.unparse(n),reasons=reasons([a,b]))
            except (ValueError,TypeError,ZeroDivisionError):return Value(symbol=a.symbol+ast.unparse(n.op)+b.symbol,reasons=reasons([a,b]))
        if isinstance(n,ast.BoolOp):
            vs=[]
            for x in n.values:
                v=self.expr(m,x,env,facts,act);vs.append(v)
                try:
                    truth=bool(raw(v))
                    if isinstance(n.op,ast.And) and not truth:return wrap(False)
                    if isinstance(n.op,ast.Or) and truth:return wrap(True)
                except ValueError: pass
            if all(v.value is not UNKNOWN for v in vs):return wrap(isinstance(n.op,ast.And))
            return Value(symbol=ast.unparse(n),reasons=reasons(vs))
        if isinstance(n,ast.Compare):
            vs=[self.expr(m,x,env,facts,act) for x in [n.left]+n.comparators]
            try:
                ops={ast.Eq:operator.eq,ast.NotEq:operator.ne,ast.Lt:operator.lt,ast.LtE:operator.le,ast.Gt:operator.gt,ast.GtE:operator.ge,ast.Is:operator.is_,ast.IsNot:operator.is_not,ast.In:lambda a,b:a in b,ast.NotIn:lambda a,b:a not in b}
                return wrap(all(ops[type(op)](raw(a),raw(b)) for a,b,op in zip(vs,vs[1:],n.ops)))
            except (ValueError,TypeError,KeyError):return Value(symbol=ast.unparse(n),reasons=reasons(vs))
        if isinstance(n,ast.IfExp):
            test=self.expr(m,n.test,env,facts,act)
            try:return self.expr(m,n.body if raw(test) else n.orelse,env,facts,act)
            except ValueError:
                self.taints.append(loc+' branch '+test.symbol+' '+str(test.reasons))
                vs=[self.expr(m,x,env.copy(),facts.copy(),act) for x in (n.body,n.orelse)]
                self.taints.pop();return join(vs,loc)
        if isinstance(n,ast.Call):return self.call(m,n,env,facts,act)
        if isinstance(n,(ast.ListComp,ast.SetComp,ast.GeneratorExp,ast.DictComp)):
            outputs=[];why=[];uncertain=[False]
            def expand(index,local):
                if index==len(n.generators):
                    outputs.append(self.expr(m,n.elt if hasattr(n,'elt') else n.value,local,facts,act));return
                gen=n.generators[index]
                v=self.expr(m,gen.iter,local,facts,act);why.extend(v.reasons)
                known=isinstance(v.value,list)
                if not known:uncertain[0]=True
                items=v.value if known else [Value(symbol=v.symbol+'[*]',reasons=v.reasons)]
                selection=self.location(m,gen.iter)
                loop={'kind':'pinned_constant','maximum':len(items),'enforcing_line':selection} if known else {'kind':'loaded_data','source':v.symbol,'selection_line':selection,'reasons':list(v.reasons)}
                self.loops.append(loop);self.chain.append(selection)
                for item in items:
                    branch=local.copy();self.assign(gen.target,item,branch,m)
                    excluded=False
                    for test in gen.ifs:
                        condition=self.expr(m,test,branch,facts,act);why.extend(condition.reasons)
                        try:excluded=excluded or not raw(condition)
                        except ValueError:uncertain[0]=True
                    if not excluded:expand(index+1,branch)
                self.chain.pop();self.loops.pop()
            expand(0,env.copy())
            return Value(UNKNOWN if uncertain[0] else outputs,ast.unparse(n),tuple(why)+reasons(outputs))
        # Discover effects nested inside syntax not modeled precisely.
        vs=[self.expr(m,x,env,facts,act) for x in ast.iter_child_nodes(n) if isinstance(x,ast.expr)]
        return Value(symbol=ast.unparse(n),reasons=reasons(vs))

    def guard(self,target):
        m,name=target;n=m.functions[name]
        if not n.args.args:return False
        arg=n.args.args[0].arg
        body=[x for x in n.body if not (isinstance(x,ast.Expr) and isinstance(x.value,ast.Constant) and isinstance(x.value.value,str))]
        if not body:return False
        x=body[0]
        return isinstance(x,ast.If) and isinstance(x.test,ast.UnaryOp) and isinstance(x.test.op,ast.Not) and isinstance(x.test.operand,ast.Name) and x.test.operand.id==arg and bool(x.body) and isinstance(x.body[0],ast.Raise)

    def constrain(self,m,n,env,facts):
        if isinstance(n,ast.BoolOp) and isinstance(n.op,ast.And):
            for x in n.values:self.constrain(m,x,env,facts)
        elif isinstance(n,ast.Compare) and len(n.ops)==1 and isinstance(n.ops[0],(ast.Eq,ast.LtE)):
            left=n.left
            if isinstance(left,ast.Call) and isinstance(left.func,ast.Name) and left.func.id=='len' and len(left.args)==1:
                iterable=self.expr(m,left.args[0],env,facts,False)
                bound=self.expr(m,n.comparators[0],env,facts,False)
                if isinstance(bound.value,int) and bound.value>=0:
                    facts['length:'+iterable.symbol]=wrap({'maximum':bound.value,'line':self.location(m,n)})
                return
            a,b=[self.expr(m,x,env,facts,False) for x in (n.left,n.comparators[0])]
            if a.value is UNKNOWN and b.value is not UNKNOWN:facts[a.symbol]=b
            elif b.value is UNKNOWN and a.value is not UNKNOWN:facts[b.symbol]=a

    def call(self,m,n,env,facts,act):
        loc=self.location(m,n);q=self.qualified(m,n.func)
        args=[self.expr(m,x,env,facts,act) for x in n.args]
        kw={x.arg:self.expr(m,x.value,env,facts,act) for x in n.keywords}
        target=self.resolve(m,n.func)
        if q in PRIMITIVES:
            if act:self.spawn(m,n,args,kw)
            return Value(symbol=loc+' process result',reasons=('process output at '+loc,))
        if target and self.guard(target):
            if act and n.args:self.constrain(m,n.args[0],env,facts)
            return wrap(None)
        if target:
            if act and (target[0].path,target[1]) in self.may_start:
                return self.invoke(*target,args,kw,loc)
            # Return taint summary of pure/non-starting helpers. Never pin a
            # filesystem round-trip, even if a preceding writer is literal.
            why=list(reasons(args+list(kw.values())))
            why.extend(sorted(self.loaded_functions.get((target[0].path,target[1]),set())))
            fn=target[0].functions[target[1]]
            for c in ast.walk(fn):
                if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr in LOAD_METHODS:
                    why.append('loaded '+self.location(target[0],c)+' '+ast.unparse(c))
            if not fn.args.args and len(fn.body)==1 and isinstance(fn.body[0],ast.Return):
                return self.expr(target[0],fn.body[0].value,{},facts,False)
            return Value(symbol=loc+' '+q+'('+','.join(v.symbol for v in args)+')',reasons=why)
        receiver=self.expr(m,n.func.value,env,facts,act) if isinstance(n.func,ast.Attribute) else Value()
        method=n.func.attr if isinstance(n.func,ast.Attribute) else ''
        if method in LOAD_METHODS or q in ('json.load','json.loads','os.getenv','os.environ.get'):
            why=reasons(args+[receiver])+('loaded '+loc+' '+ast.unparse(n),)
            return Value(symbol=loc+' '+ast.unparse(n),reasons=why)
        if method=='parse_args':return self.parse_argv(m)
        if q in ('pathlib.Path','str'):
            return args[0] if args else wrap('')
        if method in ('resolve','absolute'):
            return receiver
        if method=='relative_to':
            try:return wrap(str(Path(raw(receiver)).relative_to(raw(args[0]))))
            except (ValueError,TypeError):return Value(symbol=receiver.symbol+'.relative_to',reasons=receiver.reasons)
        if method=='get' and args:
            v=self.subvalue(receiver,args[0],loc);return facts.get(v.symbol,v)
        if method in ('upper','lower','endswith','startswith','index','split','strip'):
            try:return wrap(getattr(raw(receiver),method)(*(raw(x) for x in args)))
            except (ValueError,TypeError,AttributeError):return Value(symbol=loc+' '+ast.unparse(n),reasons=reasons([receiver]+args))
        if q=='range':
            try:return wrap(list(range(*(raw(x) for x in args))))
            except (ValueError,TypeError):return Value(symbol=loc+' range',reasons=reasons(args))
        if q in ('len','bool','int','float','tuple','list','sorted','set'):
            try:return wrap(getattr(builtins,q)(*(raw(x) for x in args)))
            except (ValueError,TypeError):return Value(symbol=loc+' '+q,reasons=reasons(args))
        if q in ('map','filter') and n.args:
            callback=self.qualified(m,n.args[0])
            if callback not in ('str','int','float','bool') and act:self.unresolved_at(m,n,'higher-order callback '+callback)
            if len(args)>1 and isinstance(args[1].value,list):return args[1]
        if method in ('values','items'):
            if isinstance(receiver.value,dict):
                return wrap(list(receiver.value.values()) if method=='values' else [[wrap(k),v] for k,v in receiver.value.items()])
        if act:self.unresolved_at(m,n,'opaque call '+q)
        return Value(symbol=loc+' '+ast.unparse(n),reasons=reasons(args+[receiver]+list(kw.values())))

    def parse_argv(self,m):
        fields=[]
        for c in ast.walk(m.tree):
            if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='add_argument' and c.args and isinstance(c.args[0],ast.Constant):
                name=c.args[0].value
                kws={x.arg:x.value for x in c.keywords}
                fields.append((name,kws))
        pos=[v for v in self.argv if not (isinstance(v.value,str) and v.value.startswith('--'))]
        out={};index=0
        for name,kws in fields:
            if name.startswith('-'):
                out[name.lstrip('-').replace('-','_')]=wrap(False if isinstance(kws.get('action'),ast.Constant) and kws['action'].value=='store_true' else None)
            else:
                nargs=kws.get('nargs');nargs=nargs.value if isinstance(nargs,ast.Constant) else None
                if nargs in ('*','+'):
                    out[name]=wrap(pos[index:]);index=len(pos)
                else:
                    out[name]=pos[index] if index<len(pos) else wrap(None) if nargs=='?' else Value(symbol='argv.'+name,reasons=('argv '+name,));index+=1
        return Value(out,'argv namespace',('argv dispatch',))

    def invoke(self,m,name,args,kw,callsite):
        key=(m.path,name)
        if key in self.active:
            self.unresolved[(m.file,m.functions[name].lineno,'recursive cycle '+name)]={'file':m.file,'line':m.functions[name].lineno,'reason':'recursive cycle '+name}
            return Value(symbol='recursive '+name,reasons=reasons(args))
        env=dict(m.constants);fn=m.functions[name]
        for i,p in enumerate(fn.args.args):env[p.arg]=args[i] if i<len(args) else kw.get(p.arg,Value(symbol='argument '+p.arg,reasons=('unbound argument '+p.arg,)))
        self.active.append(key);self.chain.append(callsite)
        result=self.block(m,fn.body,env,{})[1]
        self.chain.pop();self.active.pop()
        return result

    def block(self,m,body,env,facts):
        result=wrap(None)
        for n in body:
            loc=self.location(m,n)
            if isinstance(n,(ast.Import,ast.ImportFrom)):
                names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module or '']
                for name in names:
                    p=self.find_module(name,m.path.parent)
                    if p in self.modules and p not in self.initialized:
                        self.initialized.add(p); imported=self.modules[p]
                        self.chain.append(loc)
                        self.block(imported,imported.tree.body,dict(imported.constants),{})
                        self.chain.pop()
                continue
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Pass)):continue
            if isinstance(n,(ast.Assign,ast.AnnAssign,ast.AugAssign)):
                v=self.expr(m,n.value,env,facts)
                for t in n.targets if isinstance(n,ast.Assign) else [n.target]:self.assign(t,v,env,m)
            elif isinstance(n,ast.Expr):
                if isinstance(n.value,ast.Call):
                    target=self.resolve(m,n.value.func)
                    if target and self.guard(target) and n.value.args:
                        test=self.expr(m,n.value.args[0],env,facts)
                        try:
                            if not raw(test):return True,Value(symbol='guard halted')
                        except ValueError:pass
                result=self.expr(m,n.value,env,facts)
                if isinstance(n.value,ast.Call) and self.qualified(m,n.value.func)=='sys.exit':return True,result
            elif isinstance(n,(ast.Break,ast.Continue)):return True,Value(symbol=loc+' loop control')
            elif isinstance(n,ast.Return):return True,self.expr(m,n.value,env,facts)
            elif isinstance(n,ast.Raise):return True,Value(symbol='raise '+loc)
            elif isinstance(n,ast.If):
                test=self.expr(m,n.test,env,facts)
                try: branch=[n.body if raw(test) else n.orelse]
                except ValueError:branch=[n.body,n.orelse]
                outcomes=[]
                for code in branch:
                    local=env.copy();lf=facts.copy()
                    self.chain.append(loc);self.taints.append(loc+' branch '+ast.unparse(n.test)+' '+str(test.reasons))
                    outcomes.append((self.block(m,code,local,lf),local,lf))
                    self.taints.pop();self.chain.pop()
                live=[x for x in outcomes if not x[0][0]]
                if not live:return True,join([x[0][1] for x in outcomes],loc)
                for key in set().union(*(set(x[1]) for x in live)):env[key]=join([x[1].get(key,Value(symbol=key)) for x in live],key)
                facts.clear();facts.update({k:v for k,v in live[0][2].items() if all(k in x[2] and x[2][k].json()==v.json() for x in live)})
            elif isinstance(n,(ast.For,ast.AsyncFor,ast.While)):
                v=self.expr(m,n.iter if hasattr(n,'iter') else n.test,env,facts)
                if isinstance(n,ast.While) and v.value is False:continue
                bound=facts.get('length:'+v.symbol)
                known=isinstance(v.value,list)
                if known and not v.value:continue
                values=v.value if known else [Value(symbol=v.symbol+'[*]',reasons=v.reasons)]
                loop={'kind':'pinned_constant','maximum':len(values),'enforcing_line':loc} if known else {'kind':'loaded_data','source':v.symbol,'reasons':list(v.reasons),'selection_line':loc}
                if bound is not None:
                    loop={'kind':'pinned_constant','maximum':bound.value['maximum'].value,'enforcing_line':bound.value['line'].value}
                self.loops.append(loop);self.chain.append(loc)
                for item in values:
                    local=env.copy()
                    if hasattr(n,'target'):self.assign(n.target,item,local,m)
                    self.block(m,n.body,local,facts.copy())
                self.chain.pop();self.loops.pop()
                self.block(m,n.orelse,env,facts)
            elif isinstance(n,(ast.With,ast.AsyncWith)):
                for item in n.items:
                    v=self.expr(m,item.context_expr,env,facts)
                    if item.optional_vars:self.assign(item.optional_vars,v,env,m)
                stop,result=self.block(m,n.body,env,facts)
                if stop:return stop,result
            elif isinstance(n,ast.Try):
                stop,result=self.block(m,n.body,env,facts)
                for handler in n.handlers:self.block(m,handler.body,env.copy(),facts.copy())
                self.block(m,n.finalbody,env,facts)
                if stop:return stop,result
                self.block(m,n.orelse,env,facts)
            else:
                for x in ast.iter_child_nodes(n):
                    if isinstance(x,ast.expr):self.expr(m,x,env,facts)
        return False,result

    def spawn(self,m,n,args,kw):
        site=self.location(m,n)
        q=self.qualified(m,n.func)
        command=args[0] if args else wrap([])
        if q.startswith('os.exec') or q.startswith('os.spawn'):
            offset=1 if q.startswith('os.spawn') else 0
            executable=args[offset] if len(args)>offset else Value(symbol='unknown executable')
            if 'v' in q.rsplit('.',1)[1] and len(args)>offset+1 and isinstance(args[offset+1].value,list):
                command=wrap([executable]+args[offset+1].value[1:])
            else:command=wrap([executable]+args[offset+2:])
        elif q in ('os.system','os.popen'):
            if command.value is not UNKNOWN and isinstance(command.value,str):
                try:command=wrap(shlex.split(command.value))
                except ValueError:self.unresolved_at(m,n,'unparsed shell command string')
            self.unresolved_at(m,n,'shell command string semantics '+q)
        info={'site_id':site+':'+str(n.col_offset),'family':m.parents.get(id(n),'<module>')}
        self.record(site,command,info)
        if command.value is UNKNOWN:self.unresolved_at(m,n,'unknown process command or executable')
        if not isinstance(command.value,list):return
        tokens=command.value
        for i,token in enumerate(tokens):
            if isinstance(token.value,str) and token.value.endswith(('.py','.sh')):
                path=Path(token.value)
                if not path.is_absolute():path=self.root/path
                if not path.is_file():path=m.path.parent/Path(token.value)
                if path.is_file() and path.resolve().is_relative_to(self.root):
                    self.chain.append(site)
                    self.entry(path,tokens[i+1:])
                    self.chain.pop()
                else:self.unresolved_at(m,n,'child program outside scope or missing '+token.value)
                break

    def record(self,site,command,info=None):
        info=info or self.sites.get(site,{})
        loops=list(self.loops)
        loaded=[x for x in loops if x['kind']=='loaded_data']
        count={'kind':'loaded_data','loops':loaded} if loaded else {'kind':'pinned_constant','maximum':math.prod(x['maximum'] for x in loops),'enforcing_lines':[x['enforcing_line'] for x in loops] or [site]}
        why=list(command.reasons)
        self.paths.append({'root':self.current_root,'site':site,'site_id':info.get('site_id',site),'family':info.get('family',site),'chain':list(self.chain)+[site],'taint_reasons':list(dict.fromkeys(self.taints+why)), 'count':count,'operand_source':{'kind':'loaded_data','record_field':command.json(),'reasons':why} if why or self.has_unknown(command) else {'kind':'pinned_literal','line':site}, 'command':command.json()})

    def has_unknown(self,v):
        if v.value is UNKNOWN:return True
        if isinstance(v.value,list):return any(self.has_unknown(x) for x in v.value)
        if isinstance(v.value,dict):return any(self.has_unknown(x) for x in v.value.values())
        return False

    def entry(self,path,argv):
        previous=self.argv;self.argv=argv
        old_initialized=self.initialized; self.initialized={path.resolve()}
        if path.suffix=='.sh':self.shell(path,argv)
        else:
            m=self.load(path);self.build_graph()
            env=dict(m.constants);env['__name__']=wrap('__main__')
            self.block(m,m.tree.body,env,{})
        self.argv=previous; self.initialized=old_initialized

    def shell(self,path,argv):
        file=str(path.relative_to(self.root));data=path.read_bytes();text=data.decode('utf-8')
        self.source_snapshots[file]={'file':file,'sha256':hashlib.sha256(data).hexdigest()}
        env={'W':str(self.root),'WORKTREE':str(self.root),'SCRIPT_DIR':str(path.parent),'0':str(path)}
        env.update({str(i+1):v.value if v.value is not UNKNOWN else '${'+v.symbol+'}' for i,v in enumerate(argv)})
        functions=set(re.findall(r'^\s*(\w+)\s*\(\)\s*\{',text,re.M))
        built={'echo','printf','cd','pwd','exit','return','export','unset','set','test','[',':','true','false','break','continue','read','local','shift'}
        controls={'then','else','elif','fi','do','done','esac','in'}
        def substitutions(line):
            parts=[];out='';i=0
            while i<len(line):
                if line[i:i+2]=='$(':
                    j=i+2;depth=1
                    while j<len(line) and depth:
                        if line[j]=='(':depth+=1
                        elif line[j]==')':depth-=1
                        j+=1
                    if depth:raise ValueError('unclosed command substitution')
                    nested,clean=substitutions(line[i+2:j-1]);parts.extend(nested);parts.append(clean)
                    out+='SUBSTITUTION';i=j
                else:out+=line[i];i+=1
            return parts,out
        loop_depth=0
        case=False
        for number,line in enumerate(text.splitlines(),1):
            if not line.strip() or line.lstrip().startswith('#'):continue
            loc=file+':'+str(number)
            if re.match(r'\s*(for|while|until)\b',line):loop_depth+=1
            if line.strip().startswith('case '):case=True
            if line.strip()=='esac':case=False
            try:subs,work=substitutions(line)
            except ValueError as error:
                self.unresolved[(file,number,'shell parse')]={'file':file,'line':number,'reason':str(error)+': '+line};continue
            work=re.sub(r'^\s*\w+\s*\(\)\s*\{','',work)
            if case:
                # Case patterns are data selectors, never executable names.
                self.unresolved[(file,number,'case')]={'file':file,'line':number,'reason':'shell case conservatively reachable: '+line}
                work=re.sub(r'^.*?\)','',work) if ')' in work else ''
                work=re.sub(r';;.*','',work)
            for segment_index,segment in enumerate(subs+[work]):
                try:
                    lexer=shlex.shlex(segment,posix=True,punctuation_chars=';&|()<>' )
                    lexer.whitespace_split=True;lexer.commenters='#';tokens=list(lexer)
                except ValueError:
                    self.unresolved[(file,number,'shell parse')]={'file':file,'line':number,'reason':'unparsed shell: '+segment};continue
                chunks=[];chunk=[]
                for token in tokens+[';']:
                    if token in (';','&&','||','|','(',')','{','}'):
                        if chunk:chunks.append(chunk);chunk=[]
                    else:chunk.append(token)
                for chunk_index,tokens in enumerate(chunks):
                    while tokens and tokens[0] in ('if','elif','while','until','then','else','do'):tokens=tokens[1:]
                    if not tokens:continue
                    if tokens[0] in ('case','for'):
                        self.unresolved[(file,number,'control')]={'file':file,'line':number,'reason':'shell loop/control '+line};continue
                    while tokens and re.match(r'^[A-Za-z_][A-Za-z_0-9]*=',tokens[0]):
                        assignment=tokens.pop(0);key,value=assignment.split('=',1)
                        if '$' not in value and 'SUBSTITUTION' not in value:env[key]=value
                        elif key not in env:env[key]=value
                    if tokens and tokens[0]=='exec':tokens=tokens[1:]
                    if not tokens or tokens[0] in built or tokens[0] in controls:continue
                    cmd=tokens[0]
                    if cmd in ('source','.','eval') or cmd in functions:
                        self.unresolved[(file,number,cmd)]={'file':file,'line':number,'reason':'shell dynamic/source/function '+shlex.join(tokens)};continue
                    redirection=next((i for i,t in enumerate(tokens) if re.fullmatch(r'[<>]+',t)),len(tokens))
                    tokens=tokens[:redirection]
                    if tokens and tokens[-1].isdigit() and redirection<len(chunk):tokens=tokens[:-1]
                    def expand(s):
                        return re.sub(r'\$\{([A-Za-z_0-9]+)\}|\$([A-Za-z_0-9]+)',lambda x:str(env.get(x.group(1) or x.group(2),x.group(0))),s)
                    expanded=[expand(t) for t in tokens]
                    if not expanded:continue
                    if '$' in expanded[0] or expanded[0]=='SUBSTITUTION':
                        self.unresolved[(file,number,'dynamic command')]={'file':file,'line':number,'reason':'unresolved shell command '+shlex.join(tokens)};continue
                    site=loc
                    site_id=site+':s'+str(segment_index)+':c'+str(chunk_index)
                    info={'site':site,'site_id':site_id,'primitive':'shell command','expression':shlex.join(tokens),'family':expanded[0]}
                    self.sites[site_id]=info
                    values=[Value(x,loc,('shell argv/environment '+t,)) if '$' in x else wrap(x) for x,t in zip(expanded,tokens)]
                    if loop_depth:self.loops.append({'kind':'loaded_data','source':'shell loop','selection_line':loc,'reasons':['shell loop extent not proven']})
                    self.taints.append(loc+' shell branch/loop conservatively reachable')
                    self.record(site,wrap(values),info)
                    for i,t in enumerate(expanded):
                        child=Path(t)
                        if child.suffix in ('.py','.sh') and child.is_file() and child.resolve().is_relative_to(self.root) and child.resolve()!=path.resolve():
                            self.chain.append(loc);self.entry(child,values[i+1:]);self.chain.pop();break
                    self.taints.pop()
                    if loop_depth:self.loops.pop()
            if re.search(r'\bdone\b',line) and loop_depth:loop_depth-=1

    def result(self):
        unique={json.dumps(p,sort_keys=True):p for p in self.paths}
        snapshots=dict(self.source_snapshots)
        snapshots.update({m.file:{'file':m.file,'sha256':m.sha256} for m in self.modules.values()})
        return {'schema':'R2TR-1','sources':list(snapshots.values()),'sites':list(self.sites.values()),'paths':list(unique.values()),'unresolved':sorted(self.unresolved.values(),key=lambda x:(x['file'],x['line'],x['reason'])),'boundaries':list(self.boundaries.values()),'transitive_starters':[str(p.relative_to(self.root))+':'+n for p,n in sorted(self.may_start)],'limitations':['finite path witnesses; unknown branches included','engine and out-of-repo calls are explicit unresolved boundaries','shell branch feasibility not proven; all lexical command sites included']}


def trace(root,entries):
    tr=Tracer(root)
    for e in entries:
        p=Path(e['path']);p=p if p.is_absolute() else tr.root/p
        if p.suffix=='.py':tr.load(p)
    tr.build_graph()
    for e in entries:
        p=Path(e['path']);p=p if p.is_absolute() else tr.root/p
        tr.current_root=str(p.relative_to(tr.root))
        tr.entry(p,[wrap(x) if not isinstance(x,dict) else Value(symbol='binding '+str(x),reasons=('loaded profile binding '+str(x),)) for x in e.get('argv',[])])
    return tr.result()


def invocation_args(inv,entrypoint):
    args=inv.get('argv',[])
    for i,x in enumerate(args):
        if isinstance(x,str) and Path(x).name==Path(entrypoint).name:return args[i+1:]
    return args


def cites(obj):
    if isinstance(obj,dict):
        if 'path' in obj and 'line' in obj:yield str(obj['path'])+':'+str(obj['line'])
        for v in obj.values():yield from cites(v)
    elif isinstance(obj,list):
        for v in obj:yield from cites(v)


def compatible(command,inv):
    if not isinstance(command,list) or not command:return False
    target=[inv.get('executable_path','')]+inv.get('argv',[])
    def same(a,b):
        if isinstance(a,dict) or isinstance(b,dict):return True
        if a==b:return True
        if isinstance(a,str) and isinstance(b,str):
            an,bn=Path(a).name,Path(b).name
            if an.startswith('python') and bn.startswith('python'):return True
            if a.endswith(('.py','.sh')) and b.endswith(('.py','.sh')):return an==bn
        return False
    return len(command)==len(target) and all(same(a,b) for a,b in zip(command,target))


def coverage_for(profile,index,result,argv):
    rows=[];children=list(profile.get('children',[]))
    if profile.get('existing_admission'):
        children.append({'role':'ADMISSION_ROOT','invocation':profile['existing_admission'],'trace_site':'existing_admission'})
    for path in result['paths']:
        candidates=[]
        path_origin='ADMISSION' if any('c10w_p2_gate.py:' in x for x in path['chain']) else 'SCIENCE'
        for child in children:
            if not compatible(path['command'],child.get('invocation',{})):continue
            # Record-selection evidence separates families sharing a primitive.
            origin=child.get('origin')
            if origin and origin!=path_origin:continue
            source=child.get('operand_source',{})
            source_cites=set(cites(source.get('read_lines',[])))
            count_cites=set(cites(child.get('count',{}).get('selection_lines',[])))
            selection_cites={x for x in source_cites if any(x==link for link in path['chain'])}
            if path['count']['kind']=='loaded_data':
                count=child.get('count',{})
                if count.get('kind')!='loaded_data':continue
                loop_lines={x.get('selection_line') for x in path['count'].get('loops',[])}
                if count_cites and not count_cites & loop_lines:continue
                if not count_cites and source_cites and not selection_cites:continue
            # Loaded operands with a family require that family's source evidence.
            if path['operand_source']['kind']=='loaded_data' and source_cites and not selection_cites:continue
            candidates.append(child)
        status='GAP';evidence=[]
        for child in candidates:
            tag=child.get('trace_site','')
            refusal=profile.get('composition_refusal') or ''
            if tag and any(part.partition(':')[2].strip()==tag for part in refusal.split(';')):status='REFUSED';evidence=[refusal];break
            if path['count']['kind']=='loaded_data' or path['operand_source']['kind']=='loaded_data':continue
            if path['operand_source']['kind']=='loaded_data' and child.get('operand_source',{}).get('kind')!='loaded_data':continue
            status='REPRESENTED';evidence=[tag or 'child invocation'];break
        rows.append({'profile':index,'entrypoint':profile['entrypoint'],'argv':argv,'site':path['site'],'site_id':path.get('site_id',path['site']),'family':path['family'],'origin':path_origin,'status':status,'evidence':evidence,'chain':path['chain'],'count':path['count'],'operand_source':path['operand_source']})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--entry',action='append')
    parser.add_argument('--argv',default='[]',help='JSON argv for --entry')
    parser.add_argument('--against',type=Path)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    if args.against:
        profiles=json.loads(args.against.read_text())['profiles']
        results=[];coverage=[]
        # Scope comes from the brief, never the profile child declarations.
        stem_scope={'c10w_oracle_'+x+'.py' for x in ('step0','eval','train','read','interim','torchcheck')}
        stem_scope |= {'c10w_p2_gate.py','c10w_p2_rerun.py','run_c10w_stage.sh','run_c10w_p2_stage.sh','run_c10w_p2.sh'}
        for i,p in enumerate(profiles):
            if Path(p['entrypoint']).name not in stem_scope:continue
            argv=invocation_args(p['authorized_payload'],p['entrypoint'])
            result=trace(args.root,[{'path':p['entrypoint'],'argv':argv}]);results.append(result)
            coverage.extend(coverage_for(p,i,result,argv))
        all_entries=['experiments/track_c/'+name for name in sorted(stem_scope) if name.startswith('c10w_oracle_')]
        all_entries+=['tools/'+name for name in sorted(stem_scope) if not name.startswith('c10w_oracle_')]
        census=trace(args.root,[{'path':name,'argv':[]} for name in all_entries])
        results.append(census)
        result={'schema':'R2TR-1','coverage':coverage,'census_entries':all_entries,'unprofiled_entries':[name for name in all_entries if not any(Path(p['entrypoint']).name==Path(name).name for p in profiles)],'out_of_scope_profiles':[i for i,p in enumerate(profiles) if Path(p['entrypoint']).name not in stem_scope]}
        for key in ('sources','sites','paths','unresolved','boundaries','transitive_starters'):
            merged={json.dumps(x,sort_keys=True):x for r in results for x in r[key]};result[key]=list(merged.values())
        source_hashes={}
        for source in result['sources']:source_hashes.setdefault(source['file'],set()).add(source['sha256'])
        result['source_drift']=[file for file,hashes in source_hashes.items() if len(hashes)>1]
        result['summary']={status:sum(x['status']==status for x in coverage) for status in ('REPRESENTED','REFUSED','GAP')}
    else:
        entries=args.entry or ['experiments/track_c/c10w_oracle_'+x+'.py' for x in ('step0','eval','train','read','interim','torchcheck')]+['tools/'+x for x in ('c10w_p2_gate.py','c10w_p2_rerun.py','run_c10w_stage.sh','run_c10w_p2_stage.sh','run_c10w_p2.sh')]
        result=trace(args.root,[{'path':x,'argv':json.loads(args.argv)} for x in entries])
    result['unresolved_count']=len(result['unresolved'])
    result['boundaries_count']=len(result['boundaries'])
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.out:args.out.write_text(text)
    else:sys.stdout.write(text)
    print('UNRESOLVED %d; BOUNDARIES %d; %s'%(result['unresolved_count'],result['boundaries_count'],result.get('summary',{})),file=sys.stderr)
    return 1 if result.get('summary',{}).get('GAP',0) else 0


if __name__=='__main__':
    sys.exit(main())
