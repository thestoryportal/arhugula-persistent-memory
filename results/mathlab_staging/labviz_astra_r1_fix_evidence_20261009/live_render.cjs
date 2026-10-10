"use strict";
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=process.cwd(),site=path.join(root,'results/labviz/site');
const elements=new Map();
function element(){const attrs=new Map();return {innerHTML:'',textContent:'',dataset:{},style:{},children:[],value:'',setAttribute(k,v){attrs.set(k,String(v));},getAttribute(k){return attrs.get(k);},removeAttribute(k){attrs.delete(k);},addEventListener(){},querySelectorAll(){return [];},append(n){this.children.push(n);},after(){},focus(){},scrollIntoView(){}};}
const get=id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id);};
const document={getElementById:get,querySelectorAll:()=>[],addEventListener(){},createElement:element,head:element()};
const window={addEventListener(){}},location={hash:''},history={replaceState(_s,_t,hash){location.hash=hash;}};
const context=vm.createContext({window,document,location,history,URLSearchParams,requestAnimationFrame(){},matchMedia:()=>({matches:false}),queueMicrotask,console});
for(const name of ['data.js','cards/index.js'])vm.runInContext(fs.readFileSync(path.join(site,name),'utf8'),context);
const row=window.LAB.index.find(r=>r.source==='results/mathlab_staging/runs/harvest_20261009T184932Z_95961/events.jsonl');
assert.ok(row);
vm.runInContext(fs.readFileSync(path.join(site,'cards',row.chunk+'.js'),'utf8'),context);
const card=window.LAB_CHUNKS[row.chunk].find(c=>c.card_id===row.card_id);
assert.deepEqual(JSON.parse(JSON.stringify(card)),JSON.parse(fs.readFileSync(path.join(site,'cards',row.card_id+'.json'),'utf8')));
const expose='window.testMathlab={frame,renderRun,set:next=>{state={...initial,...next}},seed:c=>cards.set(c.card_id,c)};';
const app=fs.readFileSync(path.join(site,'app.js'),'utf8').replace('state=readURL(); renderStatus(); fire(render());',expose);
assert.ok(app.includes(expose));vm.runInContext(app,context);
window.testMathlab.seed(card);window.testMathlab.set({view:'run',run:card.card_id});window.testMathlab.frame(card);window.testMathlab.renderRun(card);
const html=get('view-content').innerHTML,text=html.replace(/<[^>]*>/g,' ').replace(/\s+/g,' ');
assert.match(get('evidence-badge').textContent,/MATH-PROXY/);assert.match(text,/Outcome: PASS/);
assert.match(text,/math estimate, not evidence/);assert.match(text,/0 of 3 recorded mint arms eligible for replay admission \(derived\)/);
assert.match(text,/all three required norm checks failed/);assert.match(text,/Operand harvest completed; math-proxy analysis remains pending/);
for(let seed=0;seed<3;seed++)assert.match(text,new RegExp('mint-norm-mint1_s'+seed));
assert.match(html,/evidence\/logs\/pending_findings\/10_mathlab_harvest_20261009T192601\.184026Z\.md/);
assert.doesNotMatch(html,/class="score"|Save SVG|Save PNG/);
fs.writeFileSync(path.join(__dirname,'harvest-render.html'),html);
fs.writeFileSync(path.join(__dirname,'harvest-render.txt'),text+'\n');
const receipt={card_id:card.card_id,source:row.source,status:row.mathlab.status,outcome:card.mathlab.state.value.outcome,
proxy_badge:get('evidence-badge').textContent,zero_eligibility:'0 of 3 recorded mint arms eligible for replay admission (derived)',
renderer:'production generated site/app.js IIFE',browser_geometry:'UNVERIFIED',assertions:'PASS'};
fs.writeFileSync(path.join(__dirname,'live-render-receipt.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
