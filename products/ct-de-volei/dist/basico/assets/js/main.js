/*!
 * main.js — Navegação, menu mobile e microinterações (Template-Mestre KE Sites)
 */
(function () {
  "use strict";

  // -------- Menu mobile acessível --------
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav-mobile');

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(isOpen));
      nav.setAttribute('aria-hidden', String(!isOpen));
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        nav.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      });
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
        document.body.style.overflow = '';
      }
    });
  }

  // -------- Marca item de navegação ativo --------
  const current = document.body.getAttribute('data-page');
  if (current) {
    document.querySelectorAll('[data-nav-link]').forEach((link) => {
      if (link.getAttribute('data-nav-link') === current) {
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  // -------- Scroll reveal suave (respeita prefers-reduced-motion) --------
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const revealEls = document.querySelectorAll('[data-reveal]');

  if (!reduceMotion && 'IntersectionObserver' in window && revealEls.length) {
    revealEls.forEach((el) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(16px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach((el) => io.observe(el));
  }

  // -------- Ano corrente no rodapé --------
  document.querySelectorAll('[data-current-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
})();
