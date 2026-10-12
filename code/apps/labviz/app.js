/* The cards are the evidence source. This file only selects and renders them. */
(() => {
  'use strict';
  const lab = window.LAB || {};
  let index = lab.index || [], indexLoading;
  const graph = lab.graph || { nodes: [], edges: [] };
  const nodes = new Map(graph.nodes.map(n => [n.node_id, n]));
  const cards = new Map(), chunks = new Map();
  const content = document.getElementById('view-content');
  const connections = document.getElementById('connections-panel');
  const value = x => x && typeof x === 'object' && Object.hasOwn(x, 'value') ? x.value : x;
  const esc = x => String(x ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const number = x => typeof x === 'number' && Number.isFinite(x);
  const fmt = x => number(x) ? x.toLocaleString('en-US', { maximumFractionDigits: 3 }) : typeof x === 'string' ? x : JSON.stringify(x);
  const array = x => Array.isArray(value(x)) ? value(x) : [];
  const docText = x => String(value(x) ?? '').replace(/^\s*>\s?/gm,'').replace(/\*\*|`/g,'').replace(/^\s*\|\s*|\s*\|\s*$/g,'').replace(/(?<!\\)\s+\|\s+/g,' · ').replace(/\\\|/g,'|').trim();
  const documentaryText = leaf => leaf?.src?.file?.endsWith('.md') || leaf?.src?.file?.startsWith('docs/') ? esc(docText(leaf)) : leafText(leaf);
  const nodeLabel = id => {
    const n=nodes.get(id), label=docText(n?.short_label || n?.label || id || 'context not recorded');
    return label === 'D1 CAPACITY LAW' ? 'D1 capacity law' : label;
  };
  const plural = (n,noun) => `${n} ${noun}${n === 1 ? '' : 's'}`;
  const natural = (a,b) => String(a).localeCompare(String(b),'en',{numeric:true,sensitivity:'base'});
  const shortEra = x => String(value(x) || '').replace(/^era:/, '');
  const eraData = id => lab.contexts?.eras?.[shortEra(id)] || lab.contexts?.eras?.['era:' + shortEra(id)] || {};
  const eraLabel = id => docText(eraData(id).name || eraData(id).label) || nodeLabel('era:' + shortEra(id));
  const recordName = card => value(card.identity?.name) || index.find(x => x.card_id === card.card_id)?.source || '';
  const isC10 = card => recordName(card).startsWith('results/c10');
  const dataLink = (card,label='Data for this view') => `<a data-for-view href="cards/${esc(card.card_id)}.json">${esc(label)}</a>`;
  const sourceURL = file => 'evidence/' + String(file || '').replace(/:[0-9]+$/, '');
  function source(leaf) {
    if (!leaf?.src) return leaf?.derived ? '<span class="source">derived from recorded inputs</span>' : '';
    const s = {...leaf.src, path:leaf.src.reader ? leaf.src.reader + ' ' + leaf.src.path : leaf.src.path};
    return `<a class="source" href="${esc(sourceURL(s.file))}${s.line ? '#L' + s.line : ''}" title="${esc(s.quote || s.path || '')}">${esc(s.file)}${s.path ? ' : ' + esc(s.path) : s.line ? ':' + s.line : ''}</a>`;
  }
  function missing(leaf, fallback = 'not recorded for this run') {
    const reason=leaf?.missing || (fallback !== 'not recorded for this run' ? fallback : '');
    const tier={ 'NOW-not-recorded':'Not recorded',REPLAY:'REPLAY · NOT EVIDENCE',NEW:'New collection','not-judged-yet':'Not judged yet' }[leaf?.tier] || leaf?.tier;
    return `<p class="missing">not recorded for this run${reason ? ' — ' + esc(reason.replace(/^not recorded for this run[;: .—-]*/i,'')) : ''}${tier ? ` <span class="tier-badge">${esc(tier)}</span>` : ''}</p>`;
  }
  function leafText(leaf) { return value(leaf) == null ? 'not recorded for this run' : esc(fmt(value(leaf))); }
  function section(card, name, body, caption, caveat, chart = false) {
    return `<section class="evidence-section"${chart ? ' data-chart' : ''}><div class="section-heading"><h3>${esc(name)}</h3>${dataLink(card)}</div>${body}${caption ? `<p class="caption">${esc(caption)}</p>` : ''}${caveat ? `<p class="caveat">Does not mean: ${esc(caveat)}</p>` : ''}</section>`;
  }
  const initial = { view:'map', run:lab.default_run || index.find(r => r.has_writes)?.card_id || '', line:'', focus:'', model:'', compare:[], fact:0, mapColumn:0, learnEra:'', learning:'learn' };
  let state = { ...initial }, renderVersion = 0, mapQuery = '', pickerSlot = '', filters = {};
  const normalView = view => ({ now:'map', science:'lines', inside:'model', models:'model-history', evaluations:'learn', history:'lines' }[view] || view);
  function readURL() {
    const p = new URLSearchParams(location.hash.slice(1));
    if (location.hash.startsWith('#run-')) return { ...initial, view:'run', run:location.hash.slice(1) };
    const s = { ...initial };
    ['view','run','line','focus','model','learnEra','learning'].forEach(k => { if (p.has(k)) s[k] = p.get(k); });
    s.view = normalView(s.view);
    if (p.has('compare')) s.compare = p.get('compare').split(',').filter(Boolean);
    if (!p.has('view')) s.view = s.compare.length ? 'compare' : p.has('model') ? 'model-history' : p.has('line') ? 'lines' : p.has('run') ? 'run' : 'map';
    return s;
  }
  function writeURL() {
    const p = new URLSearchParams();
    p.set('view', state.view);
    ['run','line','focus','model','learnEra'].forEach(k => { if (state[k]) p.set(k, state[k]); });
    if (state.compare.length) p.set('compare', state.compare.join(','));
    if (state.view === 'learn') p.set('learning', state.learning);
    history.replaceState(null, '', '#' + p.toString());
  }
  async function ensureIndex() {
    if (index.length || !lab.index_src) return index;
    if (!indexLoading) indexLoading=new Promise((resolve,reject) => {
      const script=document.createElement('script'); script.src=lab.index_src;
      script.onload=() => {
        if (!Array.isArray(lab.index)) { indexLoading=null; reject(new Error('The recorded run index did not contain an array.')); return; }
        index=lab.index; resolve(index);
      };
      script.onerror=() => { indexLoading=null; reject(new Error('Could not load the recorded run index.')); };
      document.head.append(script);
    });
    return indexLoading;
  }
  async function loadCard(id) {
    if (cards.has(id)) return cards.get(id);
    await ensureIndex();
    const entry = index.find(r => r.card_id === id);
    if (!entry) throw new Error('This card is not in the recorded index: ' + id);
    const chunk = entry.chunk;
    if (!chunks.has(chunk)) {
      chunks.set(chunk, new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = 'cards/' + chunk + '.js';
        script.onload = () => {
          const loaded = window.LAB_CHUNKS?.[chunk];
          if (!Array.isArray(loaded)) { reject(new Error('Recorded chunk did not contain a card array: ' + chunk)); return; }
          loaded.forEach(card => cards.set(card.card_id, card));
          resolve();
        };
        script.onerror = () => { chunks.delete(chunk); reject(new Error('Could not load the recorded card chunk: ' + chunk)); };
        document.head.append(script);
      }));
    }
    await chunks.get(chunk);
    if (!cards.has(id)) throw new Error('The loaded chunk does not name this card: ' + id);
    return cards.get(id);
  }
  function renderError(error) {
    content.innerHTML = `<article><h2>The recorded view could not be loaded</h2><p>${esc(error.message)}</p><a href="cards/index.json">Open the run-card index</a></article>`;
  }
  async function setState(next) {
    next = { ...next };
    if (next.compare && !Array.isArray(next.compare)) next.compare = String(next.compare).split(',');
    if (next.view) next.view = normalView(next.view);
    if (next.run && (!next.view || next.view === 'runs')) next.view = 'run';
    state = { ...state, ...next };
    if (state.line && !String(state.line).includes(':') && nodes.has('exp:' + state.line)) state.line = 'exp:' + state.line;
    writeURL();
    return render();
  }
  function show(view) { return setState({ view:normalView(view), learning:view === 'evaluations' ? 'evaluations' : state.learning }); }
  const fire = task => { Promise.resolve(task).catch(renderError); };
  function cardLine(card) {
    const entry=index.find(r => r.card_id === card.card_id);
    return card.context?.experiment?.node_id || card.context?.corpus?.node_id || card.context?.condition?.node_id || entry?.line || (entry?.experiment ? 'exp:' + entry.experiment : '');
  }
  async function chooseRun(id, view = 'run') {
    pickerSlot = '';
    const card=await loadCard(id);
    return setState({ run:id, line:cardLine(card), view, fact:0 });
  }
  async function chooseCompare(id) {
    const slot=pickerSlot === 'right' ? 1 : 0, card=await loadCard(id), pair=[...state.compare];
    pair[slot]=id; pickerSlot='';
    return setState({compare:pair,view:'compare',run:slot ? state.run : id,line:cardLine(card)});
  }
  function header(title, caption, eyebrow = '') { return `<div class="page-heading">${eyebrow ? `<p class="eyebrow">${esc(eyebrow)}</p>` : ''}<h2>${esc(title)}</h2>${caption ? `<p>${esc(caption)}</p>` : ''}</div>`; }
  function frame(card) {
    const nav = state.view === 'run' || state.view === 'compare' ? 'runs' : state.view === 'model-history' ? 'lines' : state.view;
    document.querySelectorAll('.top-nav [data-view]').forEach(button => {
      if (button.dataset.view === nav) button.setAttribute('aria-current','page'); else button.removeAttribute('aria-current');
    });
    let crumbs = '<button data-view="map">Map</button>', context='Program map · all science lines';
    const appendCrumb = label => { crumbs += `<span aria-hidden="true">›</span><span>${esc(label)}</span>`; };
    if (['run','model','compare'].includes(state.view) && card) {
      const c = card.context || {};
      for (const key of ['layer','condition','track','experiment']) {
        if (value(c[key]) != null) crumbs += `<span aria-hidden="true">›</span><button data-line="${esc(c[key].node_id || value(c[key]))}">${esc(docText(c[key]))}</button>`;
      }
      crumbs += '<span aria-hidden="true">›</span><span>Selected run</span>';
      const era=shortEra(c.era);
      context=`${era ? eraLabel(era) : 'era not recorded'} · ${docText(c.experiment || c.corpus) || 'context not recorded'}`;
    } else if (state.view === 'map') {
      if (state.focus) { context=nodeLabel(state.focus); appendCrumb(context); }
    } else if (state.view === 'lines') {
      context=state.line ? nodeLabel(state.line) : 'Science lines'; appendCrumb(context);
    } else if (state.view === 'model-history') {
      const model=state.model || 'Mistral-7B'; context=model + ' · model history'; appendCrumb(model);
    } else if (state.view === 'learn') {
      appendCrumb('Learn & evaluations');
      context='Learn & evaluations · ' + (state.learnEra ? eraLabel(state.learnEra) : 'all eras');
      if (state.learnEra) appendCrumb(eraLabel(state.learnEra));
    } else {
      context={runs:'Runs',model:'Inside the model',run:'Selected run',compare:'Compare'}[state.view] || state.view;
      appendCrumb(context);
    }
    document.getElementById('breadcrumb').innerHTML = crumbs;
    document.getElementById('context-chip').textContent = context;
    const proxy=card?.mathlab || state.view === 'compare' && state.compare.some(id => cards.get(id)?.mathlab);
    const mixed=state.view === 'runs' && index.some(row => row.mathlab);
    document.getElementById('evidence-badge').textContent = proxy ? 'MATH-PROXY · math estimate, not evidence' : mixed ? 'RECORDED + MATH-PROXY' : 'RECORDED';
    document.getElementById('evidence-badge').title = proxy || mixed ? 'math estimate, not evidence' : card?.evidence_status || 'From the named program records and documents; Lab View makes no verdict.';
    document.getElementById('frame-data').href = card ? 'cards/' + card.card_id + '.json' : 'context.json';
    document.getElementById('frame-data').dataset.card = card?.card_id || '';
  }
  function renderStatus() {
    const log = lab.latest_log || {};
    const queue = lab.queue || [];
    const active = queue.filter(q => /running|halt|block|gate/i.test(String(value(q.status))));
    const description = active.length ? active.map(q => `${value(q.name)}: ${value(q.status)}`).join(' · ') : 'Saved program status';
    const last=String(value(log.last_line) || 'No latest log line recorded'), exit=last.match(/^STAGE_EXIT=(-?\d+)$/);
    const answerCheck=last.match(/^([^\s]+)\s+canon=[\d.]+\s+para=[\d.]+/);
    const caption=exit ? 'Last stage ended with exit code ' + exit[1] : last;
    const summary=answerCheck ? 'Saved answer check for ' + answerCheck[1].replaceAll('_',' ') + '.' : '';
    document.getElementById('status-strip').innerHTML = `<div class="status-detail"><p><strong>${esc(description)}</strong></p>${summary ? `<p>${esc(summary)}</p>` : ''}<p>${esc(caption)}</p>${value(log.modified_utc) ? `<p>Log saved at ${esc(value(log.modified_utc))}</p>` : ''}<p>Log snapshot.</p></div>${log.source ? `<a href="${esc(sourceURL(value(log.source)))}">Read log</a>` : ''}`;
  }
  const columnKinds = [ ['layer'], ['spec'], ['condition'], ['track','experiment','era','hypothesis'], ['decision'], ['corpus'], ['model'] ];
  const columnNames = ['Spec layers','Spec sections','F1 conditions','Tracks & experiments','Decisions','Evidence entries','Models'];
  function kind(n) { const k=n.kind || String(n.node_id).split(':')[0]; return {exp:'experiment',hyp:'hypothesis',cond:'condition',dec:'decision','runbook-track':'track'}[k] || k; }
  function inColumn(n, i) { return columnKinds[i].includes(kind(n)); }
  function paths(id) {
    const reached = new Set([id]);
    for (const direction of ['source','target']) {
      const seen = new Set([id]), queue = [id];
      while (queue.length) {
        const current = queue.shift();
        graph.edges.forEach(e => {
          if (e[direction] !== current) return;
          const next = e[direction === 'source' ? 'target' : 'source'];
          if (!seen.has(next)) { seen.add(next); reached.add(next); queue.push(next); }
        });
      }
    }
    return reached;
  }
  function countRuns(id) {
    if (!index.length && lab.index_counts) return lab.index_counts[id] || 0;
    return index.filter(r => 'exp:' + r.experiment === id || r.line === id || r.era === id || r.era === id.replace(/^era:/,'') || r.model === id.replace(/^model:/,'')).length;
  }
  function nodeButton(n, reached = new Set()) {
    const count = countRuns(n.node_id);
    const mode = state.focus ? n.node_id === state.focus ? ' focused' : reached.has(n.node_id) ? ' connected' : ' dimmed' : '';
    const pathState=mode === ' focused' ? '● focused · ' : mode === ' connected' ? '● connected · ' : mode === ' dimmed' ? 'not on this line’s path · ' : '';
    return `<button class="map-node${mode}" data-focus="${esc(n.node_id)}" title="Documents connect these; a connection does not establish support."><strong>${esc(nodes.has(n.node_id) ? nodeLabel(n.node_id) : docText(n.short_label || n.label || n.node_id))}</strong><span class="node-kind">${esc(pathState + kind(n))}${count ? ' · ' + plural(count,'card') : ''}</span></button>`;
  }
  function edgeSources(edge) {
    const list = Array.isArray(edge.src) ? edge.src : edge.src ? [edge.src] : [];
    return list.map(s => s.file ? `<a class="source" href="${esc(sourceURL(s.file))}${s.line ? '#L' + s.line : ''}">${esc(s.file)}${s.line ? ':' + s.line : ''}</a>${s.quote ? `<p class="source">“${esc(docText(s.quote))}”</p>` : edge.quotes ? `<p class="source">“${esc(docText(edge.quotes.source))}” ↔ “${esc(docText(edge.quotes.target))}”</p>` : ''}` : '').join('') + (edge.edge === 'derived' && edge.inputs ? `<p class="source">Chain of ${plural(edge.inputs.length,'document link')}; see context data for the complete inputs.</p>${edge.inputs.filter(input => input && typeof input === 'object').map(input => `<p class="source">${esc(nodeLabel(input.source))} → ${esc(nodeLabel(input.target))}</p>${edgeSources(input)}`).join('')}` : '');
  }
  function limitedLinks(rows, noun='document links') {
    return rows.slice(0,5).join('') + (rows.length > 5 ? `<details class="more-links"><summary>${rows.length-5} more ${esc(noun)}</summary>${rows.slice(5).join('')}</details>` : '');
  }
  function scienceStatus(n,label='Status now (source):') {
    if (value(n?.status) == null || value(n.status) === 'DRAFT') return '';
    const full=docText(n.status), first=full.match(/^.*?[.!?](?:\s|$)/s)?.[0].trim() || full;
    const brief=full.length > 320 ? first : full;
    return `<p><strong>${esc(label)}</strong> <span data-science-status>${esc(brief)}</span>${source(n.status)}</p>${brief !== full ? `<details><summary>Full source status</summary><p>${esc(full)}</p>${source(n.status)}</details>` : ''}`;
  }
  function connectionsFor(id) {
    const n = nodes.get(id);
    if (!n) { connections.hidden = true; return; }
    const reached = paths(id);
    const links = graph.edges.filter(e => e.source === id || e.target === id);
    let html = `<div class="section-heading"><h3>${esc(nodeLabel(id))}</h3><a data-for-view href="context.json">Data for this view</a></div>${n.description ? `<p>${esc(docText(n.description))}</p>` : ''}${scienceStatus(n)}${value(n.framing_status) === 'DRAFT' || value(n.status) === 'DRAFT' ? '<p class="draft">Framing review: draft</p>' : ''}<div class="run-actions"><button data-line="${esc(id)}">Open this science line</button>${kind(n) === 'model' ? `<button data-model-history="${esc(id.replace(/^model:/,''))}">Model history</button>` : ''}</div><p class="caption">These links are named by documents. A link is not evidence, and an absent link does not prove no relation.</p>`;
    const shared = [...reached].filter(node => ['layer','spec','model','decision','dec'].includes(kind(nodes.get(node) || {})) && graph.edges.some(e => (e.source === node && !reached.has(e.target)) || (e.target === node && !reached.has(e.source))));
    const d1 = nodes.has('corpus:22') ? [nodes.get('corpus:22')] : graph.nodes.filter(x => /D1|capacity law|capacity-law/i.test(String(value(x.label) || x.node_id)));
    const d1Paths = new Set(d1.flatMap(x => [...paths(x.node_id)]));
    const common = [...reached].filter(node => d1Paths.has(node) && ['layer','spec','model'].includes(kind(nodes.get(node) || {}))).sort((a,b) => ['layer','spec','model'].indexOf(kind(nodes.get(a))) - ['layer','spec','model'].indexOf(kind(nodes.get(b))) || natural(nodeLabel(a),nodeLabel(b)));
    const allShared = [...new Set([...common,...shared])].slice(0,12);
    html += `<h4>Shared with other lines</h4>${allShared.length ? `<p>These named layers, sections or models also connect to another science line${common.length && /C10/i.test(id) ? ', including the D1 capacity line' : ''}.</p><div class="shared-node" data-shared>${allShared.map(node => `<button data-focus="${esc(node)}" data-shared="${esc(node)}"${common.includes(node) ? ' data-shared-with="corpus:22"' : ''}>${esc(nodeLabel(node))}${common.includes(node) ? ' · shared with D1' : ''}</button>`).join('')}</div>` : '<p>No further shared link is named in this view’s documents.</p>'}`;
    for (const derived of [false,true]) {
      const group=links.filter(e => (e.edge === 'derived') === derived), noun=derived ? 'derived document links' : 'document links';
      if (group.length) html += `<h4>${derived ? 'Derived document links' : 'Document links'}</h4>` + limitedLinks(group.map(e => `<div class="connection-row"><span class="link-type">${esc(e.edge)}</span><button data-focus="${esc(e.source === id ? e.target : e.source)}">${esc(nodeLabel(e.source))} → ${esc(nodeLabel(e.target))}</button>${edgeSources(e)}</div>`),noun);
    }
    if (!links.length) html += '<h4>Document links</h4><p>No direct link is recorded for this node.</p>';
    connections.innerHTML = html;
    connections.hidden = false;
  }
  function renderMapBody() {
    const reached = state.focus ? paths(state.focus) : new Set();
    const matching = graph.nodes.filter(n => !mapQuery || `${value(n.label)} ${n.node_id}`.toLowerCase().includes(mapQuery.toLowerCase()));
    const sortNodes = list => list.sort((a,b) => Number(reached.has(b.node_id)) - Number(reached.has(a.node_id)) || String(value(b.date) || '').localeCompare(String(value(a.date) || '')) || natural(nodeLabel(a.node_id),nodeLabel(b.node_id)));
    document.getElementById('map-columns').innerHTML = columnNames.map((name,i) => {
      const ns = sortNodes(matching.filter(n => inColumn(n,i))), shown = ns.slice(0,state.focus ? 24 : 12);
      return `<div class="map-column"><h3>${esc(name)}</h3>${shown.map(n => nodeButton(n,reached)).join('')}${ns.length > shown.length ? `<button data-map-column="${i}">${ns.length - shown.length} more · browse column</button>` : ''}</div>`;
    }).join('');
    const phoneNodes = sortNodes(matching.filter(n => inColumn(n,state.mapColumn))).slice(0,50);
    document.getElementById('phone-map').innerHTML = `<div class="controls"><button data-map-column="${Math.max(0,state.mapColumn - 1)}"${!state.mapColumn ? ' disabled' : ''}>← Back</button><div><strong>${esc(columnNames[state.mapColumn])}</strong><p class="source">Column ${state.mapColumn + 1} of 7</p></div><button data-map-column="${Math.min(6,state.mapColumn + 1)}"${state.mapColumn === 6 ? ' disabled' : ''}>Next →</button></div>${phoneNodes.map(n => nodeButton(n,reached)).join('')}${!phoneNodes.length ? '<p>No matching node in this column.</p>' : ''}`;
    if (state.focus) connectionsFor(state.focus); else connections.hidden = true;
    requestAnimationFrame(drawMapEdges);
  }
  function drawMapEdges() {
    const board = document.getElementById('map-board'), svg = document.getElementById('map-edges');
    if (!board || !svg || !board.offsetWidth) return;
    const origin = document.getElementById('map-columns').getBoundingClientRect();
    const buttons = new Map([...board.querySelectorAll('[data-focus]')].map(b => [b.dataset.focus,b]));
    const reached = state.focus ? paths(state.focus) : new Set();
    const width = board.scrollWidth - 24, height = document.getElementById('map-columns').offsetHeight;
    svg.setAttribute('width',width); svg.setAttribute('height',height); svg.style.width=width + 'px'; svg.style.height=height + 'px';
    svg.innerHTML = graph.edges.filter(e => buttons.has(e.source) && buttons.has(e.target)).map((e,i) => {
      const a = buttons.get(e.source).getBoundingClientRect(), b = buttons.get(e.target).getBoundingClientRect();
      const x1=a.right-origin.left, y1=a.top+a.height/2-origin.top, x2=b.left-origin.left, y2=b.top+b.height/2-origin.top;
      const bend = (x1+x2)/2;
      return `<path class="map-edge ${esc(e.edge)}${state.focus ? reached.has(e.source) && reached.has(e.target) ? ' highlighted' : ' dimmed' : ''}" d="M ${x1} ${y1} C ${bend} ${y1},${bend} ${y2},${x2} ${y2}" data-edge="${graph.edges.indexOf(e)}"><title>${esc(e.edge)} document link: ${esc(nodeLabel(e.source))} → ${esc(nodeLabel(e.target))}</title></path>`;
    }).join('');
  }
  function renderMap() {
    const presets = graph.nodes.filter(n => ['condition','cond','track','era'].includes(kind(n)));
    content.innerHTML = header('How the science connects','Choose a line to see its question, status and the documents that connect it to the rest of the program.','The program map') + `<div class="controls"><div class="control"><label for="map-search">Find a layer, experiment or model</label><input id="map-search" type="search" value="${esc(mapQuery)}" placeholder="G6.1, Mistral, §8.7…"></div><div class="control"><label for="map-preset">Focus on a science line</label><select id="map-preset"><option value="">All connections</option>${presets.map(n => `<option value="${esc(n.node_id)}"${state.focus === n.node_id ? ' selected' : ''}>${esc(nodeLabel(n.node_id))}</option>`).join('')}<option value="running">What is running now</option></select></div></div><div class="map-presets">${graph.nodes.filter(n => ['cond:C10','exp:G6.1','model:Mistral-7B'].includes(n.node_id)).map(n => `<button data-focus="${esc(n.node_id)}">${esc(nodeLabel(n.node_id))}</button>`).join('')}<button data-clear-focus>Show all</button></div><div data-chart class="map-layout"><div class="map-board" id="map-board"><svg class="map-edges" id="map-edges" aria-label="Document links"></svg><div class="map-columns" id="map-columns"></div></div><div class="phone-map" id="phone-map"></div><p class="caption"><span class="desktop-map-legend">Solid line: one program document names both ends. Dashed: a curated link with its quote. Dotted: a chain of links. Tap a line to see the documents.</span><span class="phone-map-legend">Choose a node to read its named document connections. Browse one column at a time.</span></p><p class="caveat">Does not mean: a link is evidence, its thickness is importance, or an absent link proves no relation.</p></div>`;
    document.getElementById('map-board').closest('.map-layout').before(connections);
    renderMapBody();
  }
  function lineRows(id) {
    if (!id) return index;
    if (['exp:','corpus:','model:'].some(prefix => id.startsWith(prefix))) return index.filter(r => r.line === id || 'exp:' + r.experiment === id || 'model:' + r.model === id || r.source === nodes.get(id)?.src?.file || cards.get(r.card_id)?.context?.corpus?.node_id === id);
    const reached = paths(id);
    return index.filter(r => r.line === id || 'exp:' + r.experiment === id || 'era:' + shortEra(r.era) === id || 'model:' + r.model === id || reached.has('exp:' + r.experiment) || reached.has(r.line));
  }
  function displayDate(date) {
    const text=String(value(date) || '');
    if (!/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(text) || !Number.isFinite(Date.parse(text))) return docText(text);
    return new Date(text).toISOString().slice(0,16).replace('T',' ') + ' UTC';
  }
  function runTitle(entry) {
    const title=docText(entry.experiment || entry.title || 'Recorded observation');
    return title.length > 100 ? title.slice(0,96).replace(/\s+\S*$/,'') + '…' : title;
  }
  function runDescription(entry) {
    if (entry.mathlab) return ['MATH-PROXY','math estimate, not evidence',entry.mathlab.run_id || entry.field,
                              entry.mathlab.purpose || 'scope not recorded',entry.mathlab.status,
                              entry.mathlab.parse_errors ? entry.mathlab.parse_errors + ' parse errors' : ''].filter(Boolean).join(' · ');
    const field=String(entry.field || ''), recipeValue=value(entry.recipe), armValue=value(entry.arm);
    const recipe=recipeValue != null && recipeValue !== '' ? String(recipeValue) : field.match(/^\.?recipes\.([^.]+)/)?.[1];
    const arm=armValue != null && armValue !== '' ? String(armValue) : field.match(/(?:^|\.)(A\d+_[^.]+)/)?.[1];
    const armLabel=arm?.replace(/^(A\d+)_([^_]+)_([^_]+)$/,'$1 $2/$3').replaceAll('_',' ');
    const detail=recipe || arm ? [recipe ? 'recipe ' + recipe : '',arm ? (/^A\d/.test(arm) ? armLabel : 'arm ' + armLabel) : ''] : [field.split('.').filter(Boolean).map(part => part === 'law5' ? 'LAW5' : part.replaceAll('_',' ').replace(/\[(\d+)\]/g,' $1')).join(' · ')];
    return [...detail,entry.role,entry.label].filter(Boolean).map(docText).join(' · ');
  }
  function runRow(entry, attrs = '') {
    return `<button class="run-row" data-run="${esc(entry.card_id)}" ${attrs}><span class="row-main"><strong>${esc(runTitle(entry))}</strong><span class="row-meta">${esc([entry.model,displayDate(entry.date)].filter(Boolean).join(' · '))}</span><span class="row-meta">${esc(runDescription(entry))}</span></span></button>`;
  }
  function scienceTimeline(id='') {
    const rows=lineRows(id), dated=rows.filter(r => r.date).sort((a,b) => String(a.date).localeCompare(String(b.date))), sourceDates=new Set();
    const observations=dated.filter(r => { const key=r.source+'|'+r.date; if (sourceDates.has(key)) return false; sourceDates.add(key); return true; });
    const reached=id ? paths(id) : new Set(graph.nodes.map(n => n.node_id));
    const decisions=graph.nodes.filter(n => kind(n) === 'decision' && reached.has(n.node_id)).sort((a,b) => String(value(a.date) || '').localeCompare(String(value(b.date) || '')) || a.node_id.localeCompare(b.node_id));
    const ownDocument=id.startsWith('corpus:') || id.startsWith('dec:');
    return `<section class="evidence-section" data-chart><div class="section-heading"><h3>${id ? 'This line’s' : 'Program'} recorded observations over time</h3><a data-for-view href="cards/index.json">Data for this view</a></div><details class="observation-timeline"><summary>${plural(observations.length,'dated source snapshot')}</summary>${observations.slice(0,50).map(r => `<div class="timeline-row"><strong>${esc(displayDate(r.date))}</strong><a data-for-view href="cards/${esc(r.card_id)}.json">Date and source for this observation</a></div>`).join('') || '<p>No dated observation is recorded for this line.</p>'}${observations.length > 50 ? `<button data-line-runs="${esc(id)}">Search all dated observations in Runs</button>` : ''}</details><p class="caption">Only recorded dates are placed on this timeline. Each line keeps its own measure; there is no common answer scale.</p><p class="caveat">Does not mean: an observation’s saved date measures its duration or proves that the finding generalises.</p></section>${!ownDocument ? `<section class="evidence-section"><div class="section-heading"><h3>Program decisions across the lines</h3><a data-for-view href="context.json">Data for this view</a></div><details><summary>${decisions.length} sourced decisions</summary>${decisions.map(n => { const e=graph.edges.find(edge => (edge.source === n.node_id || edge.target === n.node_id) && edge.src?.file); const citation=n.src || e?.src; return `<div class="timeline-row"><strong>${esc(value(n.label) || n.node_id)}</strong><p>${value(n.date) != null ? esc(value(n.date)) : 'decision date not recorded in the context data; listed by ID'}</p>${citation ? source({src:citation}) : '<p class="source">See the document chains in the context data.</p>'}<button data-focus="${esc(n.node_id)}">See the decision’s connections</button></div>`; }).join('')}</details></section>` : ''}`;
  }
  function renderLines() {
    if (!state.line) {
      content.innerHTML = header('Science lines','Browse a question in the era and part of the system where it was tested.') + `<div class="grid">${['era','condition','track','layer'].map(k => `<article><h3>${esc({era:'Research eras',condition:'Readiness conditions',track:'Registry tracks',layer:'Spec layers'}[k])}</h3>${graph.nodes.filter(n => kind(n) === k || k === 'condition' && kind(n) === 'cond').sort((a,b) => natural(nodeLabel(a.node_id),nodeLabel(b.node_id))).map(n => `<button class="run-row" data-line="${esc(n.node_id)}"><span class="row-main"><strong>${esc(nodeLabel(n.node_id))}</strong><span class="row-meta">${plural(countRuns(n.node_id),'recorded card')}</span></span></button>`).join('')}<a data-for-view href="context.json">Data for this view</a></article>`).join('')}</div><article><h3>Model history</h3>${Object.keys(lab.models || {}).map(name => `<button class="run-row" data-model-history="${esc(name)}">${esc(name)}</button>`).join('')}</article>`;
      content.innerHTML+=scienceTimeline();
      return;
    }
    const n = nodes.get(state.line), rows = lineRows(state.line), era = n?.era;
    const linked = graph.edges.filter(e => e.source === state.line || e.target === state.line);
    const documentary=state.line.startsWith('corpus:') || state.line.startsWith('dec:');
    const experiments = documentary ? [] : graph.nodes.filter(x => kind(x) === 'experiment' && (paths(state.line).has(x.node_id) || x.node_id === state.line));
    const question=docText(n?.question || n?.description), measure=docText(n?.measure || (era ? eraData(era).measure : ''));
    const draft=value(n?.framing_status) === 'DRAFT' || value(n?.status) === 'DRAFT' || value(eraData(era).status) === 'DRAFT';
    const groups=new Map();
    rows.forEach(row => { const key=row.experiment || row.line || 'Context not recorded'; if (!groups.has(key)) groups.set(key,[]); groups.get(key).push(row); });
    const groupedRuns=limitedLinks([...groups].slice(0,50).map(([name,records]) => {
      const binding=records.filter(row => row.role === 'binding' && row.label);
      const best=['PASS','LEAD','LEAD-NOT-REPLICATED','PARTIAL','TRADEOFF','NULL','UNDERFIT'].find(label => binding.some(row => row.label === label));
      const groupLine=records[0].experiment ? 'exp:' + records[0].experiment : records[0].line;
      return `<details class="line-run-group"><summary><strong>${esc(nodes.has(name) ? nodeLabel(name) : docText(name))}</strong><span class="tag">${plural(records.length,'recorded card')} · ${best ? 'best recorded binding label: ' + esc(best) : binding.length ? 'binding labels: ' + esc([...new Set(binding.map(row => row.label))].join(' · ')) : 'binding label not recorded'}</span></summary><div>${records.slice(0,5).map(row => runRow(row)).join('')}<button data-line-runs="${esc(groupLine)}">Search all ${records.length} in Runs</button></div></details>`;
    }),'experiment groups');
    content.innerHTML = header(nodeLabel(state.line), question || 'The question and measure are kept in the cited records.', era ? eraLabel(era) : 'Science line') + `<div class="run-actions"><button data-view="lines" data-reset-line>All science lines</button><button data-focus="${esc(state.line)}" data-view="map" data-map-line>See this line on the Map</button></div><article><h3>Question and framing at the time</h3>${question ? `<p>${esc(question)}</p>${source(n?.question || n?.description)}` : '<p>No single question recorded; consult the named source.</p>'}${measure ? `<p>${esc(measure)}</p>${source(n?.measure)}` : ''}${draft ? '<p class="draft">Framing review: draft</p>' : ''}${scienceStatus(n,n?.status?.src?.file === 'program/registers/EXPERIMENT_REGISTRY.md' ? 'Status now (registry):' : 'Status now (source):')}<a data-for-view href="context.json">Data for this view</a></article>${experiments.length ? `<details class="line-experiments"><summary>${plural(experiments.length,'experiment question')} and registry status</summary><div class="grid">${experiments.slice(0,50).map(x => `<article><h3>${esc(nodeLabel(x.node_id))}</h3><p>${esc(docText(x.description))}</p><button data-line="${esc(x.node_id)}">Open experiment</button><p class="source">${plural(countRuns(x.node_id),'recorded card')}</p></article>`).join('')}</div></details>` : ''}<article><h3>Recorded runs in this line</h3>${groupedRuns}${groups.size > 50 ? `<button data-line-runs="${esc(state.line)}">Search all ${rows.length} cards in Runs</button>` : ''}${!rows.length ? '<p>Documentary line; no run measurements are recorded here.</p>' : ''}</article><article><h3>Document links</h3>${limitedLinks(linked.map(e => `<div class="connection-row"><button data-line="${esc(e.source === state.line ? e.target : e.source)}">${esc(nodeLabel(e.source === state.line ? e.target : e.source))}</button>${edgeSources(e)}</div>`))}<a data-for-view href="context.json">Data for this view</a></article>`;
    content.innerHTML+=scienceTimeline(state.line);
  }
  function renderRunList() {
    const query = (filters.query || '').toLowerCase();
    let matching = index.filter(r => (!query || `${r.experiment} ${r.title} ${r.source} ${r.field} ${r.model}`.toLowerCase().includes(query)) && (!filters.era || shortEra(r.era) === filters.era) && (!filters.model || r.model === filters.model) && (!filters.label || r.label === filters.label) && (!filters.line || r.line === filters.line || 'exp:' + r.experiment === filters.line || lineRows(filters.line).some(x => x.card_id === r.card_id)) && (!filters.date || String(r.date).startsWith(filters.date)));
    matching.sort((a,b) => Number(String(b.experiment).toLowerCase().startsWith(query)) - Number(String(a.experiment).toLowerCase().startsWith(query)) || String(b.date || '').localeCompare(String(a.date || '')));
    const groups = new Map();
    matching.forEach(r => { const key=r.experiment || r.line || 'Context not recorded'; if (!groups.has(key)) groups.set(key,[]); groups.get(key).push(r); });
    document.getElementById('run-count').textContent = `${matching.length} recorded cards in ${groups.size} experiment groups`;
    let shown = 0;
    document.getElementById('run-results').innerHTML = [...groups].slice(0,50).map(([name,rows]) => {
      const records = new Map();
      rows.forEach(r => { if (!records.has(r.source)) records.set(r.source,[]); records.get(r.source).push(r); });
      const question = value(nodes.get('exp:' + name)?.description);
      return `<details class="run-group"${query ? ' open' : ''}><summary><strong>${esc(name)}</strong><span class="tag">${rows.length} cards</span></summary><div>${question ? `<p>${esc(question)}</p>` : ''}${[...records].slice(0,50).map(([src,rs]) => { const shownRows=rs.slice(0,query ? Math.max(0,50-shown) : 50); shown += shownRows.length; return rs.length > 1 ? `<details><summary>${esc(src)} · ${rs.length} observation cards</summary>${shownRows.map(r => runRow(r)).join('')}</details>` : shownRows.map(r => runRow(r)).join(''); }).join('')}${rows.length > 50 ? '<p>Narrow the search to see further observations.</p>' : ''}</div></details>`;
    }).join('') || '<p>No recorded card matches these filters.</p>';
  }
  function options(items, selected, title) { return `<option value="">${esc(title)}</option>${[...new Set(items.filter(Boolean))].sort().map(x => `<option value="${esc(x)}"${x === selected ? ' selected' : ''}>${esc(x)}</option>`).join('')}`; }
  function renderRuns() {
    frame();
    content.innerHTML = header('Recorded runs','Search the experiment first, then open one of its recorded observations. Multiple observations of one source are nested together.') + `<div class="controls"><div class="control"><label for="run-search">Find a recorded experiment</label><input id="run-search" type="search" placeholder="Registry ID or source path" value="${esc(filters.query || '')}"></div><div class="control"><label for="era-filter">Era</label><select id="era-filter">${options(index.map(r => shortEra(r.era)),filters.era,'All eras')}</select></div><div class="control"><label for="model-filter">Model</label><select id="model-filter">${options(index.map(r => r.model),filters.model,'All models')}</select></div><div class="control"><label for="line-filter">Science line</label><select id="line-filter">${options(index.map(r => 'exp:' + r.experiment).filter(x => x !== 'exp:undefined'),filters.line,'All lines')}</select></div><div class="control"><label for="label-filter">Recorded label</label><select id="label-filter">${options(index.map(r => r.label),filters.label,'All labels')}</select></div><div class="control"><label for="date-filter">Recorded date</label><input id="date-filter" type="date" value="${esc(filters.date || '')}"></div></div><div class="run-actions"><button data-view="compare">Compare two runs</button>${state.run ? `<button data-run="${esc(state.run)}">Open the selected run</button>` : ''}</div><p id="run-count" class="source" aria-live="polite"></p><div id="run-results"></div>`;
    renderRunList();
  }
  function chip(leaf, interim = false) {
    if (value(leaf) == null) return '<p class="role">not judged yet</p>';
    const validClasses = ['pass','lead','lead-unreplicated','partial','tradeoff','null','underfit','control','halted-invalid','not-labelled','not-comparable','characterization','oracle-measurement','not-a-verdict'];
    let cls = validClasses.includes(leaf.colour_class) ? leaf.colour_class : 'unknown';
    if (cls === 'not-a-verdict') return `<p>${esc(value(leaf))} · configuration name; not a verdict</p>`;
    if (cls === 'pass' && (interim || !/^PASS(?:$|-)/.test(String(value(leaf))))) cls = 'unknown';
    return `<span class="label-chip ${esc(cls)}">${esc(value(leaf))}</span>${cls === 'unknown' ? "<p class=\"source\">label not in Lab View's table</p>" : ''}${cls === 'lead' ? '<p class="caption">promising under this test; see replication</p>' : ''}`;
  }
  function badge(card) {
    if (card.mathlab) return mathlabSummary(card);
    const h=card.headline || {}, role=value(card.identity?.role), c10=isC10(card);
    let body='';
    if (number(value(h.heldout_top1))) body += `<p class="score">${fmt(value(h.heldout_top1))}% <span class="role">${esc(h.heldout_top1.plain || 'held-out top-1 correctness')}${number(value(h.rung_n)) ? ' at N=' + fmt(value(h.rung_n)) : ''}${number(value(h.heldout_baseline_top1)) ? '; recorded baseline ' + fmt(value(h.heldout_baseline_top1)) + '%' : ''}</span></p>`;
    else if (number(value(h.hits)) && number(value(h.out_of))) body += `<p class="score">${fmt(value(h.hits))} of ${fmt(value(h.out_of))}${c10 ? ' complete answers' : ' ' + esc(value(h.unit) || 'recorded outcomes')}${c10 && role === 'binding' && number(value(h.program_goal)) ? ` <span class="role">(goal ${fmt(value(h.program_goal))})</span>` : ''}</p>`;
    else if (number(value(h.rate))) body += `<p class="score">${fmt(value(h.rate))} <span class="role">${esc(value(card.context?.measure) || 'recorded rate')}</span></p>`;
    else if (number(value(h.percent))) body += `<p class="score">${fmt(value(h.percent))}% <span class="role">${esc(value(card.context?.measure) || 'recorded measure')}</span></p>`;
    else body += missing(h.hits, 'no single headline number recorded; see the source entry');
    const roles = {control:'Control arm: checks the method against ordinary answer words; not labelled by design.', reference:'Reference arm: the comparator the gates are measured against; not labelled by design.', 'shuffled-control':'Shuffled control: tests the assignment of answers to subjects; not a binding result.', 'canon-control':'Canonical-question control: tests the training question; not a binding result.'};
    if (c10 && role !== 'binding') {
      body += `<p class="role">${esc(roles[role] || 'role not in Lab View’s table; no binding judgement')}</p>`;
      if (role === 'shuffled-control' && (value(card.control_label) === 'NULL-CONTROL-ONLY' || value(card.label) === 'NULL-CONTROL-ONLY')) body += `<p class="source">Recorded control reading: NULL-CONTROL-ONLY</p>`;
    } else if (!c10 && card.label?.src?.path === '.verdict') body += `<p>${esc(value(card.label))}</p>`;
    else if (value(card.label) != null) body += chip(card.label);
    else if (card.label?.tier === 'not-judged-yet' || card.oracle_class) body += '<p class="role">not judged yet</p>';
    else body += `<p>${value(card.context?.status_now) != null ? 'Status now (registry): ' + esc(value(card.context.status_now)) : 'no label recorded; see the cited source entry'}</p>`;
    if (value(card.replica_note) != null) body += `<p class="role">${esc(value(card.replica_note))}</p>`;
    if (value(card.oracle_class) != null) body += `<p class="caveat">${esc(value(card.oracle_class))}</p>`;
    if (value(card.interim_label) != null && role === 'binding') body += chip(card.interim_label,true) + '<p class="caption">oracle measurement, not a route</p>';
    body += source(h.heldout_top1 || h.hits || h.rate || h.percent) + source(h.rung_n) + source(h.heldout_baseline_top1) + source(card.label);
    return section(card,'Recorded result',body, c10 ? 'The count is the number of complete answers recorded by this test. Its role says which judgement applies.' : value(card.context?.measure) || 'The measure and status belong to this line’s own test.', 'a high count, a control result, or a configuration measurement establishes program success.');
  }
  function plainWords(card) {
    const p=card.plain_words || {};
    const templates=(lab.evaluations || []).find(entry => entry.ref === value(p.ref))?.template_fields || [];
    const fields=[['question','Question asked'],['result','Result'],['rules_out','What it rules out'],['leaves_open','What it leaves open'],['next_step','Next step']].filter(([key]) => value(p[key]) != null && !templates.includes(key));
    if (!fields.length && !templates.length) return section(card,'In plain words','<p>no plain-words evaluation linked yet</p>','', 'an unlinked record has been interpreted by this display.');
    return section(card,'In plain words',`${fields.length ? `<dl>${fields.map(([key,title]) => `<dt>${title}</dt><dd>${documentaryText(p[key])}${source(p[key])}</dd>`).join('')}</dl>` : ''}${templates.length ? '<p class="source">Interpretation fields not separately recorded; see the source evaluation.</p>' : ''}${source(p.ref)}`,'The maintained evaluation is shown in its own words.','these captions replace the recorded limits or the source’s caveats.');
  }
  function factHits(fact) {
    const hits = value(fact.rewordings_hit) ?? value(fact.teacher_hits);
    return Array.isArray(hits) && hits.every(h => typeof h === 'boolean') ? hits : null;
  }
  function factStrip(card, compact = false) {
    const facts=card.per_fact || [];
    if (!facts.length) return section(card,'Fact-by-fact outcomes',missing(null),'One cell represents one recorded fact.','unrecorded outcomes are wrong answers.',true);
    const forced=facts.some(f => f.hit_kind === 'teacher-forced');
    const title=forced ? 'With the earlier answer pieces supplied (not a free answer)' : isC10(card) ? 'Reworded questions — free answers' : 'Held-out paraphrases — recorded answers';
    const body=`<div class="fact-strip" aria-label="${esc(title)}">${facts.map((f,i) => { const hits=factHits(f), n=hits ? hits.filter(Boolean).length : null; return `<button class="fact-cell ${n == null ? 'missing' : 'hit-' + Math.min(n,3)}${forced ? ' teacher-forced' : ''}" data-fact="${i}" data-card="${esc(card.card_id)}" title="${esc(value(f.subject))}: ${n == null ? 'not recorded' : n + ' of ' + hits.length}" aria-label="${esc(value(f.subject))}, ${n == null ? 'not recorded' : n + ' of ' + hits.length + ' right'}"><span>${i+1}</span><span>${n == null ? '?' : n + '/' + hits.length}</span>${value(f.canonical_hit) === true ? '<span class="canonical" aria-label="canonical answer right">C ✓</span>' : ''}</button>`; }).join('')}</div><p class="source">C ✓ = the canonical question was right.</p>${!compact ? `<div id="fact-panel" class="fact-panel">${factPanel(card,Math.min(state.fact,facts.length-1))}</div>` : ''}`;
    return section(card,title,body,forced ? 'Dashed outlines distinguish supplied earlier pieces. Each cell prints the recorded hit count.' : 'One square per recorded fact. The printed count shows how many questions were answered fully right.', 'free answers and supplied-piece scores can be treated as the same measurement.',true);
  }
  function factPanel(card, i) {
    const fact=card.per_fact[i]; if (!fact) return '';
    const subject=value(fact.subject), hits=factHits(fact), templates=value(fact.generated_templates) || value(card.stimulus?.questions), generated=value(fact.generated_text);
    const replace = text => typeof text === 'string' ? text.replaceAll('{}',subject || '{}') : text;
    const rows=Array.isArray(templates) ? templates.map((template,j) => `<div class="question-row"><strong>Question ${j+1}</strong><p>${esc(replace(template))}</p><p>${fact.hit_kind === 'teacher-forced' ? 'Earlier answer pieces supplied · ' : ''}${hits?.[j] === true ? 'right' : hits?.[j] === false ? 'wrong' : 'not recorded for this run'}</p>${Array.isArray(generated) && generated[j] != null ? `<p class="source">What the model wrote</p><div class="answer-text">${esc(generated[j])}</div>` : missing(fact.generated_text,'generated words need an observation REPLAY (NOT EVIDENCE)')}</div>`).join('') : missing(card.stimulus?.questions,'question text for this run’s code version not transcribed');
    const detail=value(fact.recorded_detail);
    const diagnostics=['answer_split','target_ids','prediction_before_write','proxy'].filter(k => value(fact[k]) != null).map(k => `<details><summary>${esc(k.replaceAll('_',' '))} (recorded)</summary><pre class="raw-measures">${esc(JSON.stringify(value(fact[k]),null,2))}</pre>${source(fact[k])}</details>`).join('');
    const phrasings=array(card.stimulus?.training_phrasings).filter(row => /^T\d\d$/.test(row.id));
    const trainingText=phrasings.length ? `<details><summary>${phrasings.length} sealed training phrasings (recorded)</summary>${phrasings.map(row => `<div class="question-row"><strong>${esc(row.id)}</strong><p>${esc(replace(row.template))}</p></div>`).join('')}${source(card.stimulus.training_phrasings)}<p class="caption">These are training questions. Reserved phrasings are kept separate in the source record.</p></details>` : '';
    return `<h4>${esc(subject || 'Subject not recorded')}</h4><dl><dt>Expected answer</dt><dd>${leafText(fact.answer)}</dd><dt>Answer pieces</dt><dd>${leafText(fact.answer_pieces)}</dd><dt>Canonical question</dt><dd>${value(card.stimulus?.canonical) != null ? esc(replace(value(card.stimulus.canonical))) : 'not recorded for this run'}</dd>${number(value(fact.assigned_layer)) ? `<dt>Assigned layer</dt><dd>${value(fact.assigned_layer)}</dd>` : ''}<dt>Keyed subject piece</dt><dd>${value(card.stimulus?.keyed_piece_text) != null ? leafText(card.stimulus.keyed_piece_text) : 'the last piece of the subject name (piece text not recorded for this run); needs Phase 2a extract'}</dd></dl>${rows}${trainingText}${diagnostics}${detail != null ? `<details><summary>All recorded diagnostics for this fact</summary><pre class="raw-measures">${esc(JSON.stringify(detail,null,2))}</pre>${source(fact.recorded_detail)}</details>` : ''}<p class="caption">right/wrong is the test's recorded scoring rule</p>${source(fact.subject)}${source(fact.answer)}${source(fact.rewordings_hit || fact.teacher_hits)}${dataLink(card)}`;
  }
  function validReading(v) {
    if (v == null) return false;
    if (typeof v === 'number') return Number.isFinite(v);
    if (Array.isArray(v)) return v.every(validReading);
    if (typeof v === 'object') return Object.values(v).every(validReading);
    return true;
  }
  function gauges(card) {
    const rows=card.gates || [];
    if (!rows.length) return section(card,'Side effects',missing(null),'Only the named side effects were measured.','absence of recorded limits means no side effects occurred.',true);
    const plain={L1:'Real capitals changed to the edited value',same_frame:'Other subjects under the same question frame',described_as:'Descriptions of the places stayed similar',L3:'Unrelated capitals retained their earlier answer',generic_ppl:'Writing difficulty after the write (perplexity)',cannibal:'Other coined answers displaced',sibling:'Answers switched to a sibling subject',G1:'Real capitals changed to the edited value',G2:'Unrelated capitals retained their earlier answer',G3:'Descriptions of the places stayed similar',G4:'Bystander flips: canonical frame and every recorded training frame',G5:'Rise in writing difficulty (perplexity)',G6:'General-knowledge quiz: net paired correct-item loss',G7:'Matched shuffled control: original-map cross-score'};
    const body=rows.map(g => {
      const observed=value(g.observed), ref=value(g.reference_line), ok=value(g.passed);
      const present=validReading(observed), recorded=typeof ok === 'boolean' && g.passed?.src && g.judgement === 'recorded' && (!g.observed || present);
      const reference=present && number(observed) && number(ref), referenceText=present && validReading(ref);
      const max=reference ? Math.max(Math.abs(observed),Math.abs(ref),1)*1.15 : 1;
      const reading = g.observed ? present ? `<span class="gauge-value">${esc(fmt(observed))}</span>` : 'not recorded for this run' : recorded ? 'recorded gate result' : 'not recorded for this run';
      return `<div class="gauge-row"><div><strong>${esc(!g.plain || g.plain === g.name ? plain[g.name] || g.name : g.plain)}</strong><p>${reading}${recorded ? `<span class="gate-glyph" aria-label="${ok ? 'recorded pass' : 'recorded fail'}">${ok ? '✓' : '✗'}</span>` : ''}</p>${source(g.observed || g.passed)}</div><div>${reference ? `<div class="gauge-track"><span class="gauge-mark" style="width:${Math.min(100,Math.max(0,observed/max*100))}%"></span><span class="gauge-reference" style="left:${Math.min(100,Math.max(0,ref/max*100))}%"></span></div>` : ''}${referenceText ? `<p class="source">derived reference ${Array.isArray(ref) ? 'limits, in recorded frame order' : 'line'} ${esc(g.comparison || g.reference_line.comparison || '')} ${esc(fmt(ref))}${Array.isArray(ref) ? ` (${ref.length} recorded frames; each has its own limit)` : Array.isArray(observed) && observed.length === 2 ? '; the recorded minted-piece count must also be zero' : ''}</p>` : ''}<p class="source">${esc(recorded ? 'test reader’s recorded result' : !present && g.observed ? 'not recorded for this run' : g.judgement || 'not judged yet')}</p>${source(g.reference_line?.rule_src ? {src:g.reference_line.rule_src} : null)}</div></div>`;
    }).join('');
    return section(card,'Side effects',body,'The tick is a rule-derived reference line. ✓/✗ appears only where the exact configuration has a recorded boolean.','a passing check means no damage anywhere; only these axes were measured.',true);
  }
  function writes(card, allLayers = false) {
    const rows=card.per_layer || [], layerCount=value(card.parts?.structure?.layers), unit=card.scale?.unit || rows.find(r => r.unit)?.unit;
    const maximum=value(card.scale?.max), map=new Map(rows.map(r => [r.layer,r]));
    const layers=allLayers && Number.isInteger(layerCount) ? Array.from({length:layerCount},(_,i) => layerCount-1-i) : rows.map(r => r.layer).sort((a,b) => a-b);
    if (!layers.length) return section(card,'Written layers',missing(card.parts?.structure?.layers,'write sizes and layers were not recorded'),'No write size is estimated.','a configured band establishes that a layer was written.',true);
    const body=`<p>${esc(unit || 'unit not recorded')} · shared ruler ${number(maximum) ? '0–' + fmt(maximum) : 'not recorded for this run'}</p><div class="legend"><span>Colour + number = written</span><span>Dashed outline = configured band</span><span>Grey = no recorded write</span></div>${layers.map(layer => { const r=map.get(layer), written=value(r?.written) === true && number(value(r?.write_size)), configured=value(r?.configured) === true; return `<div class="write-row"><span class="write-label">Layer ${layer}</span><div class="write-track${configured ? ' configured' : ''}" data-layer="${layer}" data-written="${written}">${written && number(maximum) && maximum > 0 ? `<span class="write-mark" style="width:${Math.min(100,value(r.write_size)/maximum*100)}%"></span>` : ''}<span class="write-number">${written ? fmt(value(r.write_size)) + ' · written' : configured ? 'configured; not written' : 'no recorded write'}</span></div></div>`; }).join('')}${source(card.scale?.max)}${number(maximum) ? '' : missing(card.scale?.max,'a shared eligible scale is required to compare bar lengths')}`;
    return section(card,'Written layers',body,'Bars use one ruler for applied writes of this unit. The band is an outline; only recorded written layers are coloured.','a longer write is a better result, or different units share a ruler.',true);
  }
  function layerMap(card) {
    const m=card.layer_map || {}, table=value(m.G_table);
    if (!Array.isArray(table) || !table.length) return '';
    const margins=array(m.margins), repeat=array(m.repeat_margins), assignment=value(m.map), recordedRunner=value(m.runner_up), runner=Array.isArray(recordedRunner?.[0]) ? recordedRunner[0] : recordedRunner, facts=card.per_fact || [];
    const maxMargin=Math.max(0,...margins.filter(number),...repeat.filter(number));
    const layers=array(card.parts?.band).length === table[0].length ? array(card.parts.band) : (card.per_layer || []).map(r => r.layer).slice(0,table[0].length);
    const body=`<div class="table-wrap"><table class="map-table"><thead><tr><th>Fact</th>${table[0].map((_,j) => `<th>Layer ${layers[j] ?? 'not recorded'}</th>`).join('')}<th>Margin / repeat</th></tr></thead><tbody>${table.map((row,i) => { const subject=value(facts[i]?.subject), chosen=Array.isArray(assignment) ? assignment[i] : assignment?.[subject], second=Array.isArray(runner) ? runner[i] : runner?.[subject]; return `<tr><th>${esc(subject || 'Fact ' + (i+1))}<br><span class="source">${factHits(facts[i] || {})?.filter(Boolean).length ?? '?'} of ${factHits(facts[i] || {})?.length ?? '?'} right</span></th>${row.map((g,j) => `<td><span class="g-cell${chosen === layers[j] ? ' chosen' : second === layers[j] ? ' runner' : ''}" title="G = ${esc(g)}">${number(g) ? g.toFixed(3) : '?'}</span></td>`).join('')}<td><span class="source">${fmt(margins[i]) ?? '?'} / ${fmt(repeat[i]) ?? '?'}</span>${number(margins[i]) && maxMargin > 0 ? `<span class="margin-mark" style="width:${margins[i]/maxMargin*100}%"></span>` : ''}</td></tr>`; }).join('')}</tbody></table></div><p>Map reproduced on repeat: ${value(m.map_reproduced) === true ? 'yes' : value(m.map_reproduced) === false ? 'no' : 'not recorded'} · δ = ${leafText(m.delta)}</p><p>Rank agreement between G and outcome on recipe B: ${leafText(m.spearman)} (recorded)</p>${source(m.spearman)}${value(m.by_layer) != null ? `<details><summary>Per-layer reading from recipe B</summary><dl>${Object.entries(value(m.by_layer)).map(([layer,row]) => `<dt>Layer ${esc(layer)}</dt><dd>${esc(JSON.stringify(row))}</dd>`).join('')}</dl></details>` : ''}`;
    return section(card,'Per-fact layer map and margins',body,'Ring = chosen depth. Underline = recorded runner-up. A longer margin shows a clearer choice; the repeat is printed beside it.','the fact lives at its chosen depth or that the selector helped the recorded outcome.',true);
  }
  function trajectorySeries(card) {
    if (!/^results\/d1_/.test(recordName(card))) return [];
    const raw=value(card.measures);
    const named=Array.isArray(raw) ? [[card.identity?.field || 'Recorded trajectory',raw]] : raw && typeof raw === 'object' ? Object.entries(raw).flatMap(([name,entry]) => Array.isArray(entry?.trajectory) ? [[name,entry.trajectory]] : name === 'trajectory' && Array.isArray(entry) ? [[name,entry]] : []) : [];
    return named.filter(([,rows]) => rows.length && rows.every(row => number(row.total) && number(row.heldout_cap_correct)));
  }
  function drawTrajectories(card) {
    trajectorySeries(card).forEach(([name,rows],i) => {
      const host=document.getElementById('trajectory-' + i); if (!host) return;
      const width=Math.max(200,host.clientWidth), height=200, count=Math.max(...rows.map(row => row.total),1);
      const x=row => 42+(width-60)*row.total/count, y=row => 16+150*(1-row.heldout_cap_correct/100);
      host.innerHTML=`<h4>${esc(name)}</h4><svg width="${width}" height="${height}" role="img" aria-label="Recorded held-out capital correctness over total writes"><line class="chart-axis" x1="42" y1="16" x2="42" y2="166"/><line class="chart-axis" x1="42" y1="166" x2="${width-18}" y2="166"/><polyline class="chart-line" points="${rows.map(row => `${x(row)},${y(row)}`).join(' ')}"/>${rows.map(row => `<circle class="chart-dot" cx="${x(row)}" cy="${y(row)}" r="3"><title>${row.total} total writes: ${row.heldout_cap_correct}% held-out capital correctness</title></circle>`).join('')}<text x="0" y="22">100%</text><text x="15" y="166">0%</text><text x="42" y="190">Total writes: 0</text><text x="${width-58}" y="190">${count}</text></svg><p class="caption">Held-out capital correctness in percent, at each recorded number of writes. Dots are recorded values.</p><p class="caveat">Does not mean: points between the recorded observations were measured, or drift on another relation is the same.</p>${dataLink(card)}`;
    });
  }
  function recordsView(card) {
    const records=card.records || [], rungs=card.rungs || [], raw=value(card.measures);
    if (!records.length && !rungs.length && !raw) return '';
    let body='';
    if (rungs.length) body += `<h4>Recorded scale rungs</h4><div class="table-wrap"><table><tbody>${rungs.map(row => `<tr>${Object.entries(row).map(([key,leaf]) => `<td><strong>${esc(key.replaceAll('_',' '))}</strong><br>${leafText(leaf)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    if (records.length) body += `<h4>Each stored record: expression and retention</h4><div class="fact-strip">${records.map((row,i) => { const expressed=value(row.expressed_at_apply), retained=value(row.retained_at_end); return `<button class="fact-cell ${typeof retained !== 'boolean' ? 'missing' : retained ? 'hit-3' : expressed ? 'hit-1' : 'hit-0'}" data-record="${i}" data-card="${esc(card.card_id)}"><span>${i+1}</span><span>E ${expressed === true ? '✓' : expressed === false ? '✗' : '?'}</span><span>R ${retained === true ? '✓' : retained === false ? '✗' : '?'}</span></button>`; }).join('')}</div><p class="caption">E = expressed when applied; R = retained at the end. The two states are recorded separately.</p><div id="record-panel" class="fact-panel"></div><details><summary>${records.length} original stored-record rows</summary>${records.map((row,i) => `<div class="timeline-row"><strong>Record ${i+1}</strong><dl>${Object.entries(row).map(([key,leaf]) => `<dt>${esc(key.replaceAll('_',' '))}</dt><dd>${leafText(leaf)}</dd>`).join('')}</dl></div>`).join('')}</details>`;
    body += trajectorySeries(card).map((_,i) => `<div id="trajectory-${i}" class="loss-chart" data-chart></div>`).join('');
    if (raw) body += `<details><summary>Recorded measures and trajectories</summary><pre class="raw-measures">${esc(JSON.stringify(raw,null,2))}</pre></details>`;
    return section(card,'The line’s recorded measures',body,'These values use the original test’s units and scale.','another line’s target or scoring rule applies here.',true);
  }
  function trainingFor(card) {
    if (card?.training) return card;
    if (!recordName(card).startsWith('experiments/c10w/runs/c10w_oracle/')) return null;
    const phase=recordName(card).split('/').slice(0,3).join('/') + '/';
    return [...cards.values()].find(other => other.training && recordName(other).startsWith(phase) && other.identity?.arm === card.identity?.arm) || null;
  }
  function training(card) {
    card=trainingFor(card);
    if (!card || !array(card.training.losses).length) return '';
    const points=array(card.training.losses);
    const fit=value(card.training.fit);
    const fitText=fit && number(fit.correct) && number(fit.n) ? `${fmt(fit.correct)} of ${fmt(fit.n)} training answers right` : leafText(card.training.fit);
    return section(card,'Recorded training steps',`<div id="training-chart" class="loss-chart"></div><div id="training-legend" class="legend"></div><div class="control"><label for="training-step">Recorded step</label><input id="training-step" type="range" min="0" max="${points.length-1}" value="0" step="1"></div><div id="training-readout" class="chart-readout" aria-live="polite"></div><p>Answers at this step: not recorded; an observation replay can re-create them (REPLAY, NOT EVIDENCE).</p><h4>Final fit, measured at the end</h4><p>${fitText}</p>${source(card.training.fit)}<details><summary>Final recorded fit by fact and training question</summary><pre>${esc(JSON.stringify(fit,null,2))}</pre></details>`,'The curves show recorded training loss. Answers were evaluated separately at the end.','low training loss establishes held-out answer quality or gives answers at an intermediate step.',true);
  }
  function drawTraining(card, at=0) {
    const host=document.getElementById('training-chart'); if (!host) return;
    card=trainingFor(card); if (!card) return;
    const phase=recordName(card).split('/').slice(0,3).join('/') + '/', unique=new Map();
    [card,...cards.values()].filter(other => other.training && recordName(other).startsWith(phase) && other.identity?.arm === card.identity?.arm).forEach(other => { const key=other.training.losses.src?.file || recordName(other); if (!unique.has(key)) unique.set(key,other); });
    const curves=[...unique.values()], points=array(card.training.losses), palette=['#d7b4ff','#ffce88','#b9c6ff','#ffadba'];
    const width=Math.max(200,host.clientWidth), height=210, max=Math.max(...curves.flatMap(c => array(c.training.losses).map(p => p.loss)).filter(number),1e-12), last=Math.max(...points.map(p => p.step),1);
    const x=p => 44+(width-62)*p.step/last, y=p => 18+(height-52)*(1-p.loss/max), current=points[at];
    host.innerHTML=`<svg width="${width}" height="${height}" role="img" aria-label="Recorded training loss by step"><line class="chart-axis" x1="44" y1="18" x2="44" y2="${height-34}"/><line class="chart-axis" x1="44" y1="${height-34}" x2="${width-18}" y2="${height-34}"/>${curves.map((c,i) => `<polyline class="chart-line" style="stroke:${palette[i%palette.length]}" stroke-dasharray="${i%2 ? '6 4' : 'none'}" points="${array(c.training.losses).map(p => `${x(p)},${y(p)}`).join(' ')}"/>`).join('')}${current ? `<circle class="chart-dot" cx="${x(current)}" cy="${y(current)}" r="5"/>` : ''}<text x="3" y="24">${fmt(max)}</text><text x="17" y="${height-32}">0</text><text x="44" y="${height-9}">Step 0</text><text x="${width-78}" y="${height-9}">${last}</text></svg>`;
    document.getElementById('training-legend').innerHTML=curves.map((c,i) => `<span style="color:${palette[i%palette.length]}">${i%2 ? 'Dashed' : 'Solid'} · seed ${leafText(c.training.seed)}${value(c.training.retrain) === true ? ' · retrain' : ''}</span>${dataLink(c)}`).join('');
    if (current) document.getElementById('training-readout').innerHTML=`<p>Step ${esc(current.step)} · loss ${esc(fmt(current.loss))} · recorded step time ${number(array(card.training.step_seconds)[current.step-1]) ? fmt(array(card.training.step_seconds)[current.step-1]) + ' seconds' : 'not recorded for this run'}</p>${source(card.training.losses)}${source(card.training.step_seconds)}`;
  }
  function events(card) {
    const timed=card.events?.timestamped || [], untimed=card.events?.untimed || [];
    if (!timed.length && !untimed.length) return section(card,'Recorded events',missing(null,'needs timestamps, log markers or recorded loss points'),'What the run recorded, in order.','the historical internal activity can be reconstructed.',true);
    return section(card,'Recorded events',`<div class="control"><label for="event-step">Choose a recorded event</label><input id="event-step" type="range" min="0" max="${timed.length+untimed.length-1}" value="0" step="1"></div><div id="event-readout" class="chart-readout" aria-live="polite"></div><details open><summary>Timestamped track · ${timed.length} events</summary>${timed.map(e => `<div class="event-track"><strong>${esc(e.name)}</strong><p>${leafText(e.at)}</p>${source(e.at)}</div>`).join('') || '<p>No recorded timestamps.</p>'}</details><details><summary>Time not recorded · ${untimed.length} events</summary>${untimed.map(e => `<div class="event-track"><strong>${esc(e.name)}</strong><p>time not recorded</p><p>${leafText(e.detail)}</p>${source(e.detail)}</div>`).join('')}</details>`,'Events with recorded timestamps have their own track. Untimed events remain in source and step order.','durations, file names or saved-file times identify when an untimed event happened.',true);
  }
  function eventReadout(card,at=0) {
    const host=document.getElementById('event-readout'); if (!host) return;
    const timed=card.events?.timestamped || [], e=[...timed,...card.events?.untimed || []][at];
    if (e) host.innerHTML=`<strong>${esc(e.name)}</strong><p>${at < timed.length ? leafText(e.at) : 'time not recorded'}</p>${e.detail ? `<p>${leafText(e.detail)}</p>` : ''}${source(e.at || e.detail)}`;
  }
  function parts(card,layer) {
    const s=card.parts?.structure || {}, row=(card.per_layer || []).find(r => r.layer === layer), written=value(row?.written) === true;
    if (value(s.layers) == null) return missing(s.layers,'model structure was not bound to this record');
    const names=[['Input normaliser','input_layernorm'],['Attention','q / k / v / o projections'],['Add back','attention branch → main line'],['Second normaliser','post_attention_layernorm'],['MLP: gate & up','SiLU(gate) × up'],['MLP: down','mlp.down_proj'],['Add back','MLP branch → main line']];
    return `<h4>Layer ${layer} · static parts</h4><div class="part-flow">${names.map(([name,module],i) => `<div class="part-box${i === 5 && written ? ' written' : ''}"><strong>${esc(name)}</strong><p>${esc(module)}</p><p>${i === 5 && written ? fmt(value(row.write_size)) + ' ' + esc(row.unit || card.scale?.unit) + ' · written' : 'not changed by this method'}</p></div>`).join('')}</div><dl><dt>Hidden width → MLP width → hidden width</dt><dd>${leafText(s.hidden_size)} → ${leafText(s.intermediate_size)} → ${leafText(s.hidden_size)}</dd><dt>Attention heads / key-value groups</dt><dd>${leafText(s.num_attention_heads)} / ${leafText(s.num_key_value_heads)}</dd><dt>Written module</dt><dd>${leafText(card.parts?.written_module)}</dd><dt>Basis for unchanged stored numbers</dt><dd>${leafText(card.parts?.untouched_basis)}</dd></dl>${source(card.parts?.untouched_basis)}<p class="missing">Per-part activity and push toward an answer: not recorded for this run; needs an observation REPLAY (NOT EVIDENCE).</p>`;
  }
  function wiring(card) {
    const count=value(card.parts?.structure?.layers), tied=value(card.parts?.structure?.tie_word_embeddings), layers=(card.per_layer || []).filter(r => value(r.written) === true).map(r => r.layer);
    if (!Number.isInteger(count)) return missing(card.parts?.structure?.layers,'the static diagram needs the recorded model structure');
    return `<p class="diagram-label" data-diagram-label="diagram, not recorded activity">diagram, not recorded activity</p><button id="animate-wiring" aria-pressed="false">Animate the diagram</button><div class="wiring" id="wiring-diagram"><span class="wire-pulse" aria-hidden="true"></span><div class="main-line"><div class="wire-stage"><strong>Input pieces → word table</strong></div><div class="wire-stage"><strong>Main line through ${count} layers</strong><p>Input normaliser → attention → add back</p><p>Second normaliser → gate × up → down → add back</p></div><div class="wire-stage${layers.length ? ' written' : ''}"><strong>${layers.length ? 'Written down projection at layers ' + layers.join(', ') : 'Written layers not recorded'}</strong><p>The key is read at ${esc(value(card.stimulus?.keyed_position) || 'a position not recorded')}. The changed matrix acts on every piece passing through a written layer.</p></div><div class="wire-stage"><strong>Final normaliser → ${tied === true ? 'the same word table (tied head)' : tied === false ? 'output head' : 'output table relationship not recorded'}</strong><p>Next-piece probabilities</p></div></div></div>`;
  }
  function picker() {
    return `<div class="control"><label for="picker-search">Choose a recorded run · search by registry ID</label><input id="picker-search" type="search" role="combobox" autocomplete="off" placeholder="C10V, G6.1, R5…" aria-controls="picker-results" aria-autocomplete="list" aria-expanded="false"></div><div id="picker-results" class="picker-results" role="listbox" aria-label="Recorded runs" aria-live="polite"></div>`;
  }
  function pickerResults(query='') {
    const target=document.getElementById('picker-results'); if (!target) return;
    const q=query.toLowerCase();
    const matches=index.filter(r => !q || `${r.experiment} ${r.title} ${r.source} ${r.model}`.toLowerCase().includes(q)).sort((a,b) => Number(String(b.experiment).toLowerCase().startsWith(q)) - Number(String(a.experiment).toLowerCase().startsWith(q)) || Number(b.role === 'binding')-Number(a.role === 'binding') || Number(b.has_writes)-Number(a.has_writes) || String(b.date || '').localeCompare(String(a.date || '')));
    const groups=new Map(); matches.forEach(r => { const name=r.experiment || r.line || 'Context not recorded'; if (!groups.has(name)) groups.set(name,[]); groups.get(name).push(r); });
    const ordered=[...groups.values()].flatMap(rows => rows.slice(0,Math.max(1,Math.floor(50/Math.max(groups.size,1))))).slice(0,50);
    target.innerHTML=ordered.map(r => `<button id="picker-option-${esc(r.card_id)}" class="picker-result" role="option" tabindex="-1" aria-selected="false" data-pick-run="${esc(r.card_id)}" data-run="${esc(r.card_id)}"><span class="row-main"><strong>${esc(runTitle(r))}</strong><span class="row-meta">${esc([r.model,displayDate(r.date)].filter(Boolean).join(' · '))}</span><span class="row-meta">${esc(runDescription(r))}</span></span></button>`).join('') || '<p>No recorded run matches.</p>';
    const search=document.getElementById('picker-search');
    search.removeAttribute('aria-activedescendant'); search.setAttribute('aria-expanded',String(ordered.length > 0));
  }
  function runActions(card) {
    const line=card.context?.experiment?.node_id || card.context?.corpus?.node_id || card.context?.condition?.node_id;
    return `<div class="run-actions">${line ? `<button data-line="${esc(line)}">Open this run’s science line</button>` : ''}<button data-model-run="${esc(card.card_id)}">Inside this run’s model</button><button data-view="compare" data-compare-run="${esc(card.card_id)}">Compare this run</button><button data-view="runs">Browse runs</button></div>`;
  }
  function cardIdentity(card) {
    const i=card.identity || {};
    return `<div class="selection-title" data-selected-run="${esc(card.card_id)}"><h3>${esc(docText(card.context?.experiment || card.context?.corpus) || 'Recorded observation')}</h3><p>${esc([value(i.model),i.recipe,i.arm,value(i.date)].filter(Boolean).join(' · '))}</p><p class="source">${esc(recordName(card))} · ${esc(i.field || '')}</p>${value(card.context?.question) != null ? `<p>${documentaryText(card.context.question)}</p>` : missing(card.context?.question,'context not recorded')}${value(card.context?.match_note) != null ? `<p class="source">${esc(docText(card.context.match_note))}</p>` : ''}${value(card.context?.framing_status) === 'DRAFT' ? '<span class="draft">draft framing, not yet reviewed</span>' : ''}</div>`;
  }
  function attachCharts(card) {
    drawTraining(card); eventReadout(card);
    const table=value(card.layer_map?.G_table);
    if (Array.isArray(table)) {
      const numbers=table.flat(), low=Math.min(...numbers), high=Math.max(...numbers);
      document.querySelectorAll('.g-cell').forEach((cell,i) => { const shade=high > low ? (numbers[i]-low)/(high-low) : 0; cell.style.backgroundColor=`rgb(${Math.round(89-52*shade)},${Math.round(101-63*shade)},${Math.round(125-71*shade)})`; });
    }
    drawTrajectories(card);
  }
  function mathlabSummary(card) {
    const s=value(card.mathlab.state);
    const scope=s.purpose === 'admission' ? 'Admission only; this receipt does not complete an experiment step.' :
                s.purpose === 'experiment' ? 'Experiment step ' + s.step : 'Run scope not recorded.';
    return section(card,'MATH-PROXY','<p><strong>math estimate, not evidence</strong></p><p>' +
      esc(s.run_id || card.identity.field) + ' · ' + esc(s.status) + '</p><p>' + esc(scope) + '</p>' +
      '<p>Outcome: ' + esc(s.outcome || 'not recorded') + '</p>' +
      (s.summary ? '<p>' + esc(s.summary) + '</p>' : '') + source(card.label),'Saved event snapshot; no liveness inferred.','');
  }
  function mathlabView(card) {
    const m=card.mathlab, s=value(m.state), errors=array(m.errors);
    const cell=x => x == null ? 'not recorded' : typeof x === 'object' ?
      '<pre class="raw-measures">' + esc(JSON.stringify(x,null,2)) + '</pre>' : esc(String(x));
    const table=(rows,columns) => rows.length ? '<div class="table-wrap"><table><thead><tr>' +
      columns.map(([,label]) => '<th>' + esc(label) + '</th>').join('') + '</tr></thead><tbody>' +
      rows.map(row => '<tr>' + columns.map(([key]) => '<td>' + cell(row[key]) + '</td>').join('') + '</tr>').join('') +
      '</tbody></table></div>' : '<p class="missing">not recorded for this run</p>';
    let body=mathlabSummary(card);
    if (errors.length) body+=section(card,'Parse errors','<div role="alert"><ul>' +
      errors.map(error => '<li>' + esc(error) + '</li>').join('') + '</ul></div>' + source(m.errors),
      'Invalid records are excluded by the shared event reader.','');
    if (s.halt) body+=section(card,'Halt','<p>' + esc(s.halt.reason) + '</p><p>Diagnostic: ' +
      esc(s.halt.diagnostic_path) + '</p>','math estimate, not evidence','');
    if (s.calibration_outcome === 'FAIL' && s.steps['3'] === 'FAIL' && s.status === 'stopped: check failed')
      body+='<p>Stop the lab cheaply: aggregate calibration failed.</p>';
    body+=section(card,'Experiment steps',table(Object.entries(s.steps).map(([step,outcome]) =>
      ({step:'Step ' + step,outcome})),[['step','Step'],['outcome','Recorded state']]),'math estimate, not evidence','');
    if (s.admission) body+=section(card,'Admission',table([s.admission],[['allowed','Allowed'],['reasons','Reasons']]),'','');
    body+=section(card,'Stages',table(s.stages,[['stage','Stage'],['plain_words','What it does'],['cap_s','Cap seconds'],
      ['ts','Started UTC'],['finished_ts','Finished UTC'],['outcome','Outcome'],['summary','Summary']]),'math estimate, not evidence','');
    body+=section(card,'Progress',table(s.progress ? [s.progress] : [],[['stage','Stage'],['done','Done'],
      ['total','Total'],['unit','Unit'],['ts','Recorded UTC']]),'','');
    const groups=Object.entries(s.gate_groups).map(([name,g]) => ({name,...g,completion:g.complete ? 'complete' : 'incomplete'}));
    const gates=s.gates.map(g => ({...g,outcome:s.gate_outcomes[g.gate_id]}));
    body+=section(card,'Gates',table(groups,[['name','Planned group'],['outcome','Outcome'],['completion','Group coverage']]) +
      table(gates,[['gate_id','Check'],['plain_words','What it checks'],['observed','Observed'],['comparison','Comparison'],
                   ['bar','Threshold'],['outcome','Outcome']]),'Outcomes and group coverage come from the shared fold. math estimate, not evidence','');
    const mintNorms=[0,1,2].map(seed => s.gates.find(g => g.gate_id === 'mint-norm-mint1_s' + seed));
    if (mintNorms.every(g => g && g.passed === false))
      body+=section(card,'Mint replay eligibility','<p>0 of 3 recorded mint arms eligible for replay admission (derived): all three required norm checks failed.</p>' +
        source(m.state.inputs[0]),'Derived eligibility, not a recorded admission receipt. math estimate, not evidence','');
    body+=section(card,'Resource samples',table(s.resource_samples,[['ts','Recorded UTC'],['avail_gib','Available GiB'],
      ['floor_gib','Floor GiB'],['rss_gib','RSS GiB'],['cpu_pct','CPU %']]),'Recorded samples; no live resource probe.','');
    body+=section(card,'Findings',m.findings.map(f => {
      const e=value(f.event), document=Array.isArray(f.document) ?
        (f.document.length ? '<pre class="raw-measures">' + esc(f.document.map(line => value(line)).join('\n')) + '</pre>' :
         '<p>Referenced finding is empty.</p>') + (f.name ? '<a class="source" href="' + esc(sourceURL(f.name)) + '">' +
         esc(f.name) + '</a>' : source(f.document[0])) : missing(f.document);
      return '<article><h4>' + esc(e.finding_id) + ' · MATH-PROXY</h4><p>math estimate, not evidence</p><p>' +
        esc(e.summary) + '</p>' + document + source(f.event) + '</article>';
    }).join('') || '<p class="missing">not recorded for this run</p>','Only findings referenced by the events are included.','');
    body+=section(card,'Candidate questions — ideas to test',s.candidates.map(c => '<article><p>' + esc(c.question) +
      '</p><p>Source: ' + esc(c.source) + ' · ' + (c.offline ? 'offline idea' : 'idea') + '</p></article>').join('') ||
      '<p class="missing">not recorded for this run</p>','Ideas to test; no finding or scientific evidence is claimed.','');
    return body;
  }
  function renderRun(card) {
    if (card.mathlab) {
      content.innerHTML=header('Math lab','math estimate, not evidence','MATH-PROXY') + cardIdentity(card) +
        '<div class="run-actions"><button data-view="runs">Browse runs</button></div>' + mathlabView(card) + events(card) +
        section(card,'Source events',dataLink(card) + '<a href="' + esc(sourceURL(recordName(card))) +
          '">Original events.jsonl</a><p>' + (card.sources || []).length + ' source files are hashed in the card.</p>' +
          source(card.mathlab.state.inputs[0]),'read_events and the shared fold supply this snapshot.','');
      eventReadout(card);
      return;
    }
    const downloads=recordName(card).startsWith('results/') && recordName(card).endsWith('.json') ? `<a href="runs/${esc(card.card_id)}.svg" download>Save SVG</a><a href="runs/${esc(card.card_id)}.png" download>Save PNG</a>` : '';
    content.innerHTML=header('The recorded run','Read this result in its own test’s terms.')+cardIdentity(card)+runActions(card)+plainWords(card)+badge(card)+factStrip(card)+gauges(card)+writes(card)+layerMap(card)+recordsView(card)+training(card)+events(card)+section(card,'Source record and saved downloads',`${dataLink(card)}<a href="${esc(sourceURL(recordName(card)))}">Original source</a>${downloads}<p class="source">${(card.sources || []).length} source files are hashed in the card.</p>`,'The JSON card holds full precision and source paths.','this display certifies the validity or comparability of a scientific record.');
    attachCharts(card);
  }
  function renderModel(card) {
    if (card.mathlab) { renderRun(card); return; }
    const count=value(card.parts?.structure?.layers), written=(card.per_layer || []).filter(r => value(r.written) === true), chosen=written[0]?.layer ?? 0;
    content.innerHTML=header('Inside the model','A layer is one processing stage. A write size measures how much its stored numbers changed.') + picker() + `<div class="selection-title">${cardIdentity(card)}</div>`+runActions(card)+`<div class="controls"><button id="show-2d" aria-pressed="true">2D recorded layers</button><button id="show-3d" aria-pressed="false">3D structure</button><div class="control"><label for="layer-pick">Open a layer</label><select id="layer-pick">${Number.isInteger(count) ? Array.from({length:count},(_,i) => `<option value="${i}"${chosen === i ? ' selected' : ''}>Layer ${i}${written.some(r => r.layer === i) ? ' · written' : ''}</option>`).join('') : '<option>Layer count not recorded</option>'}</select></div></div><div id="tower" hidden></div><p id="model-status" class="caption">The recorded 2D view is available. The optional 3D view needs WebGL and the pinned CDN.</p><div id="tower-fallback">${writes(card,true)}</div>${section(card,'Parts of a layer',`<div id="parts-diagram">${parts(card,chosen)}</div>`,'Attention reads earlier pieces; the MLP transforms the running summary. Colour marks changed stored numbers.','unchanged stored numbers produce unchanged activity after a write.',true)}${section(card,'Static wiring',wiring(card),'Each branch reads the running main line and adds its result back to it.','the animated pulse is activity recorded during this run.',true)}${section(card,'Answer signal and internal flow',missing(null,'needs TELEMETRY for a future run, or an observation REPLAY (NOT EVIDENCE)'), 'Phase 1 contains recorded results and static structure.','internal activity was measured for this historical run.')}${training(card)}${events(card)}`;
    attachCharts(card);
  }
  function comparison(left,right) {
    const lf=left.per_fact || [], rf=right.per_fact || [];
    const no=reason => ({eligible:false,reason});
    if (!lf.length || !rf.length || lf.length !== rf.length) return no('different or unrecorded fact sets');
    const key=f => JSON.stringify([value(f.subject),value(f.answer)]), rightMap=new Map(rf.map(f => [key(f),f]));
    if (rightMap.size !== rf.length || new Set(lf.map(key)).size !== lf.length) return no('ambiguous subject and answer join');
    const counts={both:0,left:0,right:0,neither:0}, joined=[];
    for (const fact of lf) {
      const other=rightMap.get(key(fact));
      if (!other) return no('different subjects or changed answers');
      if (fact.hit_kind !== other.hit_kind) return no('different scoring kinds (free answer and teacher-forced are distinct)');
      const lt=value(fact.generated_templates) || value(left.stimulus?.questions), rt=value(other.generated_templates) || value(right.stimulus?.questions);
      if (!Array.isArray(lt) || !Array.isArray(rt) || JSON.stringify(lt) !== JSON.stringify(rt)) return no('different or unrecorded question templates');
      const a=factHits(fact), b=factHits(other);
      if (!a || !b || a.length !== b.length || a.length !== lt.length) return no('scored booleans not recorded for matching templates');
      a.forEach((hit,j) => counts[hit && b[j] ? 'both' : hit ? 'left' : b[j] ? 'right' : 'neither']++);
      joined.push(value(fact.subject));
    }
    return {eligible:true,counts,joined};
  }
  function renderCompare(left,right) {
    if (left?.mathlab || right?.mathlab) {
      content.innerHTML=header('Compare run records','Math estimates retain their MATH-PROXY tier.') +
        '<div class="controls"><button id="compare-left" data-compare-slot="left">Choose left run</button>' +
        '<button id="compare-right" data-compare-slot="right">Choose right run</button></div>' + picker() +
        '<p class="missing">not comparable: math estimate, not evidence; no matched answer-evidence comparison.</p>' +
        '<div class="compare-grid">' + [left,right].map((c,i) => c ? '<article><h3>' + (i ? 'Right' : 'Left') +
          '</h3>' + cardIdentity(c) + (c.mathlab ? mathlabSummary(c) : badge(c)) +
          '<button data-run="' + esc(c.card_id) + '">Open run</button></article>' : '<article>Choose a run.</article>').join('') + '</div>';
      for (const [side,c] of [['left',left],['right',right]]) {
        const button=document.getElementById('compare-' + side);
        button.value=c?.card_id || ''; button.dataset.card=c?.card_id || '';
      }
      return;
    }
    const chosen=side => side ? [side.identity?.recipe,side.identity?.arm,recordName(side)].filter(Boolean).join(' · ') : 'Choose a recorded run';
    const result=left && right ? comparison(left,right) : null;
    content.innerHTML=header('Compare recorded runs','Two tests next to each other, using the same unit-specific rulers.')+`<div class="controls"><button id="compare-left" data-compare-slot="left">Left: ${esc(chosen(left))}</button><button id="compare-right" data-compare-slot="right">Right: ${esc(chosen(right))}</button></div>${picker()}<p class="caveat">Does not mean: differences of a few questions between two single runs are a reliable effect.</p>${result ? `<section class="evidence-section" data-chart><h3>Matched fact and question outcomes · derived</h3>${result.eligible ? `<div class="stats">${[['both','Both right'],['left','Only left'],['right','Only right'],['neither','Neither']].map(([key,title]) => `<div class="stat"><strong>${result.counts[key]}</strong>${title}</div>`).join('')}</div><p class="source">Derived from recorded booleans joined by subject, answer, question template and scoring kind; never by row index.</p>` : `<p class="missing">not comparable: ${esc(result.reason)}</p>`}<p class="caption">The joined questions show where these recorded outcomes agree and differ.</p><p class="caveat">Does not mean: a difference between two single runs is a reliable effect.</p><div class="run-actions">${left.card_id === right.card_id ? dataLink(left,'Data for both runs') : dataLink(left,'Left run data') + dataLink(right,'Right run data')}</div></section>` : ''}<div class="compare-grid">${[left,right].map((card,i) => card ? `<article><div class="compare-heading"><h3>${i ? 'Right' : 'Left'} · ${esc(docText(card.context?.experiment) || card.identity?.recipe || 'Recorded run')}</h3><button data-run="${esc(card.card_id)}">Open run</button></div>${cardIdentity(card)}${badge(card)}${factStrip(card,true)}${gauges(card)}${writes(card)}</article>` : '<article><p>Choose a recorded run for this side.</p></article>').join('')}</div>`;
    for (const [side,card] of [['left',left],['right',right]]) {
      const button=document.getElementById('compare-' + side);
      button.value=card?.card_id || ''; button.dataset.card=card?.card_id || '';
    }
  }
  async function renderModelHistory(version) {
    const name=state.model || 'Mistral-7B', catalog=lab.models?.[name] || {}, related=graph.edges.filter(e => e.source === 'model:' + name || e.target === 'model:' + name), matching=index.filter(r => String(r.model || '').replace(/^.*\//,'') === name);
    content.innerHTML=header(name,'The models and tests are shown in the era where they were used.','Model history')+`<article><h3>Recorded model context</h3><p>${esc(docText(catalog.size) || 'Size not recorded')} · ${esc(docText(catalog.status) || 'Status not recorded')}</p>${catalog.note ? `<p>${esc(docText(catalog.note))}</p>` : ''}${catalog.note_source ? `<a href="${esc(sourceURL(value(catalog.note_source)))}">Read the model’s documentary finding</a>` : ''}${related.map(e => `<div class="connection-row"><button data-line="${esc(e.source === 'model:' + name ? e.target : e.source)}">${esc(nodeLabel(e.source === 'model:' + name ? e.target : e.source))}</button>${edgeSources(e)}</div>`).join('')}<a data-for-view href="context.json">Data for this view</a></article><div id="model-history-records"><p>Loading the documentary cards…</p></div>`;
    const loaded=await Promise.all(matching.slice(0,20).map(r => loadCard(r.card_id)));
    if (version !== renderVersion) return;
    document.getElementById('model-history-records').innerHTML=loaded.length ? loaded.map(card => `<article>${cardIdentity(card)}${value(card.label) != null ? `<p>${esc(value(card.label))}</p>` : ''}${plainWords(card)}${dataLink(card)}<button data-run="${esc(card.card_id)}">Open documentary card</button></article>`).join('') : '<article><p>Documentary context only; no machine-readable run measurements recorded.</p></article>';
  }
  function renderLearn() {
    const eras=Object.keys(lab.contexts?.eras || {}), selected=shortEra(state.learnEra);
    const entries=lab.evaluations || [];
    content.innerHTML=header('Learn & evaluations','Read each line’s question, measure and finding in its own era’s terms.')+`<div class="controls"><button data-learning="learn" aria-pressed="${state.learning === 'learn'}">Learn</button><button data-learning="evaluations" aria-pressed="${state.learning === 'evaluations'}">Evaluations</button><div class="control"><label for="learn-era">Research era</label><select id="learn-era"><option value="">All eras</option>${eras.map(id => `<option value="${esc(shortEra(id))}"${shortEra(id) === selected ? ' selected' : ''}>${esc(eraLabel(id))}</option>`).join('')}</select></div></div>`;
    if (state.learning === 'learn') {
      content.innerHTML+=`<div class="grid">${eras.filter(id => !selected || shortEra(id) === selected).map(id => { const era=eraData(id); return `<article><span class="tag">${esc(eraLabel(id))}</span><h3>${esc(docText(era.question || era.name) || eraLabel(id))}</h3><p>${esc(docText(era.measure) || 'No single headline number recorded; see the source entry.')}</p><p>${esc(docText(era.bar || era.judged_against) ? 'the line’s bar: ' + docText(era.bar || era.judged_against).replace(/^(\d+)\/(\d+)$/,'$1 of $2') : 'The original test’s bar is in its cited source.')}</p><span class="draft">draft framing, not yet reviewed</span><button data-line="era:${esc(shortEra(id))}">Explore this era</button><a data-for-view href="context.json">Data for this view</a></article>`; }).join('')}</div><article><h3>Reading a recorded picture</h3><p>A weight is a stored number. A write changes some stored numbers; retrieval asks whether the tested information can still be read. A layer is one processing stage. These are different from a recorded answer or a test verdict.</p><p>A source path names the exact field behind a picture. A derived value is arithmetic over recorded inputs. A missing value stays unknown. A repeat tests whether an observation happens again.</p><a data-for-view href="context.json">Data for this view</a></article>`;
    } else {
      const filtered=entries.filter(e => !selected || shortEra(e.era) === selected);
      const eraGroups=new Map();
      function evaluationGroup(era,line,node) {
        const recordedEra=shortEra(era), key=eras.some(id => shortEra(id) === recordedEra) ? recordedEra : 'unknown';
        if (!eraGroups.has(key)) eraGroups.set(key,new Map());
        const groups=eraGroups.get(key);
        if (!groups.has(line)) groups.set(line,{entries:[],node});
        if (node) groups.get(line).node=node;
        return groups.get(line);
      }
      filtered.forEach(e => {
        const line=e.line || (String(e.ref || '').match(/CORPUS\/(\d+)/) ? 'corpus:' + String(e.ref).match(/CORPUS\/(\d+)/)[1].padStart(2,'0') : 'unknown');
        evaluationGroup(e.era,line).entries.push(e);
      });
      const scientific=graph.nodes.filter(n => kind(n) === 'experiment' && (!selected || shortEra(n.era) === selected));
      scientific.forEach(n => evaluationGroup(n.era,n.node_id,n));
      content.innerHTML+=`<div class="evaluation-list">${[...eraGroups].sort(([a],[b]) => natural(eraLabel(a),eraLabel(b))).map(([era,groups]) => {
        const entriesCount=[...groups.values()].reduce((sum,group) => sum+group.entries.length,0), registryCount=[...groups.values()].filter(group => group.node).length;
        const experiments=[...groups].sort(([a],[b]) => natural(nodeLabel(a),nodeLabel(b))).map(([line,group]) => {
        const label=['unknown','unassigned'].includes(line) ? 'Context not recorded' : nodeLabel(line), n=group.node;
        const registry=n && kind(n) === 'experiment' ? `<article><h3>Registry status and source finding</h3>${n.description ? `<p>${esc(docText(n.description))}</p>${source(n.description)}` : ''}${scienceStatus(n,'Status now (registry):')}<button data-line="${esc(line)}">Open the line and its evidence</button><a data-for-view href="context.json">Data for this view</a></article>` : '';
        const evaluations=group.entries.map(e => {
          const title=docText(e.source_result?.name || e.question || 'Evaluation'), templates=e.template_fields || [];
          const fields=[['question','Question asked'],['result','Result'],['rules_out','What it rules out'],['leaves_open','What it leaves open'],['next_step','Next step']].filter(([key]) => value(e[key]) != null && !templates.includes(key) && !(key === 'question' && docText(e[key]) === title));
          return `<article><h3>${esc(title)}</h3>${fields.length ? `<dl>${fields.map(([key,name]) => `<dt>${name}</dt><dd>${esc(docText(e[key]))}</dd>`).join('')}</dl>` : ''}${templates.length || !fields.length ? '<p class="source">Interpretation fields not separately recorded; see the source evaluation.</p>' : ''}<p class="source">${esc(docText(e.ref))}</p><a data-for-view href="evidence/docs/c10_evaluations.json">Data for this view</a></article>`;
        }).join('');
        return `<details class="evaluation-group"><summary><strong>${esc(label)}</strong><span class="tag">${group.entries.length ? plural(group.entries.length,'evaluation') : '1 documentary finding'}</span></summary><div>${evaluations}${registry}</div></details>`;
        }).join('');
        return `<details class="evaluation-era" data-science-line="era:${esc(era)}"><summary><strong>${esc(era === 'unknown' ? 'Context not recorded' : eraLabel(era))}</strong><span class="tag">${plural(entriesCount,'evaluation')}${registryCount ? ' · ' + plural(registryCount,'registry finding') : ''}</span></summary><div>${experiments}</div></details>`;
      }).join('')}</div>`;
    }
  }
  async function render() {
    const version=++renderVersion;
    if (window.LabModel) window.LabModel.stop();
    content.after(connections);
    connections.hidden=true;
    frame();
    if (state.view !== 'map') { await ensureIndex(); if (version !== renderVersion) return; }
    if (state.view === 'map') renderMap();
    else if (state.view === 'lines') renderLines();
    else if (state.view === 'runs') renderRuns();
    else if (state.view === 'learn') renderLearn();
    else if (state.view === 'model-history') await renderModelHistory(version);
    else if (state.view === 'compare') {
      const pair=state.compare.length ? state.compare : [state.run];
      const loaded=await Promise.all(pair.slice(0,2).map(id => id ? loadCard(id) : null));
      if (version !== renderVersion) return;
      renderCompare(loaded[0],loaded[1]); frame(loaded[0]);
    } else if (state.view === 'run' || state.view === 'model') {
      content.innerHTML='<p>Loading the recorded card…</p>';
      if (!state.run) { content.innerHTML='<article><p>No recorded run is available in the index.</p></article>'; return; }
      const card=await loadCard(state.run);
      if (version !== renderVersion) return;
      frame(card); state.view === 'model' ? renderModel(card) : renderRun(card);
    } else renderMap();
  }
  let modelScript;
  async function enhanceModel() {
    const card=await loadCard(state.run);
    if (!modelScript) modelScript=new Promise((resolve,reject) => {
      const script=document.createElement('script'); script.src='model.js'; script.onload=resolve; script.onerror=() => { modelScript=null; reject(new Error('The optional 3D script could not load.')); }; document.head.append(script);
    });
    await modelScript;
    await window.LabModel.start(card);
  }
  document.addEventListener('click',event => {
    const button=event.target.closest('button');
    const edge=event.target.closest('[data-edge]');
    if (edge) { const e=graph.edges[Number(edge.dataset.edge)]; connections.hidden=false; connections.innerHTML=`<h3>${esc(nodeLabel(e.source))} → ${esc(nodeLabel(e.target))}</h3><p>${esc(e.edge)} document connection; not evidence.</p>${edgeSources(e)}<a data-for-view href="context.json">Data for this view</a>`; return; }
    if (!button) return;
    const d=button.dataset;
    if (d.pickRun) {
      if (state.view === 'compare') fire(chooseCompare(d.pickRun));
      else fire(chooseRun(d.pickRun,'model'));
    } else if (d.run) fire(chooseRun(d.run));
    else if (d.modelRun) fire(chooseRun(d.modelRun,'model'));
    else if (d.compareRun) fire(setState({view:'compare',run:d.compareRun,compare:[d.compareRun]}));
    else if (d.compareSlot) { pickerSlot=d.compareSlot; document.getElementById('picker-search').focus(); }
    else if (d.modelHistory) fire(setState({view:'model-history',model:d.modelHistory,line:''}));
    else if (d.lineRuns) { filters.line=d.lineRuns; fire(show('runs')); }
    else if (d.line) fire(setState({view:'lines',line:d.line,model:''}));
    else if (d.focus) { state.focus=d.focus; state.view='map'; if (d.mapLine) state.line=d.focus; state.mapColumn=columnKinds.findIndex((_,i) => inColumn(nodes.get(d.focus) || {},i)); state.mapColumn=Math.max(0,state.mapColumn); writeURL(); fire(render()); }
    else if (d.clearFocus !== undefined) fire(setState({focus:'',view:'map'}));
    else if (d.mapColumn !== undefined) { state.mapColumn=Number(d.mapColumn); const phone=document.getElementById('phone-map'); if (matchMedia('(min-width:651px)').matches) { phone.style.display='block'; document.getElementById('map-board').style.display='none'; } renderMapBody(); }
    else if (d.fact !== undefined) { state.fact=Number(d.fact); const card=cards.get(d.card); const panel=document.getElementById('fact-panel'); if (panel && card) panel.innerHTML=factPanel(card,state.fact); }
    else if (d.record !== undefined) { const card=cards.get(d.card), row=card?.records?.[Number(d.record)], panel=document.getElementById('record-panel'); if (row && panel) panel.innerHTML=`<h4>Stored record ${Number(d.record)+1}</h4><dl>${Object.entries(row).map(([key,leaf]) => `<dt>${esc(key.replaceAll('_',' '))}</dt><dd>${leafText(leaf)}${source(leaf)}</dd>`).join('')}</dl>${dataLink(card)}`; }
    else if (d.learning) fire(setState({view:'learn',learning:d.learning}));
    else if (d.view) { if (d.resetLine !== undefined) state.line=''; fire(show(d.view)); }
    else if (button.id === 'animate-wiring') { const active=button.getAttribute('aria-pressed') !== 'true'; button.setAttribute('aria-pressed',String(active)); button.textContent=active ? 'Pause the diagram' : 'Animate the diagram'; document.getElementById('wiring-diagram').classList.toggle('animating',active); }
    else if (button.id === 'show-3d') { button.setAttribute('aria-pressed','true'); document.getElementById('show-2d').setAttribute('aria-pressed','false'); fire(enhanceModel().catch(error => { document.getElementById('model-status').textContent=error.message+' The recorded 2D view remains available.'; document.getElementById('show-3d').setAttribute('aria-pressed','false'); document.getElementById('show-2d').setAttribute('aria-pressed','true'); document.getElementById('tower').hidden=true; document.getElementById('tower-fallback').hidden=false; })); }
    else if (button.id === 'show-2d') { window.LabModel?.stop(); document.getElementById('tower').hidden=true; document.getElementById('tower-fallback').hidden=false; button.setAttribute('aria-pressed','true'); document.getElementById('show-3d').setAttribute('aria-pressed','false'); }
  });
  document.addEventListener('input',event => {
    const e=event.target;
    if (e.id === 'run-search') { filters.query=e.value; renderRunList(); }
    else if (e.id === 'picker-search') pickerResults(e.value);
    else if (e.id === 'map-search') { mapQuery=e.value; renderMapBody(); }
    else if (e.id === 'training-step') drawTraining(cards.get(state.run),Number(e.value));
    else if (e.id === 'event-step') eventReadout(cards.get(state.run),Number(e.value));
  });
  document.addEventListener('keydown',event => {
    const search=event.target; if (search.id !== 'picker-search') return;
    const target=document.getElementById('picker-results');
    if (event.key === 'Escape') {
      event.preventDefault(); search.value=''; target.innerHTML=''; search.removeAttribute('aria-activedescendant'); search.setAttribute('aria-expanded','false'); return;
    }
    if (!['ArrowDown','ArrowUp','Enter'].includes(event.key)) return;
    event.preventDefault();
    if (!target.querySelectorAll('[data-pick-run]').length && event.key !== 'Enter') pickerResults(search.value);
    const options=[...target.querySelectorAll('[data-pick-run]')];
    if (!options.length) return;
    const active=options.findIndex(option => option.id === search.getAttribute('aria-activedescendant'));
    if (event.key === 'Enter') {
      if (active < 0) return;
      if (state.view === 'compare') fire(chooseCompare(options[active].dataset.pickRun));
      else fire(chooseRun(options[active].dataset.pickRun,'model'));
      return;
    }
    const next=active < 0 ? event.key === 'ArrowDown' ? 0 : options.length-1 : (active + (event.key === 'ArrowDown' ? 1 : -1) + options.length) % options.length;
    options.forEach((option,i) => option.setAttribute('aria-selected',String(i === next)));
    search.setAttribute('aria-activedescendant',options[next].id); options[next].scrollIntoView({block:'nearest'});
  });
  document.addEventListener('focusin',event => { if (event.target.id === 'picker-search') pickerResults(event.target.value); });
  document.addEventListener('change',event => {
    const e=event.target;
    const filterNames={'era-filter':'era','model-filter':'model','line-filter':'line','label-filter':'label','date-filter':'date'};
    if (filterNames[e.id]) { filters[filterNames[e.id]]=e.value; renderRunList(); }
    else if (e.id === 'map-preset') { if (e.value === 'running') { const q=(lab.queue || []).find(x => /RUNNING/.test(x.status)); const node=graph.nodes.find(x => x.node_id.includes(q?.name) || x.label === q?.name); fire(setState({focus:node?.node_id || '',view:'map'})); } else fire(setState({focus:e.value,view:'map'})); }
    else if (e.id === 'layer-pick') { const card=cards.get(state.run); document.getElementById('parts-diagram').innerHTML=parts(card,Number(e.value)); window.LabModel?.selectLayer(Number(e.value)); }
    else if (e.id === 'learn-era') fire(setState({learnEra:e.value,view:'learn'}));
  });
  document.querySelectorAll('.top-nav button').forEach((button,i,buttons) => button.addEventListener('keydown',e => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); buttons[(i+(e.key === 'ArrowRight' ? 1 : -1)+buttons.length)%buttons.length].focus(); } }));
  window.addEventListener('hashchange',() => { state=readURL(); fire(render()); });
  window.addEventListener('resize',() => { if (state.view === 'map') drawMapEdges(); const card=cards.get(state.run); if (card?.training) drawTraining(card,Number(document.getElementById('training-step')?.value || 0)); });
  window.LabView={ setState, getState:() => JSON.parse(JSON.stringify(state)), loadCard, ensureIndex, compare:(a,b) => setState({view:'compare',compare:[typeof a === 'string' ? a : a.card_id,typeof b === 'string' ? b : b.card_id]}), show };
  state=readURL(); renderStatus(); fire(render());
})();
