(() => {
  const html = document.documentElement;
  const canvas = document.getElementById('nx-canvas');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const conn = navigator.connection || navigator.webkitConnection || navigator.mozConnection;
  const lowConn = conn && (/(2g|slow-2g)/.test(conn.effectiveType) || conn.saveData);
  const mem = navigator.deviceMemory || 8;
  const cores = navigator.hardwareConcurrency || 8;

  // Heurística: usar canvas sólo si el dispositivo va sobrado
  const allowCanvas = !prefersReduced && !lowConn && mem >= 4 && cores >= 4;

  // Spotlight (CSS vars) actualizado a ~30 FPS con interpolación suave
  let mx = 0.6, my = 0.4, pmx = mx, pmy = my, needs = true, lastSpot = 0;
  const onPointer = (e) => {
    mx = Math.min(0.98, Math.max(0.02, e.clientX / window.innerWidth));
    my = Math.min(0.98, Math.max(0.02, e.clientY / window.innerHeight));
    needs = true;
  };
  window.addEventListener('pointermove', onPointer, { passive: true });

  const spotRAF = (t) => {
    if (t - lastSpot > 33 && needs) {
      lastSpot = t; needs = false;
      pmx += (mx - pmx) * 0.25;
      pmy += (my - pmy) * 0.25;
      html.style.setProperty('--mx', (pmx * 100).toFixed(2) + '%');
      html.style.setProperty('--my', (pmy * 100).toFixed(2) + '%');
    }
    requestAnimationFrame(spotRAF);
  };
  requestAnimationFrame(spotRAF);

  if (!allowCanvas || !canvas) return;

  const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
  let dpr = Math.min(window.devicePixelRatio || 1, 1.5);
  const state = { w: 0, h: 0, running: true };

  const resize = () => {
    state.w = canvas.width = Math.floor(window.innerWidth * dpr);
    state.h = canvas.height = Math.floor(window.innerHeight * dpr);
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
  };
  window.addEventListener('resize', resize);
  resize();

  // Partículas muy pocas y baratas
  const N1 = 36, N2 = 18, parts = [];
  const rand = (a,b)=>a+Math.random()*(b-a); const TAU = Math.PI*2;

  // Sprite circular precalculado
  const sprite = document.createElement('canvas');
  sprite.width = sprite.height = 16;
  const sctx = sprite.getContext('2d');
  sctx.fillStyle = '#fff'; sctx.beginPath(); sctx.arc(8,8,6,0,TAU); sctx.fill();

  const palette = () => {
    const css = getComputedStyle(html);
    return [css.getPropertyValue('--accent').trim() || '#d2b26a',
            css.getPropertyValue('--brand').trim() || '#a88bd4'];
  };

  const make = (l) => {
    const [c1,c2] = palette();
    return {
      l,
      x: rand(0, state.w), y: rand(0, state.h),
      vx: rand(-0.02,0.02)*(l?1.8:1), vy: rand(-0.02,0.02)*(l?1.8:1),
      s: l ? rand(10,16) : rand(6,12),
      o: rand(0.25,0.6),
      c: Math.random()<0.5 ? c1 : c2
    };
  };

  for(let i=0;i<N1;i++) parts.push(make(0));
  for(let i=0;i<N2;i++) parts.push(make(1));

  // 24 FPS fijo
  let last = 0, acc = 0, step = 1000/24;

  const loop = (t) => {
    if (!state.running) return;
    if (!document.hidden) canvas.hidden = false;

    const dt = Math.min(64, t - last); last = t; acc += dt;
    if (acc < step) return requestAnimationFrame(loop);
    acc = 0;

    ctx.clearRect(0,0,state.w,state.h);
    ctx.globalCompositeOperation = 'lighter';

    for (const p of parts){
      p.x += p.vx * (step/16);
      p.y += p.vy * (step/16);
      if (p.x < -20) p.x = state.w+20;
      if (p.x > state.w+20) p.x = -20;
      if (p.y < -20) p.y = state.h+20;
      if (p.y > state.h+20) p.y = -20;

      ctx.globalAlpha = p.o;
      ctx.drawImage(sprite, p.x-8, p.y-8, p.s, p.s);
    }

    requestAnimationFrame(loop);
  };

  document.addEventListener('visibilitychange', () => {
    if (document.hidden){
      state.running = false;
      canvas.hidden = true;
    } else {
      state.running = true;
      last = 0; acc = 0;
      requestAnimationFrame(loop);
    }
  });

  canvas.hidden = false;
  requestAnimationFrame(loop);
})();
