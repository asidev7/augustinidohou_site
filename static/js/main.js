/* ==============================================
   TYPED EFFECT
   ============================================== */
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

/* ==============================================
   COUNTERS
   ============================================== */
let counted = false;
function runCounters() {
  if (counted) return;
  const nums = document.querySelectorAll('.num[data-to]');
  if (!nums.length) return;
  const first = nums[0].getBoundingClientRect().top;
  if (first > window.innerHeight) return;
  counted = true;
  nums.forEach(n => {
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

/* ==============================================
   SKILL BARS
   ============================================== */
let skillsDone = false;
function runSkillBars() {
  if (skillsDone) return;
  const el = document.getElementById('skillBars');
  if (!el || el.getBoundingClientRect().top > window.innerHeight - 60) return;
  skillsDone = true;
  document.querySelectorAll('.skill-fill').forEach(b => {
    b.style.width = (b.getAttribute('data-w') || 0) + '%';
  });
}

/* ==============================================
   FADE-UP REVEAL
   ============================================== */
function reveal() {
  document.querySelectorAll('.fade-up').forEach(el => {
    if (el.getBoundingClientRect().top < window.innerHeight - 50) el.classList.add('in');
  });
}

/* ==============================================
   SCROLL LISTENER
   ============================================== */
window.addEventListener('scroll', () => {
  reveal();
  runCounters();
  runSkillBars();
}, { passive: true });

/* Initial trigger */
reveal();
runCounters();
runSkillBars();

/* ==============================================
   SMOOTH ANCHOR SCROLL
   ============================================== */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      window.scrollTo({ top: target.offsetTop - 80, behavior: 'smooth' });
    }
  });
});
