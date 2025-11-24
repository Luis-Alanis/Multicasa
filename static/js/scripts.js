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

// Contact form handler - COMENTADO para permitir envío normal del formulario
/*
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            mostrarNotificacion('✓ Correo enviado correctamente', 'success');
            contactForm.reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});
*/

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

// Mejoras para dispositivos móviles
document.addEventListener('DOMContentLoaded', function() {
    // Detectar si es dispositivo móvil
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        // Agregar clase para móviles
        document.body.classList.add('is-mobile');
        
        // Mejorar el comportamiento de los inputs en móviles
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.setAttribute('inputmode', 'decimal');
            });
        });
        
        // Prevenir zoom en inputs en iOS
        const meta = document.querySelector('meta[name="viewport"]');
        if (meta) {
            meta.setAttribute('content', 
                'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
            );
        }
    }
    
    // Cerrar menús al hacer scroll en móviles
    let lastScroll = 0;
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (isMobile && Math.abs(currentScroll - lastScroll) > 50) {
            // Cerrar modales si están abiertos
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                if (modal.classList.contains('show')) {
                    const closeBtn = modal.querySelector('.close-modal');
                    if (closeBtn) closeBtn.click();
                }
            });
        }
        
        lastScroll = currentScroll;
    });
});