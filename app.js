/* =============================================
   FADEFLOW — APP.JS
   Interactions, animations & scroll effects
   ============================================= */

// ---- Navbar scroll effect ----
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  });
}

// ---- Hamburger menu ----
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('nav-links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
  // Close on link click
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// ---- Smooth anchor scrolling ----
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ---- Intersection Observer — reveal on scroll ----
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.12 });

// Observe problem items
document.querySelectorAll('.problem-item').forEach((el, i) => {
  el.style.transitionDelay = `${i * 0.1}s`;
  revealObserver.observe(el);
});

// Observe feature cards
document.querySelectorAll('.feature-card').forEach((el, i) => {
  el.style.transitionDelay = `${i * 0.08}s`;
  revealObserver.observe(el);
});

// Observe social cards
document.querySelectorAll('.social-card').forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = `opacity 0.55s ease ${i * 0.08}s, transform 0.55s ease ${i * 0.08}s`;
  revealObserver.observe(el);
});

// Fix — social cards need .visible class to trigger
const socialObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.social-card').forEach(el => socialObserver.observe(el));

// ---- Progress bar animation ----
const progressFill = document.querySelector('.proj-progress-fill');
if (progressFill) {
  const progressObserver = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      progressFill.style.width = progressFill.dataset.width || '68%';
    }
  });
  progressObserver.observe(progressFill);
}


// ---- Stat counter animation ----
function animateCounter(el, target, prefix = '', suffix = '') {
  const duration = 1500;
  const start = Date.now();
  const isDecimal = target % 1 !== 0;
  const update = () => {
    const elapsed = Date.now() - start;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    const val = isDecimal
      ? (ease * target).toFixed(1)
      : Math.round(ease * target);
    el.textContent = prefix + val + suffix;
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// ---- Hover tilt micro-effect on feature cards ----
document.querySelectorAll('.feature-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width  - 0.5) * 6;
    const y = ((e.clientY - rect.top)  / rect.height - 0.5) * 6;
    card.style.transform = `translateY(-4px) rotateY(${x}deg) rotateX(${-y}deg)`;
    card.style.transition = 'transform 0.1s ease';
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.style.transition = 'all 0.3s ease';
  });
});

// ---- Yellow CTA button pulse ----
const ctaBtns = document.querySelectorAll('.btn-yellow');
ctaBtns.forEach(btn => {
  btn.addEventListener('mouseenter', () => {
    btn.style.boxShadow = '0 0 0 4px rgba(255,194,46,0.25)';
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.boxShadow = '';
  });
});

console.log('%cFadeFlow ✓', 'color:#0D7A5F;font-size:14px;font-weight:800;');
