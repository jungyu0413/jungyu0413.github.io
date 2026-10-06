// Play publication videos only while they are on screen
const videos = document.querySelectorAll('.pub-thumb video');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!reduceMotion) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(({ target, isIntersecting }) => {
      if (isIntersecting) {
        target.play().catch(() => {});
      } else {
        target.pause();
      }
    });
  }, { threshold: 0.25 });

  videos.forEach(video => observer.observe(video));
}
