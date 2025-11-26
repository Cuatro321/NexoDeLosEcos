// Animar aparición de tarjetas del dashboard
document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.nx-fade');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('is-visible'); });
  }, { threshold: .12 });
  els.forEach(el => io.observe(el));

  // Pequeño “ripple” en botones primarios
  document.body.addEventListener('click', (ev) => {
    const btn = ev.target.closest('.nx-btn--primary');
    if (!btn) return;
    const r = document.createElement('span');
    r.className = 'nx-ripple';
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    r.style.width = r.style.height = size + 'px';
    r.style.left = (ev.clientX - rect.left - size/2) + 'px';
    r.style.top = (ev.clientY - rect.top - size/2) + 'px';
    btn.appendChild(r);
    setTimeout(() => r.remove(), 650);
  });
});
