/* =============================================
   FADEFLOW — APP.JS
   Interactions, scroll animations & motion
   ============================================= */

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const lerp = (a, b, t) => a + (b - a) * t;
const ease = t => 1 - Math.pow(1 - t, 3);

// ---- Navbar: scrolled state, hide on scroll down, mobile menu ----
const nav = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
let lastY = window.scrollY;

if (nav) {
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    nav.classList.toggle('is-scrolled', y > 20);
    if (!nav.classList.contains('is-open')) {
      nav.classList.toggle('is-hidden', y > lastY && y > 400);
    }
    lastY = y;
  }, { passive: true });
}

if (hamburger && nav) {
  const setOpen = open => {
    nav.classList.toggle('is-open', open);
    hamburger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };
  hamburger.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
  nav.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => setOpen(false)));
}

// Mark the current page in the nav
const page = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.getAttribute('href') === page) a.classList.add('active');
});

// ---- Scroll progress bar ----
const progress = document.getElementById('scroll-progress');
if (progress) {
  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
  };
  window.addEventListener('scroll', updateProgress, { passive: true });
  updateProgress();
}

// ---- Split headings into words for the mask reveal ----
document.querySelectorAll('.split').forEach(el => {
  const nodes = [...el.childNodes];
  el.textContent = '';
  let i = 0;
  const wrap = (content, open) => {
    const w = document.createElement('span');
    w.className = open ? 'w w-open' : 'w';
    const inner = document.createElement('span');
    inner.style.transitionDelay = `${i++ * 70}ms`;
    inner.append(content);
    w.append(inner);
    el.append(w);
  };
  nodes.forEach(node => {
    if (node.nodeType === Node.TEXT_NODE) {
      node.textContent.split(/(\s+)/).forEach(part => {
        if (!part) return;
        if (/^\s+$/.test(part)) el.append(document.createTextNode(' '));
        else wrap(part, false);
      });
    } else if (node.nodeName === 'BR') {
      el.append(node);
    } else {
      wrap(node, node.querySelector && !!node.querySelector('svg, .ghost') || node.classList.contains('ghost'));
    }
  });
});

// Ghosted "manual work." — each letter fades away
document.querySelectorAll('.ghost').forEach(el => {
  const text = el.textContent;
  el.textContent = '';
  [...text].forEach((ch, i) => {
    const s = document.createElement('span');
    s.className = 'ch';
    s.style.setProperty('--i', i);
    s.textContent = ch === ' ' ? ' ' : ch;
    el.append(s);
  });
});

// ---- Reveal on scroll ----
const revealIO = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-in');
      revealIO.unobserve(entry.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.reveal, .split, .steps').forEach(el => {
  // Stagger siblings that reveal together
  if (el.classList.contains('reveal')) {
    const sibs = [...el.parentElement.children].filter(c => c.classList.contains('reveal'));
    el.style.transitionDelay = `${(sibs.indexOf(el) % 6) * 80}ms`;
  }
  revealIO.observe(el);
});

// ---- Counters ----
const countIO = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = +el.dataset.count;
    const suffix = el.dataset.suffix || '';
    const start = performance.now();
    const tick = now => {
      const t = clamp((now - start) / 1600, 0, 1);
      el.textContent = Math.round(ease(t) * target) + suffix;
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    countIO.unobserve(el);
  });
}, { threshold: 0.6 });
document.querySelectorAll('[data-count]').forEach(el => countIO.observe(el));

// ---- Hero: live automation feed ----
const feedList = document.getElementById('feed-list');
if (feedList) {
  const icons = {
    doc: '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    chat: '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
    mail: '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    chart: '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    bell: '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    truck: '<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" rx="2"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>'
  };
  const events = [
    ['doc', 'Invoice INV-2231 generated', 'From job card TES-JOB-4', false],
    ['chat', 'WhatsApp lead qualified', 'Passed to sales team', true],
    ['mail', '23 emails sorted', '4 flagged for reply today', false],
    ['bell', 'Payment reminder sent', 'Invoice overdue by 7 days', true],
    ['truck', 'Job status updated', 'Ongoing → Completed', false],
    ['chart', 'Daily summary delivered', 'Sent to owner on WhatsApp', true],
    ['doc', 'Quotation drafted', 'Using your rates & template', false],
    ['mail', 'Bill data extracted', 'PO #8812 entered automatically', true]
  ];
  let idx = 0;
  const push = () => {
    const [ico, title, sub, y] = events[idx++ % events.length];
    const item = document.createElement('div');
    item.className = 'feed-item' + (y ? ' y' : '');
    item.innerHTML = `<div class="feed-ico">${icons[ico]}</div><div class="feed-text"><b>${title}</b><span>${sub}</span></div><div class="feed-time">now</div>`;
    feedList.prepend(item);
    [...feedList.children].forEach((c, i) => {
      if (i > 0) c.querySelector('.feed-time').textContent = `${i * 2}m`;
      if (i > 5) c.remove();
    });
  };
  for (let i = 0; i < 4; i++) push();
  if (!reduceMotion) setInterval(push, 2400);
}

// ---- Chaos → Flow sticky scene ----
const chaos = document.getElementById('problem');
const board = document.getElementById('chaos-board');
if (chaos && board) {
  const scraps = [...board.querySelectorAll('.scrap')];
  const meter = document.getElementById('chaos-meter');
  // Scattered positions as fractions of the free board area, plus rotation
  const scatter = [[-0.7, -0.85, -9], [0.6, -0.55, 7], [-0.15, -0.2, -4], [0.65, 0.2, 10], [-0.6, 0.5, 6], [0.2, 0.9, -7]];
  let active = false;

  const render = now => {
    const rect = chaos.getBoundingClientRect();
    const p = clamp(-rect.top / (rect.height - innerHeight), 0, 1);
    const t = ease(clamp((p - 0.12) / 0.6, 0, 1));
    const W = board.clientWidth, H = board.clientHeight;
    const sw = scraps[0].offsetWidth, sh = scraps[0].offsetHeight;
    const fx = Math.max(0, W / 2 - sw / 2), fy = Math.max(0, H / 2 - sh / 2);
    const gap = sh + 10;

    scraps.forEach((s, i) => {
      const [cx, cy, cr] = scatter[i];
      const wob = reduceMotion ? 0 : Math.sin(now / 900 + i * 1.7) * 6 * (1 - t);
      const x = lerp(cx * fx, 0, t);
      const y = lerp(cy * fy, (i - (scraps.length - 1) / 2) * gap, t) + wob;
      const r = lerp(cr, 0, t);
      s.style.transform = `translate3d(${x}px, ${y}px, 0) rotate(${r}deg)`;
      s.style.zIndex = t > 0.5 ? 1 : i + 1;
    });
    chaos.classList.toggle('is-flow', t > 0.55);
    if (meter) meter.style.setProperty('--p', t.toFixed(3));
    if (active) requestAnimationFrame(render);
  };

  new IntersectionObserver(([entry]) => {
    active = entry.isIntersecting;
    if (active) requestAnimationFrame(render);
  }).observe(chaos);
  requestAnimationFrame(render);
}

// ---- Browser mockup: untilts as it scrolls into view ----
const browser = document.getElementById('browser');
if (browser && !reduceMotion) {
  const tilt = () => {
    // Flat on tablets and phones; the 3D tilt only works with the side-by-side layout
    if (innerWidth <= 1080) { browser.style.transform = ''; return; }
    const r = browser.getBoundingClientRect();
    const t = clamp(1 - (r.top + r.height / 2 - innerHeight / 2) / innerHeight, 0, 1);
    browser.style.transform = `rotateY(${lerp(-22, -4, t)}deg) rotateX(${lerp(14, 2, t)}deg)`;
  };
  window.addEventListener('scroll', tilt, { passive: true });
  tilt();
}

// ---- Copy buttons (free resources) ----
const copyText = async text => {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for browsers/contexts without the async clipboard API
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;';
    document.body.append(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch {}
    ta.remove();
    return ok;
  }
};
document.querySelectorAll('[data-copy]').forEach(btn => {
  btn.addEventListener('click', async () => {
    const src = document.getElementById(btn.dataset.copy);
    if (!src) return;
    const ok = await copyText(src.textContent.trim());
    const label = btn.querySelector('.copy-label') || btn;
    if (!label.dataset.text) label.dataset.text = label.textContent;
    label.textContent = ok ? 'Copied ✓' : 'Select & copy';
    btn.classList.toggle('is-copied', ok);
    if (!ok) {
      const range = document.createRange();
      range.selectNodeContents(src);
      getSelection().removeAllRanges();
      getSelection().addRange(range);
    }
    clearTimeout(btn._t);
    btn._t = setTimeout(() => {
      label.textContent = label.dataset.text;
      btn.classList.remove('is-copied');
    }, 2000);
  });
});

// ---- Prompt library: search + category filter ----
const lookSearch = document.getElementById('look-search');
if (lookSearch) {
  const cards = [...document.querySelectorAll('.look-card')];
  const groups = [...document.querySelectorAll('.look-group')];
  const chips = [...document.querySelectorAll('.lib-chip')];
  const count = document.getElementById('look-count');
  const empty = document.getElementById('look-empty');
  const noun = count.dataset.noun || 'looks';
  let cat = 'all';
  const apply = () => {
    const q = lookSearch.value.trim().toLowerCase();
    let shown = 0;
    cards.forEach(c => {
      const ok = (cat === 'all' || c.dataset.cat === cat) && (!q || c.dataset.text.includes(q));
      c.hidden = !ok;
      if (ok) shown++;
    });
    groups.forEach(g => { g.hidden = !g.querySelector('.look-card:not([hidden])'); });
    count.textContent = `${shown} of ${cards.length} ${noun}`;
    empty.hidden = shown > 0;
  };
  const reset = () => {
    lookSearch.value = '';
    cat = 'all';
    chips.forEach(c => c.classList.toggle('active', c.dataset.filter === 'all'));
    apply();
  };
  chips.forEach(chip => chip.addEventListener('click', () => {
    cat = chip.dataset.filter;
    chips.forEach(c => c.classList.toggle('active', c === chip));
    apply();
  }));
  lookSearch.addEventListener('input', apply);
  document.getElementById('look-reset').addEventListener('click', reset);
  document.getElementById('look-reset-2').addEventListener('click', reset);
}

// ---- "Built for ___" word rotator ----
const rotator = document.getElementById('rotator');
if (rotator && !reduceMotion) {
  const words = [...rotator.children];
  let cur = 0;
  setInterval(() => {
    const prev = words[cur];
    cur = (cur + 1) % words.length;
    prev.classList.remove('on');
    prev.classList.add('out');
    words[cur].classList.remove('out');
    words[cur].classList.add('on');
    setTimeout(() => prev.classList.remove('out'), 700);
  }, 2200);
}

// ---- Pointer effects (desktop only) ----
if (finePointer && !reduceMotion) {
  // Yellow dot cursor
  const cursor = document.getElementById('cursor');
  if (cursor) {
    let mx = 0, my = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      cursor.classList.add('is-on');
    });
    document.addEventListener('mouseleave', () => cursor.classList.remove('is-on'));
    const loop = () => {
      cx = lerp(cx, mx, 0.2); cy = lerp(cy, my, 0.2);
      cursor.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
      requestAnimationFrame(loop);
    };
    loop();
    document.querySelectorAll('a, button, .use, .chip').forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('is-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('is-hover'));
    });
  }

  // Magnetic buttons
  document.querySelectorAll('[data-magnetic]').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const r = btn.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width / 2) * 0.25;
      const y = (e.clientY - r.top - r.height / 2) * 0.35;
      btn.style.transform = `translate(${x}px, ${y}px)`;
    });
    btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
  });

  // CTA spotlight
  const cta = document.getElementById('cta');
  const spot = document.getElementById('cta-spot');
  if (cta && spot) {
    cta.addEventListener('mousemove', e => {
      const r = cta.getBoundingClientRect();
      spot.style.left = `${e.clientX - r.left}px`;
      spot.style.top = `${e.clientY - r.top}px`;
    });
  }
}
