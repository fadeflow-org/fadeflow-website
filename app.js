/* =============================================
   FADEFLOW — APP.JS
   Interactions, Animations, Scroll Reveals
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

  // ============================================
  // NAVBAR — Scrolled state
  // ============================================
  const navbar = document.getElementById('navbar');
  const onScroll = () => {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  // ============================================
  // HAMBURGER MENU
  // ============================================
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    hamburger.classList.toggle('active');
  });
  // Close nav when clicking a link
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });

  // ============================================
  // SMOOTH SCROLL for anchor links
  // ============================================
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        const offset = 80;
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  // ============================================
  // SCROLL REVEAL — general elements
  // ============================================
  const revealElements = document.querySelectorAll(
    '.benefit-card, .industry-card, .showcase-item, ' +
    '.social-proof, .vision-pillar, .proof-logo-item, ' +
    '.problem-item, .solution-card'
  );

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Add staggered animation for cards
          const siblings = entry.target.parentElement?.querySelectorAll(
            '.benefit-card, .industry-card, .vision-pillar'
          );
          if (siblings && siblings.length > 1) {
            siblings.forEach((el, i) => {
              el.style.transitionDelay = `${i * 0.08}s`;
              el.classList.add('visible');
            });
          }
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -60px 0px' }
  );

  // Add reveal class to elements
  revealElements.forEach(el => {
    el.classList.add('reveal');
    revealObserver.observe(el);
  });

  // ============================================
  // FLOW STEPS — Staggered reveal on scroll
  // ============================================
  const flowSteps = document.querySelectorAll('.flow-step');
  const flowObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const idx = parseInt(entry.target.dataset.step || '1');
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, (idx - 1) * 120);
          flowObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );
  flowSteps.forEach(step => flowObserver.observe(step));

  // ============================================
  // BENEFIT CARDS — staggered animation
  // ============================================
  const benefitCards = document.querySelectorAll('.benefit-card');
  const benefitObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some(e => e.isIntersecting)) {
        benefitCards.forEach((card, i) => {
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, i * 80);
        });
        entries.forEach(e => benefitObserver.unobserve(e.target));
      }
    },
    { threshold: 0.1 }
  );
  benefitCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(24px)';
    card.style.transition = 'opacity 0.55s ease, transform 0.55s ease, box-shadow 0.2s ease, border-color 0.2s ease';
    benefitObserver.observe(card);
  });

  // ============================================
  // INDUSTRY CARDS — staggered animation
  // ============================================
  const industryCards = document.querySelectorAll('.industry-card');
  const industryObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some(e => e.isIntersecting)) {
        industryCards.forEach((card, i) => {
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, i * 60);
        });
        entries.forEach(e => industryObserver.unobserve(e.target));
      }
    },
    { threshold: 0.1 }
  );
  industryCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease, box-shadow 0.2s ease, border-color 0.2s ease';
    industryObserver.observe(card);
  });

  // ============================================
  // SHOWCASE ITEMS — slide in from sides
  // ============================================
  const showcaseItems = document.querySelectorAll('.showcase-item');
  const showcaseObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          showcaseObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  showcaseItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(40px)';
    item.style.transition = 'opacity 0.7s ease, transform 0.7s ease';
    showcaseObserver.observe(item);
  });

  // ============================================
  // VISION PILLARS — staggered
  // ============================================
  const visionPillars = document.querySelectorAll('.vision-pillar');
  const visionObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some(e => e.isIntersecting)) {
        visionPillars.forEach((pillar, i) => {
          setTimeout(() => {
            pillar.style.opacity = '1';
            pillar.style.transform = 'translateY(0)';
          }, i * 100);
        });
        entries.forEach(e => visionObserver.unobserve(e.target));
      }
    },
    { threshold: 0.15 }
  );
  visionPillars.forEach(pillar => {
    pillar.style.opacity = '0';
    pillar.style.transform = 'translateY(24px)';
    pillar.style.transition = 'opacity 0.55s ease, transform 0.55s ease, background 0.2s ease, border-color 0.2s ease';
    visionObserver.observe(pillar);
  });

  // ============================================
  // SECTION HEADERS — fade in
  // ============================================
  const sectionHeaders = document.querySelectorAll('.section-label, .section-title, .section-sub, .cta-headline, .cta-sub, .vision-headline, .vision-sub, .vision-body, .vision-label');
  const headerObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          headerObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );
  sectionHeaders.forEach((el, i) => {
    // Don't animate hero elements (already animated with CSS)
    if (!el.closest('.hero')) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = `opacity 0.6s ease, transform 0.6s ease`;
      headerObserver.observe(el);
    }
  });

  // ============================================
  // PIPELINE CARDS — animate in hero
  // ============================================
  const pipelineCards = document.querySelectorAll('.pipeline-card');
  pipelineCards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(10px)';
    setTimeout(() => {
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 800 + i * 120);
  });

  // ============================================
  // PROBLEM ITEMS — staggered
  // ============================================
  const problemItems = document.querySelectorAll('.problem-item');
  const problemObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some(e => e.isIntersecting)) {
        problemItems.forEach((item, i) => {
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
          }, i * 80);
        });
        entries.forEach(e => problemObserver.unobserve(e.target));
      }
    },
    { threshold: 0.1 }
  );
  problemItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateX(-20px)';
    item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    problemObserver.observe(item);
  });

  // ============================================
  // PROGRESS BAR — animate when visible
  // ============================================
  const progressFill = document.querySelector('.proj-progress-fill');
  if (progressFill) {
    const originalWidth = progressFill.style.width;
    progressFill.style.width = '0';
    const progressObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              progressFill.style.width = originalWidth;
            }, 300);
            progressObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.5 }
    );
    progressObserver.observe(progressFill);
  }

  // ============================================
  // CTA BUTTON — micro interaction
  // ============================================
  document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('mousedown', () => {
      btn.style.transform = 'translateY(1px) scale(0.98)';
    });
    btn.addEventListener('mouseup', () => {
      btn.style.transform = '';
    });
  });

  // ============================================
  // FLOW STEPS — hover connection effect
  // ============================================
  flowSteps.forEach(step => {
    step.addEventListener('mouseenter', () => {
      step.style.borderColor = '#1D4ED8';
    });
    step.addEventListener('mouseleave', () => {
      step.style.borderColor = '';
    });
  });

  // ============================================
  // STAT COUNTER ANIMATION
  // ============================================
  function animateCounter(el, target, duration = 1500) {
    const start = performance.now();
    const startVal = 0;
    const update = (time) => {
      const elapsed = time - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(startVal + eased * target);
      el.textContent = current;
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = target;
    };
    requestAnimationFrame(update);
  }

  const statValues = document.querySelectorAll('.stat-value');
  const statObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const text = el.textContent.trim();
          // Only animate pure numbers
          if (/^\d+$/.test(text)) {
            animateCounter(el, parseInt(text));
          }
          statObserver.unobserve(el);
        }
      });
    },
    { threshold: 0.8 }
  );
  statValues.forEach(sv => statObserver.observe(sv));

  // ============================================
  // ACTIVE NAV LINK on scroll
  // ============================================
  const sections = document.querySelectorAll('section[id]');
  const navLinkEls = document.querySelectorAll('.nav-links a');

  const activeSectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinkEls.forEach(link => {
            link.style.color = '';
            link.style.background = '';
          });
          const active = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
          if (active) {
            active.style.color = '#1D4ED8';
            active.style.background = '#EFF6FF';
          }
        }
      });
    },
    { threshold: 0.4 }
  );
  sections.forEach(s => activeSectionObserver.observe(s));

});
