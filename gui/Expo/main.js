(function () {
  const root = document.getElementById('spooky-sidebar-app');
  const sidebar = document.getElementById('spookySidebar');
  const content = document.getElementById('spookyContent');
  const menuBtn = document.getElementById('spookyMenuBtn');
  const collapseBtn = document.getElementById('spookyCollapseBtn');
  const backdrop = document.getElementById('spookyBackdrop');
  const items = Array.from(root.querySelectorAll('.spooky-item'));
  const views = Array.from(root.querySelectorAll('[data-view]'));
  const faq = document.getElementById('spookyFaq');

  function setActive(section) {
    items.forEach(btn => {
      const on = btn.getAttribute('data-section') === section;
      btn.setAttribute('aria-current', on ? 'page' : 'false');
    });
    views.forEach(v => {
      const isActive = v.getAttribute('data-view') === section;
      v.classList.toggle('active', isActive);
    });
    sessionStorage.setItem('spooky-active', section);
    if (content) {
      content.focus({ preventScroll: true });
    }
  }

  function openMobile() {
    sidebar.classList.add('open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'true');
    if (backdrop) {
      backdrop.hidden = false;
      backdrop.classList.add('show');
    }
  }

  function closeMobile() {
    sidebar.classList.remove('open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
    if (backdrop) {
      backdrop.classList.remove('show');
      setTimeout(() => {
        backdrop.hidden = true;
      }, 200);
    }
  }

  // Event listener para menú móvil (solo si existe)
  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      const mobile = window.matchMedia('(max-width: 720px)').matches;
      if (mobile) {
        if (sidebar.classList.contains('open')) {
          closeMobile();
        } else {
          openMobile();
        }
      }
    });
  }

  // Event listener para cerrar con backdrop
  if (backdrop) {
    backdrop.addEventListener('click', closeMobile);
  }

  // Event listener para colapsar sidebar en escritorio
  if (collapseBtn) {
    collapseBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
      const isCollapsed = sidebar.classList.contains('collapsed');
      collapseBtn.setAttribute(
        'aria-label',
        isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'
      );
    });
  }

  // Event listeners para navegación entre secciones
  items.forEach(btn => {
    btn.addEventListener('click', () => {
      setActive(btn.getAttribute('data-section'));
      const mobile = window.matchMedia('(max-width: 720px)').matches;
      if (mobile) {
        closeMobile();
      }
    });
  });

  // Event listener para preguntas frecuentes
  if (faq) {
    faq.addEventListener('click', e => {
      const q = e.target.closest('.q');
      if (!q) return;
      const item = q.parentElement;
      item.classList.toggle('open');
    });
  }

  // Activar sección guardada
  const saved = sessionStorage.getItem('spooky-active') || 'home';
  setActive(saved);
})();