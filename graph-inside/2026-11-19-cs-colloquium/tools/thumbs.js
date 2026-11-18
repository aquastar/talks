// Regenerate thumbs/NN.png, the pictures in the Esc grid. Run after every change to the slides.
// usage: NODE_PATH=$(npm root -g) node tools/thumbs.js
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
const RV='/tmp/claude-0/rv/node_modules/reveal.js/';const THREE='/tmp/claude-0/rv/node_modules/three/build/three.min.js';
(async()=>{const dir=path.resolve(__dirname,'..');const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:660}});
await p.route('**/*',r=>{const u=r.request().url();
 if(u.includes('cdnjs.cloudflare.com/ajax/libs/reveal.js')&&fs.existsSync(RV)){let f=u.split('/5.1.0/')[1].replace('.min.','.');if(f==='reveal.css')f='dist/reveal.css';else if(f==='reveal.js')f='dist/reveal.js';else if(f.startsWith('theme/'))f='dist/'+f;return r.fulfill({path:RV+f});}
 if(u.includes('cdnjs.cloudflare.com/ajax/libs/three.js')&&fs.existsSync(THREE))return r.fulfill({path:THREE});
 return r.continue();});
await p.goto('file://'+dir+'/index.html?thumbs=1');await p.waitForFunction(()=>window.Reveal&&Reveal.isReady());
const n=await p.evaluate(()=>Reveal.getHorizontalSlides().length);
for(let h=0;h<n;h++){await p.evaluate(h=>{Reveal.slide(h,0);let i=0;while(Reveal.nextFragment()&&i<20)i++;},h);
 const demo=await p.evaluate(()=>!!Reveal.getCurrentSlide().getAttribute('data-background-iframe'));await p.waitForTimeout(demo?6000:2600);
 await p.screenshot({path:path.join(dir,'thumbs',String(h).padStart(2,'0')+'.png')});}
for(const f of fs.readdirSync(path.join(dir,'thumbs'))){const k=parseInt(f);if(!isNaN(k)&&k>=n)fs.unlinkSync(path.join(dir,'thumbs',f));}
console.log('thumbs',n,'(resize to 400 px wide with: python3 tools/thumbs_resize.py)');await b.close();})();
