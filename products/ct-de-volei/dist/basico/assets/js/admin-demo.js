/*!
 * admin-demo.js — Painel Administrativo DEMO ONLY (Template-Mestre KE Sites)
 * Abas acessíveis (WAI-ARIA Tabs) + CRUD local de clientes via localStorage
 * (somente no navegador — nenhum dado é enviado a um servidor).
 */
(function () {
  "use strict";

  // -------- Tabs acessíveis --------
  var tabs = Array.from(document.querySelectorAll('.admin-tab[role="tab"]'));
  var panels = Array.from(document.querySelectorAll('[role="tabpanel"]'));
  if (!tabs.length) return;

  function activate(tab) {
    tabs.forEach(function (t) {
      var selected = t === tab;
      t.setAttribute('aria-selected', String(selected));
      t.tabIndex = selected ? 0 : -1;
      t.classList.toggle('is-active', selected);
    });
    panels.forEach(function (p) {
      p.hidden = p.getAttribute('aria-labelledby') !== tab.id;
    });
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { activate(tab); });
    tab.addEventListener('keydown', function (e) {
      var next = null;
      if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
      if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
      if (e.key === 'Home') next = tabs[0];
      if (e.key === 'End') next = tabs[tabs.length - 1];
      if (next) { e.preventDefault(); next.focus(); activate(next); }
    });
  });

  // -------- CRUD demo de clientes (localStorage, apenas neste navegador) --------
  var STORAGE_KEY = 'ke-sites-admin-clientes-demo';
  var seed = [
    { nome: 'Fernanda Lima', tel: '(11) 98888-1010', visita: '02/07' },
    { nome: 'Patrícia Nogueira', tel: '(11) 98888-2020', visita: '10/07' },
    { nome: 'Aline Costa', tel: '(11) 98888-3030', visita: '14/07' }
  ];

  function loadClientes() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : seed.slice();
    } catch (err) {
      return seed.slice();
    }
  }

  function saveClientes(list) {
    try { window.localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); } catch (err) { /* ambiente sem storage — segue apenas em memória */ }
  }

  function renderClientes() {
    var tbody = document.getElementById('clientes-tbody');
    if (!tbody) return;
    var list = loadClientes();
    tbody.innerHTML = '';
    list.forEach(function (c, idx) {
      var tr = document.createElement('tr');

      var tdNome = document.createElement('td'); tdNome.textContent = c.nome;
      var tdTel = document.createElement('td'); tdTel.textContent = c.tel || '—';
      var tdVisita = document.createElement('td'); tdVisita.textContent = c.visita || '—';
      var tdAcao = document.createElement('td');
      var btn = document.createElement('button');
      btn.type = 'button'; btn.className = 'btn btn-ghost btn-sm'; btn.textContent = 'Remover';
      btn.addEventListener('click', function () {
        var current = loadClientes();
        current.splice(idx, 1);
        saveClientes(current);
        renderClientes();
      });
      tdAcao.appendChild(btn);

      tr.appendChild(tdNome); tr.appendChild(tdTel); tr.appendChild(tdVisita); tr.appendChild(tdAcao);
      tbody.appendChild(tr);
    });
  }

  var form = document.getElementById('form-add-cliente');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var nome = document.getElementById('ad-cliente-nome').value.trim();
      var tel = document.getElementById('ad-cliente-tel').value.trim();
      if (!nome) return;
      var list = loadClientes();
      list.unshift({ nome: nome, tel: tel, visita: 'Hoje' });
      saveClientes(list);
      renderClientes();
      form.reset();
      document.getElementById('ad-cliente-nome').focus();
    });
    renderClientes();
  }
})();
