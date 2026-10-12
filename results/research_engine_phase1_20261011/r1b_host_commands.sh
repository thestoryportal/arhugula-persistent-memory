#!/bin/bash
# Prospective MAESTRO read-only collector/guards. No install, build, cleanup or service commands.
# Run from the worktree; on Intel, supply the reviewed exported manifest absolute path.
# Every write is beneath the one retained mktemp directory. This script is NOT RUN by R1B.
set -euo pipefail
umask 077
if [ "$#" -lt 2 ]; then
  printf 'usage: bash r1b_host_commands.sh MODE MANIFEST [ENTRY_OR_OBSERVATION]\n' >&2
  exit 64
fi
# Existing read-only verifier, not the interpreter being provisioned. Probe first; no bootstrap.
: "${R1B_READ_PYTHON:=/usr/bin/python3}"
[ -x "$R1B_READ_PYTHON" ] || { printf 'Existing read-only Python tool missing: %s\n' "$R1B_READ_PYTHON" >&2; exit 69; }
export PYTHONDONTWRITEBYTECODE=1
exec "$R1B_READ_PYTHON" -I -B - "$@" <<'R1B_PY'
import hashlib,json,os,pathlib,re,stat,subprocess,sys,tarfile,tempfile,time,urllib.parse,zipfile
mode,manifest_path=sys.argv[1:3]
arg=sys.argv[3] if len(sys.argv)>3 else None
m=json.loads(pathlib.Path(manifest_path).read_text())
assert sys.version_info >= (3,9), 'Existing read-only verifier requires Python >=3.9; no bootstrap'
assert m['schema']=='R1B-v2', 'Manifest schema mismatch'
byid={a['id']:a for a in m['artifacts']}
assert len(byid)==len(m['artifacts']), 'Duplicate manifest ID'
started=time.monotonic()  # Before first collector write; all fetch/staging time counts.
shared=os.environ.get('R1B_FETCH_RECEIPT_DIR')
if shared:
    work=pathlib.Path(shared)
    assert work.parent==pathlib.Path('/private/tmp') and work.name.startswith('r1b.') and work.is_dir() and not work.is_symlink(), 'Shared directory must be a retained r1b mktemp root'
    assert work.stat().st_uid==os.getuid() and stat.S_IMODE(work.stat().st_mode)==0o700, 'Wrong staging owner/mode'
else:
    assert mode not in ['fetch','wheel','archive-index','inspect'], 'First run inventory; export its RETAINED_MKTEMP as R1B_FETCH_RECEIPT_DIR; all acquisitions reuse one directory'
    work=pathlib.Path(tempfile.mkdtemp(prefix='r1b.',dir='/private/tmp'))
receipts=pathlib.Path(tempfile.mkdtemp(prefix='receipts-',dir=str(work)))
print('RETAINED_MKTEMP='+str(work),flush=True)
print('INVOCATION_RECEIPTS='+str(receipts),flush=True)
receipt_limit=10000000
written=sum(x.stat().st_size for x in work.rglob('*.json') if x.is_file())

def stop(message):
    raise RuntimeError(message)
def remaining():
    n=900-(time.monotonic()-started)
    if n<=0: stop('900-second provisioning/acquisition deadline exceeded; retain all files')
    return n
def save(name,value):
    global written
    data=(json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
    written+=len(data)
    if written>receipt_limit: stop('Receipt allowance exceeded')
    (receipts/name).write_bytes(data)
    return value
def run(argv):
    remaining()
    p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=min(remaining(),90))
    record={'argv':argv,'exit':p.returncode,'stdout':p.stdout.decode(errors='strict'),'stderr':p.stderr.decode(errors='strict')}
    save('command-%04d.json'%len(list(receipts.glob('command-*'))),record)
    if p.returncode!=0: stop('Command failed: '+repr(argv)+'; see retained receipt')
    if not p.stdout.strip() and not p.stderr.strip(): stop('Empty observation: '+repr(argv))
    return record['stdout'].strip()
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            remaining();h.update(chunk)
    return h.hexdigest()
def ispin(value): return isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None
def record(path):
    p=pathlib.Path(path);s=p.lstat()
    base={'path':str(p),'realpath':str(p.resolve()),'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid,'device':s.st_dev,'inode':s.st_ino,'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512}
    if p.is_symlink():base.update(kind='symlink',target=os.readlink(p))
    elif p.is_file():base.update(kind='file',sha256=digest(p))
    elif p.is_dir():base['kind']='directory'
    else:stop('Unsupported file type: '+str(p))
    return base
def checkfile(a,p):
    obs=record(p)
    if obs['kind']!='file':stop('Artifact is not a regular file: '+a['id'])
    if ispin(a['expected_sha256']) and obs['sha256']!=a['expected_sha256']:stop('SHA256 mismatch: '+a['id'])
    if isinstance(a['size_bytes'],int) and obs['logical_bytes']!=a['size_bytes']:stop('Length mismatch: '+a['id'])
    save(a['id'].replace(':','-')+'-bytes.json',obs)
    return obs

def download(url,name,limit):
    if not isinstance(url,str) or not url.startswith('https://'):stop('Exact HTTPS URL unresolved: '+str(url))
    if not isinstance(limit,int) or limit<=0:stop('Download bound unresolved')
    if limit>500000000:stop('Collector per-file bound exceeds read-only staging plan')
    cache_name=hashlib.sha256(url.encode()).hexdigest()[:16]+'-'+name
    dest=work/cache_name
    cached=work/(cache_name+'.download.json')
    if dest.exists():
        if not cached.is_file():stop('Retained incomplete acquisition; no retry or overwrite')
        prior=json.loads(cached.read_text())
        if prior['url']!=url or prior['sha256']!=digest(dest) or dest.stat().st_size!=prior['size_bytes']:stop('Retained artifact changed')
        return dest
    run(['/usr/bin/curl','--disable','--fail','--show-error','--silent','--location','--proto','=https','--proto-redir','=https','--connect-timeout','10','--max-time',str(int(min(remaining(),90))),'--max-filesize',str(limit),'--output',str(dest),url,'--write-out','%{url_effective}\n%{http_code}\n%{size_download}\n'])
    if not dest.is_file() or not 0<dest.stat().st_size<=limit:stop('Empty or over-limit download')
    total=sum(p.stat().st_size for p in work.rglob('*') if p.is_file())
    if total>600000000:stop('Collector staging growth exceeds 600 MB sub-bound; retain files')
    cached.write_text(json.dumps({'url':url,'sha256':digest(dest),'size_bytes':dest.stat().st_size})+'\n')
    return dest

def inventory():
    host={
      'account':run(['/usr/bin/id','-un']),
      'hostname':run(['/bin/hostname']),
      'os':run(['/usr/bin/sw_vers','-productVersion']),
      'build':run(['/usr/bin/sw_vers','-buildVersion']),
      'arch':run(['/usr/bin/uname','-m']),
      'macports':run(['/opt/local/bin/port','version']).removeprefix('Version: ').strip(),
      'hardware_identity':run(['/usr/sbin/system_profiler','SPHardwareDataType','-json'])}
    for key,expected in m['host'].items():
        if key in host and expected!='NEEDS-FETCH' and host[key]!=expected:stop('Host mismatch: '+key)
    clt=run(['/usr/sbin/pkgutil','--pkg-info','com.apple.pkg.CLTools_Executables'])
    clt_match=re.search(r'^version: (.+)$',clt,re.M)
    if not clt_match or clt_match[1]!=m['host']['clt']:stop('CLT receipt mismatch')
    host['clt']=clt_match[1]
    save('host.json',host)
    for argv in [['/usr/sbin/pkgutil','--pkg-info','org.macports.MacPorts'],['/usr/bin/xcode-select','-p'],['/usr/sbin/pkgutil','--pkg-info','com.apple.pkg.CLTools_Executables'],['/opt/local/bin/port','installed'],['/bin/ps','-axo','pid,ppid,pgid,ni,rss,%cpu,comm'],['/usr/bin/vm_stat'],['/usr/bin/memory_pressure']]:run(argv)
    for topic in ['info','deps','rdeps','contents','install','archivefetch','fetch','checksum']:
        run(['/opt/local/bin/port','help',topic])
    for a in m['artifacts']:
        if a['source_url'].startswith('/'):
            p=pathlib.Path(a['source_url'])
            if p.is_file():checkfile(a,p)
            elif p.is_dir():save(a['id'].replace(':','-')+'-directory.json',record(p))
            else:stop('Baseline path missing: '+str(p))
    ports=[]
    for name in m['selection']['runtime_names']:
        portdir=run(['/opt/local/bin/port','-q','dir',name])
        recipe=pathlib.Path(portdir)/'Portfile'
        if not recipe.is_file() or not recipe.resolve().is_relative_to(pathlib.Path(m['tree']['root']).resolve()):stop('Portfile escapes pinned tree: '+name)
        a=byid['port:'+name];d=digest(recipe)
        if ispin(a.get('portfile_sha256')) and d!=a['portfile_sha256']:stop('Recipe mismatch: '+name)
        info=run(['/opt/local/bin/port','-q','info','--version','--revision',name])
        info_full=run(['/opt/local/bin/port','info',name])
        deps=run(['/opt/local/bin/port','deps',name])
        rdeps=run(['/opt/local/bin/port','rdeps',name])
        ports.append({'entry':a['id'],'dir':portdir,'portfile_sha256':d,'version_revision_raw':info,'info_raw':info_full,'deps_raw':deps,'recursive_build_and_runtime_raw':rdeps})
    run(['/opt/local/bin/port','-q','rdeps','--no-build','openjdk21','python312'])
    save('ports-closure-recipes.json',ports)
    for conf in ['sources.conf','macports.conf','archive_sites.conf','pubkeys.conf','variants.conf']:
        p=pathlib.Path('/opt/local/etc/macports')/conf
        save('config-'+conf+'.json',{'identity':record(p),'content':p.read_text()})
    # Capture exact installed verification implementation; do not guess its digest algorithm.
    methods=[]
    for p in pathlib.Path('/opt/local/share/macports/Tcl').rglob('*.tcl'):
        text=p.read_text()
        if 'signature' in text and ('openssl' in text or 'pubkey' in text):
            methods.append({'identity':record(p),'content':text})
    if not methods:stop('MacPorts signature verifier implementation not located')
    save('installed-signature-methods.json',methods)
    roots=[pathlib.Path('/opt/local'),pathlib.Path('/Applications/MacPorts'),pathlib.Path(m['paths']['root']),pathlib.Path('/private/tmp')]
    observations=[]
    for p in roots:
        existing=p
        while not existing.exists():existing=existing.parent
        run(['/bin/df','-k',str(existing)])
        if p.exists():
            run(['/usr/bin/du','-sk',str(p)])
            observations.append({'root':str(p),'identity':record(p),'files':[record(q) for q in p.rglob('*')]})
        else:observations.append({'root':str(p),'absent':True,'parent_identity':record(existing)})
    save('preinventory.json',observations)
    return 'RAW-INVENTORY-ONLY; dependency edge normalization, variants, pools and writer reservation require review'

def treecheck():
    for id in ['ports-tar','ports-tar-signature','ports-rmd160','portindex','portindex-quick','portindex-signature','macports-key']:
        checkfile(byid[id],byid[id]['source_url'])
    root=pathlib.Path(m['tree']['root']);commit=(root/'.git_commit').read_text().strip()
    if commit!=m['tree']['commit']:stop('Tree commit mismatch')
    sources=pathlib.Path('/opt/local/etc/macports/sources.conf').read_text()
    active=[x.strip() for x in sources.splitlines() if x.strip() and not x.lstrip().startswith('#')]
    if active!=[m['tree']['source_line']]:stop('Active source order/content mismatch')
    seen=set();records=[]
    with tarfile.open(byid['ports-tar']['source_url'],'r|gz') as t:
        for entry in t:
            n=pathlib.PurePosixPath(entry.name)
            if n.is_absolute() or '..' in n.parts:stop('Unsafe tree tar path')
            parts=[x for x in n.parts if x!='.']
            if not parts or parts==['ports']:continue
            if parts[0]!='ports':stop('Unexpected tree tar root; freeze exact observed layout before comparison')
            rel=pathlib.Path(*parts[1:]);dest=root/rel
            if str(rel) in seen:stop('Duplicate tar member')
            seen.add(str(rel))
            if not dest.exists() and not dest.is_symlink():stop('Missing effective tree member: '+str(rel))
            if entry.isfile():
                f=t.extractfile(entry);h=hashlib.sha256()
                for chunk in iter(lambda:f.read(1024*1024),b''):remaining();h.update(chunk)
                if dest.is_symlink() or not dest.is_file() or digest(dest)!=h.hexdigest():stop('Effective content mismatch: '+str(rel))
                records.append({'path':str(rel),'sha256':h.hexdigest(),'mode':entry.mode})
            elif entry.issym():
                resolved=(dest.parent/entry.linkname).resolve()
                if not resolved.is_relative_to(root.resolve()) or not dest.is_symlink() or os.readlink(dest)!=entry.linkname:stop('Tree symlink mismatch/escape')
            elif entry.isdir():
                if dest.is_symlink() or not dest.is_dir():stop('Tree directory mismatch')
            else:stop('Hardlink/device/special tree member needs an explicit reviewed identity rule')
    effective={str(p.relative_to(root)) for p in root.rglob('*')}
    extra=effective-seen-set(m['tree']['index_derived_allowlist'])
    if extra:stop('Unadmitted effective tree members: '+repr(sorted(extra)))
    save('effective-tree-content.json',records)
    a=byid['ports-tar'];algorithm=a.get('signature_algorithm')
    if algorithm not in ['sha256','sha512','ripemd160']:stop('NEEDS-FETCH: exact installed signature algorithm/method and raw key/signature pins must be reviewed first')
    for id in ['macports-key','ports-tar-signature']:
        if not ispin(byid[id]['expected_sha256']):stop('Unpinned key or signature')
    run(['/usr/bin/openssl','dgst','-'+algorithm,'-verify',byid['macports-key']['source_url'],'-signature',byid['ports-tar-signature']['source_url'],a['source_url']])
    return 'TREE-CONTENT-AND-SIGNATURE-OBSERVATION; needs reviewed receipt admission'

def archive_inventory(path):
    records=[]
    with tarfile.open(path,'r|*') as t:
        seen=set()
        for entry in t:
            n=pathlib.PurePosixPath(entry.name)
            if n.is_absolute() or '..' in n.parts or entry.name in seen:stop('Unsafe/duplicate payload member')
            seen.add(entry.name)
            row={'path':entry.name,'size':entry.size,'mode':entry.mode,'kind':'directory' if entry.isdir() else 'symlink' if entry.issym() else 'file' if entry.isfile() else 'unsupported'}
            if entry.isfile():
                f=t.extractfile(entry);h=hashlib.sha256()
                for chunk in iter(lambda:f.read(1024*1024),b''):remaining();h.update(chunk)
                row['sha256']=h.hexdigest()
            elif entry.issym():row['target']=entry.linkname
            elif not entry.isdir():stop('Payload hardlinks/special files require reviewed mapping')
            records.append(row)
    save('payload-inventory.json',records)
    return records

def fetch(a):
    if not isinstance(a['size_bytes'],int):stop('Exact compressed artifact size unresolved: '+a['id'])
    p=download(a['source_url'],'artifact',a['size_bytes']);obs=checkfile(a,p)
    if a['route']=='binary archive':
        sig=download(a['signature_url'],'signature',1000000)
        save('signature-bytes.json',record(sig))
        if ispin(a.get('signature_sha256')) and digest(sig)!=a['signature_sha256']:stop('Archive signature byte mismatch')
        alg=a.get('signature_algorithm')
        if alg in ['sha256','sha512','ripemd160'] and ispin(byid['macports-key']['expected_sha256']):
            key=byid['macports-key']['source_url'];checkfile(byid['macports-key'],key)
            run(['/usr/bin/openssl','dgst','-'+alg,'-verify',key,'-signature',str(sig),str(p)])
        else:save('signature-pending.json',{'status':'NEEDS-FETCH','requirement':'Review installed signature method, key and raw signature digest before admission'})
    if 'checksum_url' in a:
        checksum=download(a['checksum_url'],'upstream.sha256',4096).read_text().strip()
        match=re.fullmatch(r'([0-9a-fA-F]{64})(?:\s+\*?([^\s]+))?',checksum)
        if not match or match[1].lower()!=obs['sha256']:stop('Published checksum and downloaded bytes differ')
        if match[2] and match[2]!=a['source_url'].rsplit('/',1)[1]:stop('Checksum filename mismatch')
    archive_inventory(p)
    return 'FETCHED-OBSERVATION; not installation authorization'

def wheel(a):
    raw=download(a['metadata_url'],'pypi.json',2000000)
    meta=json.loads(raw.read_text())
    if meta['info']['version']!=a['version_revision']:stop('PyPI version mismatch')
    candidates=[]
    for u in meta['urls']:
        match=re.fullmatch(r'duckdb-1\.5\.5-cp312-cp312-macosx_(\d+)_(\d+)_x86_64\.whl',u['filename'])
        if match and (int(match[1]),int(match[2]))<=(14,8) and u['packagetype']=='bdist_wheel' and not u.get('yanked',False):candidates.append(u)
    if len(candidates)!=1:stop('Require exactly one locked Intel cp312 wheel; found '+str(len(candidates)))
    u=candidates[0]
    lock=pathlib.Path(byid['duckdb-lock']['source_url'])
    if not lock.is_file(): lock=pathlib.Path(m['paths']['duckdb_lock'])
    checkfile(byid['duckdb-lock'],lock)
    lock_text=lock.read_text()
    if not lock_text.startswith('duckdb==1.5.5 '):stop('Lock requirement mismatch')
    lock_hashes=re.findall(r'--hash=sha256:([0-9a-f]{64})',lock_text)
    if len(lock_hashes)!=35 or u['digests']['sha256'] not in lock_hashes:stop('Wheel digest absent from governing lock')
    if ispin(a['expected_sha256']) and a['expected_sha256']!=u['digests']['sha256']:stop('Selected wheel repinned by metadata')
    if a['source_url']!='NEEDS-FETCH' and a['source_url']!=u['url']:stop('Selected wheel URL mismatch')
    if u['size']>30000000:stop('Wheel compressed allowance exceeded')
    p=download(u['url'],u['filename'],u['size'])
    if p.stat().st_size!=u['size'] or digest(p)!=u['digests']['sha256']:stop('Wheel bytes mismatch PyPI/lock')
    with zipfile.ZipFile(p) as z:
        if sum(x.file_size for x in z.infolist())>100000000:stop('Wheel unpacked allowance exceeded')
        names=z.namelist()
        if any(pathlib.PurePosixPath(x).is_absolute() or '..' in pathlib.PurePosixPath(x).parts for x in names):stop('Unsafe wheel member')
        if len(names)!=len(set(names)):stop('Duplicate wheel member')
        metadata={x:z.read(x).decode() for x in names if x.endswith('/WHEEL') or x.endswith('/METADATA')}
        save('wheel-metadata.json',metadata)
        save('wheel-members.json',[{'path':x,'sha256':hashlib.sha256(z.read(x)).hexdigest(),'size':z.getinfo(x).file_size} for x in names if not x.endswith('/')])
    save('selected-wheel.json',u)
    return 'LOCK-MEMBER-OBSERVATION; ABI/linkage and installer remain pending'

def inspect(a):
    source=a['source_url']
    if source.startswith('manifest:'):
        parent=byid[source[len('manifest:'):]]
        fetch(parent)
        return 'DERIVED-MEMBER-IDENTITIES in payload-inventory.json; exact member/tool versions require review'
    if source.startswith('/') or pathlib.Path(source).is_file():
        p=pathlib.Path(source)
        if p.is_dir():save('directory-identity.json',record(p))
        else:checkfile(a,p)
        return 'BASELINE-IDENTITY-OBSERVATION'
    return fetch(a)

def sourceplan(a):
    name=a['name'];directory=run(['/opt/local/bin/port','-q','dir',name])
    recipe=pathlib.Path(directory)/'Portfile'
    if not recipe.resolve().is_relative_to(pathlib.Path(m['tree']['root']).resolve()):stop('Recipe outside admitted tree')
    save('source-recipe.json',{'identity':record(recipe),'content':recipe.read_text()})
    for argv in [['/opt/local/bin/port','info',name],['/opt/local/bin/port','deps',name],['/opt/local/bin/port','rdeps',name]]:run(argv)
    save('source-resolution-status.json',{'status':'NEEDS-FETCH','required':'Resolve evaluated source/patch URLs, checksums, PortGroups, exact build-only closure and flags from this pinned recipe; review before any fetch/build. Read-only recipe capture cannot measure build work/time.'})
    return 'RAW-SOURCE-PLAN-INPUTS; not a complete build lock'

def admission(observation):
    if not observation:stop('guard requires independently captured observation JSON path')
    o=json.loads(pathlib.Path(observation).read_text())
    unresolved=[]
    def walk(v,path):
        if isinstance(v,dict):
            for k,x in v.items():walk(x,path+'/'+k)
        elif isinstance(v,list):
            for i,x in enumerate(v):walk(x,path+'/'+str(i))
        elif isinstance(v,str) and ('NEEDS-FETCH' in v or v.startswith('BLOCKED')):unresolved.append(path)
    walk(m,'manifest')
    if unresolved:stop('Refuse before installation; unresolved fields: '+', '.join(unresolved))
    for key in ['account','hostname','hardware_identity','os','build','arch','macports','clt','pool_map']:
        if o['host'][key]!=m['host'][key]:stop('Observed/expected host mismatch: '+key)
    for a in m['artifacts']:
        actual=o['artifacts'][a['id']]
        for key in ['version_revision','variants','source_url','size_bytes','route']:
            if actual[key]!=a[key]:stop('Observed/expected artifact mismatch: '+a['id']+'/'+key)
        if actual['sha256']!=a['expected_sha256']:stop('Observed/expected artifact SHA256 mismatch: '+a['id'])
        if actual.get('signature_verified') is not True and a['route']=='binary archive':stop('Unverified archive signature')
    if o['tree']!=m['tree']:stop('Expected/observed effective tree mismatch')
    if o['paths']!=m['paths']:stop('Path map mismatch')
    if o['preinstalled_ports']!=[]:stop('Unexpected preinstalled ports')
    if o['projected_setup_peak_bytes']>m['budget']['setup_cap_bytes'] or o['projected_provisioning_seconds']>900:stop('Budget/time bound fails')
    for pool in o['pools']:
        if pool['free_bytes']<pool['projected_peak_bytes']+max(m['budget']['free_floor_bytes'],m['budget']['additional_headroom_bytes']):stop('Physical pool headroom fails')
    if not all(m['authorization'][k] is True for k in ['staging','building','installation']):stop('Separately authorized staged/build/install boundary absent')
    if not o['writer_reservation_matches'] or not o['no_queued_external_writers']:stop('Exclusive writer reservation unavailable')
    save('admission-comparisons.json',{'observations':observation,'result':'comparisons satisfied; keep lock/reservation through postcheck'})
    return 'GUARD-ONLY; this program contains no install entry point'

def compareinstalled():
    expected=m['postinstall']['expected_payloads']
    if not isinstance(expected,dict) or not expected:stop('NEEDS-FETCH: admitted archive/build-to-install payload mapping absent')
    observed={}
    for path,want in expected.items():
        got=record(path)
        for key in ['kind','mode']:
            if got[key]!=want[key]:stop('Installed file type/mode mismatch: '+path)
        if want['kind']=='file' and got['sha256']!=want['sha256']:stop('Installed payload digest mismatch: '+path)
        if want['kind']=='symlink' and got['target']!=want['target']:stop('Installed symlink mismatch: '+path)
        observed[path]=got
    actual=set()
    names=m['selection']['registered_names']
    if not isinstance(names,list) or not names:stop('Complete expected registered runtime/build port set unresolved')
    for name in names:
        raw=run(['/opt/local/bin/port','-q','contents',name])
        actual.update(x.strip() for x in raw.splitlines() if x.strip().startswith('/'))
    ports=run(['/opt/local/bin/port','installed'])
    got=set(re.findall(r'^\s+(\S+)\s+@',ports,re.M))
    if got!=set(names):stop('Installed port set mismatch')
    for line in ports.splitlines():
        match=re.fullmatch(r'\s+(\S+)\s+@(\S+)\s+\(active\)\s*',line)
        if not match:
            if line.strip().startswith('The following ports'):continue
            if line.strip():stop('Unexpected installed registry line or inactive port')
        else:
            a=byid['port:'+match[1]]
            variants=a['variants']
            if not isinstance(variants,list):stop('Installed variants expectation unresolved')
            observed_ident=match[2].split('+')
            if observed_ident[0]!=a['version_revision'] or sorted('+'+x for x in observed_ident[1:])!=sorted(variants):stop('Installed version/revision/variants mismatch: '+a['id'])
    allowed=m['postinstall']['generated_file_allowlist']
    if not isinstance(allowed,dict):stop('Generated-file rules unresolved')
    if actual-set(expected)-set(allowed):stop('Unexpected installed port payloads')
    if set(expected)-actual-set(m['postinstall'].get('non_port_payload_paths',[])):stop('Missing registry-owned expected payload')
    for path,rule in allowed.items():
        got=record(path)
        if got['kind']!=rule['kind'] or got['mode']!=rule['mode']:stop('Generated file rule mismatch')
        if got['kind']=='file' and got['logical_bytes']>rule['max_bytes']:stop('Generated file size exceeds rule')
    save('installed-comparisons.json',observed)
    return 'PAYLOAD-COMPARISON-OBSERVATION; native linkage/version and source chain checks still required'

if mode=='inventory':result=inventory()
elif mode=='tree':result=treecheck()
elif mode=='guard':result=admission(arg)
elif mode=='compare-installed':result=compareinstalled()
else:
    if arg not in byid:stop('Exact manifest entry argument required')
    a=byid[arg]
    if mode=='fetch':result=fetch(a)
    elif mode=='wheel':result=wheel(a)
    elif mode=='inspect':result=inspect(a)
    elif mode=='source-plan':result=sourceplan(a)
    elif mode=='archive-index':
        url='https://packages.macports.org/'+a['name']+'/'
        p=download(url,'archive-index.html',2000000)
        names=re.findall(r'href="([^"/]+\.tbz2)"',p.read_text())
        pattern=re.escape(a['name']+'-'+a['version_revision'])+r'(?:\+[^./]+)*\.darwin_23\.(?:x86_64|noarch)\.tbz2'
        exact=[x for x in names if re.fullmatch(pattern,x)]
        if not exact:stop('No compatible exact archive; no automatic source route')
        save('archive-candidates.json',exact);result='INDEX-ONLY; review exact variants, URL, signature and byte sizes before admission'
    elif mode=='r3':
        if not a['source_url'].startswith('/') or not ispin(a['expected_sha256']):stop('BLOCKED-R3-ARTIFACT: MAESTRO must supply the reviewed exact package/version/path/hash and review receipt; fetch cannot author them')
        checkfile(a,a['source_url']);result='R3-BYTE-OBSERVATION; compare review binding and command vectors before dispatch'
    else:stop('Unknown mode; no mutation/installation mode exists')
save('summary.json',{'mode':mode,'entry':arg,'result':result,'elapsed_seconds':time.monotonic()-started,'status':'OBSERVATION-ONLY','retained_dir':str(work)})
print(result,flush=True)
R1B_PY
