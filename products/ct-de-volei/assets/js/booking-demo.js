/*!
 * booking-demo.js — Fluxo de agendamento DEMO ONLY (Template-Mestre KE Sites)
 * Não cria agendamentos reais. Ao final, monta uma mensagem de WhatsApp
 * com os dados escolhidos para confirmação humana pela equipe.
 */
(function () {
  "use strict";
  var form = document.getElementById('form-agendamento');
  if (!form) return;

  var steps = Array.from(form.querySelectorAll('[data-step]'));
  var indicators = Array.from(document.querySelectorAll('[data-step-indicator]'));
  var live = document.getElementById('booking-live');
  var current = 1;

  var dateInput = document.getElementById('bk-data');
  if (dateInput) {
    var today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
  }

  function showStep(n) {
    steps.forEach(function (fs) {
      var isTarget = Number(fs.getAttribute('data-step')) === n;
      fs.hidden = !isTarget;
    });
    indicators.forEach(function (el) {
      var idx = Number(el.getAttribute('data-step-indicator'));
      el.classList.toggle('is-active', idx === n);
      el.classList.toggle('is-done', idx < n);
    });
    current = n;
    if (live) live.textContent = 'Etapa ' + n + ' de ' + steps.length;
    var activeFieldset = form.querySelector('[data-step="' + n + '"]');
    var firstField = activeFieldset && activeFieldset.querySelector('select, input');
    if (firstField) firstField.focus({ preventScroll: false });
  }

  function validateStep(n) {
    var fieldset = form.querySelector('[data-step="' + n + '"]');
    var required = fieldset.querySelectorAll('[required]');
    for (var i = 0; i < required.length; i++) {
      if (!required[i].value) {
        required[i].reportValidity();
        return false;
      }
    }
    return true;
  }

  form.addEventListener('click', function (e) {
    if (e.target.matches('[data-step-next]')) {
      if (validateStep(current)) showStep(Math.min(current + 1, steps.length));
    }
    if (e.target.matches('[data-step-back]')) {
      showStep(Math.max(current - 1, 1));
    }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!validateStep(current)) return;

    var data = new FormData(form);
    var servico = data.get('servico') || '';
    var profissional = data.get('profissional') || 'Sem preferência';
    var dataEscolhida = data.get('data') || '';
    var horario = data.get('horario') || '';

    var msg = 'Olá! Gostaria de confirmar um horário:\n' +
      '• Serviço: ' + servico + '\n' +
      '• Profissional: ' + profissional + '\n' +
      '• Data: ' + dataEscolhida + '\n' +
      '• Horário: ' + horario + '\n' +
      '(Simulação enviada pelo site — DEMO ONLY)';

    var whatsappNumber = document.body.getAttribute('data-wa') || '';
    var url = 'https://wa.me/' + whatsappNumber + '?text=' + encodeURIComponent(msg);
    window.open(url, '_blank', 'noopener');
  });

  showStep(1);
})();
