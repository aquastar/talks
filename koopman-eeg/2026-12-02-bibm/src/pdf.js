// Render every slide (all fragments shown) at 2x and write OUT/deck.pdf via Chromium screenshots.
const { chromium } = require('playwright');
(async () => {
  const OUT = process.env.OUT; const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/../index.html'); await p.waitForTimeout(1500);
  const n = await p.evaluate(() => Reveal.getTotalSlides());
  for (let i = 0; i < n; i++) {
    await p.evaluate(i => { Reveal.slide(i); Reveal.getCurrentSlide().querySelectorAll('.fragment').forEach(f => f.classList.add('visible')); document.querySelector('.controls').style.display='none'; }, i);
    await p.waitForTimeout(i === 0 ? 5200 : 300);
    await p.screenshot({ path: `${OUT}/p${String(i).padStart(2, '0')}.png` });
  }
  await b.close();
})();
