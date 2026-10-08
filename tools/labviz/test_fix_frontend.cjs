'use strict';

/* These tests execute the production IIFEs. The document adapter provides the
 * render boundary, not a layout engine; measured browser geometry stays deferred. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');
const packageRoot = __dirname;
const documentary = text => ({ value:text, src:{file:'CORPUS/22_D1_CAPACITY_LAW.md',line:7,quote:text} });
const recorded = text => ({ value:text, src:{file:'results/fixture.json',path:'.value'} });
const text = html => String(html).replace(/<[^>]*>/g,' ').replace(/&amp;/g,'&').replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/&gt;/g,'>').replace(/&lt;/g,'<').replace(/\s+/g,' ').trim();
const occurrences = (html, word) => text(html).split(word).length - 1;

function element(id = '') {
  const attributes = new Map();
  return {
    id, innerHTML:'', textContent:'', hidden:false, dataset:{}, style:{}, value:'', children:[], offsetWidth:0,
    setAttribute(key,value) { attributes.set(key,String(value)); },
    getAttribute(key) { return attributes.get(key) ?? null; },
    removeAttribute(key) { attributes.delete(key); },
    addEventListener() {}, querySelectorAll(selector) {
      if (selector !== '[data-pick-run]') return [];
      return [...this.innerHTML.matchAll(/<button\b([^>]*)>/g)].map(match => {
        const option=element();
        for (const attribute of match[1].matchAll(/([\w-]+)="([^"]*)"/g)) {
          option.setAttribute(attribute[1],attribute[2]);
          if (attribute[1] === 'id') option.id=attribute[2];
          if (attribute[1] === 'data-pick-run') option.dataset.pickRun=attribute[2];
        }
        return option;
      }).filter(option=>option.dataset.pickRun);
    },
    append(node) { this.children.push(node); node.parentNode=this; },
    before(node) { this.beforeNode=node; node.parentNode=this.parentNode; },
    after(node) { this.afterNode=node; node.parentNode=this.parentNode; },
    closest() { return this; }, focus() {}, scrollIntoView() {},
  };
}

function card(id, experiment='G6.1') {
  return {
    schema:'labviz.run_card/v1',card_id:id,evidence_status:'RECORDED',built:{builder_sha256:'fixture'},sources:[],
    identity:{name:recorded('results/fixture.json'),model:recorded('Qwen2.5-3B'),date:recorded('2026-06-01'),field:'result'},
    context:{experiment:{...documentary(experiment),node_id:'exp:'+experiment},era:documentary('viability'),question:documentary('The recorded question'),measure:documentary('held-out correctness'),status_now:documentary('SPLIT')},
    headline:{},label:{value:null,missing:'no label recorded',tier:'NOW-not-recorded'},plain_words:{},
    per_fact:[],per_layer:[],gates:[],parts:{structure:{}},events:{timestamped:[],untimed:[]},
  };
}

function fixture(extra={}) {
  const nodes = [
    {node_id:'cond:C1',kind:'cond',label:'C1'}, {node_id:'cond:C10',kind:'cond',label:'C10',status:documentary('OPEN MUST-FIX'),framing_status:documentary('DRAFT')},
    {node_id:'cond:C2',kind:'cond',label:'C2'}, {node_id:'corpus:22',kind:'corpus',label:'22 — D1 CAPACITY LAW: the full documentary title',short_label:documentary('D1 CAPACITY LAW'),question:documentary('At a fixed total edit count, does corruption depend on concentration?'),measure:documentary('held-out same-relation read corruption vs concentration'),framing_status:documentary('DRAFT')},
    {node_id:'layer:Write Engine',kind:'layer',label:'Write Engine'}, {node_id:'model:Qwen2.5-3B',kind:'model',label:'Qwen2.5-3B'},
    {node_id:'exp:G6.1',kind:'exp',label:'G6.1',description:documentary('Read corruption at scale'),status:documentary('SPLIT'),era:'viability'},
    {node_id:'exp:C10W-oracle',kind:'exp',label:'C10W-oracle',era:'c10'},
  ];
  const edges = [
    {source:'layer:Write Engine',target:'cond:C10',edge:'direct',src:{file:'docs/F1_DETERMINATION.md',line:71,quote:'C10 names Write Engine'}},
    {source:'layer:Write Engine',target:'corpus:22',edge:'direct',src:{file:'CORPUS/22_D1_CAPACITY_LAW.md',line:7,quote:'D1 names Write Engine'}},
    {source:'cond:C10',target:'model:Qwen2.5-3B',edge:'direct'},
    {source:'corpus:22',target:'model:Qwen2.5-3B',edge:'direct'},
  ];
  return {
    graph:{nodes,edges},contexts:{eras:{viability:{name:'Editing and serving viability',question:'Can an edit be served?',measure:'recorded corruption',bar:'the original bar'},c10:{name:'Multi-token editing',question:'Can complete answers be written?'}}},
    index:[{card_id:'run-g6',source:'results/fixture.json',chunk:'line-g6',line:'exp:G6.1',experiment:'G6.1',era:'viability',model:'Qwen2.5-3B',title:'Read corruption at scale'},{card_id:'run-c10w',source:'results/fixture-c10w.json',chunk:'line-c10w',line:'exp:C10W-oracle',experiment:'C10W-oracle',era:'c10',model:'Qwen2.5-3B',title:'The oracle test'}],
    models:{},evaluations:[],queue:[],latest_log:{},default_run:'run-g6',...extra,
  };
}

function app(lab=fixture(), allCards=[card('run-g6'),card('run-c10w','C10W-oracle')], lazyRows=null) {
  const elements = new Map();
  const listeners = new Map();
  const document = {
    getElementById(id) { if (!elements.has(id)) elements.set(id,element(id)); return elements.get(id); },
    createElement(tag) { const e=element(); e.tagName=tag.toUpperCase(); return e; },
    querySelectorAll() { return []; },
    addEventListener(name,callback) { listeners.set(name,callback); },
  };
  document.head=element('head');
  const window = { LAB:lab, LAB_CHUNKS:{}, addEventListener() {} };
  const location={hash:''};
  const history={replaceState(_state,_title,hash) { location.hash=hash; }};
  const append=document.head.append.bind(document.head);
  document.head.append=script => {
    append(script);
    queueMicrotask(() => {
      if (script.src === lab.index_src) window.LAB.index=lazyRows;
      else {
        const chunk=String(script.src).replace(/^cards\//,'').replace(/\.js$/,'');
        window.LAB_CHUNKS[chunk]=allCards.filter(c=>lab.index.find(r=>r.card_id===c.card_id)?.chunk===chunk);
      }
      script.onload();
    });
  };
  const api = `window.__renderTest={frame,renderStatus,nodeButton,connectionsFor,renderMapBody,renderMap,renderLines,renderLearn,renderModel,renderCompare,plainWords,factPanel,missing,badge,pickerResults,chooseRun,runRow,scienceTimeline,set:next=>{state={...initial,...next};},get:()=>state,seed:card=>cards.set(card.card_id,card)};`;
  const script=fs.readFileSync(path.join(packageRoot,'app.js'),'utf8').replace('state=readURL(); renderStatus(); fire(render());',api);
  vm.runInNewContext(script,{window,document,location,history,URLSearchParams,requestAnimationFrame(){},matchMedia:()=>({matches:false}),queueMicrotask,console},{filename:'app.js'});
  return {api:window.__renderTest,view:window.LabView,window,document,location,element:id=>document.getElementById(id),click:(dataset,id='')=>{const button=id?document.getElementById(id):element();button.dataset=dataset;return listeners.get('click')({target:{closest:selector=>selector==='button'?button:null}});},focus:id=>listeners.get('focusin')?.({target:document.getElementById(id)}),key:key=>listeners.get('keydown')?.({target:document.getElementById('picker-search'),key,preventDefault(){}})};
}

// Break caught: a retained model/line supplies the frame on another view.
test('Learn owns its frame after the Mistral model and D1 line were selected', () => {
  const r=app();r.api.set({view:'learn',model:'Mistral-7B',line:'corpus:22'});r.api.frame();
  assert.equal(r.element('context-chip').textContent,'Learn & evaluations · all eras');
  assert.match(text(r.element('breadcrumb').innerHTML),/Learn & evaluations$/);
  assert.doesNotMatch(text(r.element('breadcrumb').innerHTML),/Mistral|D1/);
});
test('Map focus owns its chip and breadcrumb', () => {
  const r=app();r.api.set({view:'map',focus:'cond:C10',model:'Mistral-7B',line:'corpus:22'});r.api.frame();
  assert.equal(r.element('context-chip').textContent,'C10');assert.equal(text(r.element('breadcrumb').innerHTML),'Map › C10');
});
test('Model history ignores a retained science line', () => {
  const r=app();r.api.set({view:'model-history',model:'Mistral-7B',line:'corpus:22'});r.api.frame();
  assert.equal(text(r.element('breadcrumb').innerHTML),'Map › Mistral-7B');
});
test('D1 frame uses the short documentary label', () => {
  const r=app();r.api.set({view:'lines',line:'corpus:22'});r.api.frame();
  assert.equal(r.element('context-chip').textContent,'D1 capacity law');
});

// Break caught: shared links exist in data but lack visible shared-with-D1 text.
test('C10 shared links start with common D1 nodes and carry a visible label and science status', () => {
  const lab=fixture();for(let i=0;i<15;i++){lab.graph.nodes.push({node_id:'dec:D-C10-'+i,kind:'dec',label:'D-C10-'+i});lab.graph.edges.push({source:'cond:C10',target:'dec:D-C10-'+i,edge:'direct'},{source:'cond:C1',target:'dec:D-C10-'+i,edge:'direct'});}
  const r=app(lab);r.api.connectionsFor('cond:C10');const html=r.element('connections-panel').innerHTML;
  assert.match(html,/<[^>]+data-science-status[^>]*>OPEN MUST-FIX/);
  const common=html.match(/<button[^>]*data-shared-with="corpus:22"[^>]*>([\s\S]*?)<\/button>/g)||[];
  assert.equal(common.length,2);assert.ok(common.every(button=>text(button).includes('shared with D1')));
  assert.ok(html.indexOf('data-shared="layer:Write Engine"')<html.indexOf('data-shared="dec:D-C10-'));
});
test('Long sourced status keeps its first sentence visible and preserves the full value in collapsed details', () => {
  const lab=fixture(),n=lab.graph.nodes.find(n=>n.node_id==='cond:C10');n.status=documentary('OPEN MUST-FIX. '+ 'Detailed source qualification. '.repeat(20));const before=JSON.stringify(n.status);
  const r=app(lab);r.api.connectionsFor('cond:C10');const html=r.element('connections-panel').innerHTML,detail=html.indexOf('<details');
  assert.ok(detail>0);assert.match(text(html.slice(0,detail)),/OPEN MUST-FIX\./);assert.doesNotMatch(text(html.slice(0,detail)),/Detailed source qualification/);assert.match(text(html.slice(detail)),/Full source status OPEN MUST-FIX\. Detailed source qualification/);assert.equal(JSON.stringify(n.status),before);
});
test('Map connected and dimmed nodes state their path in words', () => {
  const r=app();r.api.set({view:'map',focus:'cond:C10'});
  assert.match(text(r.api.nodeButton({node_id:'layer:Write Engine',kind:'layer',label:'Write Engine'},new Set(['layer:Write Engine']))),/connected/);
  assert.match(text(r.api.nodeButton({node_id:'cond:C1',kind:'cond',label:'C1'})),/not on this line.?s path/);
});
test('Map singular count is one card', () => { const r=app();assert.match(text(r.api.nodeButton({node_id:'exp:G6.1',kind:'exp',label:'G6.1'})),/1 card$/); });
test('Map conditions are naturally ordered', () => { const r=app();r.api.renderMapBody();const html=r.element('map-columns').innerHTML;assert.ok(html.indexOf('data-focus="cond:C2"')<html.indexOf('data-focus="cond:C10"')); });

// Break caught: DRAFT is displayed as scientific status and an era measure masks D1.
test('D1 line renders its own sourced question and measure separately from framing review', () => {
  const r=app();r.api.set({view:'lines',line:'corpus:22'});r.api.renderLines();const html=r.element('view-content').innerHTML;
  assert.match(text(html),/D1 capacity law/);assert.match(text(html),/At a fixed total edit count/);assert.match(text(html),/held-out same-relation read corruption vs concentration/);
  assert.match(text(html),/Framing review: draft/);assert.doesNotMatch(text(html),/Status now \(registry\) DRAFT|No single question recorded/);
});
test('Line document links show five rows before a collapsed counted remainder', () => {
  const lab=fixture();lab.graph.edges=Array.from({length:8},(_,i)=>({source:'corpus:22',target:'spec:§8.'+i,edge:'direct',src:{file:'CORPUS/22_D1_CAPACITY_LAW.md',line:i+1,quote:'Named link '+i}}));
  const r=app(lab);r.api.set({view:'lines',line:'corpus:22'});r.api.renderLines();const html=r.element('view-content').innerHTML;
  const start=html.indexOf('Document links');const detail=html.indexOf('<details',start);assert.ok(start>=0&&detail>start);
  assert.equal((html.slice(start,detail).match(/class="connection-row"/g)||[]).length,5);assert.match(text(html.slice(detail)),/3 more document links/);assert.doesNotMatch(html.slice(detail,html.indexOf('>',detail)+1),/\bopen\b/);
});
test('Map derived links show five rows before the counted collapsed remainder', () => {
  const lab=fixture();lab.graph.edges=Array.from({length:8},(_,i)=>({source:'cond:C10',target:'spec:§8.'+i,edge:'derived',inputs:['source edge']}));
  const r=app(lab);r.api.connectionsFor('cond:C10');const html=r.element('connections-panel').innerHTML;const start=html.indexOf('Derived document links'),detail=html.indexOf('<details',start);
  assert.ok(start>=0&&detail>start);assert.equal((html.slice(start,detail).match(/class="connection-row"/g)||[]).length,5);assert.match(text(html.slice(detail)),/3 more derived document links/);
});

test('Evaluations group by line in closed counted details without duplicate titles or absent-field boilerplate', () => {
  const lab=fixture({evaluations:[{id:'e1',line:'exp:G6.1',era:'viability',source_result:{name:'A sourced retention finding'},result:'The recorded result',question:'Would this help: A sourced retention finding?',template_fields:['question'],ref:'CORPUS/13'},{id:'e2',line:'exp:G6.1',era:'viability',source_result:{name:'A second retention finding'},result:'Another recorded result',ref:'CORPUS/13'}]});
  const r=app(lab);r.api.set({view:'learn',learning:'evaluations'});r.api.renderLearn();const html=r.element('view-content').innerHTML;
  assert.match(html,/<details[^>]*class="evaluation-group"[^>]*>/);assert.doesNotMatch(html.match(/<details[^>]*class="evaluation-group"[^>]*>/)[0],/\bopen\b/);
  assert.match(text(html),/G6\.1 .*2 evaluations/);assert.equal(occurrences(html,'A sourced retention finding'),1);assert.doesNotMatch(text(html),/Would this help|What it leaves open not recorded|Next step not recorded/);
  assert.match(text(html),/Interpretation fields not separately recorded/);
});
test('Evaluation eras are the outer science lines and experiments stay collapsed one level below', () => {
  const lab=fixture({evaluations:[{line:'exp:G6.1',era:'viability',source_result:{name:'Retention finding'},result:'Recorded'},{line:'exp:C10W-oracle',era:'c10',source_result:{name:'Oracle finding'},result:'Recorded'}]});
  for(let i=0;i<8;i++)lab.graph.nodes.push({node_id:'exp:E'+i,kind:'exp',label:'E'+i,era:'viability',status:documentary('Recorded status')});
  const r=app(lab);r.api.set({view:'learn',learning:'evaluations'});r.api.renderLearn();const html=r.element('view-content').innerHTML;
  const stack=[],eras=[],experiments=[];
  for(const match of html.matchAll(/<details\b[^>]*>|<\/details>/g)) {
    if(match[0]==='</details>'){stack.pop();continue;}
    const entry={tag:match[0],ancestors:[...stack]};if(entry.tag.includes('class="evaluation-era"'))eras.push(entry);if(entry.tag.includes('class="evaluation-group"'))experiments.push(entry);stack.push(entry);
  }
  assert.equal(eras.length,2);assert.ok(eras.every(e=>!e.tag.includes(' open')));assert.ok(experiments.length>2);assert.ok(experiments.every(e=>e.ancestors.some(p=>p.tag.includes('class="evaluation-era"'))&&!e.tag.includes(' open')));
  assert.match(text(html),/Editing and serving viability/);assert.match(text(html),/Multi-token editing/);
});
test('Era-filtered evaluations do not include another era', () => {
  const lab=fixture({evaluations:[{line:'exp:G6.1',era:'viability',source_result:{name:'Earlier finding'},result:'Recorded'}]});const r=app(lab);r.api.set({view:'learn',learning:'evaluations',learnEra:'c10'});r.api.renderLearn();assert.doesNotMatch(text(r.element('view-content').innerHTML),/Earlier finding/);
});
test('An unassigned evaluation keeps a visible unknown context without claiming a science line', () => {
  const entry={id:'loop',line:'unassigned',era:'unknown',source_result:{name:'A loop-ledger observation'},result:'Recorded loop observation'},lab=fixture({evaluations:[entry]}),before=JSON.stringify(entry);
  const r=app(lab);r.api.set({view:'learn',learning:'evaluations'});r.api.renderLearn();assert.match(text(r.element('view-content').innerHTML),/Context not recorded 1 evaluation/);assert.equal(JSON.stringify(entry),before);
});
test('Plain words hide only explicitly flagged historical templates', () => {
  const lab=fixture({evaluations:[{ref:'CORPUS/13',template_fields:['question','next_step']}]});const r=app(lab);const c=card('run-g6');c.plain_words={question:documentary('Would this help: fixture?'),result:documentary('The authored **finding**.'),next_step:documentary('A next step is not recorded.'),ref:documentary('CORPUS/13')};
  const html=r.api.plainWords(c);assert.doesNotMatch(text(html),/Would this help|A next step is not recorded/);assert.match(text(html),/The authored finding\./);
});

// Break caught: display cleanup leaks into scientific generated answers or evidence.
test('Documentary markdown is cleaned only in the display and typed evidence stays identical', () => {
  const r=app();const node={node_id:'exp:A7',kind:'exp',label:documentary('A7 · **Bias ablation** `HF`')};const before=JSON.stringify(node);
  assert.match(text(r.api.nodeButton(node)),/A7 · Bias ablation HF/);assert.doesNotMatch(text(r.api.nodeButton(node)),/\*\*|`/);assert.equal(JSON.stringify(node),before);
  const c=card('run-g6');c.per_fact=[{subject:recorded('River'),answer:recorded('Answer'),rewordings_hit:recorded([true]),generated_templates:recorded(['Question {}']),generated_text:recorded(['**raw** | `token`'])}];const cardBefore=JSON.stringify(c);
  assert.match(r.api.factPanel(c,0),/\*\*raw\*\* \| `token`/);assert.equal(JSON.stringify(c),cardBefore);
});
test('Documentary table cleanup preserves conditional-probability pipes in prose', () => {
  const lab=fixture();const n=lab.graph.nodes.find(n=>n.node_id==='cond:C10');n.description=documentary('**Probability** P(full\\|first) | Sourced clause');const before=JSON.stringify(n);
  const r=app(lab);r.api.connectionsFor('cond:C10');assert.match(text(r.element('connections-panel').innerHTML),/Probability P\(full\|first\) · Sourced clause/);assert.equal(JSON.stringify(n),before);
});
test('Missing values display an evidence tier badge without the internal Needs token', () => {
  const r=app();const html=r.api.missing({value:null,missing:'no measurement was recorded',tier:'NOW-not-recorded'});
  assert.match(html,/class="tier-badge"/);assert.doesNotMatch(text(html),/Needs|NOW-not-recorded/);assert.equal(occurrences(html,'not recorded for this run'),1);
});
test('G6 top-1 headline retains its percentage, rung and baseline source', () => {
  const r=app();const c=card('run-g6');c.headline={heldout_top1:{...recorded(33.3),unit:'percent',plain:'edited-relation top-1 correctness vs truth'},rung_n:recorded(100),heldout_baseline_top1:recorded(100)};
  const html=r.api.badge(c);assert.match(text(html),/33\.3% edited-relation top-1 correctness vs truth at N=100; recorded baseline 100%/);assert.doesNotMatch(text(html),/not recorded for this run/);
});
test('Stage exit token is explained with no invented event time', () => {
  const r=app(fixture({latest_log:{last_line:'STAGE_EXIT=2',source:'results/fixture.log'}}));r.api.renderStatus();const html=r.element('status-strip').innerHTML;
  assert.match(text(html),/Last stage ended with exit code 2/);assert.doesNotMatch(text(html),/STAGE_EXIT|process liveness is not recorded|saved|2026-/);
});
test('Log modification time is labelled as a saved snapshot rather than an event time', () => {
  const r=app(fixture({latest_log:{last_line:'STAGE_EXIT=2',modified_utc:'2026-10-08T01:02:03Z'}}));r.api.renderStatus();assert.match(text(r.element('status-strip').innerHTML),/Log saved at 2026-10-08T01:02:03Z/);
});

test('Picker starts empty and filters real index rows after input or focus', () => {
  const r=app();r.api.renderModel(card('run-g6'));assert.equal(r.element('picker-results').innerHTML,'');r.api.pickerResults('G6');assert.match(r.element('picker-results').innerHTML,/data-run="run-g6"/);assert.doesNotMatch(r.element('picker-results').innerHTML,/run-c10w/);
  r.api.renderModel(card('run-g6'));r.focus('picker-search');assert.match(r.element('picker-results').innerHTML,/data-run="run-g6"/);
});
test('Choosing a cross-line run updates the selected run and line in the URL', async () => {
  const r=app();r.api.seed(card('run-c10w','C10W-oracle'));r.api.set({view:'model',line:'exp:G6.1'});await r.api.chooseRun('run-c10w','model');
  assert.equal(r.view.getState().line,'exp:C10W-oracle');const hash=new URLSearchParams(r.location.hash.slice(1));assert.equal(hash.get('line'),'exp:C10W-oracle');assert.equal(hash.get('run'),'run-c10w');
});
test('Compare labels its two data links by side', () => {
  const r=app();const a=card('run-a'),b=card('run-b');a.per_fact=b.per_fact=[{subject:recorded('River'),answer:recorded('Answer'),rewordings_hit:recorded([true]),generated_templates:recorded(['Question {}'])}];r.api.renderCompare(a,b);const html=r.element('view-content').innerHTML;
  const joined=html.slice(html.indexOf('Matched fact'),html.indexOf('<div class="compare-grid"'));
  assert.match(joined,/>Left run data<\/a>/);assert.match(joined,/>Right run data<\/a>/);assert.doesNotMatch(joined,/Data for this view/);
});

test('Lazy home map counts cards without loading the run index', () => {
  const r=app(fixture({index:[],index_src:'cards/index.js',index_counts:{'exp:G6.1':4}}));assert.match(text(r.api.nodeButton({node_id:'exp:G6.1',kind:'exp',label:'G6.1'})),/4 cards$/);assert.equal(r.window.LAB.index.length,0);
});
test('Non-map route loads the classic index once and renders its recorded groups', async () => {
  const rows=fixture().index;const r=app(fixture({index:[],index_src:'cards/index.js'}),[],rows);await r.view.setState({view:'runs'});
  assert.match(r.element('run-results').innerHTML,/data-run="run-g6"/);await r.view.setState({view:'runs'});assert.equal(r.document.head.children.filter(n=>n.src==='cards/index.js').length,1);
});
test('Lazy index rejects an invalid published shape', async () => {
  const r=app(fixture({index:[],index_src:'cards/index.js'}),[],{wrong:'shape'});assert.equal(typeof r.view.ensureIndex,'function');await assert.rejects(r.view.ensureIndex(),/array/);
});

test('Small 3D canvas labels retain every fourth layer and the selected layer', () => {
  const labels=Array.from({length:32},(_,layer)=>({element:{hidden:false,style:{}},layer,position:{clone(){return {x:0,y:0,z:0,applyMatrix4(){return this;},project(){return this;}};}}}));
  const script=fs.readFileSync(path.join(packageRoot,'model.js'),'utf8').replace('window.LabModel={start,stop,selectLayer};','window.__modelTest={placeLabels,setup:(testLabels)=>{host={clientWidth:844,clientHeight:251};card={parts:{structure:{layers:{value:32}}}};selectedLayer=5;objects={matrixWorld:{}};camera={};labels.push(...testLabels);}};');
  const window={};vm.runInNewContext(script,{window,document:{getElementById(){return null;}},console},{filename:'model.js'});window.__modelTest.setup(labels);window.__modelTest.placeLabels();
  assert.equal(labels[3].element.hidden,true);assert.equal(labels[4].element.hidden,false);assert.equal(labels[5].element.hidden,false);
});

test('Rendered write fill separates the recorded mark from its track by at least 3 to 1', () => {
  const css=fs.readFileSync(path.join(packageRoot,'style.css'),'utf8');const fill=css.match(/\.write-mark\s*\{[^}]*background:(#[\da-f]{6})/i)[1];
  const lum=hex=>{const channels=hex.slice(1).match(/../g).map(c=>parseInt(c,16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);return .2126*channels[0]+.7152*channels[1]+.0722*channels[2];};
  const contrast=(lum(fill)+.05)/(lum('#101721')+.05);assert.ok(contrast>=3,`write fill contrast ${contrast.toFixed(3)} is below 3:1`);
});

// Round 2: opening a 50-result picker must not add 50 sequential Tab stops.
for (const view of ['model','compare']) test(view + ' picker exposes options through one keyboard control', () => {
  const lab=fixture();lab.index=Array.from({length:80},(_,i)=>({...lab.index[0],card_id:'run-'+i}));
  const r=app(lab);r.api.set({view});
  if(view==='model')r.api.renderModel(card('run-g6'));else r.api.renderCompare(null,null);
  const html=r.element('view-content').innerHTML;
  assert.match(html,/<input[^>]*id="picker-search"[^>]*role="combobox"/);
  assert.match(html,/<div[^>]*id="picker-results"[^>]*role="listbox"/);
  r.focus('picker-search');const options=r.element('picker-results').querySelectorAll('[data-pick-run]');
  assert.equal(options.length,50);
  assert.ok(options.every(option=>option.getAttribute('role')==='option'&&option.getAttribute('tabindex')==='-1'));
});
test('Picker arrows navigate both directions and Enter chooses a different run', async () => {
  const r=app();r.api.set({view:'model',run:'run-g6'});r.api.seed(card('run-c10w','C10W-oracle'));
  r.api.renderModel(card('run-g6'));r.focus('picker-search');
  r.key('ArrowDown');assert.equal(r.element('picker-search').getAttribute('aria-activedescendant'),'picker-option-run-g6');
  r.key('ArrowDown');assert.equal(r.element('picker-search').getAttribute('aria-activedescendant'),'picker-option-run-c10w');
  r.key('ArrowUp');assert.equal(r.element('picker-search').getAttribute('aria-activedescendant'),'picker-option-run-g6');
  r.key('ArrowUp');assert.equal(r.element('picker-search').getAttribute('aria-activedescendant'),'picker-option-run-c10w');
  r.key('Enter');await new Promise(resolve=>setImmediate(resolve));
  assert.equal(r.view.getState().run,'run-c10w');assert.equal(r.view.getState().line,'exp:C10W-oracle');
});
test('Escape closes and clears picker options and its active descendant', () => {
  const r=app();r.api.renderModel(card('run-g6'));r.element('picker-search').value='G6';r.api.pickerResults('G6');r.key('ArrowDown');r.key('Escape');
  assert.equal(r.element('picker-results').innerHTML,'');assert.equal(r.element('picker-search').value,'');
  assert.equal(r.element('picker-search').getAttribute('aria-expanded'),'false');
  assert.equal(r.element('picker-search').getAttribute('aria-activedescendant'),null);
});
test('Line runs are closed experiment groups with five previews and scoped search links', () => {
  const lab=fixture();lab.index=Array.from({length:15},(_,i)=>({...lab.index[1],card_id:'run-'+i,source:'results/source-'+i+'.json',role:i===0?'control':'binding',label:i===0?'PASS':i===1?'LEAD':'NULL'}));
  const r=app(lab);r.api.set({view:'lines',line:'exp:C10W-oracle'});r.api.renderLines();const html=r.element('view-content').innerHTML;
  const stack=[],groups=[],rows=[];
  for(const match of html.matchAll(/<details\b[^>]*>|<\/details>|<button\b[^>]*class="run-row"[^>]*>/g)){
    if(match[0]==='</details>'){stack.pop();continue;}
    if(match[0].startsWith('<button')){rows.push({tag:match[0],parents:[...stack]});continue;}
    if(match[0].includes('class="line-run-group"'))groups.push(match[0]);stack.push(match[0]);
  }
  assert.equal(groups.length,1);assert.doesNotMatch(groups[0],/\bopen\b/);assert.equal(rows.length,5);
  assert.ok(rows.every(row=>row.parents.includes(groups[0])));
  assert.match(text(html),/15 recorded cards.*best recorded binding label: LEAD/);
  assert.match(html,/data-line-runs="exp:C10W-oracle"/);assert.match(text(html),/Search all 15 in Runs/);
});
test('A large line folds extra experiment groups without dropping their run previews', () => {
  const lab=fixture();lab.index=Array.from({length:12},(_,i)=>({...lab.index[1],card_id:'run-'+i,experiment:'Experiment '+i,line:'exp:Experiment '+i}));
  const r=app(lab);r.api.set({view:'lines',line:'era:c10'});r.api.renderLines();
  const html=r.element('view-content').innerHTML;
  const runs=html.slice(html.indexOf('<h3>Recorded runs in this line</h3>'),html.indexOf('<h3>Document links</h3>'));
  const folded=runs.indexOf('<details class="more-links">');assert.ok(folded>0);
  assert.equal((runs.slice(0,folded).match(/class="line-run-group"/g)||[]).length,5);
  assert.equal((runs.match(/class="line-run-group"/g)||[]).length,12);
  assert.match(text(runs),/7 more experiment groups/);
  assert.equal((runs.match(/data-run="run-/g)||[]).length,12);
});
test('Dated timeline is a closed source count and does not duplicate run rows', () => {
  const lab=fixture();lab.index=[{...lab.index[0],date:'2026-10-08T03:32:19.123Z'},{...lab.index[0],card_id:'duplicate',date:'2026-10-08T03:32:19.123Z'}];
  const r=app(lab);const html=r.api.scienceTimeline('exp:G6.1');
  assert.match(html,/<details[^>]*class="observation-timeline"[^>]*>/);
  assert.doesNotMatch(html.match(/<details[^>]*class="observation-timeline"[^>]*>/)[0],/\bopen\b/);
  assert.match(text(html),/1 dated source snapshot/);assert.doesNotMatch(html,/class="run-row"/);
  assert.match(text(html),/2026-10-08 03:32 UTC/);assert.doesNotMatch(text(html),/T03:32|\.123Z/);
  const closing=html.indexOf('</details>');assert.ok(html.indexOf('class="caption"')>closing&&html.indexOf('class="caveat"')>closing);
});
test('Run rows clean and shorten documentary titles without changing source text', () => {
  const r=app();
  for(const line of ['corpus:22','era:f1-conditions','era:t-branch']){
    const row={card_id:'run-doc',line,title:'**D1** `DILUTED` trajectory '+ 'A full documentary paragraph. '.repeat(10),source:'results/d1.json',field:'DILUTED.trajectory'};
    const before=JSON.stringify(row),html=r.api.runRow(row),title=text(html.match(/<strong>([\s\S]*?)<\/strong>/)[1]);
    assert.doesNotMatch(text(html),/\*\*|`/);assert.ok(title.length<=100);assert.match(title,/D1 DILUTED trajectory/);assert.equal(JSON.stringify(row),before);
  }
});
test('Run row distinguishes recipe and arm in words and formats recorded UTC time', () => {
  const r=app();const html=r.api.runRow({card_id:'run-a7',experiment:'C10V-layerpick',field:'recipes.B.delta_norms.A7_coined_coined',role:'binding',label:'NULL',date:'2026-10-08T03:32:19.123Z',model:'Qwen2.5-3B'});
  assert.match(text(html),/recipe B · A7 coined\/coined · binding · NULL/);
  assert.match(text(html),/2026-10-08 03:32 UTC/);assert.doesNotMatch(text(html),/recipes\.B|delta_norms|A7_coined_coined|T03:32/);
});
test('Documentary run rows accept typed missing recipe and arm metadata', () => {
  const r=app();let html;
  assert.doesNotThrow(()=>{html=r.api.runRow({card_id:'run-doc',title:'D1 · DILUTED trajectory',field:'DILUTED.trajectory',recipe:{value:null,missing:'not recorded',tier:'NOW-not-recorded'},arm:{value:null,missing:'not recorded',tier:'NOW-not-recorded'}});});
  assert.match(text(html),/D1 · DILUTED trajectory/);assert.match(text(html),/DILUTED · trajectory/);
  assert.doesNotMatch(text(html),/\[object Object\]|DILUTED\.trajectory/);
});
test('Indexed numeric arm zero remains a named arm in a run row', () => {
  const r=app();let html;
  assert.doesNotThrow(()=>{html=r.api.runRow({card_id:'run-zero',title:'Sub-batch sweep',field:'arms[0].heldout_by_seed.hoseed0.edited_rel',arm:0});});
  assert.match(text(html),/arm 0/);assert.doesNotMatch(text(html),/arms\[0\]|heldout_by_seed|\[object Object\]/);
});
test('Learn labels era options and identifies a numerical bar as a threshold', () => {
  const lab=fixture();lab.contexts.eras.c10.bar='61/72';const r=app(lab);r.api.renderLearn();const html=r.element('view-content').innerHTML;
  assert.match(html,/<option value="c10"[^>]*>Multi-token editing<\/option>/);
  assert.match(text(html),/the line.s bar: 61 of 72/);assert.doesNotMatch(text(html),/61\/72/);
});
test('Failed 3D request restores the pressed 2D toggle and visible fallback', async () => {
  const r=app();r.api.seed(card('run-g6'));r.api.set({view:'model',run:'run-g6'});
  r.window.LabModel={start:async()=>{throw new Error('3D unavailable in this fixture');},stop(){}};
  r.element('show-3d').setAttribute('aria-pressed','true');r.element('show-2d').setAttribute('aria-pressed','false');
  r.click({},'show-3d');await new Promise(resolve=>setImmediate(resolve));
  assert.equal(r.element('show-3d').getAttribute('aria-pressed'),'false');assert.equal(r.element('show-2d').getAttribute('aria-pressed'),'true');
  assert.equal(r.element('tower').hidden,true);assert.equal(r.element('tower-fallback').hidden,false);
});
test('Compare places data links in one spaced action row', () => {
  const r=app();r.api.renderCompare(card('run-a'),card('run-b'));const html=r.element('view-content').innerHTML;
  assert.match(html,/<div class="run-actions"><a[^>]*>Left run data<\/a><a[^>]*>Right run data<\/a><\/div>/);
});
test('Status introduces a saved answer check while preserving its recorded log line', () => {
  const line='A1_single canon=100.0 para=100.0 kl 1.99579 ppl 21.755->19.84';
  const r=app(fixture({latest_log:{last_line:line,source:'results/fixture.log'}}));r.api.renderStatus();const html=r.element('status-strip').innerHTML;
  assert.match(text(html),/Saved answer check for A1 single/);assert.ok(text(html).includes(line));
});
