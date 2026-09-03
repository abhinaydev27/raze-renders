/**
 * Portfolio Interactive Core
 * Abhinay Yadav — Independent Video Editor
 */

document.addEventListener('DOMContentLoaded', () => {
  // Enhanced Project Database
  const portfolioData = {
    // 1. Short-Form Video 1 (Reel) - Gaming Edit
    'reel-gaming': {
      id: 'reel-gaming',
      no: 'REEL 01',
      title: 'Gaming Velocity Montage',
      category: 'Gaming Highlights · 60 FPS',
      year: '2024',
      duration: '0:19 sec',
      aspectRatio: '16/9',
      role: 'Gaming Video Editor & SFX Designer',
      director: 'Abhinay (RaZe Renders)',
      metrics: '60 FPS · Sound Synced',
      synopsis: 'High-tempo gaming cut with sound-synced combat impacts, custom velocity speed ramps, and layered spatial audio.',
      details: 'Cut at 60 FPS with tight beat alignment, dynamic motion tracking, and impact camera shakes.',
      videoUrl: 'assets/videos/reel-gaming.mp4',
      poster: 'assets/images/reel-gaming.jpg'
    },

    // 2. Short-Form Video 2 (9:16 Reel) - MWM
    'reel-01': {
      id: 'reel-01',
      no: 'REEL 02',
      title: 'High-Retention Talking Head',
      category: 'Short-Form Reel · 60 FPS',
      year: '2024',
      duration: '1:08 min',
      aspectRatio: '9/16',
      role: 'Short-Form Video Editor & Sound Design',
      director: 'Abhinay (RaZe Renders)',
      metrics: '60 FPS · High Retention',
      synopsis: 'Dynamic talking head edit engineered for maximum retention with kinetic subtitle animations, pattern-interrupt b-roll, and crisp sound-sync.',
      details: 'Optimized for TikTok, Instagram Reels, and YouTube Shorts algorithms. Features micro-pacing with zero dead air and frame-accurate impact foley.',
      videoUrl: 'assets/videos/reel-01.mp4',
      poster: 'assets/images/reel-01-poster.jpg'
    },

    // 3. Short-Form Video 3 (9:16 Reel) - Meta Ad
    'reel-02': {
      id: 'reel-02',
      no: 'REEL 03',
      title: 'Direct Response Ad Creative',
      category: 'Paid Social · Performance Ad',
      year: '2024',
      duration: '1:31 min',
      aspectRatio: '9/16',
      role: 'Commercial Video Editor & Motion Designer',
      director: 'Abhinay (RaZe Renders)',
      metrics: '60 FPS · Direct Response',
      synopsis: 'High-converting performance marketing ad creative designed with fast 3-second hook variations, bold problem-solution text callouts, and clear CTA pacing.',
      details: 'Structured for paid Facebook, Instagram, and TikTok acquisition funnels to maintain high click-through rates and strong ROAS.',
      videoUrl: 'assets/videos/reel-02.mp4',
      poster: 'assets/images/reel-02-poster.jpg'
    },

    // 4. Short-Form Video 4 (9:16 Reel) - Anime Explainer
    'reel-03': {
      id: 'reel-03',
      no: 'REEL 04',
      title: 'Anime Explainer Short',
      category: 'Viral Storytelling · 60 FPS',
      year: '2024',
      duration: '0:51 sec',
      aspectRatio: '9/16',
      role: 'Video Essayist & Anime Editor',
      director: 'Abhinay (RaZe Renders)',
      metrics: '60 FPS · Viral Storytelling',
      synopsis: 'Fast-paced anime narrative breakdown analyzing pivotal story moments with beat-matched cutaways, voice sync, and high-impact sound design.',
      details: 'Crafted for anime and pop culture communities with seamless loop transitions and tension-building audio.',
      videoUrl: 'assets/videos/reel-03.mp4',
      poster: 'assets/images/reel-03-poster.jpg'
    },

    // 5. Long-Form Film 1 (16:9) - The Secret To The Nets (HIGHLIGHT 1)
    'film-01': {
      id: 'film-01',
      no: 'FEATURED 01',
      title: 'YouTube Cashcow & Documentary Essay',
      category: 'Faceless Storytelling / Sports Doc',
      year: '2024',
      duration: '1:33 min',
      aspectRatio: '16/9',
      role: 'Video Essayist & Lead Editor',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'A high-energy sports documentary breakdown analyzing tactical turnarounds, team chemistry, and high-stakes roster strategy.',
      details: 'Engineered for top-tier YouTube retention with dynamic player stat graphics, animated tactical overlays, fast voiceover pacing, and multi-track stadium sound foley.',
      videoUrl: 'assets/videos/film-01.mp4',
      poster: 'assets/images/film-01-poster.jpg'
    },

    // 6. Long-Form Film 2 (16:9) - Bharat Ke Veer (HIGHLIGHT 2)
    'film-02': {
      id: 'film-02',
      no: 'FEATURED 02',
      title: 'Historical Biography & Documentary',
      category: '4K Archival Historical Feature',
      year: '2024',
      duration: '19:15 min',
      aspectRatio: '16/9',
      role: 'Lead Documentary Editor & Post Supervisor',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'A grand historical documentary chronicling monumental leadership, strategic diplomacy, and enduring national legacy.',
      details: 'Features archival photo restoration, vintage paper & map route motion design, authentic historical sound architecture, and cinema color grading in Premiere Pro & After Effects.',
      videoUrl: 'assets/videos/doc-atal.mp4',
      poster: 'assets/images/doc-atal-poster.jpg'
    },

    // 7. Long-Form Film 3 (16:9) - B2B Brand Creative (HIGHLIGHT 3)
    'film-03': {
      id: 'film-03',
      no: 'FEATURED 03',
      title: 'B2B Brand Creative & Commercial',
      category: 'Corporate Storytelling / Brand Campaign',
      year: '2024',
      duration: '1:16 min',
      aspectRatio: '16/9',
      role: 'Commercial Editor & Sound Mixer',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'Polished B2B brand story cut for digital business campaigns, featuring clean kinetic typography, graphic lower-thirds, and authoritative corporate pacing.',
      details: 'High-framerate 50 FPS commercial cut delivering corporate value propositions clearly for digital ad campaigns and executive presentations.',
      videoUrl: 'assets/videos/film-03.mp4',
      poster: 'assets/images/film-03-poster.jpg'
    },

    // 8. Long-Form Film 4 (16:9) - Anime Explainer Long Form (HIGHLIGHT 4)
    'film-anime': {
      id: 'film-anime',
      no: 'FEATURED 04',
      title: 'Long-Form Anime Video Essay',
      category: 'Extended Narrative Essay / Deep Dive',
      year: '2024',
      duration: '5:00 min',
      aspectRatio: '16/9',
      role: 'Video Essayist & Story Editor',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'An atmospheric, deep-dive anime video essay exploring fictional post-apocalyptic realities, existential themes, and worldbuilding lore.',
      details: 'Paced with cinematic scene selection, immersive ambient sound design, custom title graphics, and seamless narrative progression.',
      videoUrl: 'assets/videos/doc-anime.mp4',
      poster: 'assets/images/doc-anime-poster.jpg'
    },

    // 9. Long-Form Film 5 (16:9) - Wedding Cinema
    'film-04': {
      id: 'film-04',
      no: 'FEATURED 05',
      title: 'Wedding Film & Color Grading',
      category: 'Wedding Cinema / Cinematic Teaser',
      year: '2024',
      duration: '0:31 min',
      aspectRatio: '16/9',
      role: 'Lead Video Editor & Colourist',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'A lyrical, acoustic slow-motion wedding film capturing intimate vows, festive celebration energy, and candid warmth in rich film tones.',
      details: 'Crafted with rhythmic acoustic pacing, gentle speed-ramped emotional beats, and warm Kodak film color grading in Premiere Pro & After Effects.',
      videoUrl: 'assets/videos/film-02.mp4',
      poster: 'assets/images/film-02-poster.jpg'
    }
  };

  // --- 1. Mobile Menu Drawer ---
  const menuToggle = document.getElementById('menuToggle');
  const mobileNav = document.getElementById('mobileNav');

  if (menuToggle && mobileNav) {
    menuToggle.addEventListener('click', () => {
      const isOpen = mobileNav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', isOpen);
      menuToggle.innerHTML = isOpen
        ? `<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16"></path><path d="M4 18h16"></path><path d="M4 6h16"></path></svg>`;
    });

    mobileNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 12h16"></path><path d="M4 18h16"></path><path d="M4 6h16"></path></svg>`;
      });
    });
  }

  // --- 2. Live 24fps Timecode Clock ---
  const timecodeEl = document.getElementById('liveTimecode');
  if (timecodeEl) {
    let frames = 0, seconds = 0, minutes = 0, hours = 0;
    setInterval(() => {
      frames = (frames + 1) % 24;
      if (frames === 0) {
        seconds = (seconds + 1) % 60;
        if (seconds === 0) {
          minutes = (minutes + 1) % 60;
          if (minutes === 0) hours = (hours + 1) % 24;
        }
      }
      const pad = n => String(n).padStart(2, '0');
      timecodeEl.textContent = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}:${pad(frames)}`;
    }, 1000 / 24);
  }

  // --- 3. Featured Inline Showreel Player Handler ---
  const inlineShowreelVideo = document.getElementById('inlineShowreelVideo');
  const inlineShowreelBtn = document.getElementById('inlineShowreelBtn');
  const inlineShowreelCard = document.getElementById('inlineShowreelCard');

  if (inlineShowreelBtn && inlineShowreelVideo && inlineShowreelCard) {
    inlineShowreelBtn.addEventListener('click', () => {
      if (inlineShowreelVideo.paused) {
        inlineShowreelVideo.play();
        inlineShowreelCard.classList.add('playing');
      } else {
        inlineShowreelVideo.pause();
        inlineShowreelCard.classList.remove('playing');
      }
    });

    inlineShowreelVideo.addEventListener('play', () => {
      inlineShowreelCard.classList.add('playing');
    });

    inlineShowreelVideo.addEventListener('pause', () => {
      inlineShowreelCard.classList.remove('playing');
    });
  }

  // Friendly URL Alias Map for Deep Linking
  const aliasMap = {
    'reel-01': 'reel-01', 'talkinghead': 'reel-01', 'talking-head': 'reel-01', 'mwm': 'reel-01', 'short1': 'reel-01',
    'reel-02': 'reel-02', 'ad': 'reel-02', 'meta-ad': 'reel-02', 'direct-response': 'reel-02', 'short2': 'reel-02',
    'reel-03': 'reel-03', 'anime-short': 'reel-03', 'manga': 'reel-03', 'short3': 'reel-03',
    'reel-gaming': 'reel-gaming', 'gaming': 'reel-gaming', 'montage': 'reel-gaming', 'roblox': 'reel-gaming', 'short4': 'reel-gaming',
    'film-01': 'film-01', 'nets': 'film-01', 'sports': 'film-01', 'cashcow': 'film-01', 'doc1': 'film-01',
    'film-02': 'film-02', 'doc-atal': 'film-02', 'atal': 'film-02', 'history': 'film-02', 'documentary': 'film-02', 'doc2': 'film-02',
    'film-03': 'film-03', 'b2b': 'film-03', 'commercial': 'film-03', 'corporate': 'film-03', 'doc3': 'film-03',
    'film-anime': 'film-anime', 'doc-anime': 'film-anime', 'anime': 'film-anime', 'anime-essay': 'film-anime', 'doc4': 'film-anime',
    'film-04': 'film-04', 'wedding': 'film-04', 'wedding-film': 'film-04', 'teaser': 'film-04', 'doc5': 'film-04'
  };

  // --- 4. Universal Video Modal with Deep Linking & Shareable URLs ---
  const modalBackdrop = document.getElementById('projectModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalHomeBtn = document.getElementById('modalHomeBtn');
  const modalBottomHomeBtn = document.getElementById('modalBottomHomeBtn');

  const modalTitle = document.getElementById('modalTitle');
  const modalNo = document.getElementById('modalNo');
  const modalType = document.getElementById('modalType');
  const modalYear = document.getElementById('modalYear');
  const modalRole = document.getElementById('modalRole');
  const modalDirector = document.getElementById('modalDirector');
  const modalCopy = document.getElementById('modalCopy');
  const modalDetails = document.getElementById('modalDetails');
  const modalMediaContainer = document.getElementById('modalMediaContainer');

  let currentOpenVideoId = null;

  function openMediaModal(rawId, updateHistory = true) {
    if (!rawId) return;
    const resolvedId = aliasMap[rawId.toLowerCase()] || rawId;
    const item = portfolioData[resolvedId];
    if (!item || !modalBackdrop) return;

    currentOpenVideoId = resolvedId;

    // Toggle vertical orientation for 9:16 Reels
    if (item.aspectRatio === '9/16') {
      modalBackdrop.classList.add('vertical-mode');
    } else {
      modalBackdrop.classList.remove('vertical-mode');
    }

    modalNo.textContent = item.no || 'PORTFOLIO';
    modalTitle.textContent = item.title;
    modalType.textContent = item.category || 'Video Project';
    modalYear.textContent = item.year || '2024';
    modalRole.textContent = item.role || 'Editor';
    modalDirector.textContent = item.director || 'Abhinay Yadav';
    modalCopy.textContent = item.synopsis || '';
    modalDetails.textContent = item.details || '';

    // Check if it's a direct HTML5 video file or embed
    const isDirectVideo = item.videoUrl && (
      item.videoUrl.endsWith('.mp4') || 
      item.videoUrl.endsWith('.webm') || 
      item.videoUrl.endsWith('.mov') ||
      item.videoUrl.startsWith('assets/videos/')
    );

    if (isDirectVideo) {
      modalMediaContainer.innerHTML = `
        <video controls autoplay playsinline preload="auto" poster="${item.poster || ''}">
          <source src="${item.videoUrl}" type="video/mp4">
          Your browser does not support video tag.
        </video>
      `;
    } else if (item.videoUrl) {
      modalMediaContainer.innerHTML = `
        <iframe src="${item.videoUrl}" 
                title="${item.title}" 
                frameborder="0" 
                allow="autoplay; fullscreen; picture-in-picture" 
                allowfullscreen>
        </iframe>
      `;
    } else {
      modalMediaContainer.innerHTML = `
        <img src="${item.poster}" alt="${item.title}">
      `;
    }

    modalBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Update browser URL state with deep link ?v=...
    if (updateHistory) {
      const newUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}?v=${resolvedId}`;
      window.history.pushState({ videoId: resolvedId }, '', newUrl);
    }
  }

  function closeMediaModal(updateHistory = true) {
    if (!modalBackdrop) return;
    modalBackdrop.classList.remove('active');
    document.body.style.overflow = '';
    
    // Stop audio/video playback immediately
    if (modalMediaContainer) {
      modalMediaContainer.innerHTML = '';
    }

    // Reset URL back to base homepage if closed
    if (updateHistory && currentOpenVideoId) {
      const cleanUrl = `${window.location.protocol}//${window.location.host}${window.location.pathname}`;
      window.history.pushState(null, '', cleanUrl);
    }
    currentOpenVideoId = null;
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', () => closeMediaModal(true));
  if (modalHomeBtn) modalHomeBtn.addEventListener('click', () => closeMediaModal(true));
  if (modalBottomHomeBtn) modalBottomHomeBtn.addEventListener('click', () => closeMediaModal(true));

  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', e => {
      if (e.target === modalBackdrop) closeMediaModal(true);
    });
  }

  window.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modalBackdrop?.classList.contains('active')) {
      closeMediaModal(true);
    }
  });

  // Handle browser Back / Forward navigation (PopState)
  window.addEventListener('popstate', e => {
    if (e.state && e.state.videoId) {
      openMediaModal(e.state.videoId, false);
    } else {
      closeMediaModal(false);
    }
  });

  // Attach triggers for all video items in DOM
  document.querySelectorAll('[data-video-id]').forEach(element => {
    const videoId = element.getAttribute('data-video-id');
    element.addEventListener('click', e => {
      e.preventDefault();
      openMediaModal(videoId, true);
    });
    element.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openMediaModal(videoId, true);
      }
    });
  });

  // Check URL on page load for direct video links (e.g. ?v=reel-01, ?watch=wedding, #film-01)
  function checkUrlDeepLink() {
    try {
      const params = new URLSearchParams(window.location.search);
      let targetId = params.get('v') || params.get('video') || params.get('watch') || params.get('id');
      
      const hash = window.location.hash ? window.location.hash.replace('#', '').trim() : '';
      if (!targetId && hash) {
        if (hash.startsWith('v=') || hash.startsWith('video=') || hash.startsWith('watch=')) {
          targetId = hash.split('=')[1];
        } else if (aliasMap[hash.toLowerCase()] || portfolioData[hash]) {
          targetId = hash;
        }
      }

      if (targetId) {
        const resolvedId = aliasMap[targetId.toLowerCase()] || targetId;
        if (portfolioData[resolvedId]) {
          setTimeout(() => {
            openMediaModal(resolvedId, false);
          }, 200);
        }
      }
    } catch (e) {
      console.warn('Deep link parse error:', e);
    }
  }

  checkUrlDeepLink();

  // --- 5. Scrollspy for Active Navbar State ---
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.desktop-nav a');

  function updateActiveNav() {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 140;
      const sectionId = current.getAttribute('id');

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav);

  // --- 6. Contact Form Processing (Direct to Gmail Inbox & WhatsApp) ---
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');
  const sendWhatsAppBtn = document.getElementById('sendWhatsAppBtn');

  if (contactForm && formStatus) {
    contactForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const name = contactForm.querySelector('[name="name"]')?.value.trim();
      const email = contactForm.querySelector('[name="email"]')?.value.trim();
      const project = contactForm.querySelector('[name="project"]')?.value.trim();
      const message = contactForm.querySelector('[name="message"]')?.value.trim();

      if (!name || !email || !message) {
        formStatus.textContent = 'Please fill out all required fields.';
        formStatus.style.color = 'var(--red)';
        return;
      }

      const originalBtnText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Sending Enquiry...';
      formStatus.textContent = 'Delivering message to Abhinay...';
      formStatus.style.color = 'var(--text-dim)';

      try {
        const formData = new FormData(contactForm);
        const response = await fetch('https://formsubmit.co/ajax/abhinaydev27@gmail.com', {
          method: 'POST',
          headers: {
            'Accept': 'application/json'
          },
          body: formData
        });

        const result = await response.json().catch(() => ({}));

        if (response.ok || result.success === "true" || result.success === true) {
          formStatus.innerHTML = `✓ Thank you, ${name}! Your project enquiry has been sent directly to <strong>abhinaydev27@gmail.com</strong>. I will reply within 24 hours.`;
          formStatus.style.color = '#4ade80';
          contactForm.reset();
        } else {
          // If AJAX response is not ok, submit form natively without opening mail app
          contactForm.submit();
        }
      } catch (err) {
        // Submit directly via browser POST to FormSubmit
        contactForm.submit();
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    });
  }

  // Direct WhatsApp Quick Submit
  if (sendWhatsAppBtn && contactForm) {
    sendWhatsAppBtn.addEventListener('click', () => {
      const name = contactForm.querySelector('[name="name"]')?.value.trim() || 'Client';
      const email = contactForm.querySelector('[name="email"]')?.value.trim() || 'Not specified';
      const project = contactForm.querySelector('[name="project"]')?.value.trim() || 'Video Project';
      const message = contactForm.querySelector('[name="message"]')?.value.trim() || 'Hi Abhinay, I want to discuss a video project.';

      const waText = encodeURIComponent(
        `🎬 *RaZe Renders Project Enquiry*\n\n*Name:* ${name}\n*Email:* ${email}\n*Project Type:* ${project}\n\n*Brief & Timeline:*\n${message}`
      );
      window.open(`https://wa.me/919520760443?text=${waText}`, '_blank');
    });
  }
});
