console.log('main.js versión 2 cargado');


    document.addEventListener('DOMContentLoaded', () => {
    // Animación de aparición
    const fadeIns = document.querySelectorAll('.fade-in');
    console.log('fadeIns:', fadeIns);
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
  
    fadeIns.forEach(el => observer.observe(el));
  
    // Animación de FAQ
    const faqItems = document.querySelectorAll('.faq-item');
    console.log('faqItems:', faqItems);
  
    faqItems.forEach(item => {
      const question = item.querySelector('.faq-question');
      const answer = item.querySelector('.faq-answer');
      console.log('item:', item, 'question:', question, 'answer:', answer);
  
      if (question && answer) {
        question.addEventListener('click', () => {
          answer.classList.toggle('visible');
          item.classList.toggle('open');
        });
      }
    });
  })