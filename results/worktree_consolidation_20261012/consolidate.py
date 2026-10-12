import os,sys,json
W,M,mode=sys.argv[1],sys.argv[2],sys.argv[3]
paths=[l for l in open(sys.argv[4]).read().split('\n') if l]+[l for l in open(sys.argv[5]).read().split('\n') if l]
SKIP=('results/labviz','tools/labviz_serve.sh','results/context_audit_20261012/','graft/','.claude/','.DS_Store','__pycache__')
moved,skipped,coll=[],[],[]
for p in sorted(set(paths)):
    rp=p.rstrip('/')
    if any(rp.startswith(s.rstrip('/')) or ('/'+s) in ('/'+rp) for s in SKIP): skipped.append(rp); continue
    src=os.path.join(W,rp); dst=os.path.join(M,rp)
    if not os.path.lexists(src): continue
    if os.path.lexists(dst): coll.append(rp); continue
    size=sum(os.lstat(os.path.join(d,f)).st_size for d,_,fs in os.walk(src) for f in fs) if os.path.isdir(src) and not os.path.islink(src) else os.lstat(src).st_size
    if mode=='apply':
        os.makedirs(os.path.dirname(dst),exist_ok=True); os.rename(src,dst)
        assert os.path.lexists(dst) and not os.path.lexists(src)
    moved.append([rp,size])
print(json.dumps({'mode':mode,'moved_n':len(moved),'moved_GB':round(sum(s for _,s in moved)/1e9,2),'skipped_n':len(skipped),'collisions':coll},indent=1))
if mode=='apply': json.dump({'from':W,'to':M,'moved':moved,'skipped':skipped,'collisions':coll},open(sys.argv[6],'w'),indent=0)
