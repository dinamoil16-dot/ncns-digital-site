(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const menu = $('menuToggle');
  const nav = $('primaryNavigation');
  menu.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    menu.setAttribute('aria-expanded','false');
  }));
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
  const motionOK = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
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
  if(motionOK && window.matchMedia('(pointer:fine)').matches) {
    orbit.addEventListener('pointermove',e=>{
      const r=orbit.getBoundingClientRect();
      const x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
      orbit.style.transform='perspective(900px) rotateY('+(x*6)+'deg) rotateX('+(-y*6)+'deg)';
    });
    orbit.addEventListener('pointerleave',()=>orbit.style.transform='');
  }
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
