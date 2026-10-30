(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const $ = (id) => document.getElementById(id);
  const menu = $('menuToggle');
  const nav = $('primaryNavigation');
  const setMenu = (open, restoreFocus = false) => {
    nav.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    if (restoreFocus) menu.focus();
  };
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      setMenu(false, true);
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-nav')) setMenu(false);
  });
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', () => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      setMenu(false);
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({preventScroll: true});
    });
  });
  const mobileNav = window.matchMedia('(max-width: 800px)');
  mobileNav.addEventListener('change', () => setMenu(false));
  const stages = [
    ['01 / 04', '◎', 'Start with the real problem.', 'We learn what matters to your customers and what a better digital experience should achieve.'],
    ['02 / 04', '◇', 'Give the idea its own identity.', 'We translate the strategy into a distinct interface and clear user journey.'],
    ['03 / 04', '▣', 'Make every interaction count.', 'Responsive implementation, considered motion and useful functionality.'],
    ['04 / 04', '↗', 'Launch. Learn. Improve.', 'Test the experience, address feedback and evolve the product with real data.'],
  ];
  const stageButtons = Array.from(document.querySelectorAll('[data-step]'));
  let stage = 0;
  function setStage(index) {
    stage = index;
    const [count,glyph,heading,description] = stages[stage];
    $('workflowCount').textContent = count;
    $('workflowGlyph').textContent = glyph;
    $('workflowHeading').textContent = heading;
    $('workflowDescription').textContent = description;
    stageButtons.forEach((b,i) => {
      b.classList.toggle('active', i === stage);
      b.setAttribute('aria-pressed',String(i === stage));
    });
  }
  stageButtons.forEach((b,i) => b.addEventListener('click', () => setStage(i)));
  $('nextStep').addEventListener('click', () => setStage((stage+1)%stages.length));
  setStage(0);
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const motionOK = !motionPreference.matches;
  motionPreference.addEventListener('change', () => {
    if (motionPreference.matches) {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'));
      $('heroOrbit').style.transform = '';
    }
  });
  if (window.matchMedia('(min-width: 801px) and (pointer: fine)').matches) {
    document.querySelectorAll('.service-card').forEach(card => {
      card.addEventListener('pointermove', event => {
        if (motionPreference.matches) return;
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--pointer-x', `${event.clientX - rect.left}px`);
        card.style.setProperty('--pointer-y', `${event.clientY - rect.top}px`);
      });
    });
  }
  if (motionOK && window.IntersectionObserver) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if(e.isIntersecting) {e.target.classList.add('visible');io.unobserve(e.target);}
    }), {threshold:0.12});
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));
  }
  let ticking=false;
  window.addEventListener('scroll', () => {
    if(ticking)return;
    ticking=true;
    requestAnimationFrame(()=>{
      const max=document.documentElement.scrollHeight-innerHeight;
      $('scrollProgress').style.transform = 'scaleX(' + (max>0?Math.min(1,scrollY/max):0) + ')';
      ticking=false;
    });
  }, {passive:true});
  const orbit = $('heroOrbit');
  const hero = document.querySelector('.hero');
  const depthAllowed = window.matchMedia('(min-width: 801px) and (pointer: fine)');
  let depthFrame = 0;
  const resetDepth = () => {
    cancelAnimationFrame(depthFrame);
    orbit.style.transform = '';
    hero.style.removeProperty('--scene-x');
    hero.style.removeProperty('--scene-y');
  };
  hero.addEventListener('pointermove', event => {
    if (motionPreference.matches || !depthAllowed.matches) return;
    cancelAnimationFrame(depthFrame);
    depthFrame = requestAnimationFrame(() => {
      const rect = hero.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - .5;
      const y = (event.clientY - rect.top) / rect.height - .5;
      orbit.style.transform = `perspective(1200px) rotateY(${x * 2}deg) rotateX(${-y * 2}deg)`;
      hero.style.setProperty('--scene-x', `${x * -5}px`);
      hero.style.setProperty('--scene-y', `${y * -3}px`);
    });
  });
  hero.addEventListener('pointerleave', resetDepth);
  depthAllowed.addEventListener('change', resetDepth);
  motionPreference.addEventListener('change', resetDepth);
  $('briefForm').addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const type=$('projectType').value,details=$('projectDetails').value.trim();
    if(!details){
      $('formStatus').textContent='Please describe your project first.';
      $('projectDetails').focus();
      return;
    }
    const brief='NCNS Digital — project enquiry\nService: '+type+'\nProject: '+details+'\n\nDraft only — not sent.';
    try {
      if(!navigator.clipboard?.writeText)throw Error('clipboard unavailable');
      await navigator.clipboard.writeText(brief);
      $('formStatus').textContent='Project brief copied. No message has been sent.';
    } catch {
      const ta=document.createElement('textarea');
      ta.value=brief; ta.readOnly=true;
      ta.style.width='100%';ta.style.minHeight='130px';
      $('formStatus').replaceChildren(ta);ta.focus();ta.select();
    }
  });
})();
