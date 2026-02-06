// ===== NAVBAR SCROLL EFFECT =====
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ===== SMOOTH SCROLL FOR NAV LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ===== GSAP ANIMATIONS =====
window.addEventListener('load', () => {
    if (typeof gsap === 'undefined') return;

    gsap.registerPlugin(ScrollTrigger);

    // -- HERO ENTRANCE --
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    heroTl
        .from('.hero-badge', { opacity: 0, y: 20, duration: 0.6 })
        .from('.hero-title', { opacity: 0, y: 40, duration: 0.8 }, '-=0.3')
        .from('.hero-subtitle', { opacity: 0, y: 30, duration: 0.6 }, '-=0.4')
        .from('.hero-actions', { opacity: 0, y: 25, duration: 0.6 }, '-=0.3')
        .from('.hero-stats .stat', { opacity: 0, y: 20, stagger: 0.12, duration: 0.5 }, '-=0.3')
        .from('.hero-stats .stat-divider', { opacity: 0, scaleY: 0, stagger: 0.1, duration: 0.3 }, '-=0.4');

    // -- COUNTER ANIMATION --
    document.querySelectorAll('.stat-number[data-count]').forEach(el => {
        const target = parseInt(el.dataset.count);
        gsap.to(el, {
            textContent: target,
            duration: 1.5,
            ease: 'power2.out',
            snap: { textContent: 1 },
            delay: 0.8
        });
    });

    // -- SECTION HEADERS --
    gsap.utils.toArray('.section-header').forEach(header => {
        gsap.from(header.children, {
            scrollTrigger: {
                trigger: header,
                start: 'top 85%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            y: 30,
            stagger: 0.12,
            duration: 0.7,
            ease: 'power3.out'
        });
    });

    // -- FEATURE CARDS --
    gsap.utils.toArray('.feature-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 88%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            y: 40,
            duration: 0.6,
            delay: i * 0.08,
            ease: 'power3.out'
        });
    });

    // -- STEPS --
    gsap.utils.toArray('.step-card').forEach((step, i) => {
        gsap.from(step, {
            scrollTrigger: {
                trigger: step,
                start: 'top 88%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            y: 30,
            duration: 0.6,
            delay: i * 0.15,
            ease: 'power3.out'
        });
    });

    gsap.utils.toArray('.step-connector').forEach((conn, i) => {
        gsap.from(conn, {
            scrollTrigger: {
                trigger: conn,
                start: 'top 88%',
                toggleActions: 'play none none none'
            },
            scaleX: 0,
            duration: 0.5,
            delay: i * 0.15 + 0.2,
            ease: 'power2.out'
        });
    });

    // -- CATEGORY CHIPS --
    gsap.utils.toArray('.category-chip').forEach((chip, i) => {
        gsap.from(chip, {
            scrollTrigger: {
                trigger: '.categories-grid',
                start: 'top 85%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            scale: 0.85,
            duration: 0.4,
            delay: i * 0.06,
            ease: 'back.out(1.5)'
        });
    });

    // -- RISK CARDS --
    gsap.utils.toArray('.risk-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 88%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            x: -30,
            duration: 0.5,
            delay: i * 0.12,
            ease: 'power3.out'
        });
    });

    // -- TECH CARDS --
    gsap.utils.toArray('.tech-card').forEach((card, i) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 90%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            y: 30,
            scale: 0.95,
            duration: 0.5,
            delay: i * 0.06,
            ease: 'power3.out'
        });
    });

    // -- CTA SECTION --
    gsap.from('.cta-card', {
        scrollTrigger: {
            trigger: '.cta-card',
            start: 'top 85%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        y: 50,
        scale: 0.97,
        duration: 0.8,
        ease: 'power3.out'
    });

    gsap.from('.cta-title', {
        scrollTrigger: {
            trigger: '.cta-card',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        y: 25,
        duration: 0.6,
        delay: 0.2,
        ease: 'power3.out'
    });

    gsap.from('.cta-desc', {
        scrollTrigger: {
            trigger: '.cta-card',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        y: 20,
        duration: 0.6,
        delay: 0.35,
        ease: 'power3.out'
    });

    gsap.from('.cta-actions', {
        scrollTrigger: {
            trigger: '.cta-card',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        y: 20,
        duration: 0.6,
        delay: 0.5,
        ease: 'power3.out'
    });
});
