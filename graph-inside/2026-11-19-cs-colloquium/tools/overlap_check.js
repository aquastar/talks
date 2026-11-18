// Overlap check for every main slide with all fragments shown.
// Reports text overlapping text, and text crossed by a straight line or a path.
// usage: NODE_PATH=$(npm root -g) node tools/overlap_check.js [slide numbers comma separated]
const {chromium}=require('playwright');const path=require('path');
const RV='/tmp/claude-0/rv/node_modules/reveal.js/';
(async()=>{const only=process.argv[2]?process.argv[2].split(',').map(Number):null;
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:660}});
await p.route('**/*',r=>{const u=r.request().url();if(u.includes('cdnjs.cloudflare.com/ajax/libs/reveal.js')){let f=u.split('/5.1.0/')[1].replace('.min.','.');if(f==='reveal.css')f='dist/reveal.css';else if(f==='reveal.js')f='dist/reveal.js';else if(f.startsWith('theme/'))f='dist/'+f;return r.fulfill({path:RV+f});}if(u.startsWith('file://'))return r.continue();return r.abort();});
await p.goto('file://'+path.resolve(__dirname,'..','index.html'));await p.waitForFunction(()=>window.Reveal&&Reveal.isReady());
const n=await p.evaluate(()=>Reveal.getHorizontalSlides().length);let total=0;
for(let h=0;h<n;h++){if(only&&!only.includes(h+1))continue;
 await p.evaluate(h=>{Reveal.slide(h,0);let i=0;while(Reveal.nextFragment()&&i<20)i++;},h);await p.waitForTimeout(2600);
 const issues=await p.evaluate(()=>{
  const sec=Reveal.getCurrentSlide();const vis=e=>{let x=e;while(x&&x!==sec){const cs=getComputedStyle(x);if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)<0.2)return false;x=x.parentElement;}return true;};
  const shrink=(r,d)=>({l:r.left+d,r:r.right-d,t:r.top+d,b:r.bottom-d});
  const T=[...sec.querySelectorAll('svg text')].filter(e=>e.textContent.trim()&&vis(e)).map(e=>({e,r:shrink(e.getBoundingClientRect(),1.5),s:e.textContent.trim().slice(0,40)}));
  const hit=(a,b)=>a.l<b.r&&b.l<a.r&&a.t<b.b&&b.t<a.b;const out=[];
  for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++){if(T[i].e.contains(T[j].e)||T[j].e.contains(T[i].e))continue;if(hit(T[i].r,T[j].r))out.push('text/text: "'+T[i].s+'" x "'+T[j].s+'"');}
  const G=[...sec.querySelectorAll('svg line, svg path, svg polyline')].filter(e=>vis(e)&&e.getAttribute('stroke')&&e.getAttribute('stroke')!=='none'&&!e.closest('marker')&&!e.closest('defs'));
  for(const g of G){let len=0;try{len=g.getTotalLength();}catch(e){continue;}if(!len||len>4000)continue;const m=g.getScreenCTM();if(!m)continue;
   const step=Math.max(2,len/300);for(const t of T){const r=t.r;let crossed=false;
    for(let s=0;s<=len;s+=step){const q=g.getPointAtLength(s);const x=m.a*q.x+m.c*q.y+m.e,y=m.b*q.x+m.d*q.y+m.f;if(x>r.l+1&&x<r.r-1&&y>r.t+2&&y<r.b-2){crossed=true;break;}}
    if(crossed)out.push('line/text: <'+g.tagName+'> crosses "'+t.s+'"');}}
  return [...new Set(out)];});
 if(issues.length){total+=issues.length;console.log('slide',h+1);issues.forEach(x=>console.log('  ',x));}}
console.log('total',total);await b.close();})();
