/*!
 * client-area-demo.js — Área da Cliente DEMO ONLY (Template-Mestre KE Sites)
 * Não autentica, não armazena senha, não persiste dados reais.
 */
(function () {
  "use strict";
  var form = document.getElementById('form-client-login');
  if (!form) return;

  var loginCard = document.getElementById('client-login-card');
  var dashboard = document.getElementById('client-dashboard');
  var greeting = document.getElementById('client-greeting');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var nome = form.nome.value.trim() || 'Cliente';
    if (greeting) greeting.textContent = 'Olá, ' + nome + '!';
    if (loginCard) loginCard.closest('section').hidden = true;
    if (dashboard) {
      dashboard.hidden = false;
      dashboard.setAttribute('tabindex', '-1');
      dashboard.focus();
    }
  });
})();
