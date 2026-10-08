/* Classic-script enhancement. All text remains measurable HTML over the canvas. */
(() => {
  'use strict';
  let THREE, OrbitControls, dependencies, renderer, controls, frame, resizeObserver;
  let scene, camera, objects, card, host, labelHost, tooltip, selectedLayer=0, epoch=0;
  const labels=[], pickable=[], selectedParts=[];
  let partLayer=0;
  const value=x => x && typeof x === 'object' && Object.hasOwn(x,'value') ? x.value : x;
  const finite=x => typeof x === 'number' && Number.isFinite(x);
  const fmt=x => finite(x) ? x.toLocaleString('en-US',{maximumFractionDigits:3}) : 'not recorded';
  const escape=x => String(x ?? '').replace(/[&<>"']/g,c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function status(message) {
    const node=document.getElementById('model-status');
    if (node) node.textContent=message;
  }
  function fallback(message) {
    if (host) host.hidden=true;
    const flat=document.getElementById('tower-fallback'); if (flat) flat.hidden=false;
    status(message+' The recorded 2D view remains available.');
  }
  function stop() {
    epoch++;
    if (frame) cancelAnimationFrame(frame);
    frame=null;
    resizeObserver?.disconnect(); resizeObserver=null;
    controls?.dispose(); controls=null;
    if (objects) objects.traverse(object => { object.geometry?.dispose(); if (Array.isArray(object.material)) object.material.forEach(m => m.dispose()); else object.material?.dispose(); });
    renderer?.dispose(); renderer=null;
    labels.length=0; pickable.length=0; selectedParts.length=0;
  }
  async function load() {
    if (!dependencies) dependencies=Promise.all([
      import('https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js'),
      import('https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js')
    ]).then(([three,orbit]) => { THREE=three; OrbitControls=orbit.OrbitControls; });
    return dependencies;
  }
  function label(text,position,layer,priority=false,part=false) {
    const element=document.createElement('span'); element.className='tower-label'; element.textContent=text;
    labelHost.append(element); labels.push({element,position,layer,priority,part});
  }
  function box(width,height,depth,x,y,z,colour,layer) {
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(width,height,depth),new THREE.MeshPhongMaterial({color:colour}));
    mesh.position.set(x,y,z); mesh.userData.layer=layer; objects.add(mesh);
    if (Number.isInteger(layer)) pickable.push(mesh);
    return mesh;
  }
  function outline(width,height,depth,x,y,z) {
    const geometry=new THREE.EdgesGeometry(new THREE.BoxGeometry(width,height,depth));
    const lines=new THREE.LineSegments(geometry,new THREE.LineBasicMaterial({color:0xffce88}));
    lines.position.set(x,y,z); objects.add(lines); return lines;
  }
  function build() {
    const count=value(card.parts.structure.layers), maximum=value(card.scale?.max), rowMap=new Map((card.per_layer || []).map(r => [r.layer,r]));
    const step=.42, bottom=-(count-1)*step/2;
    for (let layer=0;layer<count;layer++) {
      const row=rowMap.get(layer), written=value(row?.written) === true && finite(value(row?.write_size)), configured=value(row?.configured) === true, y=bottom+layer*step;
      const slab=box(4.3,.12,2.1,0,y,0,0x526785,layer);
      // The small last box is the recorded written module, separate from attention.
      box(.8,.17,1.95,1.65,y,0,written ? 0xa67ec9 : 0x526785,layer);
      if (configured) outline(4.5,.24,2.3,0,y,0);
      label('Layer '+layer,new THREE.Vector3(-2.6,y,0),layer);
      if (written) {
        const size=value(row.write_size);
        if (finite(maximum) && maximum > 0) {
          const length=Math.max(.008,size/maximum*3.3);
          box(length,.13,.2,2.7+length/2,y,0,0xd7b4ff,layer);
        }
        label(fmt(size)+' · written',new THREE.Vector3(2.55,y,.15),layer,true);
      }
      slab.userData.written=written;
    }
    const y=bottom+selectedLayer*step;
    const selected=(card.per_layer || []).find(r => r.layer === selectedLayer), written=value(selected?.written) === true;
    selectedParts.push(box(1.3,.4,.8,-3.8,y,1,0x718ab0,selectedLayer),box(1.6,.4,.8,0,y,2.2,0x718ab0,selectedLayer),box(1.2,.4,.8,2.5,y,2.2,written ? 0xa67ec9 : 0x718ab0,selectedLayer),outline(1.3,.4,.8,-3.8,y,1));
    partLayer=selectedLayer;
    label('Attention · q/k/v/o',new THREE.Vector3(-3.8,y+.4,1),selectedLayer,true,true);
    label('MLP · gate × up',new THREE.Vector3(0,y+.4,2.2),selectedLayer,true,true);
    label(written ? 'down_proj · written' : 'down_proj · no recorded write',new THREE.Vector3(2.5,y+.4,2.2),selectedLayer,true,true);
    const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-1.3,bottom-.5,0),new THREE.Vector3(-1.3,-bottom+.7,0)]),new THREE.LineBasicMaterial({color:0xb9c6ff})); objects.add(line);
    label('Main line · static wiring',new THREE.Vector3(-1.3,-bottom+.9,0),selectedLayer,true);
  }
  function resize() {
    if (!renderer || !host || !host.isConnected) return;
    const width=host.clientWidth, height=host.clientHeight;
    if (!width || !height) return;
    renderer.setSize(width,height,false); camera.aspect=width/height; camera.updateProjectionMatrix();
  }
  function placeLabels() {
    const width=host.clientWidth, height=host.clientHeight, rows=[];
    const stride=Math.max(height < 300 ? 4 : 1,Math.ceil(value(card.parts.structure.layers)*20/height));
    labels.forEach(entry => {
      const point=entry.position.clone().applyMatrix4(objects.matrixWorld).project(camera);
      const visible=point.z > -1 && point.z < 1 && !(height < 300 && entry.part) && (entry.priority || entry.layer === selectedLayer || entry.layer%stride === 0);
      const x=(point.x+1)*width/2, y=(1-point.y)*height/2;
      entry.element.hidden=!visible || x < 0 || x > width-80 || y < 0 || y > height-22;
      if (!entry.element.hidden) { entry.element.style.left=Math.round(x)+'px'; entry.element.style.top=Math.round(y)+'px'; rows.push(entry); }
    });
  }
  function selectLayer(layer) {
    selectedLayer=layer;
    if (!renderer) return;
    const assigned=(card.per_fact || []).filter(f => value(f.assigned_layer) === layer);
    const row=(card.per_layer || []).find(r => r.layer === layer);
    const shift=(layer-partLayer)*.42;
    selectedParts.forEach(object => { object.position.y+=shift; object.userData.layer=layer; });
    labels.filter(entry => entry.part).forEach(entry => { entry.position.y+=shift; entry.layer=layer; if (entry.element.textContent.startsWith('down_proj')) entry.element.textContent=value(row?.written) === true ? 'down_proj · written' : 'down_proj · no recorded write'; });
    selectedParts[2]?.material.color.setHex(value(row?.written) === true ? 0xa67ec9 : 0x718ab0);
    partLayer=layer;
    const words=assigned.map(f => `${value(f.subject)} → ${value(f.answer)}`).join('; ');
    tooltip.innerHTML=`<strong>Layer ${layer}</strong> · ${value(row?.written) === true ? fmt(value(row.write_size))+' '+escape(row.unit || card.scale?.unit)+' · written' : 'no recorded write'}<span class="tower-compact-label"> · static diagram; assigned facts</span>${words ? '<p>'+escape(words)+'</p>' : '<p>Fact assignment not recorded for this layer.</p>'}<p>Static diagram; words are assigned facts, not the layer’s thoughts.</p>`;
    const select=document.getElementById('layer-pick'); if (select) select.value=String(layer);
  }
  async function start(nextCard) {
    stop(); const token=epoch;
    card=nextCard; host=document.getElementById('tower');
    const count=value(card.parts?.structure?.layers);
    if (!host || !Number.isInteger(count) || count < 1) { fallback('Model layer count was not recorded for this run.'); return; }
    status('Loading the optional pinned 3D structure; the recorded 2D view remains available.');
    try {
      await load(); if (token !== epoch || !host?.isConnected) return;
      renderer=new THREE.WebGLRenderer({antialias:true,alpha:false}); renderer.setPixelRatio(Math.min(devicePixelRatio,2)); renderer.setClearColor(0x111a29);
      host.replaceChildren(renderer.domElement);
      labelHost=document.createElement('div'); labelHost.className='tower-labels'; host.append(labelHost);
      tooltip=document.createElement('div'); tooltip.className='tower-tooltip'; host.append(tooltip);
      host.hidden=false; document.getElementById('tower-fallback').hidden=true;
      scene=new THREE.Scene(); camera=new THREE.PerspectiveCamera(38,1,.1,180);
      scene.add(new THREE.AmbientLight(0xffffff,2)); const light=new THREE.DirectionalLight(0xffffff,2.8); light.position.set(8,15,12); scene.add(light);
      objects=new THREE.Group(); scene.add(objects);
      selectedLayer=Number(document.getElementById('layer-pick')?.value || 0);
      build(); camera.position.set(13,3,Math.max(23,count*.8));
      controls=new OrbitControls(camera,renderer.domElement); controls.target.set(0,0,0); controls.enableDamping=true;
      resizeObserver=new ResizeObserver(resize); resizeObserver.observe(host); resize();
      renderer.domElement.addEventListener('webglcontextlost',event => { event.preventDefault(); stop(); fallback('WebGL context was lost.'); });
      const ray=new THREE.Raycaster(), pointer=new THREE.Vector2();
      renderer.domElement.addEventListener('pointermove',event => {
        const rect=renderer.domElement.getBoundingClientRect(); pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);
        ray.setFromCamera(pointer,camera); const hit=ray.intersectObjects(pickable)[0]; if (hit) selectLayer(hit.object.userData.layer);
      });
      selectLayer(selectedLayer);
      status('3D static structure · drag to rotate; pinch to zoom. Numbers use the recorded shared ruler. Diagram, not recorded activity.');
      const draw=() => { if (!host?.isConnected || token !== epoch || !renderer) return; frame=requestAnimationFrame(draw); controls.update(); objects.updateMatrixWorld(); renderer.render(scene,camera); placeLabels(); };
      draw();
    } catch (error) { stop(); fallback('3D unavailable (WebGL or CDN): '+error.message); }
  }
  window.LabModel={start,stop,selectLayer};
})();
