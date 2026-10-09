#!/usr/bin/env python3
"""NEW1 offline arithmetic worker. Only its live supervisor may dispatch it."""
import argparse
import contextlib
from dataclasses import dataclass
import hashlib
import importlib.metadata
import math
import os
from pathlib import Path
import socket
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.new1_supervisor import BOUNDARY, TIER, Stop, durable_json, sha_file, strict_json, verify_prereg

BAND=[4,5,6,7,8]
ARMS=['A7_coined_coined','A1_single','A2_coherent2','A7_canon','A7_shuf']
P=Path('results/c10w_oracle/p1_20261007T223707_598959Z')
H=Path('results/mathlab/harvest_20261009T184950.056951Z')
TRAIN=Path('results/c10w_oracle/step0_20261007T223638_531381Z/train_inputs.json')
MODEL_REV='3aab1f1954e9cc14eb9509a215f9e5ca08227a9b'
HARVEST_PREREG='4852d1a229e186c1d054c6f1849f3c130f333738aa9dfc297bedac8cd44ad507'
PINNED = {'results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A1_single_s0_r16.safetensors': '23c199f91412da368d5e2c9204cbac06f2153dd8958da572d69c1ba7785cefe1', 'results/c10w_oracle/p1_20261007T223707_598959Z/train/A1_single_s0_r16.json': '11d1dbef51b0babfd8ceb1cb794ff6a84080b0b08da82c84250d7449dbfe99dc', 'results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A2_coherent2_s0_r16.safetensors': 'd5d9832620fb2db0c6f1ed984ef5e79b34361f61efb253ccc873c07885b35e90', 'results/c10w_oracle/p1_20261007T223707_598959Z/train/A2_coherent2_s0_r16.json': '37c32338c1420a2f385e5d8281c97c30fd9b2b6ab5b83ae0a990753b26220e0e', 'results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_canon_s0_r16.safetensors': '869905010f81fd3c6e006b3a5cf0a809221ac7b5b315f7a3665ee2f58874cd53', 'results/c10w_oracle/p1_20261007T223707_598959Z/train/A7_canon_s0_r16.json': 'dd35028e619ed762a6ed430de056f6eb6b3c71153b425eba711b1847dd84e3c4', 'results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_coined_coined_s0_r16.safetensors': '4e2ae47a450f7014b4d3b003c125796beeb9b37ac94a32f937a65f6187cd124f', 'results/c10w_oracle/p1_20261007T223707_598959Z/train/A7_coined_coined_s0_r16.json': 'a4c4757f6251f8600c47689738b0ba0525827018126f543d376fe49794939977', 'results/c10w_oracle/p1_20261007T223707_598959Z/adapters/A7_shuf_s0_r16.safetensors': '9ce29297d07622e47d5354bd769b26cc0ce89d07128769cfeea39e84a5df094b', 'results/c10w_oracle/p1_20261007T223707_598959Z/train/A7_shuf_s0_r16.json': '3938136ee161d8afdc55b47798854c8ea92e53badffd23ba5463c3f83194d6a0', '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.4.mlp.down_proj_float32_mom2_t100_100000.npz': 'f6ae787454e5bae9eff52155ac699386351246b03e60ab68d728335b0c9a5b58', '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.5.mlp.down_proj_float32_mom2_t100_100000.npz': '26773779c5f95647c844fb42c553221aa81e48206cb3e61602237b3da4e53b3d', '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.6.mlp.down_proj_float32_mom2_t100_100000.npz': '72a4a42bf7586f1b7de5bfce365263d2a84b66f6ffc4ce20f9fa113d115887fd', '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.7.mlp.down_proj_float32_mom2_t100_100000.npz': 'ed2f4c64356fc6388ae4623ccc2bfc9101660fe92a787c193d593a24992aaba5', '/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.8.mlp.down_proj_float32_mom2_t100_100000.npz': '430c1aa56a7cde6626ff02e241b45fd706d02d81d97931536fbed38d8974dd2a', 'results/mathlab/harvest_20261009T184950.056951Z/manifest.json': 'bb9a6f9ad76678ae2289151c9fa64fb0033a6b8b2d7aff0b9a03150180f1ba7e', 'results/mathlab/harvest_20261009T184950.056951Z/inloop_A7_coined_coined.pt': 'abb882982f406ddd5d6536529ce49dee8f31ad3b3243495e93687266e7c6582f', 'experiments/track_c/c10w_oracle_train.py': '64a01fbcbbd8e836f67e623bc50f66ecff8dd59a29d7c82db3bba287d76ea463', 'results/c10w_oracle/step0_20261007T223638_531381Z/train_inputs.json': 'd0fa96af0de8d98c5b0fbd90609cd2f2fa1d27a03013c1db9c530e3ec804c050', 'results/c10w_oracle/step0_20261007T223638_531381Z/step0.json': '82ef86437b5ba00fa78a1b55cfe64e4d85baaceb37aa0726f3015c2b2f7d673e'}


class Invalid(ValueError): pass


def require(value,message):
    if not value: raise Invalid(message)


def torch_module():
    import torch
    return torch


def finite(value):
    torch=torch_module()
    require(value.device.type=='cpu' and bool(torch.isfinite(value).all()),'nonfinite or non-CPU operand')


def verify_file(path,expected):
    require(sha_file(path)==expected,'INVALID-SOURCE: file SHA mismatch: '+str(path))


@contextlib.contextmanager
def bound_input(path,expected):
    path=Path(path); before=path.stat()
    verify_file(path,expected)
    yield path
    after=path.stat()
    require((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==
            (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns),'INVALID-SOURCE: input mutated while consumed')
    verify_file(path,expected)


@dataclass
class Spectrum:
    left: object
    s: object
    right: object


def effective_rank(s):
    finite(s)
    energy=s.double().square()
    require(float(energy.sum())>0,'zero update energy')
    return float(energy.sum().square()/energy.square().sum())


def rank95(s):
    torch=torch_module(); effective_rank(s)
    energy=s.double().square()
    return int(torch.searchsorted(energy.cumsum(0),.95*energy.sum()))+1


def spectrum(matrix):
    torch=torch_module(); finite(matrix)
    require(matrix.ndim==2,'matrix required')
    U,s,Vh=torch.linalg.svd(matrix.double(),full_matrices=False)
    effective_rank(s)
    return Spectrum(U,s,Vh.T)


def adapter_spectrum(A,B,scale):
    torch=torch_module(); finite(A); finite(B)
    require(A.ndim==B.ndim==2 and A.shape[0]==B.shape[1] and math.isfinite(scale),'adapter orientation/scale')
    QB,RB=torch.linalg.qr(B.double(),mode='reduced')
    QA,RA=torch.linalg.qr(A.double().T,mode='reduced')
    U,s,Vh=torch.linalg.svd(scale*RB@RA.T,full_matrices=False)
    effective_rank(s)
    return Spectrum(QB@U,s,QA@Vh.T)


def gap(s,j):
    if j<=0 or j>=len(s): return True
    return float((s[j-1]-s[j])/max(float(s[j-1]),float(s[j]),1e-12*float(s[0])))>1e-4


def leading(spec):
    rank=int((spec.s>1e-6*spec.s[0]).sum())
    r=min(16,rank)
    return Spectrum(spec.left[:,:r],spec.s[:r],spec.right[:,:r]), rank<=16 or gap(spec.s,16)


def energy(Z,Q,indices):
    torch=torch_module(); finite(Q)
    Q=Q.double()
    if isinstance(Z,Spectrum):
        finite(Z.s); require(Z.right.shape[0]==Q.shape[0],'transposed input axis')
        denominator=float(Z.s.square().sum())
    else:
        finite(Z); require(Z.ndim==2 and Z.shape[1]==Q.shape[0],'transposed input axis')
        denominator=float(Z.double().square().sum())
    require(denominator>0,'zero update energy')
    result=0.
    for start in range(0,len(indices),256):
        basis=Q[:,indices[start:start+256]]
        values=(Z.s[:,None]*(Z.right.T@basis)) if isinstance(Z,Spectrum) else Z.double()@basis
        result+=float(values.square().sum())
    return result/denominator


def overlap(a,b):
    torch=torch_module(); finite(a); finite(b)
    cosines=torch.linalg.svdvals(a.double().T@b.double())
    require(bool(((cosines>=-1e-8)&(cosines<=1+1e-8)).all()),'principal cosine outside roundoff range')
    return {'O16':float(cosines.square().sum()/16),'angles_deg':
            (torch.acos(cosines.clamp(0,1))*180/math.pi).tolist(),'ranks':[a.shape[1],b.shape[1]]}


def load_covariance(path):
    import numpy as np
    torch=torch_module()
    with np.load(path,allow_pickle=False) as data:
        moment=data['mom2.mom2']; count=data['mom2.count']
        require(moment.dtype==np.float32 and moment.ndim==2 and moment.shape[0]==moment.shape[1], 'covariance shape/dtype')
        require(count.shape==() and count.dtype==np.int64 and int(count)>0,'moment count must be positive scalar int64')
        # Preserve the producer's native-dtype division, without centering.
        C=torch.from_numpy(np.divide(moment,count,dtype=np.float32))
    finite(C); return C


def covariance_basis(C,k=1024,cell=None):
    torch=torch_module(); finite(C)
    require(C.dtype==torch.float32 and C.ndim==2 and C.shape[0]==C.shape[1] and 0<k<C.shape[0],'native covariance shape')
    d=C.shape[0]
    denom=sum(float(C[:,i:i+256].double().square().sum()) for i in range(0,d,256))
    require(denom>0,'zero covariance')
    if cell: cell('covariance-svd')
    U,s,Vh=torch.linalg.svd(C,full_matrices=False)
    if cell: cell('covariance-checks')
    errors={'symmetry':0.,'svd':0.,'psd':0.,'orthogonality':0.}
    scaled=U*s
    for start in range(0,d,256):
        end=min(d,start+256)
        reference=C[:,start:end].double()
        errors['symmetry']+=float((reference-C[start:end,:].T.double()).square().sum())
        errors['svd']+=float((reference-(scaled@Vh[:,start:end]).double()).square().sum())
        errors['psd']+=float((reference-(scaled@U[start:end,:].T).double()).square().sum())
        orth=(U.T@U[:,start:end]).double()
        orth[torch.arange(start,end),torch.arange(end-start)]-=1
        errors['orthogonality']+=float(orth.square().sum())
    for name in ('symmetry','svd','psd'): errors[name]=math.sqrt(errors[name]/denom)
    errors['orthogonality']=math.sqrt(errors['orthogonality']/d)
    require(errors['symmetry']<=1e-6 and all(errors[n]<=1e-5 for n in ('svd','psd','orthogonality')),
            'covariance numerical/PSD validity failed: '+str(errors))
    del scaled,Vh
    subsets={'top':list(range(k)),'bottom':list(range(d-k,d)),
             'excluded':(s>=.005).nonzero(as_tuple=True)[0].tolist(),
             'allowed':(s<.005).nonzero(as_tuple=True)[0].tolist()}
    return {'Q':U,'s':s,'subsets':subsets,'checks':errors,
            'dimensions':{key:len(value) for key,value in subsets.items()},
            'valid':{'top':gap(s,k),'bottom':gap(s,d-k),'excluded':True,'allowed':True}}


def tensor_sha(tensor):
    finite(tensor)
    digest=hashlib.sha256()
    value=tensor.detach().contiguous()
    rows=value.reshape(-1)
    for i in range(0,len(rows),1<<20): digest.update(rows[i:i+(1<<20)].numpy().tobytes())
    return digest.hexdigest()


def projector_matches(P,null_n,expected_n,expected_sha,probes):
    torch=torch_module()
    if null_n!=expected_n: return False
    if tensor_sha(P)==expected_sha: return True
    if len(probes)!=4: return False
    for j,reference in enumerate(probes):
        actual=P@torch.randn(P.shape[0],generator=torch.Generator().manual_seed(j))
        finite(reference)
        norm=float(reference.double().norm())
        if norm==0 or float((actual.double()-reference.double()).norm())/norm>1e-6: return False
    return True


def validate_capture(bundle,layer,P,null_n):
    prefix=f'l{layer}.'
    needed=['ca_zero','ca_norm','ca_sha256','upd_precast','upd_sha256','Pi_null_n','Pi_sha256',
            *[f'Pi_probe{j}' for j in range(4)]]
    require(all(prefix+key in bundle for key in needed),'missing projector/cache/update capture metadata')
    torch=torch_module()
    update=bundle[prefix+'upd_precast'].clone()
    require(update.dtype==torch.float32 and update.shape==(2048,11008),'saved update shape/dtype mismatch')
    finite(update)
    require(bool(bundle[prefix+'ca_zero']) and float(bundle[prefix+'ca_norm'])==0,'captured cache is not zero')
    digest=hashlib.sha256(); n=P.numel()*4; block=bytes(1<<20)
    while n:
        take=min(n,len(block)); digest.update(block[:take]); n-=take
    require(bytes(bundle[prefix+'ca_sha256'].tolist()).hex()==digest.hexdigest(),'zero-cache byte SHA mismatch')
    require(tensor_sha(update)==bytes(bundle[prefix+'upd_sha256'].tolist()).hex(),'update byte SHA mismatch')
    require(projector_matches(P,null_n,int(bundle[prefix+'Pi_null_n']),
        bytes(bundle[prefix+'Pi_sha256'].tolist()).hex(),[bundle[prefix+f'Pi_probe{j}'].clone() for j in range(4)]),
        'projector identity/probes mismatch')
    return update.double()


def random_control(output_dim,input_dim,ds,layer,j):
    import numpy as np
    torch=torch_module()
    rng=np.random.Generator(np.random.PCG64(20261009+100*layer+j))
    factors=[]
    for dimension in (output_dim,input_dim):
        Q,R=np.linalg.qr(rng.standard_normal((dimension,16)),mode='reduced')
        Q*=np.where(np.diag(R)<0,-1.,1.)
        factors.append(torch.from_numpy(Q))
    ds=ds.double()
    require(len(ds)==16,'rank-16 control needs all sixteen singular values')
    flat=torch.ones(16,dtype=torch.float64)*float(ds.norm())/4
    return Spectrum(factors[0],flat,factors[1]), Spectrum(factors[0],ds,factors[1])


def m16_diagnostic(spec,Q,subsets):
    retained,valid=leading(spec)
    fractions={key:energy(retained,Q,index) for key,index in subsets.items()} if valid else None
    if fractions is not None: validate_fractions(fractions)
    return {'role':'secondary','valid':valid,
        'retained_energy':float(retained.s.square().sum()/spec.s.square().sum()),
        'r_eff':effective_rank(retained.s),
        'energy':fractions}


def validate_fractions(fractions):
    require(all(math.isfinite(v) and -1e-5<=v<=1+1e-5 for v in fractions.values()) and
            abs(fractions['excluded']+fractions['allowed']-1)<=1e-5,'INVALID-ARITHMETIC: energy complement identity')


def summarize_draws(draws):
    require(len(draws)==20,'twenty random draws required')
    result={'mean_energy':{},'q95_energy':{},'overlap':{}}
    for key in draws[0]['energy']:
        values=[v['energy'][key] for v in draws]
        result['mean_energy'][key]=sum(values)/20
        result['q95_energy'][key]=q95(values)
    for key in ('norm','r_eff'):
        values=[v[key] for v in draws]
        result['mean_'+key]=sum(values)/20; result['q95_'+key]=q95(values)
    for side in ('input','output'):
        records=[v[side+'_subspace'] for v in draws]
        result['overlap'][side]={'valid':all(r is not None for r in records)}
        if result['overlap'][side]['valid']:
            values=[r['O16'] for r in records]
            result['overlap'][side].update(mean=sum(values)/20,q95=q95(values))
    return result


def q95(values):
    require(len(values)==20 and all(math.isfinite(v) for v in values),'twenty finite controls required')
    return sorted(values)[18]


def predictions(rows):
    names=['H-COV','H-TOP','H-RANK','H-OVERLAP']
    if len(rows)!=5 or sorted(row['layer'] for row in rows)!=BAND: return dict.fromkeys(names,'INVALID')
    outcomes={}
    for name in names:
        if any(not row.get('valid',False) or (name=='H-TOP' and not row.get('top_valid',False)) or
               (name=='H-OVERLAP' and not row.get('overlap_valid',False)) for row in rows):
            outcomes[name]='INVALID'; continue
        passes=[]
        for row in rows:
            D,M,R=row['D'],row['M'],row['random']
            if name=='H-COV': ok=D['energy']['excluded']>=.25 and D['energy']['excluded']-M['energy']['excluded']>=.15 and D['energy']['excluded']>=R['excluded_q95']+.10
            elif name=='H-TOP': ok=D['energy']['top']-M['energy']['top']>=.10 and D['energy']['top']>=R['top_q95']+.05
            elif name=='H-RANK': ok=D['r_eff']>=8 and D['r_eff']/M['r_eff']>=1.25
            else: ok=D['input_overlap']<=.25 and D['input_overlap']>=R['input_overlap_q95']+.05
            passes.append(ok)
        outcomes[name]='PASS' if sum(passes)>=3 else 'FAIL'
    return outcomes


def verify_manifest(manifest,training):
    require(manifest.get('prereg_sha256')==HARVEST_PREREG,'harvest1 prereg identity mismatch')
    require(manifest.get('source_start')==manifest.get('source_end') and bool(manifest.get('source_start')),'harvest source identity drift')
    require(manifest.get('files',{}).get('inloop_A7_coined_coined.pt',{}).get('sha256')==PINNED[str(H/'inloop_A7_coined_coined.pt')],'harvest1 A7 identity mismatch')
    require(all(isinstance(manifest.get('gates',{}).get(key),dict) and
        manifest['gates'][key].get('passed') is True for key in ('context','law3','law5','observer-parity')),
        'harvest A7 source gates not passed')
    subjects=[p['subject'] for p in manifest['prompts'] if p['kind']=='CANON']
    require(subjects==training['fiction'] and len(subjects)==24,'subject identity/order mismatch')


class Client:
    def __init__(self):
        try:
            require(int(os.environ['NEW1_SUPERVISOR_PID'])==os.getppid(),'supervisor PID mismatch')
            self.socket=socket.socket(fileno=int(os.environ['NEW1_CONTROL_FD']))
            require(self.socket.family==socket.AF_UNIX and self.socket.type==socket.SOCK_STREAM,'private supervisor socket required')
            self.file=self.socket.makefile('rwb',buffering=0)
            self.send({'type':'hello','pid':os.getpid()})
            ack=self.receive()
            require(ack=={'ok':True,'supervisor_pid':os.getppid()},'live supervisor handshake refused')
        except (KeyError,OSError,ValueError) as error:
            raise Invalid('live NEW1 supervisor required before numerical imports: '+str(error)) from error

    def send(self,message): self.file.write((__import__('json').dumps(message)+'\n').encode())

    def receive(self):
        line=self.file.readline(1<<20)
        require(line.endswith(b'\n'),'supervisor IPC closed or partial')
        return strict_json(line)

    def cell(self,phase,name):
        self.send({'type':'cell','phase':phase,'cell':name})
        require(self.receive()=={'ok':True},'supervisor did not grant heavy cell')


def save_controls(path,flat,matched):
    import numpy as np
    with Path(path).open('xb') as out:
        np.savez(out,output=flat.left.numpy(),input=flat.right.numpy(),
                 flat_s=flat.s.numpy(),spectrum_s=matched.s.numpy())
        out.flush(); os.fsync(out.fileno())
    fd=os.open(Path(path).parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    return sha_file(path)


def analyse_layer(C,adapters,M,layer,cell,control_dir):
    return analyse_layer_with_basis(covariance_basis(C,cell=cell),adapters,M,layer,cell,control_dir)


def analyse_layer_with_basis(basis,adapters,M,layer,cell,control_dir):
    torch=torch_module()
    Q,subsets=basis['Q'],basis['subsets']
    cell('update-svd')
    mspec=spectrum(M); mlead,mvalid=leading(mspec)
    row={'layer':layer,'valid':True,'top_valid':basis['valid']['top'],
         'basis':{'checks':basis['checks'],'valid':basis['valid'],'dimensions':basis['dimensions']},'arms':{}}
    cell('projections')
    menergy={key:energy(M,Q,index) for key,index in subsets.items()}
    validate_fractions(menergy)
    require(menergy['excluded']<=1e-4,'closed-form excluded-energy parity failed')
    row['M']={'energy':menergy,'r_eff':effective_rank(mspec.s),'r95':rank95(mspec.s),
              'numerical_rank':int((mspec.s>mspec.s[0]*1e-6).sum()),'norm':float(mspec.s.norm())}
    row['M16']=m16_diagnostic(mspec,Q,subsets)
    # Keep only the leading M bases after its full-spectrum statistics.
    del mspec
    dspec=None; dlead=None
    for name,(A,B,scale) in adapters.items():
        cell('update-svd'); spec=adapter_spectrum(A,B,scale); lead,valid=leading(spec)
        cell('projections'); fractions={key:energy(spec,Q,index) for key,index in subsets.items()}
        validate_fractions(fractions)
        record={'energy':fractions,'r_eff':effective_rank(spec.s),'r95':rank95(spec.s),
            'norm':float(spec.s.norm()),'numerical_rank':int((spec.s>spec.s[0]*1e-6).sum()),
            'overlap_valid':valid and mvalid}
        if record['overlap_valid']:
            record['input_overlap']=overlap(lead.right,mlead.right)['O16']
            record['input_subspace']=overlap(lead.right,mlead.right)
            record['output_subspace']=overlap(lead.left,mlead.left)
        else: record['input_overlap']=None
        record['norm_ratio']=record['norm']/row['M']['norm']
        signed=0.
        for start in range(0,M.shape[1],256):
            update=(spec.left*spec.s)@spec.right[start:start+256].T
            signed+=float((update*M[:,start:start+256]).sum())
        record['matrix_cosine']=signed/(record['norm']*row['M']['norm'])
        row['arms'][name]=record
        if name==ARMS[0]: dspec,dlead=spec,lead
    row['D']=row['arms'][ARMS[0]]; row['overlap_valid']=row['D']['overlap_valid']
    row['shuf_excluded']=row['arms']['A7_shuf']['energy']['excluded']
    cell('random-controls'); draws=[]; secondary=[]
    control_dir.mkdir(parents=True,exist_ok=False)
    for j in range(20):
        flat,matched=random_control(M.shape[0],M.shape[1],dspec.s,layer,j)
        proof=save_controls(control_dir/f'draw{j:02}.npz',flat,matched)
        require(abs(float(flat.s.norm())/float(dspec.s.norm())-1)<=1e-10 and abs(effective_rank(flat.s)-16)<=1e-8,'flat random instrument validity')
        require(abs(float(matched.s.norm())/float(dspec.s.norm())-1)<=1e-10 and abs(effective_rank(matched.s)-effective_rank(dspec.s))<=1e-8,'spectrum random instrument validity')
        for target,spec in ((draws,flat),(secondary,matched)):
            lead,valid=leading(spec)
            record={'j':j,'factor_sha256':proof,'r_eff':effective_rank(spec.s),
                    'norm':float(spec.s.norm()),'energy':{key:energy(spec,Q,index) for key,index in subsets.items()}}
            validate_fractions(record['energy'])
            record['input_subspace']=overlap(lead.right,mlead.right) if valid and mvalid else None
            record['output_subspace']=overlap(lead.left,mlead.left) if valid and mvalid else None
            target.append(record)
    for key,index in subsets.items():
        mean=sum(v['energy'][key] for v in draws)/20
        require(abs(mean-len(index)/M.shape[1])<=.01,'random energy instrument validity')
    row['random']={'draws':draws,**summarize_draws(draws),
                  'excluded_q95':q95([v['energy']['excluded'] for v in draws]),
                  'top_q95':q95([v['energy']['top'] for v in draws]),
                  'input_overlap_q95':q95([v['input_subspace']['O16'] for v in draws]) if mvalid else None}
    row['secondary_random']={'role':'secondary','draws':secondary,**summarize_draws(secondary)}
    return row


def run(client,run_dir,prereg_sha):
    try: verify_prereg(ROOT/'docs/NEW1_ADAPTER_GEOMETRY_PREREG.md',prereg_sha)
    except Stop as error: raise Invalid(str(error)) from error
    client.cell('imports','numerical-dependencies')
    require(sys.version.split()[0]=='3.11.16','Python version mismatch')
    for package,version in {'torch':'2.8.0','numpy':'2.4.6','safetensors':'0.8.0'}.items():
        require(importlib.metadata.version(package)==version,'package version mismatch: '+package)
    torch=torch_module(); torch.set_num_threads(8)
    from safetensors.torch import load_file
    client.cell('load','source-identity')
    for name,digest in PINNED.items(): verify_file(ROOT/Path(name),digest)
    manifest=strict_json((ROOT/H/'manifest.json').read_text())
    training=strict_json((ROOT/TRAIN).read_text()); verify_manifest(manifest,training)
    adapters={}
    for name in ARMS:
        path=ROOT/P/'adapters'/f'{name}_s0_r16.safetensors'
        with bound_input(path,PINNED[str(path.relative_to(ROOT))]): values=load_file(str(path),device='cpu')
        require(values['layers'].tolist()==BAND and float(values['scale'])==1,'adapter scale/layer order mismatch')
        record=strict_json((ROOT/P/'train'/f'{name}_s0_r16.json').read_text())
        require(record['model_revision']==MODEL_REV and record['model_id']=='Qwen/Qwen2.5-3B' and record['layers']==BAND,'model identity mismatch')
        require(record['training_input_sha256']==PINNED[str(TRAIN)] and record['trainer_sha256']==PINNED['experiments/track_c/c10w_oracle_train.py'],'adapter training identity mismatch')
        for layer in BAND:
            A,B=values[f'A_{layer}'],values[f'B_{layer}']
            require(A.dtype==B.dtype==torch.float32 and A.shape==(16,11008) and B.shape==(2048,16),'adapter shape/dtype')
            finite(A); finite(B)
        adapters[name]=values
    bundle_path=ROOT/H/'inloop_A7_coined_coined.pt'
    bundle=torch.load(bundle_path,map_location='cpu',weights_only=True,mmap=True)
    rows=[]
    for layer in BAND:
        client.cell('load',f'l{layer}-operands')
        path=Path(manifest['covariances'][str(layer)]['path'])
        require(str(path) in PINNED and manifest['covariances'][str(layer)]['sha256']==PINNED[str(path)],'cache identity mismatch')
        with bound_input(path,PINNED[str(path)]): C=load_covariance(path)
        require(C.shape==(11008,11008),'production covariance shape mismatch')
        cell=lambda phase:client.cell(phase,f'l{layer}')
        # A single covariance decomposition is reused by identity checks and all arm statistics.
        basis=covariance_basis(C,cell=cell)
        cell('covariance-checks')
        Q=basis['Q']; idx=basis['subsets']['allowed']
        projector=Q[:,idx]@Q[:,idx].T
        M=validate_capture(bundle,layer,projector,len(idx)); del projector
        # analyse_layer consumes this existing basis; never decompose C twice.
        selected={name:(v[f'A_{layer}'],v[f'B_{layer}'],float(v['scale'])) for name,v in adapters.items()}
        row=analyse_layer_with_basis(basis,selected,M,layer,cell,run_dir/'controls'/f'l{layer}')
        client.cell('output',f'l{layer}-statistics')
        path=run_dir/'layers'/f'l{layer}.json'
        durable_json(path,{'tier':TIER,'boundary':BOUNDARY,**row})
        client.send({'type':'artifact','path':str(path.relative_to(run_dir))})
        rows.append(row)
        del C,Q,basis,M,row
    client.cell('load','post-consumption-identity')
    for name,digest in PINNED.items(): verify_file(ROOT/Path(name),digest)
    client.cell('output','final-statistics')
    result={'tier':TIER,'boundary':BOUNDARY,'prereg_sha256':prereg_sha,'harvest':str(H),
        'harvest_prereg_sha256':HARVEST_PREREG,'input_shas':PINNED,'layers':rows,'predictions':predictions(rows),
        'specificity':'NON-SPECIFIC' if sum(abs(r['D']['energy']['excluded']-r['shuf_excluded'])<=.05 for r in rows)>=3 else 'NO SPECIFICITY CLAIM',
        'queue_action':'NONE — calibration and prospective utility not established',
        'budget_feasibility':'UNVERIFIED','behavior':'NOT MEASURED: locality and held-out generalization'}
    durable_json(run_dir/'geometry.json',result)
    client.send({'type':'complete','path':'geometry.json'})


def main():
    # The private live socket is required before parsing any execution flags or importing numerical deps.
    try: client=Client()
    except Invalid as error: print(error,file=sys.stderr); return 3
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir',type=Path,required=True)
    parser.add_argument('--prereg-sha',required=True)
    args=parser.parse_args()
    try: run(client,args.run_dir,args.prereg_sha)
    except BaseException as error:
        durable_json(args.run_dir/'worker_failure.json',{'tier':TIER,'boundary':BOUNDARY,
            'error_type':type(error).__name__,'message':str(error),'prediction_verdict':'NOT COMPUTED'})
        raise
    return 0


if __name__=='__main__': sys.exit(main())
