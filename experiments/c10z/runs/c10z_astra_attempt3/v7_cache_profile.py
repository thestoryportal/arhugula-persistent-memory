import numpy as np, json, sys
from scipy.stats import rankdata
obs={4:.9856,5:.9805,6:.9528,7:.8734,8:.7719,9:.8136,10:.8013,11:.8085,12:.7670}
P="/Volumes/memit/llm-database-poc-mirror/arhugula-persistent-memory/covariance_caches/Qwen_Qwen2.5-3B/wikipedia_stats/model.layers.{}.mlp.down_proj_float32_mom2_t100_100000.npz"
rng=np.random.default_rng(0)
def sp(a,b):
    ra,rb=rankdata(a),rankdata(b); return np.corrcoef(ra,rb)[0,1]
out={}
for l in range(4,13):
    with np.load(P.format(l)) as z:
        d=np.diag(z["mom2.mom2"]).astype(np.float64)/int(z["mom2.count"]); cnt=int(z["mom2.count"])
    ld=np.log10(np.maximum(d,1e-30))
    srt=np.sort(d)[::-1]
    top1=srt[:110].sum()/d.sum()
    # sigma of multiplicative lognormal noise that reproduces the observed Spearman
    sig=None
    for s in np.arange(0.02,3.0,0.02):
        r=np.mean([sp(d,d*np.exp(s*rng.standard_normal(d.size))) for _ in range(2)])
        if r<=obs[l]: sig=round(float(s),2); break
    out[l]=dict(count=cnt,nonfinite=int((~np.isfinite(d)).sum()),zeros=int((d<=0).sum()),
        log10_p1=round(float(np.percentile(ld,1)),2),log10_p50=round(float(np.percentile(ld,50)),2),log10_p99=round(float(np.percentile(ld,99)),2),
        iqr_log10=round(float(np.percentile(ld,75)-np.percentile(ld,25)),3),top1pct_mass=round(float(top1),3),max_over_median=round(float(d.max()/np.median(d)),1),
        sigma_for_observed=sig,obs=obs[l])
    print(l,out[l],flush=True)
json.dump(out,open(sys.argv[1],"w"),indent=1)
