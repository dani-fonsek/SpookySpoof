(function () {
  const root = document.getElementById('spooky-sidebar-app');
  const sidebar = document.getElementById('spookySidebar');
  const content = document.getElementById('spookyContent');
  const collapseBtn = document.getElementById('spookyCollapseBtn');
  const items = Array.from(root.querySelectorAll('.spooky-item'));
  const views = Array.from(root.querySelectorAll('[data-view]'));

  function setActive(section) {
    items.forEach(btn => {
      const active = btn.getAttribute('data-section') === section;
      btn.setAttribute('aria-current', active ? 'page' : 'false');
    });
    views.forEach(view => {
      const active = view.getAttribute('data-view') === section;
      view.classList.toggle('active', active);
    });
    sessionStorage.setItem('spooky-active', section);
    if (content) content.focus({ preventScroll: true });
  }

  if (collapseBtn) {
    collapseBtn.addEventListener('click', () => {
      sidebar.classList.toggle('collapsed');
    });
  }

  items.forEach(btn => {
    btn.addEventListener('click', () => {
      setActive(btn.getAttribute('data-section'));
    });
  });

  const quizOptions = document.querySelectorAll('.quiz-option');
  if (quizOptions.length) {
    quizOptions.forEach(option => {
      option.addEventListener('click', () => {
        const feedback = document.getElementById('quiz-feedback');
        const correct = option.dataset.correct === "true";
        feedback.textContent = correct
          ? "✅ Correcto! Eso es MAC Spoofing."
          : "❌ Incorrecto. Intenta de nuevo.";
        feedback.style.color = correct ? "limegreen" : "crimson";
      });
    });
  }

  const saved = sessionStorage.getItem('spooky-active') || 'home';
  setActive(saved);

  // 🔍 MONITOREO: Cargar datos desde /data
fetch('/data')
  .then(res => res.json())
  .then(data => {
    if (!Array.isArray(data) || data.length === 0) return;

    const monitoringSection = document.querySelector('section[data-view="monitoring"]');
    if (!monitoringSection) return;

    const tabla = document.createElement('table');
    tabla.classList.add('spooky-table');

    tabla.innerHTML = `
      <tr>
        <th>MAC</th>
        <th>IP</th>
        <th>Paquetes</th>
        <th>Hora</th>
        <th>Confianza</th>
      </tr>
      ${data.map(d => `
        <tr>
          <td>${d.mac}</td>
          <td>${d.ip}</td>
          <td>${d.paquetes}</td>
          <td>${d.hora}</td>
          <td>${(d.confianza * 100).toFixed(1)}%</td>
        </tr>
      `).join('')}
    `;

    // Mover el botón debajo de la tabla
    const boton = monitoringSection.querySelector('button.btn-gradient');
    if (boton) {
      boton.remove(); // lo sacamos de su posición original
      monitoringSection.appendChild(tabla);
      monitoringSection.appendChild(boton); // lo colocamos justo después
    } else {
      monitoringSection.appendChild(tabla);
    }
  })
  .catch(err => console.error("Error al cargar datos:", err));
})();

const botonContener = document.querySelector('[data-view="monitoring"] .btn-gradient');
if (botonContener) {
  botonContener.addEventListener('click', () => {
    const tabla = document.querySelector('.spooky-table');
    if (!tabla) return;

    const primeraFila = tabla.querySelector('tr:nth-child(2)');
    if (!primeraFila) return;

    const mac = primeraFila.children[0].textContent;

    fetch('/contener', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mac })
    })
    .then(res => res.json())
    .then(data => {
      console.log("Resultado del script:", data);
      alert(data.stdout || "Comando ejecutado.");
    })
    .catch(err => {
      console.error("Error al ejecutar script:", err);
      alert("Error al contener tráfico.");
    });
  });
}