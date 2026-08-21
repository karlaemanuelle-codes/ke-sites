/*!
 * modal.js — Sistema de modal próprio e acessível (Template-Mestre KE Sites)
 * Sem alert()/prompt()/confirm(). Suporta:
 *  - role="dialog" + aria-modal
 *  - focus trap (Tab/Shift+Tab presos dentro do modal)
 *  - fechar com Escape
 *  - clique no overlay fecha
 *  - foco inicial no primeiro elemento focável (ou [data-autofocus])
 *  - devolve o foco ao elemento que abriu o modal
 *  - bloqueia scroll do body enquanto aberto
 */
(function () {
  "use strict";

  const FOCUSABLE = [
    'a[href]', 'button:not([disabled])', 'textarea:not([disabled])',
    'input:not([disabled]):not([type="hidden"])', 'select:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  let lastTrigger = null;
  let activeModal = null;

  function getFocusable(modal) {
    return Array.from(modal.querySelectorAll(FOCUSABLE)).filter(
      (el) => el.offsetParent !== null || el === document.activeElement
    );
  }

  function openModal(modal, trigger) {
    if (!modal) return;
    lastTrigger = trigger || document.activeElement;
    activeModal = modal;

    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    const autofocus = modal.querySelector('[data-autofocus]');
    const focusable = getFocusable(modal);
    const target = autofocus || focusable[0] || modal.querySelector('.modal-box');
    if (target) {
      requestAnimationFrame(() => target.focus());
    }

    document.addEventListener('keydown', onKeydown, true);
    modal.dispatchEvent(new CustomEvent('modal:open'));
  }

  function closeModal(modal) {
    if (!modal) return;
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    document.removeEventListener('keydown', onKeydown, true);
    activeModal = null;

    if (lastTrigger && typeof lastTrigger.focus === 'function') {
      lastTrigger.focus();
    }
    modal.dispatchEvent(new CustomEvent('modal:close'));
  }

  function onKeydown(e) {
    if (!activeModal) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      closeModal(activeModal);
      return;
    }

    if (e.key === 'Tab') {
      const focusable = getFocusable(activeModal);
      if (focusable.length === 0) {
        e.preventDefault();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      } else if (!activeModal.contains(document.activeElement)) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  document.addEventListener('click', (e) => {
    const opener = e.target.closest('[data-modal-open]');
    if (opener) {
      const id = opener.getAttribute('data-modal-open');
      const modal = document.getElementById(id);
      if (modal) {
        e.preventDefault();
        openModal(modal, opener);
      }
      return;
    }

    const closer = e.target.closest('[data-modal-close]');
    if (closer) {
      const modal = closer.closest('.modal-overlay');
      e.preventDefault();
      closeModal(modal);
      return;
    }

    // Clique no overlay (fora da caixa) fecha o modal
    if (e.target.classList && e.target.classList.contains('modal-overlay')) {
      closeModal(e.target);
    }
  });

  // API pública mínima, usada por outros scripts (ex: booking-demo.js)
  window.KEModal = { open: openModal, close: closeModal };
})();
