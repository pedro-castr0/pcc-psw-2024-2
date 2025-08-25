// content-loader.js
(function() {
  // 1) Função utilitária: espera todas as imagens dentro de um nó
  function waitImages(node) {
    const imgs = Array.from(node.querySelectorAll('img'));
    if (imgs.length === 0) return Promise.resolve();
    return Promise.all(imgs.map(img => {
      if (img.complete) return Promise.resolve();
      return new Promise(res => img.addEventListener('load', res, { once: true }));
    }));
  }

  // 2) Inicializa o fade/see-more em posts ou cards
  function initContentWrappers(root = document) {
    const WRAPPERS = [
      { selector: '.post-content-wrapper', limit: 300 },
      { selector: '.post-card-wrapper',    limit: 100 } // cards menores
    ];

    WRAPPERS.forEach(({ selector, limit }) => {
      const wrappers = root.querySelectorAll(selector);
      wrappers.forEach(wrapper => {
        if (wrapper.dataset.enhanced) return; // evita duplicar
        wrapper.dataset.enhanced = '1';

        const content = wrapper.querySelector('.post-content');
        const fade    = wrapper.querySelector('.fade-overlay');
        const btn     = wrapper.querySelector('.see-more-btn');
        if (!content || !fade || !btn) return;

        function apply() {
          const hasOverflow = content.scrollHeight > limit;
          fade.classList.toggle('d-none', !hasOverflow);
          btn.classList.toggle('d-none', !hasOverflow);
        }

        apply();

        // Recalcular quando conteúdo mudar de tamanho
        const ro = new ResizeObserver(apply);
        ro.observe(content);

        // Recalcula quando imagens carregarem
        waitImages(content).then(apply);
      });
    });
  }

  // 3) Click handler de abas AJAX
  document.addEventListener('click', function(e) {
    const link = e.target.closest('.load-content');
    if (!link) return;

    e.preventDefault();

    // marca aba ativa
    document.querySelectorAll('.load-content').forEach(a => a.classList.remove('active'));
    link.classList.add('active');

    const url = link.getAttribute('href');
    const target = document.querySelector(link.dataset.target);
    if (!target) return;

    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' }})
      .then(res => res.text())
      .then(html => {
        target.innerHTML = html;
        return waitImages(target).then(() => initContentWrappers(target));
      })
      .catch(err => console.error('Erro carregando conteúdo:', err));
  });

  // 4) Inicialização na carga da página
  document.addEventListener('DOMContentLoaded', function() {
    const initial = document.getElementById('selectedButton') || document.querySelector('.load-content');
    if (initial) initial.click();

    // Inicializa conteúdo já presente na página
    initContentWrappers(document);
  });
})();
