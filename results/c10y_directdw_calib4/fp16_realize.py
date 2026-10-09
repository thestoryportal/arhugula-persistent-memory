import sys, torch
from safetensors import safe_open
torch.manual_seed(0)
import json; idx=json.load(open(sys.argv[1]+'/model.safetensors.index.json'))['weight_map']
norms={4:15.844840305550647,5:12.115956650516095,6:12.02611881845846,7:20.007982773715508,8:28.623633564518745}  # A7 recipe-A write norms (c10x rerun3 pass1 write_norms_float64)
def dist(a,b): a=a.double();b=b.double();return float((a-b).norm()/a.norm())
if True:
    for l,n in norms.items():
        k=f'model.layers.{l}.mlp.down_proj.weight'; W0=safe_open(sys.argv[1]+'/'+idx[k],'pt',device='cpu').get_tensor(k).half()
        R=torch.randn(W0.shape[0],24,dtype=torch.float64);B=torch.randn(24,W0.shape[1],dtype=torch.float64)
        u64=R@B;u64*=n/u64.norm()
        u_ref=u64.float()                                  # path 1: one fp32 rounding of the exact product
        u_fac=(R.float()@B.float())*(n/float((R@B).norm()))  # path 2: fp32 factored product (different rounding)
        out=[]
        for name,u2 in (('fp32-reassoc',u_fac),('rel1e-6',u_ref*(1+1e-6*torch.randn_like(u_ref))),('rel1e-5',u_ref*(1+1e-5*torch.randn_like(u_ref)))):
            D1=(W0+u_ref.half()).half().float()-W0.float(); D2=(W0+u2.half()).half().float()-W0.float()
            out.append(f"{name}: fp32 {dist(u_ref,u2):.1e} -> realized {dist(D1,D2):.2e} (elements changed {float((D1!=D2).float().mean()):.2%})")
        print(f"L{l}", " | ".join(out))
