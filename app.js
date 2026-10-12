const progress = document.querySelector('.scroll-progress span');
const header = document.querySelector('.site-header');
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('.site-header nav');

function updateProgress() {
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${max > 0 ? (window.scrollY / max) * 100 : 0}%`;
}
window.addEventListener('scroll', updateProgress, { passive: true });
window.addEventListener('resize', updateProgress);
updateProgress();

const observer = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    entry.target.classList.add('is-visible');
    header.classList.toggle('on-light', entry.target.classList.contains('light') || entry.target.classList.contains('recordings-section') || entry.target.classList.contains('appendix-section') || entry.target.classList.contains('documents-section'));
  }
}, { threshold: 0.14, rootMargin: '-14% 0px -35% 0px' });
document.querySelectorAll('.story-panel, .contents-section, .recordings-section, .slides-intro, .appendix-section, .documents-section').forEach(el => observer.observe(el));

menu.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
  menu.textContent = open ? 'Close' : 'Menu';
});
nav.addEventListener('click', event => {
  if (!event.target.closest('a')) return;
  nav.classList.remove('open');
  menu.setAttribute('aria-expanded', 'false');
  menu.textContent = 'Menu';
});

// A slide clip and the complete walkthrough can both be on the page. Keep one
// narration active at a time.
document.querySelectorAll('video').forEach(video => {
  video.addEventListener('play', () => {
    document.querySelectorAll('video').forEach(other => {
      if (other !== video && !other.paused) other.pause();
    });
  });
});

document.querySelectorAll('.slide-player').forEach(player => {
  const video = player.querySelector('video');
  const button = player.querySelector('.slide-play');
  button.addEventListener('click', () => video.play());
  video.addEventListener('play', () => player.classList.add('is-playing'));
  video.addEventListener('pause', () => player.classList.remove('is-playing'));
  video.addEventListener('ended', () => player.classList.remove('is-playing'));
});
