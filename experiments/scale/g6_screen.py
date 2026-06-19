import os, sys
LLMDB_ROOT = os.environ.get("LLMDB_ROOT", "/workspace")
import os, sys, json
os.environ["HF_HOME"]=f"{LLMDB_ROOT}/hf_cache"; os.environ["HF_HUB_OFFLINE"]="0"
ENGINE_ROOT=f"{LLMDB_ROOT}/memit_dry_run/memit"; sys.path.insert(0,ENGINE_ROOT); os.chdir(ENGINE_ROOT)
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# G6.1 screener — Qwen2.5-3B (the proven in-solve-AlphaEdit target). Select entities confident+CORRECT
# on the EDIT attributes (capital/currency/language) so the null floor is clean (avoids the Llama false-no-op
# trap). continent kept too (used as a same-entity untouched probe in the scale harness). Pool ~45 -> keep
# those passing all three edit-attrs -> scale harness takes the first ~34 (3 fields each ~= 100 records).
ID="Qwen/Qwen2.5-3B"; REV="3aab1f1954e9cc14eb9509a215f9e5ca08227a9b"
tok=AutoTokenizer.from_pretrained(ID, revision=REV)
if tok.pad_token is None: tok.pad_token=tok.eos_token
model=AutoModelForCausalLM.from_pretrained(ID, revision=REV, torch_dtype=torch.float16, device_map="cuda").eval()

@torch.no_grad()
def predict(p,k=3):
    ids=tok(p,return_tensors="pt").to("cuda"); pr=torch.softmax(model(**ids).logits[0,-1].float(),dim=-1); t=torch.topk(pr,k)
    return [(tok.decode([int(i)]),round(float(v),4)) for i,v in zip(t.indices,t.values)]

TMPL={"capital":"The capital of {} is the city of",
      "currency":"The official currency of {} is the",
      "continent":"{} is located on the continent of",
      "language":"The official language of {} is"}
TRUTH={
 "France":{"capital":"Paris","currency":"euro","continent":"Europe","language":"French"},
 "Japan":{"capital":"Tokyo","currency":"yen","continent":"Asia","language":"Japanese"},
 "Egypt":{"capital":"Cairo","currency":"pound","continent":"Africa","language":"Arabic"},
 "Germany":{"capital":"Berlin","currency":"euro","continent":"Europe","language":"German"},
 "Italy":{"capital":"Rome","currency":"euro","continent":"Europe","language":"Italian"},
 "Spain":{"capital":"Madrid","currency":"euro","continent":"Europe","language":"Spanish"},
 "Russia":{"capital":"Moscow","currency":"ruble","continent":"Europe","language":"Russian"},
 "China":{"capital":"Beijing","currency":"yuan","continent":"Asia","language":"Chinese"},
 "Greece":{"capital":"Athens","currency":"euro","continent":"Europe","language":"Greek"},
 "Norway":{"capital":"Oslo","currency":"krone","continent":"Europe","language":"Norwegian"},
 "Poland":{"capital":"Warsaw","currency":"zloty","continent":"Europe","language":"Polish"},
 "Turkey":{"capital":"Ankara","currency":"lira","continent":"Asia","language":"Turkish"},
 "Portugal":{"capital":"Lisbon","currency":"euro","continent":"Europe","language":"Portuguese"},
 "Austria":{"capital":"Vienna","currency":"euro","continent":"Europe","language":"German"},
 "Sweden":{"capital":"Stockholm","currency":"krona","continent":"Europe","language":"Swedish"},
 "Finland":{"capital":"Helsinki","currency":"euro","continent":"Europe","language":"Finnish"},
 "Denmark":{"capital":"Copenhagen","currency":"krone","continent":"Europe","language":"Danish"},
 "Hungary":{"capital":"Budapest","currency":"forint","continent":"Europe","language":"Hungarian"},
 "Iran":{"capital":"Tehran","currency":"rial","continent":"Asia","language":"Persian"},
 "Iraq":{"capital":"Baghdad","currency":"dinar","continent":"Asia","language":"Arabic"},
 "Thailand":{"capital":"Bangkok","currency":"baht","continent":"Asia","language":"Thai"},
 "Vietnam":{"capital":"Hanoi","currency":"dong","continent":"Asia","language":"Vietnamese"},
 "Indonesia":{"capital":"Jakarta","currency":"rupiah","continent":"Asia","language":"Indonesian"},
 "Kenya":{"capital":"Nairobi","currency":"shilling","continent":"Africa","language":"Swahili"},
 "Nigeria":{"capital":"Abuja","currency":"naira","continent":"Africa","language":"English"},
 "Morocco":{"capital":"Rabat","currency":"dirham","continent":"Africa","language":"Arabic"},
 "Peru":{"capital":"Lima","currency":"sol","continent":"America","language":"Spanish"},
 "Chile":{"capital":"Santiago","currency":"peso","continent":"America","language":"Spanish"},
 "Switzerland":{"capital":"Bern","currency":"franc","continent":"Europe","language":"German"},
 "Netherlands":{"capital":"Amsterdam","currency":"euro","continent":"Europe","language":"Dutch"},
 "Ukraine":{"capital":"Kyiv","currency":"hryvnia","continent":"Europe","language":"Ukrainian"},
 "Romania":{"capital":"Bucharest","currency":"leu","continent":"Europe","language":"Romanian"},
 "Serbia":{"capital":"Belgrade","currency":"dinar","continent":"Europe","language":"Serbian"},
 "Croatia":{"capital":"Zagreb","currency":"euro","continent":"Europe","language":"Croatian"},
 "Cuba":{"capital":"Havana","currency":"peso","continent":"America","language":"Spanish"},
 "Israel":{"capital":"Jerusalem","currency":"shekel","continent":"Asia","language":"Hebrew"},
 "Belgium":{"capital":"Brussels","currency":"euro","continent":"Europe","language":"Dutch"},
 "Argentina":{"capital":"Buenos","currency":"peso","continent":"America","language":"Spanish"},
 "Bulgaria":{"capital":"Sofia","currency":"lev","continent":"Europe","language":"Bulgarian"},
 "Slovakia":{"capital":"Bratislava","currency":"euro","continent":"Europe","language":"Slovak"},
 "Lebanon":{"capital":"Beirut","currency":"pound","continent":"Asia","language":"Arabic"},
 "Cambodia":{"capital":"Phnom","currency":"riel","continent":"Asia","language":"Khmer"},
 "Mongolia":{"capital":"Ulaanbaatar","currency":"tugrik","continent":"Asia","language":"Mongolian"},
 "Ghana":{"capital":"Accra","currency":"cedi","continent":"Africa","language":"English"},
 "Ecuador":{"capital":"Quito","currency":"dollar","continent":"America","language":"Spanish"},
 "Estonia":{"capital":"Tallinn","currency":"euro","continent":"Europe","language":"Estonian"},
 "Latvia":{"capital":"Riga","currency":"euro","continent":"Europe","language":"Latvian"},
 "Lithuania":{"capital":"Vilnius","currency":"euro","continent":"Europe","language":"Lithuanian"},
 "Slovenia":{"capital":"Ljubljana","currency":"euro","continent":"Europe","language":"Slovenian"},
 "Iceland":{"capital":"Reykjavik","currency":"krona","continent":"Europe","language":"Icelandic"},
 "Albania":{"capital":"Tirana","currency":"lek","continent":"Europe","language":"Albanian"},
 "Georgia":{"capital":"Tbilisi","currency":"lari","continent":"Asia","language":"Georgian"},
 "Armenia":{"capital":"Yerevan","currency":"dram","continent":"Asia","language":"Armenian"},
 "Pakistan":{"capital":"Islamabad","currency":"rupee","continent":"Asia","language":"Urdu"},
 "Bangladesh":{"capital":"Dhaka","currency":"taka","continent":"Asia","language":"Bengali"},
 "Philippines":{"capital":"Manila","currency":"peso","continent":"Asia","language":"Filipino"},
 "Syria":{"capital":"Damascus","currency":"pound","continent":"Asia","language":"Arabic"},
 "Jordan":{"capital":"Amman","currency":"dinar","continent":"Asia","language":"Arabic"},
 "Tunisia":{"capital":"Tunis","currency":"dinar","continent":"Africa","language":"Arabic"},
 "Algeria":{"capital":"Algiers","currency":"dinar","continent":"Africa","language":"Arabic"},
 "Venezuela":{"capital":"Caracas","currency":"bolivar","continent":"America","language":"Spanish"},
 "Colombia":{"capital":"Bogota","currency":"peso","continent":"America","language":"Spanish"},
 "Uruguay":{"capital":"Montevideo","currency":"peso","continent":"America","language":"Spanish"},
 "Korea":{"capital":"Seoul","currency":"won","continent":"Asia","language":"Korean"},
 "India":{"capital":"Delhi","currency":"rupee","continent":"Asia","language":"Hindi"},
 "Brazil":{"capital":"Brasilia","currency":"real","continent":"America","language":"Portuguese"},
 "Mexico":{"capital":"Mexico","currency":"peso","continent":"America","language":"Spanish"},
 "Saudi Arabia":{"capital":"Riyadh","currency":"riyal","continent":"Asia","language":"Arabic"},
 "Qatar":{"capital":"Doha","currency":"riyal","continent":"Asia","language":"Arabic"},
 "Oman":{"capital":"Muscat","currency":"rial","continent":"Asia","language":"Arabic"},
 "Yemen":{"capital":"Sanaa","currency":"rial","continent":"Asia","language":"Arabic"},
 "Libya":{"capital":"Tripoli","currency":"dinar","continent":"Africa","language":"Arabic"},
 "Sudan":{"capital":"Khartoum","currency":"pound","continent":"Africa","language":"Arabic"},
 "Bahrain":{"capital":"Manama","currency":"dinar","continent":"Asia","language":"Arabic"},
 "Kuwait":{"capital":"Kuwait","currency":"dinar","continent":"Asia","language":"Arabic"},
 "Nepal":{"capital":"Kathmandu","currency":"rupee","continent":"Asia","language":"Nepali"},
 "Ethiopia":{"capital":"Addis","currency":"birr","continent":"Africa","language":"Amharic"},
 "Senegal":{"capital":"Dakar","currency":"franc","continent":"Africa","language":"French"},
 "Cameroon":{"capital":"Yaounde","currency":"franc","continent":"Africa","language":"French"},
 "Angola":{"capital":"Luanda","currency":"kwanza","continent":"Africa","language":"Portuguese"},
 "Mozambique":{"capital":"Maputo","currency":"metical","continent":"Africa","language":"Portuguese"},
 "Zimbabwe":{"capital":"Harare","currency":"dollar","continent":"Africa","language":"English"},
 "Zambia":{"capital":"Lusaka","currency":"kwacha","continent":"Africa","language":"English"},
 "Honduras":{"capital":"Tegucigalpa","currency":"lempira","continent":"America","language":"Spanish"},
 "Nicaragua":{"capital":"Managua","currency":"cordoba","continent":"America","language":"Spanish"},
 "Paraguay":{"capital":"Asuncion","currency":"guarani","continent":"America","language":"Spanish"},
 "Kazakhstan":{"capital":"Astana","currency":"tenge","continent":"Asia","language":"Kazakh"},
 "Uzbekistan":{"capital":"Tashkent","currency":"som","continent":"Asia","language":"Uzbek"},
 "Czechia":{"capital":"Prague","currency":"koruna","continent":"Europe","language":"Czech"},
 "Malaysia":{"capital":"Kuala","currency":"ringgit","continent":"Asia","language":"Malay"},
 "Afghanistan":{"capital":"Kabul","currency":"afghani","continent":"Asia","language":"Pashto"},
}
def correct(top1, truth):
    a=top1.strip().lower(); b=truth.lower()
    return bool(a) and (a==b or b.startswith(a) or a.startswith(b))
def single_tok(s):  # leading-token of " <value>" — counterfact must be cleanly single-token (multi-token = G7)
    return len(tok(" "+s, add_special_tokens=False)["input_ids"])==1

EDIT_ATTRS=["capital","language"]; EDIT_CONF=0.40
out={"model":ID,"screen":{},"edit_attrs":EDIT_ATTRS,"edit_conf":EDIT_CONF}
print(f"\n=== G6 SCREEN — {ID} — top1(p) | correct? | single-tok? ===")
for e,tr in TRUTH.items():
    row={}; print(f"\n{e}")
    for a,t in TMPL.items():
        top=predict(t.format(e)); ok=correct(top[0][0],tr[a]); st=single_tok(tr[a])
        row[a]={"top1":top[0][0],"p":top[0][1],"truth":tr[a],"correct":ok,"single_tok":st,"top3":top}
        print(f"  {a:10s} p={top[0][1]:.3f} top1='{top[0][0]}' truth='{tr[a]}' {'OK' if ok else 'X'} {'1tok' if st else 'MULTI'}")
    out["screen"][e]=row

# Select: both EDIT attrs correct & p>=EDIT_CONF (clean null floor). single_tok of TRUTH recorded but NOT
# gating — expression keys on the first token; the single-token constraint applies to the COUNTERFACT target,
# which the scale harness assigns from a single-token value pool.
sel={}
for e,r in out["screen"].items():
    if all(r[a]["correct"] and r[a]["p"]>=EDIT_CONF for a in EDIT_ATTRS):
        sel[e]={a:{"truth":r[a]["truth"],"p":r[a]["p"],"single_tok":r[a]["single_tok"]} for a in EDIT_ATTRS}
        sel[e]["continent"]={"truth":r["continent"]["truth"],"correct":r["continent"]["correct"],"p":r["continent"]["p"]}
out["selected"]=sel
print(f"\n=== SELECTED (both edit-attrs correct & p>={EDIT_CONF}) — {len(sel)} entities, {len(sel)*2} records ===")
for e in sel: print(f"  {e}: "+", ".join(f"{a}='{sel[e][a]['truth']}'({sel[e][a]['p']:.2f}){'' if sel[e][a]['single_tok'] else '[MT]'}" for a in EDIT_ATTRS))
# v2: expanded TRUTH dict (~91 candidates) for the A2 50/10/10 disjoint-pool split (N=100).
# Written to a NEW file to preserve g6_screen_qwen3b.json (the A0/A1 stimulus, 56 entities).
fn=f"{LLMDB_ROOT}/configs/screens/g6_screen_qwen3b_v2.json"; json.dump(out,open(fn,"w"),indent=2)
print("\nwrote",fn,f"\n>>> {len(sel)} entities pass; {len(sel)*2} records (2 fields each). A2 needs >=70 (50/10/10).")
