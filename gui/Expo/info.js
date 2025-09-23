document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".info-section");

  sections.forEach(section => {
    const titulo = section.querySelector(".toggle-titulo");

    titulo.addEventListener("click", () => {
      section.classList.toggle("active");
    });
  });
});
