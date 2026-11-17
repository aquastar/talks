// Render every slide at 1280x720 and run the layout gate.
// Fails (exit 1) on a main slide with: overflow past the reference line or slide edge, text overlap,
// more than one orange item, underfilled layout, SVG text under 16 px. Prints small figures.
// Writes OUT/sNN.png screenshots and OUT/imgboxes.json for the pixel palette check.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const OUT = process.env.OUT;
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto('file://' + __dirname + '/../index.html');
  await p.waitForTimeout(1500);
  const n = await p.evaluate(() => Reveal.getTotalSlides());
  const fails = [], notes = [], boxes = {};
  for (let i = 0; i < n; i++) {
    await p.evaluate(i => { Reveal.slide(i); Reveal.getCurrentSlide().querySelectorAll('.fragment').forEach(f => f.classList.add('visible')); }, i);
    await p.waitForTimeout(i === 0 ? 2500 : 300);
    if (OUT) await p.screenshot({ path: `${OUT}/s${String(i).padStart(2, '0')}.png` });
    const r = await p.evaluate(() => {
      const s = Reveal.getCurrentSlide(), sb = s.getBoundingClientRect();
      const main = !s.dataset.backup;
      const ref = s.querySelector('.ref');
      const lim = ref ? ref.getBoundingClientRect().top - 8 : sb.top + 700;
      const out = { main, fail: [], note: [], imgs: [] };
      const vis = e => !e.closest('aside') && e.getBoundingClientRect().height > 0;
      // overflow
      s.querySelectorAll('h2,p,li,img,svg,.people,.photos,iframe,.audio-row,table,.gallery').forEach(e => {
        if (!vis(e) || e.closest('.ref') || e.closest('.fullbleed') || (e.tagName === 'svg' && e.closest('svg') !== e)) return;
        const q = e.getBoundingClientRect();
        if (q.bottom > lim + 0.5 || q.right > sb.left + 1280 - 20 || q.left < sb.left + 20) out.fail.push(`overflow ${e.tagName} bottom ${Math.round(q.bottom - sb.top)} right ${Math.round(q.right - sb.left)}`);
      });
      // text overlap
      const els = [...s.querySelectorAll('h2,p,li,figcaption,svg text,.audio-row span,.ref,.status')].filter(vis);
      const R = els.map(e => e.getBoundingClientRect());
      for (let a = 0; a < R.length; a++) for (let c = a + 1; c < R.length; c++) {
        if (els[a].contains(els[c]) || els[c].contains(els[a])) continue;
        const x = Math.min(R[a].right, R[c].right) - Math.max(R[a].left, R[c].left), y = Math.min(R[a].bottom, R[c].bottom) - Math.max(R[a].top, R[c].top);
        if (x > 3 && y > 3) out.fail.push(`overlap "${els[a].textContent.trim().slice(0, 22)}" / "${els[c].textContent.trim().slice(0, 22)}"`);
      }
      // orange items: every orange element counts, a <g data-accent> counts once
      const OR = ['rgb(247, 105, 2)', 'rgb(196, 82, 0)'];
      const isOr = v => v && OR.includes(v);
      let orange = 0; const groups = new Set();
      s.querySelectorAll('*').forEach(e => {
        if (e.closest('aside') || e.closest('.ref') || e.closest('marker') || e.closest('iframe')) return;
        const cs = getComputedStyle(e);
        const svgEl = e.closest('svg');
        let hit;
        if (svgEl) hit = (isOr(cs.fill) && e.tagName !== 'svg' && e.tagName !== 'g') || (isOr(cs.stroke) && cs.stroke !== 'none' && e.tagName !== 'g' && e.tagName !== 'svg');
        else {
          const bb = cs.borderBottomStyle !== 'none' && parseFloat(cs.borderBottomWidth) > 0 && isOr(cs.borderBottomColor);
          const bg = isOr(cs.backgroundColor);
          const tx = isOr(cs.color) && [...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim());
          const be = getComputedStyle(e, '::before');
          const pb = be.content && be.content !== 'none' && parseFloat(be.borderBottomWidth) > 0 && be.borderBottomStyle !== 'none' && isOr(be.borderBottomColor);
          hit = bb || bg || tx || pb;
        }
        if (!hit) return;
        const g = e.closest('[data-accent]');
        if (g) groups.add(g); else orange++;
      });
      orange += groups.size;
      if (orange > 1) out.fail.push(`orange items ${orange}`);
      // fill, small text, figure size
      const sparse = s.classList.contains('breath') || s.querySelector('.thesis') || s.classList.contains('cover') || s.dataset.sparse;
      let low = 0, bigfig = 0;
      s.querySelectorAll('h2,p,li,img,svg,.people,.photos,iframe,.audio-row,table,.gallery').forEach(e => {
        if (!vis(e) || e.closest('.ref')) return; const q = e.getBoundingClientRect(); low = Math.max(low, q.bottom - sb.top);
        if ((e.tagName === 'IMG' || (e.tagName === 'svg' && e.classList.contains('fig')) || e.tagName === 'IFRAME')) bigfig = Math.max(bigfig, q.height);
      });
      if (!sparse && low < 470) out.fail.push(`underfilled, content ends at y ${Math.round(low)}`);
      if (!sparse && bigfig && bigfig < 380) out.note.push(`small figure ${Math.round(bigfig)} px`);
      s.querySelectorAll('svg text').forEach(t => { if (!vis(t)) return; const h = parseFloat(getComputedStyle(t).fontSize) * (t.getScreenCTM ? t.getScreenCTM().a : 1); if (h < 15.5) out.fail.push(`small svg text ${h.toFixed(1)} px "${t.textContent.slice(0, 20)}"`); });
      s.querySelectorAll('img').forEach(im => { if (!vis(im) || im.closest('.people')) return; const q = im.getBoundingClientRect();
        out.imgs.push({ src: im.getAttribute('src'), x: q.left - sb.left, y: q.top - sb.top, w: q.width, h: q.height, exempt: im.classList.contains('photo') || im.classList.contains('ph') || im.hasAttribute('data-evidence') }); });
      return out;
    });
    boxes[i] = r.imgs;
    const uniq = [...new Set(r.fail)].slice(0, 6);
    if (uniq.length) (r.main ? fails : notes).push(`slide ${i}${r.main ? '' : ' (backup)'}: ${uniq.join(' | ')}`);
    if (r.note.length && r.main) notes.push(`slide ${i}: ${r.note.join(' | ')}`);
  }
  if (OUT) fs.writeFileSync(`${OUT}/imgboxes.json`, JSON.stringify(boxes));
  if (notes.length) console.log('notes:\n  ' + notes.join('\n  '));
  if (fails.length) { console.log('GATE FAIL:\n  ' + fails.join('\n  ')); await b.close(); process.exit(1); }
  console.log('gate: pass');
  await b.close();
})();
