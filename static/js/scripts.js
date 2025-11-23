// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
});

// Animated counter
function animateCounter() {
    const counter = document.querySelector('.counter');
    if (!counter) return;
    let count = 7899;
    const max = 9999;

    setInterval(() => {
        count = (count + 1) > max ? 0 : count + 1;
        const digits = count.toString().padStart(5, '0').split('');
        counter.innerHTML = digits.map(d => `<span>${d}</span>`).join('');
    }, 3000);
}

animateCounter();

function initHeroSlider() {
    const slides = document.querySelectorAll('.hero-slider .slide');
    if (!slides.length) return;
    let i = 0;
    setInterval(() => {
        slides[i].classList.remove('active');
        i = (i + 1) % slides.length;
        slides[i].classList.add('active');
    }, 5000);
}

document.addEventListener('DOMContentLoaded', initHeroSlider);

(function(){
    const pwd = document.getElementById('contrasena');
    if(!pwd) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.innerHTML = '<i class="fa fa-eye"></i>';
    btn.style.cssText = 'position:absolute;right:8px;top:32px;background:transparent;border:none;cursor:pointer;font-size:16px;color:#134563;';
    const parent = pwd.parentElement;
    parent.style.position='relative';
    parent.appendChild(btn);
    btn.addEventListener('click', () => {
        const showing = pwd.type === 'text';
        pwd.type = showing ? 'password' : 'text';
        btn.innerHTML = showing ? '<i class="fa fa-eye"></i>' : '<i class="fa fa-eye-slash"></i>';
    });
}());

// Contact form handler
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Mostrar notificación de éxito
            mostrarNotificacion('✓ Correo enviado correctamente', 'success');
            
            // Limpiar el formulario
            contactForm.reset();
            
            // Scroll suave hacia arriba para ver la notificación
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = 'success') {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion notificacion-${tipo}`;
    notificacion.textContent = mensaje;
    
    // Agregar al body
    document.body.appendChild(notificacion);
    
    // Mostrar con animación
    setTimeout(() => {
        notificacion.classList.add('mostrar');
    }, 100);
    
    // Ocultar y remover después de 3 segundos
    setTimeout(() => {
        notificacion.classList.remove('mostrar');
        setTimeout(() => {
            notificacion.remove();
        }, 300);
    }, 3000);
}