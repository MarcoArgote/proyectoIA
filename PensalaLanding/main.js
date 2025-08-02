// Modal detalles
const detailsData = {
  basica: {
    title: 'Membresía Básica',
    features: [
      { text: 'Personalización de la web con identidad de marca', check: true },
      { text: 'Hosting sin costo fijo (solo paga si hay reservas en su web)', check: true },
      { text: 'Búsqueda de imágenes y contenido (nosotros lo buscamos por usted)', check: false },
      { text: 'Actualizaciones constantes en la página', check: false },
      { text: 'Atención preferencial (soporte antes que otros clientes)', check: false },
      { text: 'Ajustes estratégicos de marca y asesoramiento personalizado', check: false },
    ]
  },
  pro: {
    title: 'Membresía Pro',
    features: [
      { text: 'Personalización de la web con identidad de marca', check: true },
      { text: 'Hosting sin costo fijo (solo paga si hay reservas en su web)', check: true },
      { text: 'Búsqueda de imágenes y contenido (nosotros lo buscamos por usted)', check: true },
      { text: 'Actualizaciones constantes en la página', check: true },
      { text: 'Atención preferencial (soporte antes que otros clientes)', check: false },
      { text: 'Ajustes estratégicos de marca y asesoramiento personalizado', check: false },
    ]
  },
  premium: {
    title: 'Membresía Premium',
    features: [
      { text: 'Personalización de la web con identidad de marca', check: true },
      { text: 'Hosting sin costo fijo (solo paga si hay reservas en su web)', check: true },
      { text: 'Búsqueda de imágenes y contenido (nosotros lo buscamos por usted)', check: true },
      { text: 'Actualizaciones constantes en la página', check: true },
      { text: 'Atención preferencial (soporte antes que otros clientes)', check: true },
      { text: 'Ajustes estratégicos de marca y asesoramiento personalizado', check: true },
    ]
  },
  landing: {
    title: 'Landing Page',
    features: [
      { text: 'Diseño profesional', check: true },
      { text: 'Optimización SEO', check: true },
      { text: 'Formulario de contacto', check: true },
      { text: 'Integración con redes sociales', check: true },
      { text: 'Dominio incluido', check: false },
      { text: 'Soporte técnico', check: true },
    ]
  },
  appweb: {
    title: 'Aplicación Web',
    features: [
      { text: 'Desarrollo a medida', check: true },
      { text: 'Panel de administración', check: true },
      { text: 'Soporte técnico', check: true },
      { text: 'Certificado SSL', check: true },
      { text: 'Dominio incluido', check: false },
      { text: 'Actualizaciones mensuales', check: true },
    ]
  },
  appmovil: {
    title: 'Aplicación Móvil',
    features: [
      { text: 'Desarrollo multiplataforma', check: true },
      { text: 'Publicación en tiendas', check: true },
      { text: 'Soporte técnico', check: true },
      { text: 'Certificado SSL', check: false },
      { text: 'Dominio incluido', check: false },
      { text: 'Actualizaciones mensuales', check: true },
    ]
  }
};

document.querySelectorAll('.details-btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    const plan = this.closest('.box').getAttribute('data-plan');
    const modal = document.getElementById('details-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalList = document.getElementById('modal-list');
    const data = detailsData[plan];
    modalTitle.textContent = data.title;
    modalList.innerHTML = '';
    data.features.forEach(f => {
      modalList.innerHTML += `<li><i class="ri-${f.check ? 'check-line check' : 'close-line x'}"></i> ${f.text}</li>`;
    });
    modal.classList.add('active');
  });
});

document.querySelector('.details-modal-close').onclick = function() {
  document.getElementById('details-modal').classList.remove('active');
};

window.onclick = function(event) {
  const modal = document.getElementById('details-modal');
  if (event.target === modal) {
    modal.classList.remove('active');
  }
};
// Mobile Menu

let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
    menu.classList.toggle('bx-x');
    navbar.classList.toggle('active');
}

window.onscroll = () => {
    menu.classList.remove('bx-x');
    navbar.classList.remove('active');
}

// Scroll Reveal

const sr = ScrollReveal ({
    distance: '60px',
    duration: 2500,
    delay: 400,
    reset: true
})

sr.reveal('.text', { delay: 200, origin: 'top'})
sr.reveal('.form-container form', { delay: 400, origin: 'left'})
sr.reveal('.heading', { delay: 400, origin: 'top'})
sr.reveal('.ride-container .box', { delay: 200, origin: 'top'})
sr.reveal('.services-container .box', { delay: 200, origin: 'top'})
sr.reveal('.about-container', { delay: 200, origin: 'top'})
sr.reveal('.reviews-container', { delay: 200, origin: 'top'})
sr.reveal('.newsletter .box', { delay: 400, origin: 'bottom'})