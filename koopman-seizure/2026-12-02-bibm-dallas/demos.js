/* Live demos for the KSNet BIBM 2026 talk. Plain canvas, no libraries.
   Each <div class="demo" data-demo="NAME"> gets a canvas. Demos start when their slide is shown,
   stop when it is left, and advance with the slide's fragments (Reveal fragment index).
   Pure math lives in DM (testable without a browser). */
(function (root) {
  'use strict';
  var DM = {};
  // ---------- math ----------
  DM.rng = function (seed) { // mulberry32
    var a = seed >>> 0;
    return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  };
  DM.gauss = function (r) { var u = 1 - r(), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
  DM.solve = function (A, b) { // Gaussian elimination with partial pivoting, A is n x n (copied)
    var n = b.length, M = A.map(function (r, i) { return r.slice().concat([b[i]]); });
    for (var c = 0; c < n; c++) {
      var p = c; for (var r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      var t = M[c]; M[c] = M[p]; M[p] = t;
      for (r = c + 1; r < n; r++) { var f = M[r][c] / M[c][c]; for (var k = c; k <= n; k++) M[r][k] -= f * M[c][k]; }
    }
    var x = new Array(n);
    for (r = n - 1; r >= 0; r--) { var s = M[r][n]; for (k = r + 1; k < n; k++) s -= M[r][k] * x[k]; x[r] = s / M[r][r]; }
    return x;
  };
  // delay embedded DMD with identity observables = AR(m) fit, x[k+m] = sum a_i x[k+i]
  DM.arfit = function (seg, m, ridge) {
    var n = seg.length, mu = 0, sd = 0, i, j, k;
    for (i = 0; i < n; i++) mu += seg[i]; mu /= n;
    for (i = 0; i < n; i++) sd += (seg[i] - mu) * (seg[i] - mu); sd = Math.sqrt(sd / n) + 1e-9;
    var z = seg.map(function (v) { return (v - mu) / sd; });
    var G = [], h = new Array(m).fill(0);
    for (i = 0; i < m; i++) G.push(new Array(m).fill(0));
    for (k = 0; k + m < n; k++) {
      for (i = 0; i < m; i++) { h[i] += z[k + i] * z[k + m]; for (j = 0; j < m; j++) G[i][j] += z[k + i] * z[k + j]; }
    }
    for (i = 0; i < m; i++) G[i][i] += ridge * (n - m);
    return DM.solve(G, h);
  };
  // roots of z^m - a_{m-1} z^{m-1} - ... - a_0 by Durand Kerner, complex as [re, im]
  DM.roots = function (a) {
    var m = a.length, i, j, it;
    var c = []; for (i = 0; i < m; i++) c.push(-a[i]); // monic poly coeffs c_0..c_{m-1}, leading 1
    function ev(re, im) { // Horner
      var pr = 1, pi = 0;
      for (var k = m - 1; k >= 0; k--) { var nr = pr * re - pi * im + c[k], ni = pr * im + pi * re; pr = nr; pi = ni; }
      return [pr, pi];
    }
    var z = []; for (i = 0; i < m; i++) { var ang = 2 * Math.PI * i / m + 0.4; z.push([0.9 * Math.cos(ang), 0.9 * Math.sin(ang)]); }
    for (it = 0; it < 300; it++) {
      var delta = 0;
      for (i = 0; i < m; i++) {
        var num = ev(z[i][0], z[i][1]), dr = 1, di = 0;
        for (j = 0; j < m; j++) if (j !== i) { var er = z[i][0] - z[j][0], ei = z[i][1] - z[j][1], nr = dr * er - di * ei, ni = dr * ei + di * er; dr = nr; di = ni; }
        var den = dr * dr + di * di + 1e-30, qr = (num[0] * dr + num[1] * di) / den, qi = (num[1] * dr - num[0] * di) / den;
        z[i] = [z[i][0] - qr, z[i][1] - qi]; delta = Math.max(delta, Math.abs(qr) + Math.abs(qi));
      }
      if (delta < 1e-12) break;
    }
    return z;
  };
  // frequency (Hz) of the AR spectral peak between f0 and f1, and the pole closest to it
  DM.peak = function (a, poles, fs, f0, f1) {
    var m = a.length, best = -1, bf = f0;
    for (var f = f0; f <= f1; f += 0.1) {
      var w = 2 * Math.PI * f / fs, re = Math.cos(m * w), im = Math.sin(m * w);
      for (var i = 0; i < m; i++) { re -= a[i] * Math.cos(i * w); im -= a[i] * Math.sin(i * w); }
      var s = 1 / (re * re + im * im); if (s > best) { best = s; bf = f; }
    }
    var wt = 2 * Math.PI * bf / fs, bi = 0, bd = 1e9;
    poles.forEach(function (p, i) { var d = Math.abs(Math.abs(Math.atan2(p[1], p[0])) - wt); if (d < bd) { bd = d; bi = i; } });
    return { f: bf, i: bi, r: Math.hypot(poles[bi][0], poles[bi][1]) };
  };
  DM.auc = function (scores, labels) { // Mann Whitney with ties
    var idx = scores.map(function (s, i) { return i; }).sort(function (p, q) { return scores[p] - scores[q]; });
    var ranks = new Array(scores.length), i = 0;
    while (i < idx.length) { var j = i; while (j + 1 < idx.length && scores[idx[j + 1]] === scores[idx[i]]) j++; for (var k = i; k <= j; k++) ranks[idx[k]] = (i + j) / 2 + 1; i = j + 1; }
    var np = 0, nn = 0, rs = 0; labels.forEach(function (l, i) { if (l) { np++; rs += ranks[i]; } else nn++; });
    return np && nn ? (rs - np * (np + 1) / 2) / (np * nn) : 0.5;
  };
  // ---- leakage simulation: 4 days of 5 min segments, seizures at night, model sees only the clock ----
  DM.leakSim = function () {
    var r = DM.rng(7), seg = 5, n = 4 * 24 * 60 / seg, onsets = [], i;
    var plan = [[0, 3.1], [0, 22.5], [1, 4.2], [1, 21.0], [2, 2.4], [2, 23.2], [3, 3.6], [3, 20.5]]; // day, hour
    plan.forEach(function (p) { onsets.push(Math.round((p[0] * 24 + p[1] + 0.3 * DM.gauss(r)) * 60 / seg)); });
    onsets.sort(function (a, b) { return a - b; });
    function labelsFor(on) { var L = new Array(n).fill(0); on.forEach(function (o) { for (var k = o - 6; k < o; k++) if (k >= 0) L[k] = 1; }); return L; }
    var lab = labelsFor(onsets);
    var t = []; for (i = 0; i < n; i++) t.push(i);
    var tod = t.map(function (k) { return (k * seg / 60) % 24; });
    function knn(trainIdx, testIdx, dist, K, L) {
      return testIdx.map(function (q) {
        var d = trainIdx.map(function (p) { return [dist(p, q), L[p]]; }).sort(function (x, y) { return x[0] - y[0]; });
        var s = 0; for (var k = 0; k < K; k++) s += d[k][1]; return s / K;
      });
    }
    var dAbs = function (p, q) { return Math.abs(p - q); };
    var dTod = function (p, q) { var x = Math.abs(tod[p] - tod[q]); return Math.min(x, 24 - x); };
    var all = t.slice(), rr = DM.rng(11), shuf = all.slice().sort(function () { return rr() - 0.5; });
    var nTest = Math.round(n * 0.2), testR = shuf.slice(0, nTest).sort(function (a, b) { return a - b; }), trainR = shuf.slice(nTest);
    var half = n / 2, trainP = t.filter(function (k) { return k < half; }), testP = t.filter(function (k) { return k >= half; });
    var res = {};
    var s1 = knn(trainR, testR, dAbs, 4, lab); res.random = { test: testR, score: s1, auc: DM.auc(s1, testR.map(function (k) { return lab[k]; })) };
    var s2 = knn(trainP, testP, dAbs, 12, lab); res.pastAbs = { test: testP, score: s2, auc: DM.auc(s2, testP.map(function (k) { return lab[k]; })) };
    var s3 = knn(trainP, testP, dTod, 24, lab); res.pastTod = { test: testP, score: s3, auc: DM.auc(s3, testP.map(function (k) { return lab[k]; })) };
    // fake onsets: test half onsets moved by whole days inside the test half (day 3 <-> day 4), clock of day kept
    var fake = onsets.map(function (o) { if (o < half) return o; var d = o < half + n / 4 ? n / 4 : -n / 4; return o + d; });
    var labF = labelsFor(fake);
    res.fake = { test: testP, score: s3, auc: DM.auc(s3, testP.map(function (k) { return labF[k]; })), onsets: fake, lab: labF };
    return { n: n, seg: seg, onsets: onsets, lab: lab, tod: tod, half: half, res: res };
  };
  root.DM = DM;

  if (typeof document === 'undefined') return;
  // ---------- drawing ----------
  var C = { bg: '#FBFAF7', ink: '#1F1E1B', ink2: '#5F5D50', axis: '#ACA39A', rule: '#D7D2CB', group: '#F1EDE7', acc: '#F76902', accT: '#C45200', tint: '#FAD6BA', slate: '#4C5B66', fail: '#DA291C' };
  var FONT = 'et-book, Georgia, serif';
  function canvasFor(el) {
    var w = el.clientWidth || parseInt(el.style.width), h = el.clientHeight || parseInt(el.style.height), dpr = 2;
    var cv = document.createElement('canvas'); cv.width = w * dpr; cv.height = h * dpr; cv.style.width = w + 'px'; cv.style.height = h + 'px';
    el.appendChild(cv); var g = cv.getContext('2d'); g.scale(dpr, dpr); return { cv: cv, g: g, w: w, h: h };
  }
  function txt(g, s, x, y, size, col, align, weight, italic) {
    g.font = (italic ? 'italic ' : '') + (weight || 400) + ' ' + size + 'px ' + FONT; g.fillStyle = col || C.ink; g.textAlign = align || 'left'; g.fillText(s, x, y);
  }
  function line(g, x1, y1, x2, y2, col, w, dash) { g.beginPath(); g.setLineDash(dash || []); g.strokeStyle = col; g.lineWidth = w || 1; g.moveTo(x1, y1); g.lineTo(x2, y2); g.stroke(); g.setLineDash([]); }
  function dot(g, x, y, r, col, alpha) { g.globalAlpha = alpha == null ? 1 : alpha; g.beginPath(); g.arc(x, y, r, 0, 2 * Math.PI); g.fillStyle = col; g.fill(); g.globalAlpha = 1; }
  function unitCircle(g, cx, cy, R) {
    line(g, cx - R - 16, cy, cx + R + 16, cy, C.rule, 1); line(g, cx, cy - R - 16, cx, cy + R + 16, C.rule, 1);
    g.beginPath(); g.arc(cx, cy, R, 0, 2 * Math.PI); g.strokeStyle = C.axis; g.lineWidth = 1.5; g.stroke();
    txt(g, '|λ| = 1', cx + R * 0.72 + 6, cy - R * 0.72 - 6, 14, C.ink2);
  }
  var REG = {};

  // ===== D1: sliding window DMD on real chb01 EEG =====
  REG.dmd = function (el) {
    var D = root.CHB01_T8P8, x = D.x, fs = D.fs, T = x.length / fs, onset = D.onset - D.t0;
    var c = canvasFor(el), g = c.g, W = c.w, H = c.h;
    var tx0 = 10, tx1 = 650, ty = 40, th = H - 200, cx = W - 190, cy = 40 + (H - 90) / 2 - 10, R = Math.min(150, (H - 120) / 2);
    var win = 4, m = 10, t = 0, playing = false, last = 0, raf = 0, trail = [], TRACK = [];
    for (var tt = 0; tt <= T - win; tt += 0.5) { var sg = x.slice(Math.round(tt * fs), Math.round(tt * fs) + win * fs), aa = DM.arfit(sg, m, 1e-2), pp = DM.roots(aa); TRACK.push([tt, DM.peak(aa, pp, fs, 0.5, 20).r]); }
    var btn = document.createElement('button'); btn.className = 'demo-btn'; btn.textContent = 'Pause'; btn.style.cssText = 'position:absolute;left:' + tx0 + 'px;bottom:6px';
    el.appendChild(btn);
    btn.onclick = function () { playing = !playing; btn.textContent = playing ? 'Pause' : 'Play'; if (playing) { last = 0; raf = requestAnimationFrame(loop); } };
    c.cv.addEventListener('click', function (e) { var r = c.cv.getBoundingClientRect(), px = (e.clientX - r.left) * (W / r.width); if (px >= tx0 && px <= tx1) { t = Math.max(0, Math.min(T - win, (px - tx0) / (tx1 - tx0) * T - win / 2)); trail = []; draw(); } });
    function X(s) { return tx0 + s / T * (tx1 - tx0); }
    function draw() {
      g.clearRect(0, 0, W, H);
      // trace
      var mid = ty + th / 2, sc = th / 2 / 260;
      g.fillStyle = C.group; g.fillRect(X(onset), ty - 8, tx1 - X(onset), th + 16);
      txt(g, 'seizure, as annotated', tx1 - 6, ty + 8, 14, C.accT, 'right');
      g.beginPath(); g.strokeStyle = C.ink2; g.lineWidth = 0.8;
      for (var i = 0; i < x.length; i++) { var px = X(i / fs), py = mid - Math.max(-260, Math.min(260, x[i])) * sc; if (i) g.lineTo(px, py); else g.moveTo(px, py); }
      g.stroke();
      line(g, X(onset), ty - 12, X(onset), ty + th + 12, C.acc, 2);
      var yT = ty + th + 34, hT = 70;
      line(g, tx0, yT + hT, tx1, yT + hT, C.axis, 1); txt(g, 'radius of the strongest rhythm, |λ|', tx0, yT - 6, 14, C.ink2);
      [0.8, 1.0].forEach(function (v) { var yy = yT + hT - (v - 0.75) / 0.27 * hT; line(g, tx0, yy, tx1, yy, C.rule, 1, [3, 3]); txt(g, v.toFixed(1), tx1 + 6, yy + 4, 13, C.ink2); });
      g.beginPath(); g.strokeStyle = C.acc; g.lineWidth = 1.8; var first = true;
      TRACK.forEach(function (q) { if (q[0] > t) return; var xx = X(q[0] + win / 2), yy = yT + hT - (Math.max(0.75, q[1]) - 0.75) / 0.27 * hT; if (first) { g.moveTo(xx, yy); first = false; } else g.lineTo(xx, yy); }); g.stroke();
      for (var s = -50; s <= 40; s += 10) { var xx = X(s + onset); line(g, xx, yT + hT, xx, yT + hT + 5, C.axis, 1); txt(g, (s > 0 ? '+' : s < 0 ? '\u2212' : '') + Math.abs(s) + ' s', xx, yT + hT + 21, 14, C.ink2, 'center'); }
      txt(g, 'chb01, file 03, channel T8 to P8, real recording', tx0, 18, 15, C.ink2);
      // window
      g.globalAlpha = 0.22; g.fillStyle = C.acc; g.fillRect(X(t), ty - 4, X(t + win) - X(t), th + 8); g.globalAlpha = 1;
      g.strokeStyle = C.acc; g.lineWidth = 1.5; g.strokeRect(X(t), ty - 4, X(t + win) - X(t), th + 8);
      // dmd
      var a0 = Math.round(t * fs), seg = x.slice(a0, a0 + win * fs);
      var a = DM.arfit(seg, m, 1e-2), poles = DM.roots(a), pk = DM.peak(a, poles, fs, 0.5, 20);
      trail.push(poles); if (trail.length > 10) trail.shift();
      unitCircle(g, cx, cy, R);
      trail.forEach(function (ps, k) { if (k < trail.length - 1) ps.forEach(function (p) { dot(g, cx + p[0] * R, cy - p[1] * R, 3, C.ink2, 0.08 + 0.03 * k); }); });
      poles.forEach(function (p, i) { dot(g, cx + p[0] * R, cy - p[1] * R, 5, C.ink2, 0.9); });
      var p = poles[pk.i]; dot(g, cx + p[0] * R, cy - p[1] * R, 8, C.acc); dot(g, cx + p[0] * R, cy + p[1] * R, 8, C.acc);
      var rel = t + win / 2 - onset;
      txt(g, 'eigenvalues of the window’s linear operator', cx, 18, 15, C.ink2, 'center');
      txt(g, (rel >= 0 ? '+' : '\u2212') + Math.abs(rel).toFixed(0) + ' s from onset', cx - R - 10, H - 34, 18, rel >= 0 ? C.accT : C.ink, 'left', 600);
      txt(g, 'strongest rhythm ' + pk.f.toFixed(1) + ' Hz,  |λ| = ' + pk.r.toFixed(2), cx - R - 10, H - 12, 16, C.ink2);
    }
    function loop(ts) {
      if (!playing) return;
      if (last) { t += (ts - last) / 1000 * 6; if (t > T - win) t = 0, trail = []; }
      last = ts; draw(); raf = requestAnimationFrame(loop);
    }
    return {
      start: function () { if (!playing) { playing = true; btn.textContent = 'Pause'; last = 0; raf = requestAnimationFrame(loop); } },
      stop: function () { playing = false; cancelAnimationFrame(raf); },
      step: function () {}, draw: draw
    };
  };

  // ===== D2: a clock that never sees EEG, under four tests =====
  REG.leak = function (el) {
    var S = DM.leakSim(), c = canvasFor(el), g = c.g, W = c.w, H = c.h, state = 0, anim = 0, raf = 0;
    var x0 = 10, x1 = W - 300, n = S.n;
    function X(k) { return x0 + k / n * (x1 - x0); }
    var MODES = [null,
      { key: 'random', name: 'Random split', feat: 'feature: time stamp', note: 'every test segment has neighbors from the same seizure' },
      { key: 'pastAbs', name: 'Train on the past only', feat: 'feature: time stamp', note: 'no neighbors left in the future' },
      { key: 'pastTod', name: 'Past only, clock of day', feat: 'feature: hour of the day', note: 'seizures here come mostly at night' },
      { key: 'fake', name: 'Same model, fake seizure times', feat: 'onsets moved by whole days', note: 'it scores just as well: a shortcut' }];
    function draw(prog) {
      g.clearRect(0, 0, W, H);
      var yL = 40, yS = 120, hS = 190, mode = MODES[state];
      // nights
      for (var d = 0; d < 4; d++) { var a = X(d * 288), b = X(d * 288 + 72); g.fillStyle = '#EEF0F2'; g.fillRect(a, yL - 18, b - a, yS + hS - yL + 26); txt(g, 'day ' + (d + 1), X(d * 288 + 144), yL - 24, 14, C.ink2, 'center'); }
      txt(g, 'night', X(36), yS + hS + 22, 13, C.ink2, 'center');
      var lab = state === 4 ? S.res.fake.lab : S.lab, ons = state === 4 ? S.res.fake.onsets : S.onsets;
      for (var k = 0; k < n; k++) { if (lab[k]) { g.fillStyle = C.acc; g.fillRect(X(k), yL, Math.max(1.2, X(k + 1) - X(k)), 22); } }
      g.strokeStyle = C.axis; g.lineWidth = 1; g.strokeRect(x0, yL, x1 - x0, 22);
      ons.forEach(function (o) { line(g, X(o), yL - 6, X(o), yL + 28, state === 4 ? C.fail : C.ink, 1.5); });
      txt(g, state === 4 ? 'labels from fake seizure times' : 'orange: the 30 min before each seizure', x0, yL + 44, 14, state === 4 ? C.fail : C.ink2);
      if (!mode) { txt(g, 'A model that only knows when each 5 minute segment was recorded', x0, yS + 40, 18, C.ink); return; }
      var r = S.res[mode.key], show = Math.floor(r.test.length * prog);
      if (mode.key !== 'random') { g.globalAlpha = 0.5; g.fillStyle = C.group; g.fillRect(x0, yS, X(S.half) - x0, hS); g.globalAlpha = 1; txt(g, 'training data', (x0 + X(S.half)) / 2, yS + hS / 2 + 5, 15, C.ink2, 'center'); }
      line(g, x0, yS + hS, x1, yS + hS, C.axis, 1);
      for (var i = 0; i < show; i++) {
        var q = r.test[i], s = r.score[i], hh = Math.max(1, s * hS);
        g.fillStyle = lab[q] ? C.acc : C.slate; g.globalAlpha = lab[q] ? 1 : 0.35; g.fillRect(X(q), yS + hS - hh, Math.max(1.2, X(q + 1) - X(q)), hh); g.globalAlpha = 1;
      }
      txt(g, 'bars: the model’s warning score on test segments', x0, yS + hS + 40, 14, C.ink2);
      // readout
      var rx = W - 270;
      txt(g, mode.name, rx, 48, 20, C.ink, 'left', 600); txt(g, mode.feat, rx, 72, 15, C.ink2);
      var aucShown = 0.5 + (r.auc - 0.5) * prog;
      txt(g, aucShown.toFixed(2), rx, 150, 64, state === 4 ? C.fail : (r.auc > 0.8 ? C.accT : C.ink), 'left', 400);
      txt(g, 'AUC, 0.5 is chance', rx, 176, 15, C.ink2);
      if (state === 4) txt(g, 'real seizures: ' + S.res.pastTod.auc.toFixed(2), rx, 202, 16, C.ink);
      txt(g, mode.note, rx, 232, 15, C.ink2, 'left', 400, true);
    }
    function play() { cancelAnimationFrame(raf); var t0 = 0; function f(ts) { if (!t0) t0 = ts; var p = Math.min(1, (ts - t0) / 1400); draw(p); if (p < 1) raf = requestAnimationFrame(f); } raf = requestAnimationFrame(f); }
    return { start: function () { draw(1); }, stop: function () { cancelAnimationFrame(raf); }, step: function (f) { var ns = f + 1; if (ns !== state) { state = Math.max(0, Math.min(4, ns)); play(); } }, draw: function () { draw(1); } };
  };

  // ===== D3: a ball in a flattening valley (critical slowing down) =====
  REG.tip = function (el) {
    var c = canvasFor(el), g = c.g, W = c.w, H = c.h, r = DM.rng(5), k = 1, kT = 1, xs = [], xv = 0, raf = 0, on = false;
    var dt = 0.05, sig = 0.35;
    function draw() {
      g.clearRect(0, 0, W, H);
      var cx = 150, base = H - 70, sx = 60, sy = 55;
      g.beginPath(); g.strokeStyle = C.ink2; g.lineWidth = 2;
      for (var u = -2.3; u <= 2.3; u += 0.05) { var px = cx + u * sx, py = base - 0.5 * k * u * u * sy; if (u === -2.3) g.moveTo(px, py); else g.lineTo(px, py); }
      g.stroke();
      var bx = cx + Math.max(-2.3, Math.min(2.3, xv)) * sx, by = base - 0.5 * k * xv * xv * sy - 11;
      dot(g, bx, by, 11, C.acc);
      txt(g, 'valley depth', cx, H - 30, 15, C.ink2, 'center'); txt(g, k > 0.5 ? 'deep: kicks fade fast' : 'shallow: kicks linger', cx, H - 10, 15, k > 0.5 ? C.ink2 : C.accT, 'center');
      // trace
      var x0 = 320, x1 = W - 10, mid = H / 2 - 20;
      line(g, x0, mid, x1, mid, C.rule, 1);
      g.beginPath(); g.strokeStyle = C.ink2; g.lineWidth = 1.2;
      xs.forEach(function (v, i) { var px = x0 + i / 300 * (x1 - x0), py = mid - Math.max(-3, Math.min(3, v)) * 32; if (i) g.lineTo(px, py); else g.moveTo(px, py); });
      g.stroke();
      // lag one autocorrelation = leading eigenvalue of the fitted linear map
      var n = xs.length, ac = 0;
      if (n > 50) { var m = 0, i; for (i = 0; i < n; i++) m += xs[i]; m /= n; var num = 0, den = 0; for (i = 1; i < n; i++) num += (xs[i] - m) * (xs[i - 1] - m); for (i = 0; i < n; i++) den += (xs[i] - m) * (xs[i] - m); ac = num / den; }
      txt(g, 'leading eigenvalue of the fitted map', x0, 22, 15, C.ink2);
      txt(g, 'λ = ' + ac.toFixed(2), x0, H - 22, 30, ac > 0.95 ? C.accT : C.ink, 'left', 600);
      txt(g, 'theory: 1 − depth × dt = ' + (1 - k * dt).toFixed(2), x0 + 170, H - 26, 15, C.ink2);
    }
    function loop() {
      if (!on) return;
      k += (kT - k) * 0.01;
      for (var s = 0; s < 2; s++) { xv += -k * xv * dt + sig * Math.sqrt(dt) * DM.gauss(r); xs.push(xv); if (xs.length > 300) xs.shift(); }
      draw(); raf = requestAnimationFrame(loop);
    }
    return { start: function () { on = true; loop(); }, stop: function () { on = false; cancelAnimationFrame(raf); }, step: function (f) { kT = f >= 0 ? 0.04 : 1; }, draw: draw };
  };

  // ===== D4: all eigenvalues decay, the signal still grows first (non normal operator) =====
  REG.nonnormal = function (el) {
    var c = canvasFor(el), g = c.g, W = c.w, H = c.h, coup = 0, target = 0, raf = 0, on = false, l1 = 0.92, l2 = 0.85;
    var sl = document.createElement('input'); sl.type = 'range'; sl.min = 0; sl.max = 3; sl.step = 0.05; sl.value = 0; sl.className = 'demo-range';
    sl.style.cssText = 'position:absolute;left:330px;bottom:4px;width:150px';
    el.appendChild(sl); sl.oninput = function () { target = +sl.value; };
    function norms(cp) { var x = [0, 1], out = []; for (var k = 0; k <= 60; k++) { out.push(Math.hypot(x[0], x[1])); x = [l1 * x[0] + cp * x[1], l2 * x[1]]; } return out; }
    function draw() {
      g.clearRect(0, 0, W, H);
      var cx = 120, cy = H / 2 - 20, R = 95;
      unitCircle(g, cx, cy, R); dot(g, cx + l1 * R, cy, 7, C.acc); dot(g, cx + l2 * R, cy, 7, C.acc);
      txt(g, 'eigenvalues 0.92 and 0.85', cx, cy + R + 36, 15, C.ink2, 'center'); txt(g, 'never move', cx, cy + R + 56, 15, C.ink2, 'center');
      var x0 = 330, x1 = W - 20, y0 = H - 60, y1 = 20, nv = norms(coup), mx = 7;
      line(g, x0, y0, x1, y0, C.axis, 1); line(g, x0, y0, x0, y1, C.axis, 1);
      var yOne = y0 - 1 / mx * (y0 - y1); line(g, x0, yOne, x1, yOne, C.rule, 1, [4, 4]); txt(g, 'start size', x1, yOne - 6, 13, C.ink2, 'right');
      g.beginPath(); g.strokeStyle = C.acc; g.lineWidth = 2.5;
      nv.forEach(function (v, k) { var px = x0 + k / 60 * (x1 - x0), py = y0 - Math.min(mx, v) / mx * (y0 - y1); if (k) g.lineTo(px, py); else g.moveTo(px, py); });
      g.stroke();
      var pkv = Math.max.apply(null, nv);
      txt(g, 'size of the disturbance over 60 steps', x0 + 10, y1 + 8, 15, C.ink2);
      txt(g, 'peak ×' + pkv.toFixed(1), x1, y1 + 32, 26, pkv > 1.05 ? C.accT : C.ink, 'right', 600);
      txt(g, 'coupling ' + coup.toFixed(2) + ', drag to change', x1, H - 12, 15, C.ink2, 'right');
    }
    function loop() { if (!on) return; coup += (target - coup) * 0.06; draw(); raf = requestAnimationFrame(loop); }
    return { start: function () { on = true; loop(); }, stop: function () { on = false; cancelAnimationFrame(raf); },
      step: function (f) { target = f >= 0 ? 1.4 : 0; sl.value = target; }, draw: draw };
  };

  // ---------- wiring to Reveal ----------
  var LIVE = [];
  function init() {
    document.querySelectorAll('.demo[data-demo]').forEach(function (el) {
      var make = REG[el.getAttribute('data-demo')]; if (!make) return;
      var d = make(el); d.el = el; d.sec = el.closest('section'); LIVE.push(d); try { d.draw(); } catch (e) { }
    });
  }
  function sync() {
    var cur = root.Reveal ? Reveal.getCurrentSlide() : null, f = root.Reveal ? Reveal.getIndices().f : -1;
    if (f === undefined) f = -1;
    LIVE.forEach(function (d) { if (d.sec === cur) { d.start(); d.step(f); } else d.stop(); });
  }
  root.DEMOS = { init: init, sync: sync };
})(this);
