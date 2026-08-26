/* ═══════════════════════════════════════════════════════════
   RaZe Renders — interactions
   ═══════════════════════════════════════════════════════════ */
(() => {
  'use strict';

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ── time helpers ─────────────────────────────────────── */
  const pad = n => String(Math.floor(n)).padStart(2, '0');
  const clock = t => `${pad(t / 60)}:${pad(t % 60)}`;
  // SMPTE-ish timecode HH:MM:SS:FF (25fps) for the flavour counters
  const smpte = (t) => {
    const f = Math.floor((t % 1) * 25);
    return `${pad(t / 3600)}:${pad((t / 60) % 60)}:${pad(t % 60)}:${pad(f)}`;
  };

  /* ═══ INTRO / PRELOADER ═══════════════════════════════ */
  const intro    = $('#intro');
  const introBar = $('#introBar');
  const introNum = $('#introCount');

  const finishIntro = () => {
    if (!intro || intro.classList.contains('done')) return;
    intro.classList.add('done');
    document.body.style.overflow = '';
  };

  const runIntro = () => {
    if (!intro || intro.classList.contains('done')) return;
    // No point animating a loader nobody is looking at — and background tabs
    // throttle timers, which would leave it stuck. Skip straight to the page.
    if (prefersReduced || document.hidden) { finishIntro(); return; }
    document.body.style.overflow = 'hidden';
    let p = 0;
    // setInterval (not requestAnimationFrame) so the loader still completes
    // if the page is opened in a background tab, where rAF is paused.
    const timer = setInterval(() => {
      p += Math.max(1, (100 - p) * 0.12);
      if (p >= 100) p = 100;
      if (introBar) introBar.style.width = p + '%';
      if (introNum) introNum.textContent = pad(p);
      if (p >= 100) {
        clearInterval(timer);
        setTimeout(finishIntro, 260);
      }
    }, 16);
  };
  window.addEventListener('load', runIntro, { once: true });
  // if the visitor tabs away mid-load, don't leave them a frozen loader
  document.addEventListener('visibilitychange', () => { if (document.hidden) finishIntro(); });
  // start even if 'load' is slow, and hard-clear the loader no matter what
  setTimeout(runIntro, 1200);
  setTimeout(finishIntro, 4000);

  /* ═══ NAV shrink on scroll ════════════════════════════ */
  const nav = $('#nav');
  const onScroll = () => { nav.classList.toggle('shrink', window.scrollY > 40); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ═══ REVEAL on scroll ════════════════════════════════ */
  const revealIO = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); revealIO.unobserve(e.target); } });
  }, { threshold: 0.16 });
  $$('.reveal').forEach(el => revealIO.observe(el));

  /* ═══ SINGLE-AUDIO manager ════════════════════════════
     Only one video may play sound at a time. Unmuting one
     mutes every other. */
  let audioOwner = null;
  const claimAudio = (video, card) => {
    if (audioOwner && audioOwner.video !== video) {
      audioOwner.video.muted = true;
      audioOwner.card.classList.remove('sound-on');
    }
    audioOwner = { video, card };
  };
  const releaseAudio = (video) => {
    if (audioOwner && audioOwner.video === video) audioOwner = null;
  };

  /* ═══ LAZY-LOAD: set src only when near viewport ══════ */
  const ensureSrc = (video) => {
    if (video.dataset.src && !video.src) {
      video.src = video.dataset.src;
      video.load();
    }
  };

  /* ═══ SHOWREEL (hero) ═════════════════════════════════ */
  const reel      = $('#showreel');
  const reelBtn   = $('#reelSound');
  const reelTC    = $('#reelTC');
  const reelStage = $('[data-reel]');

  if (reel) {
    ensureSrc(reel);
    const tryPlay = () => { const p = reel.play(); if (p) p.catch(() => {}); };
    tryPlay();

    // pause hero reel when scrolled away (perf)
    const heroIO = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) tryPlay(); else reel.pause();
    }, { threshold: 0.15 });
    heroIO.observe(reel);

    // live timecode
    reel.addEventListener('timeupdate', () => {
      if (reelTC) reelTC.textContent = smpte(reel.currentTime || 0);
    });

    // sound toggle
    const setReelSound = (on) => {
      reel.muted = !on;
      const label = $('[data-label-sound]', reelBtn);
      if (on) { claimAudio(reel, reelStage); reelStage.classList.add('sound-on'); if (label) label.textContent = 'Mute showreel'; tryPlay(); }
      else    { releaseAudio(reel); reelStage.classList.remove('sound-on'); if (label) label.textContent = 'Play showreel with sound'; }
    };
    if (reelBtn) reelBtn.addEventListener('click', () => setReelSound(reel.muted));
    // clicking the reel itself also toggles sound
    reelStage.addEventListener('click', (e) => { if (e.target.closest('.hero__content')) return; setReelSound(reel.muted); });
  }

  /* ═══ VIDEO CARDS (work + reels) ══════════════════════ */
  $$('[data-video]').forEach((card) => {
    const frame = $('.vcard__frame', card);
    const video = $('video', card);
    const btnPlay = $('[data-play]', card);
    const btnMute = $('[data-mute]', card);
    const btnFull = $('[data-full]', card);
    const scrub   = $('[data-scrub]', card);
    const bar     = $('[data-progress]', card);
    const timeEl  = $('[data-time]', card);
    if (!video) return;

    let userPaused = false; // becomes true only if the user explicitly pauses

    /* lazy-load + autoplay when in view, pause when out (hybrid behaviour) */
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        ensureSrc(video);
        if (!userPaused) { const p = video.play(); if (p) p.catch(() => {}); }
      } else {
        video.pause();
        if (!video.muted) { video.muted = true; frame.classList.remove('sound-on'); releaseAudio(video); }
      }
    }, { threshold: 0.45 });
    io.observe(video);

    video.addEventListener('play',  () => frame.classList.add('playing'));
    video.addEventListener('pause', () => frame.classList.remove('playing'));

    /* progress + time */
    video.addEventListener('timeupdate', () => {
      if (video.duration) {
        const pct = (video.currentTime / video.duration) * 100;
        if (bar) bar.style.width = pct + '%';
        if (timeEl) timeEl.textContent = clock(video.currentTime);
      }
    });
    video.addEventListener('loadedmetadata', () => { if (timeEl) timeEl.textContent = clock(0); });

    /* play / pause */
    const togglePlay = () => {
      if (video.paused) { userPaused = false; ensureSrc(video); const p = video.play(); if (p) p.catch(() => {}); }
      else { userPaused = true; video.pause(); }
    };
    if (btnPlay) btnPlay.addEventListener('click', (e) => { e.stopPropagation(); togglePlay(); });

    /* mute / unmute (with single-audio manager) */
    const setSound = (on) => {
      video.muted = !on;
      if (on) { claimAudio(video, frame); frame.classList.add('sound-on'); if (video.paused) video.play().catch(() => {}); }
      else    { releaseAudio(video); frame.classList.remove('sound-on'); }
    };
    if (btnMute) btnMute.addEventListener('click', (e) => { e.stopPropagation(); setSound(video.muted); });

    /* fullscreen */
    if (btnFull) btnFull.addEventListener('click', (e) => {
      e.stopPropagation();
      const el = video;
      if (document.fullscreenElement) document.exitFullscreen();
      else if (el.requestFullscreen) { el.requestFullscreen(); video.muted = false; setSound(true); }
      else if (el.webkitEnterFullscreen) el.webkitEnterFullscreen(); // iOS
    });

    /* scrub bar seek */
    if (scrub) {
      const seek = (clientX) => {
        const r = scrub.getBoundingClientRect();
        const ratio = Math.min(1, Math.max(0, (clientX - r.left) / r.width));
        if (video.duration) video.currentTime = ratio * video.duration;
      };
      let dragging = false;
      scrub.addEventListener('pointerdown', (e) => { e.stopPropagation(); dragging = true; seek(e.clientX); });
      window.addEventListener('pointermove', (e) => { if (dragging) seek(e.clientX); });
      window.addEventListener('pointerup', () => { dragging = false; });
    }

    /* click the frame → desktop: toggle sound · touch: toggle play */
    const isTouch = window.matchMedia('(hover: none)').matches;
    frame.addEventListener('click', (e) => {
      if (e.target.closest('[data-controls]')) return; // let controls handle themselves
      if (isTouch) togglePlay();
      else setSound(video.muted);
    });

    /* desktop hover → unmute, leave → mute (only while in view) */
    if (!isTouch) {
      frame.addEventListener('mouseenter', () => { if (!video.paused) setSound(true); });
      frame.addEventListener('mouseleave', () => { setSound(false); });
    }
  });

  /* ═══ FOOTER live clock ═══════════════════════════════ */
  const clockEl = $('#clock');
  if (clockEl) {
    const tick = () => {
      const d = new Date();
      clockEl.textContent = `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    };
    tick();
    setInterval(tick, 1000);
  }

  /* ═══ DISCORD — copy handle to clipboard ═════════════════ */
  const dc = $('[data-discord]');
  if (dc) {
    const original = dc.textContent;
    dc.addEventListener('click', async () => {
      const handle = dc.dataset.discord;
      try { await navigator.clipboard.writeText(handle); }
      catch (e) {
        const t = document.createElement('textarea');
        t.value = handle; t.style.position = 'fixed'; t.style.opacity = '0';
        document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); } catch (_) {}
        t.remove();
      }
      dc.classList.add('copied');
      dc.textContent = 'Copied ✓ ' + handle;
      setTimeout(() => { dc.classList.remove('copied'); dc.textContent = original; }, 1800);
    });
  }

  /* ═══ CUSTOM CURSOR — branded crosshair over video frames ═
     Purely cosmetic. Disabled on touch / reduced-motion so it
     can never interfere with playback controls. */
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (finePointer && !prefersReduced) {
    const cursor = document.createElement('div');
    cursor.className = 'cutcursor';
    cursor.innerHTML = '<span class="cutcursor__x"></span><b>PLAY</b>';
    document.body.appendChild(cursor);
    document.body.classList.add('has-cutcursor');

    let cx = 0, cy = 0, shown = false, raf = 0;
    const render = () => {
      cursor.style.transform = `translate(${cx}px, ${cy}px) translate(-50%, -50%)`;
      raf = 0;
    };
    window.addEventListener('pointermove', (e) => {
      cx = e.clientX; cy = e.clientY;
      if (!raf) raf = requestAnimationFrame(render);
    }, { passive: true });

    $$('.vcard__frame').forEach((frame) => {
      frame.addEventListener('pointerenter', () => { shown = true; cursor.classList.add('on'); });
      frame.addEventListener('pointerleave', () => { shown = false; cursor.classList.remove('on'); });
      // reflect play state on the label
      const v = $('video', frame);
      if (v) {
        v.addEventListener('play',  () => { if (shown) cursor.querySelector('b').textContent = 'SOUND'; });
        v.addEventListener('pause', () => { cursor.querySelector('b').textContent = 'PLAY'; });
      }
    });
  }
})();
