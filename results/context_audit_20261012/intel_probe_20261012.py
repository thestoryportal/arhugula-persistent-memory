import os,json,subprocess
out={}
out['volumes']=sorted(os.listdir('/Volumes'))
out['df']=subprocess.run(['/bin/df','-h'],capture_output=True,text=True).stdout
home=os.path.expanduser('~'); out['home']=home
out['home_top']=sorted(os.listdir(home))
hits=[]
roots=[home]+['/Volumes/'+v for v in os.listdir('/Volumes') if v!='Macintosh HD']
for r in roots:
  for dp,dn,fn in os.walk(r):
    if dp.count(os.sep)-r.count(os.sep)>4: dn[:]=[]; continue
    dn[:]=[d for d in dn if d not in ('Library','.Trash','node_modules','.git')]
    for n in dn+fn:
      l=n.lower()
      if any(k in l for k in ('memit','llm-database','arhugula','corpus','c10','staging','persistent-memory')): hits.append(os.path.join(dp,n))
out['name_hits']=hits[:80]
print(json.dumps(out,indent=1))
