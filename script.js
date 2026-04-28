/* ==============================
   LOADER
   ============================== */
window.addEventListener('load', () => {
  const loader = document.getElementById('loader');
  setTimeout(() => loader.classList.add('hidden'), 800);
});

/* ==============================
   TYPED EFFECT
   ============================== */
const roles = [
  'Développeur Full Stack',
  'Développeur Mobile',
  'Ingénieur Backend',
  'Passionné UI/UX',
  'Entrepreneur Digital',
];
let roleIdx = 0, charIdx = 0, deleting = false;
const typedEl = document.getElementById('typed');

function type() {
  const current = roles[roleIdx];
  if (!deleting) {
    typedEl.textContent = current.slice(0, ++charIdx);
    if (charIdx === current.length) {
      deleting = true;
      setTimeout(type, 1800);
      return;
    }
  } else {
    typedEl.textContent = current.slice(0, --charIdx);
    if (charIdx === 0) {
      deleting = false;
      roleIdx = (roleIdx + 1) % roles.length;
    }
  }
  setTimeout(type, deleting ? 60 : 100);
}
type();

/* ==============================
   HERO PHOTO FALLBACK
   ============================== */
const heroImg = document.getElementById('heroImg');
const placeholder = document.getElementById('photoPlaceholder');
if (heroImg) {
  heroImg.addEventListener('error', () => {
    heroImg.style.display = 'none';
    if (placeholder) placeholder.style.display = 'flex';
  });
  heroImg.addEventListener('load', () => {
    if (placeholder) placeholder.style.display = 'none';
  });
}

/* ==============================
   HEADER SCROLL
   ============================== */
const header = document.getElementById('header');
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  const scrolled = window.scrollY > 50;
  header.classList.toggle('scrolled', scrolled);
  backToTop.classList.toggle('visible', window.scrollY > 400);
  updateActiveNav();
  animateOnScroll();
  animateSkillBars();
  animateCounters();
});

backToTop?.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

/* ==============================
   ACTIVE NAV LINK
   ============================== */
function updateActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navItems = document.querySelectorAll('.nav-item');
  const scrollY = window.scrollY + 120;

  sections.forEach(section => {
    const top    = section.offsetTop;
    const height = section.offsetHeight;
    const id     = section.getAttribute('id');
    if (scrollY >= top && scrollY < top + height) {
      navItems.forEach(item => {
        item.classList.toggle('active', item.getAttribute('href') === `#${id}`);
      });
    }
  });
}

/* ==============================
   MOBILE BURGER
   ============================== */
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');

burger?.addEventListener('click', () => {
  burger.classList.toggle('open');
  navLinks.classList.toggle('open');
});

navLinks?.querySelectorAll('.nav-item').forEach(link => {
  link.addEventListener('click', () => {
    burger.classList.remove('open');
    navLinks.classList.remove('open');
  });
});

/* ==============================
   AOS-LIKE SCROLL ANIMATIONS
   ============================== */
function animateOnScroll() {
  document.querySelectorAll('[data-aos]').forEach(el => {
    const rect = el.getBoundingClientRect();
    const delay = parseInt(el.getAttribute('data-delay') || 0);
    if (rect.top < window.innerHeight - 80) {
      setTimeout(() => el.classList.add('aos-animate'), delay);
    }
  });
}
animateOnScroll();

/* ==============================
   SKILL BARS ANIMATION
   ============================== */
let skillsAnimated = false;
function animateSkillBars() {
  if (skillsAnimated) return;
  const section = document.querySelector('.skills-bars');
  if (!section) return;
  const rect = section.getBoundingClientRect();
  if (rect.top < window.innerHeight - 100) {
    skillsAnimated = true;
    document.querySelectorAll('.skill-fill').forEach(bar => {
      const width = bar.getAttribute('data-width');
      bar.style.width = width + '%';
    });
  }
}
animateSkillBars();

/* ==============================
   COUNTERS ANIMATION
   ============================== */
let countersAnimated = false;
function animateCounters() {
  if (countersAnimated) return;
  const section = document.querySelector('.stats-container');
  if (!section) return;
  const rect = section.getBoundingClientRect();
  if (rect.top < window.innerHeight - 80) {
    countersAnimated = true;
    document.querySelectorAll('.stat-number').forEach(el => {
      const target = parseInt(el.getAttribute('data-target'));
      let current = 0;
      const step = Math.ceil(target / 60);
      const timer = setInterval(() => {
        current = Math.min(current + step, target);
        el.textContent = current;
        if (current >= target) clearInterval(timer);
      }, 25);
    });
  }
}
animateCounters();

/* ==============================
   TESTIMONIALS SLIDER
   ============================== */
const cards = document.querySelectorAll('.testimonial-card');
const dotsContainer = document.getElementById('sliderDots');
let currentSlide = 0, autoplayTimer;

function initSlider() {
  cards.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'dot' + (i === 0 ? ' active' : '');
    dot.setAttribute('aria-label', `Témoignage ${i + 1}`);
    dot.addEventListener('click', () => goToSlide(i));
    dotsContainer.appendChild(dot);
  });
  showSlide(0);
  autoplayTimer = setInterval(() => goToSlide((currentSlide + 1) % cards.length), 5000);
}

function showSlide(idx) {
  cards.forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.dot').forEach(d => d.classList.remove('active'));
  if (cards[idx]) cards[idx].classList.add('active');
  const dots = document.querySelectorAll('.dot');
  if (dots[idx]) dots[idx].classList.add('active');
  currentSlide = idx;
}

function goToSlide(idx) {
  clearInterval(autoplayTimer);
  showSlide(idx);
  autoplayTimer = setInterval(() => goToSlide((currentSlide + 1) % cards.length), 5000);
}

if (cards.length) initSlider();

/* ==============================
   CONTACT FORM
   ============================== */
const contactForm = document.getElementById('contactForm');
const submitBtn   = document.getElementById('submitBtn');
const formSuccess = document.getElementById('formSuccess');

contactForm?.addEventListener('submit', e => {
  e.preventDefault();
  submitBtn.disabled = true;
  submitBtn.querySelector('span').textContent = 'Envoi en cours...';

  setTimeout(() => {
    submitBtn.disabled = false;
    submitBtn.querySelector('span').textContent = 'Envoyer le message';
    formSuccess.classList.add('show');
    contactForm.reset();
    setTimeout(() => formSuccess.classList.remove('show'), 5000);
  }, 1500);
});

/* ==============================
   SMOOTH ANCHOR SCROLL
   ============================== */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

/* ==============================
   PARALLAX SHAPES
   ============================== */
window.addEventListener('scroll', () => {
  const scrolled = window.scrollY;
  document.querySelectorAll('.shape').forEach((shape, i) => {
    const speed = [0.08, 0.12, 0.06, 0.1][i] || 0.08;
    shape.style.transform = `translateY(${scrolled * speed}px)`;
  });
});

/* ==============================
   SERVICE CARDS — MOUSE TILT
   ============================== */
document.querySelectorAll('.service-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 10;
    const y = ((e.clientY - rect.top) / rect.height - 0.5) * -10;
    card.style.transform = `translateY(-8px) rotateX(${y}deg) rotateY(${x}deg)`;
    card.style.transition = 'transform .05s ease';
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.style.transition = 'transform .35s cubic-bezier(.4,0,.2,1)';
  });
});

/* ==============================
   DOTS LOADING ANIMATION
   ============================== */
let dotsCount = 0;
setInterval(() => {
  const dotsEl = document.querySelector('.dots');
  if (dotsEl) {
    dotsCount = (dotsCount + 1) % 4;
    dotsEl.textContent = '.'.repeat(dotsCount);
  }
}, 400);
