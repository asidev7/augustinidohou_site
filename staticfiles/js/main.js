/* DARK / LIGHT MODE */
const html = document.documentElement;
const themeBtn = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

const saved = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', saved);
themeIcon.className = saved === 'dark' ? 'fas fa-moon' : 'fas fa-sun';

themeBtn?.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  themeIcon.className = next === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
});

/* HEADER SCROLL */
const header = document.getElementById('header');
const topBtn = document.getElementById('topBtn');

window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 40);
  topBtn.classList.toggle('show', window.scrollY > 400);
  highlightNav();
  reveal();
  runCounters();
  runSkillBars();
}, { passive: true });

topBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

/* ACTIVE NAV */
function highlightNav() {
  const sections = document.querySelectorAll('section[id]');
  const y = window.scrollY + 90;
  sections.forEach(s => {
    const link = document.querySelector(`.nav-item[href="#${s.id}"]`);
    if (link) link.classList.toggle('active', y >= s.offsetTop && y < s.offsetTop + s.offsetHeight);
  });
}

/* BURGER */
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');
burger?.addEventListener('click', () => {
  burger.classList.toggle('open');
  navLinks.classList.toggle('open');
});
navLinks?.querySelectorAll('.nav-item').forEach(l => l.addEventListener('click', () => {
  burger.classList.remove('open');
  navLinks.classList.remove('open');
}));

/* TYPED */
const roles = [
  'Administrateur Linux', 'Ingénieur DevOps', 'Expert CI/CD',
  'Architecte Cloud', 'Spécialiste Ansible', 'Sysadmin & SRE'
];
let ri = 0, ci = 0, del = false;
const typedEl = document.getElementById('typed');
function type() {
  if (!typedEl) return;
  const w = roles[ri];
  typedEl.textContent = del ? w.slice(0, --ci) : w.slice(0, ++ci);
  if (!del && ci === w.length) { del = true; setTimeout(type, 1800); return; }
  if (del && ci === 0) { del = false; ri = (ri + 1) % roles.length; }
  setTimeout(type, del ? 50 : 90);
}
type();

/* COUNTERS */
let counted = false;
function runCounters() {
  if (counted) return;
  const el = document.querySelector('.about-stats');
  if (!el || el.getBoundingClientRect().top > window.innerHeight) return;
  counted = true;
  document.querySelectorAll('.num').forEach(n => {
    const target = +n.getAttribute('data-to');
    let v = 0;
    const step = Math.ceil(target / 40);
    const t = setInterval(() => {
      v = Math.min(v + step, target);
      n.textContent = v;
      if (v >= target) clearInterval(t);
    }, 35);
  });
}

/* SKILL BARS */
let skillsDone = false;
function runSkillBars() {
  if (skillsDone) return;
  const el = document.querySelector('.skill-bars');
  if (!el || el.getBoundingClientRect().top > window.innerHeight - 60) return;
  skillsDone = true;
  document.querySelectorAll('.skill-fill').forEach(b => {
    b.style.width = b.getAttribute('data-w') + '%';
  });
}
runSkillBars();

/* SKILL TABS */
document.querySelectorAll('.stab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.stab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.getAttribute('data-cat');
    document.querySelectorAll('.skill-item').forEach(item => {
      item.classList.toggle('hidden', cat !== 'all' && item.getAttribute('data-cat') !== cat);
    });
  });
});

/* FADE-UP ON SCROLL */
document.querySelectorAll('.srv-card, .blog-card, .tl-content, .info-card, .contact-form, .about-text, .skills-col').forEach(el => {
  el.classList.add('fade-up');
});
function reveal() {
  document.querySelectorAll('.fade-up').forEach(el => {
    if (el.getBoundingClientRect().top < window.innerHeight - 50) el.classList.add('in');
  });
}
reveal();

/* SMOOTH ANCHOR */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); window.scrollTo({ top: t.offsetTop - 76, behavior: 'smooth' }); }
  });
});

/* INITIAL SCROLL TRIGGER */
window.dispatchEvent(new Event('scroll'));
