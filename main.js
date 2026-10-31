(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const pointer = matchMedia('(min-width: 801px) and (pointer: fine)');
  const hero = document.querySelector('.hero');
  const nav = $('primaryNavigation');
  const menu = $('menuToggle');
  let userPaused = false;
  const canMove = () => !motion.matches && !document.hidden && !userPaused;
  const setMenu = (open, restore = false) => {
    nav.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    if (restore) menu.focus();
  };
  menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') setMenu(false, true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-nav')) setMenu(false);
  });
  matchMedia('(max-width: 800px)').addEventListener('change', () => setMenu(false));
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', () => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      if (target.matches('details')) target.open = true;
      setMenu(false);
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({preventScroll: true});
    });
  });

  document.querySelectorAll('[data-service]').forEach(link => link.addEventListener('click', () => {
    $('projectType').value = link.dataset.service;
    $('briefForm').dispatchEvent(new Event('input', {bubbles:true}));
  }));
  const openHash = () => {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (target?.matches('details')) target.open = true;
  };
  addEventListener('hashchange', openHash); openHash();

  // One frame per pointer update; only scenery moves, never the original lettering.
  let depthFrame = 0;
  const resetDepth = () => {
    cancelAnimationFrame(depthFrame);
    ['--scene-x', '--scene-y', '--foreground-x', '--foreground-y'].forEach(name => hero.style.removeProperty(name));
  };
  hero.addEventListener('pointermove', event => {
    if (!canMove() || !pointer.matches) return;
    cancelAnimationFrame(depthFrame);
    depthFrame = requestAnimationFrame(() => {
      if (!canMove()) return;
      const rect = hero.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - .5;
      const y = (event.clientY - rect.top) / rect.height - .5;
      hero.style.setProperty('--scene-x', `${x * -5}px`);
      hero.style.setProperty('--scene-y', `${y * -3}px`);
      hero.style.setProperty('--foreground-x', `${x * 3}px`);
      hero.style.setProperty('--foreground-y', `${y * 2}px`);
    });
  });
  hero.addEventListener('pointerleave', resetDepth);
  const cards = [...document.querySelectorAll('.service-card')];
  const cardFrames = new Map();
  const resetCard = card => {
    cancelAnimationFrame(cardFrames.get(card));
    ['--tilt-x', '--tilt-y', '--pointer-x', '--pointer-y'].forEach(name => card.style.removeProperty(name));
  };
  cards.forEach(card => {
    card.addEventListener('pointermove', event => {
      if (!canMove() || !pointer.matches) return;
      cancelAnimationFrame(cardFrames.get(card));
      cardFrames.set(card, requestAnimationFrame(() => {
        if (!canMove()) return;
        const rect = card.getBoundingClientRect();
        const x = event.clientX - rect.left, y = event.clientY - rect.top;
        card.style.setProperty('--pointer-x', `${x}px`);
        card.style.setProperty('--pointer-y', `${y}px`);
        card.style.setProperty('--tilt-x', `${-(y / rect.height - .5) * 2}deg`);
        card.style.setProperty('--tilt-y', `${(x / rect.width - .5) * 2}deg`);
      }));
    });
    card.addEventListener('pointerleave', () => resetCard(card));
  });

  const reveals = [...document.querySelectorAll('.reveal')];
  document.querySelectorAll('.service-grid, .capability-grid, .about-principles').forEach(group => {
    [...group.children].forEach((child, index) => child.style.setProperty('--reveal-delay', `${index * 85}ms`));
  });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    }), {threshold: .08});
    reveals.forEach(element => observer.observe(element));
  } else reveals.forEach(element => element.classList.add('visible'));

  let scrollFrame = 0;
  const navLinks = [...nav.querySelectorAll('a:not(.nav-contact)')];
  const updateScroll = () => {
    scrollFrame = 0;
    const extent = document.documentElement.scrollHeight - innerHeight;
    $('scrollProgress').style.transform = `scaleX(${extent > 0 ? Math.min(1, scrollY / extent) : 0})`;
    let current = '#home';
    navLinks.forEach(link => {
      if (document.querySelector(link.hash).getBoundingClientRect().top <= innerHeight * .35) current = link.hash;
    });
    navLinks.forEach(link => {
      if (link.hash === current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  };
  const queueScroll = () => {
    if (!document.hidden && !scrollFrame) scrollFrame = requestAnimationFrame(updateScroll);
  };
  addEventListener('scroll', queueScroll, {passive: true});
  addEventListener('resize', queueScroll);
  const syncMotion = () => {
    document.documentElement.classList.toggle('motion-paused', document.hidden || userPaused);
    const control = $('motionToggle');
    control.hidden = false; control.disabled = motion.matches;
    control.textContent = motion.matches ? 'Reduced motion enabled' : userPaused ? 'Resume ambient motion' : 'Pause ambient motion';
    control.setAttribute('aria-pressed', String(userPaused || motion.matches));
    resetDepth();
    cards.forEach(resetCard);
    if (motion.matches) reveals.forEach(element => element.classList.add('visible'));
    if (document.hidden) { cancelAnimationFrame(scrollFrame); scrollFrame = 0; }
    else queueScroll();
  };
  $('motionToggle').addEventListener('click', () => { userPaused = !userPaused; syncMotion(); });
  motion.addEventListener('change', syncMotion);
  pointer.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', syncMotion);

  // Accessible native-button tabs: arrows, Home and End follow the selected step.
  const phaseTabs = [...document.querySelectorAll('[data-phase]')];
  const setPhase = (index, focus = false) => {
    phaseTabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      $(`phase-${i}`).hidden = i !== index;
    });
    if (focus) phaseTabs[index].focus();
  };
  phaseTabs.forEach((tab, index) => {
    tab.addEventListener('click', () => setPhase(index));
    tab.addEventListener('keydown', event => {
      const next = {ArrowRight: (index + 1) % 4, ArrowLeft: (index + 3) % 4, Home: 0, End: 3}[event.key];
      if (next !== undefined) { event.preventDefault(); setPhase(next, true); }
    });
  });
  setPhase(0);

  // Clipboard fallback always exposes the actual text; neither form sends data.
  async function copyText(text, status, selectable) {
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(text);
      status.textContent = 'Copied to your clipboard. No message has been sent.';
    } catch {
      status.textContent = 'Automatic copy is unavailable. Select and copy the draft below. Nothing has been sent.';
      selectable.value = text;
      selectable.hidden = false;
      selectable.focus();
      selectable.select();
    }
  }
  const fields = [...document.querySelectorAll('[data-lab-step]')];
  let labStep = 0;
  const buildDraft = () => {
    const scope = [...document.querySelectorAll('input[name="scope"]:checked')].map(input => input.value);
    return `NCNS Digital — planning draft\nDirection: ${$('labService').value}\nGoal: ${$('labGoal').value.trim()}\nTiming: ${$('labTiming').value}\nExplore: ${scope.length ? scope.join(', ') : 'To define together'}\n\nLocal planning draft only — not a quotation. No message sent.`;
  };
  const showLab = (step, focus = false) => {
    labStep = step;
    fields.forEach((field, index) => field.hidden = index !== step);
    document.querySelectorAll('[data-lab-marker]').forEach((marker, index) => {
      if (index === step) marker.setAttribute('aria-current', 'step');
      else marker.removeAttribute('aria-current');
    });
    $('labBack').hidden = step === 0;
    $('labNext').hidden = step === 2;
    $('labRestart').hidden = step !== 2;
    $('labLive').textContent = `Step ${step + 1} of 3 — ${['Choose a direction', 'Set your priorities', 'Review your local draft'][step]}. Nothing is submitted.`;
    if (step === 2) {
      $('labResult').value = buildDraft();
      $('labResult').style.height = 'auto';
      $('labResult').style.height = `${$('labResult').scrollHeight + 2}px`;
      $('copyLab').disabled = false;
      $('useLab').disabled = false;
    }
    if (focus) {
      fields[step].scrollIntoView({behavior: motion.matches ? 'instant' : 'smooth', block: 'nearest'});
      fields[step].querySelector('select, textarea').focus({preventScroll: true});
    }
  };
  $('labNext').addEventListener('click', () => {
    if (labStep === 1) {
      $('labGoal').setCustomValidity($('labGoal').value.trim() ? '' : 'Please describe your main goal.');
      if (!$('labGoal').reportValidity()) return;
    }
    $('labCopyStatus').textContent = '';
    showLab(labStep + 1, true);
  });
  $('labGoal').addEventListener('input', () => $('labGoal').setCustomValidity(''));
  $('labBack').addEventListener('click', () => showLab(Math.max(0, labStep - 1), true));
  $('labRestart').addEventListener('click', () => {
    $('labForm').reset(); $('labResult').value = ''; $('labCopyStatus').textContent = '';
    showLab(0, true);
  });
  $('copyLab').addEventListener('click', () => copyText($('labResult').value, $('labCopyStatus'), $('labResult')));
  $('useLab').addEventListener('click', () => {
    $('projectType').value = $('labService').value;
    $('projectDetails').value = buildDraft();
    $('briefForm').dispatchEvent(new Event('input', {bubbles:true}));
    $('contact').scrollIntoView({behavior: motion.matches ? 'instant' : 'smooth'});
    $('projectDetails').focus({preventScroll: true});
    $('formStatus').textContent = 'Your planning draft is ready to edit. No message has been sent.';
  });
  $('labForm').addEventListener('submit', event => event.preventDefault());
  $('briefForm').addEventListener('submit', event => event.preventDefault());
  $('copyBrief').disabled = false;
  $('copyBrief').addEventListener('click', () => {
    const details = $('projectDetails').value.trim();
    if (!details) {
      $('formStatus').textContent = 'Please describe your project first.';
      $('projectDetails').focus(); return;
    }
    const draft = `NCNS Digital — project brief\nService: ${$('projectType').value}\nProject: ${details}\nCurrent process: ${$('currentProcess').value.trim() || 'To discuss'}\nReply channel: ${$('replyChannel').value.trim() || 'Not supplied'}\n\nDraft only — not sent.`;
    let fallback = $('briefFallback');
    if (!fallback) {
      fallback = document.createElement('textarea'); fallback.id = 'briefFallback';
      fallback.readOnly = true; fallback.hidden = true; fallback.rows = 8;
      fallback.setAttribute('aria-label', 'Project brief — select and copy manually');
      $('briefForm').append(fallback);
    }
    copyText(draft, $('formStatus'), fallback);
  });
  showLab(0);
  document.documentElement.classList.add('js');
  syncMotion();
})();
