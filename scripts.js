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