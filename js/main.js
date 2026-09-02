/**
 * Portfolio Interactive Core
 * Abhinay Yadav — Independent Video Editor
 */

document.addEventListener('DOMContentLoaded', () => {
  // Enhanced Project Database
  const portfolioData = {
    // 1. Featured Master Showcase (4K Historical Documentary)
    'showreel': {
      id: 'showreel',
      no: 'FEATURED MASTERPIECE',
      title: 'Bharat Ke Veer: Atal Bihari Vajpayee',
      category: '4K Historical Biography Documentary',
      year: '2024',
      duration: '19:15 min',
      aspectRatio: '16/9',
      role: 'Lead Documentary Editor & Post Supervisor',
      director: 'Abhinay Yadav',
      synopsis: 'A grand, sweeping historical biography chronicling the monumental leadership, strategic diplomacy, and enduring legacy of Atal Bihari Vajpayee.',
      details: 'Features archival photo restoration, multi-layered historical audio foley, map animations, and cinematic color grading in DaVinci Resolve.',
      videoUrl: 'assets/videos/doc-atal.mp4',
      poster: 'assets/images/doc-atal-poster.jpg'
    },

    // 2. Short-Form Video 1 (9:16 Reel) - MWM
    'reel-01': {
      id: 'reel-01',
      no: 'REEL 01',
      title: 'MWM · High Retention Edit',
      category: 'Short-Form Reel / Fast Paced',
      year: '2024',
      duration: '1:08 min',
      aspectRatio: '9/16',
      role: 'Short-Form Video Editor & Sound Design',
      director: 'Abhinay Yadav',
      metrics: '60 FPS · High Retention',
      synopsis: 'Dynamic, retention-engineered vertical short with kinetic sound design, micro-pacing, and punchy cuts.',
      details: 'Optimized for high-retention social distribution on Instagram Reels, TikTok, and YouTube Shorts. Features synchronized foley and frame-accurate cuts.',
      videoUrl: 'assets/videos/reel-01.mp4',
      poster: 'assets/images/reel-01-poster.jpg'
    },

    // 3. Short-Form Video 2 (9:16 Reel) - Meta Ad
    'reel-02': {
      id: 'reel-02',
      no: 'REEL 02',
      title: 'Direct Response · Meta Ad Creative',
      category: 'Paid Social / Meta Ad',
      year: '2024',
      duration: '1:31 min',
      aspectRatio: '9/16',
      role: 'Commercial Video Editor & Motion Designer',
      director: 'Abhinay Yadav',
      metrics: '60 FPS · Conversion Focused',
      synopsis: 'High-converting direct-response Meta Ad engineered with rapid pattern interrupts, dynamic text overlays, and strong CTA hooks.',
      details: 'Crafted specifically for performance marketing campaigns on Facebook, Instagram, and TikTok with high CTR pacing.',
      videoUrl: 'assets/videos/reel-02.mp4',
      poster: 'assets/images/reel-02-poster.jpg'
    },

    // 4. Short-Form Video 3 (9:16 Reel) - Anime Explainer
    'reel-03': {
      id: 'reel-03',
      no: 'REEL 03',
      title: 'Halkenburg · Anime Explainer',
      category: 'Anime Explainer / Viral Short',
      year: '2024',
      duration: '0:51 sec',
      aspectRatio: '9/16',
      role: 'Video Essayist & Anime Editor',
      director: 'Abhinay Yadav',
      metrics: '60 FPS · Viral Storytelling',
      synopsis: 'Engaging, fast-paced anime breakdown analyzing pivotal story moments with beat-sync transitions and punchy sound design.',
      details: 'Tailored for anime and entertainment communities with seamless loop transitions and dynamic sound staging.',
      videoUrl: 'assets/videos/reel-03.mp4',
      poster: 'assets/images/reel-03-poster.jpg'
    },

    // 5. Short-Form Video 4 (9:16 Reel) - Gaming Edit
    'reel-gaming': {
      id: 'reel-gaming',
      no: 'REEL 04',
      title: 'Clutch · Gaming Edit',
      category: 'Gaming Breakdown / High Intensity',
      year: '2024',
      duration: '0:30 sec',
      aspectRatio: '9/16',
      role: 'Gaming Video Editor & SFX Designer',
      director: 'Abhinay (RaZe Renders)',
      metrics: 'High Impact · Sound Synced',
      synopsis: 'Intense, beat-synced gaming highlights cut with impact camera shakes, slow-motion speed ramps, and layered combat sound design.',
      details: 'Crafted for esports creators and gaming community engagement with rapid jump cuts and punchy audio.',
      videoUrl: 'assets/videos/reel-gaming.mp4',
      poster: 'assets/images/reel-gaming.jpg'
    },

    // 5. Long-Form Film 1 (16:9) - The Secret To The Nets
    'film-01': {
      id: 'film-01',
      no: 'DOCUMENTARY 01',
      title: 'The Secret To The Nets',
      category: 'Documentary Essay / YouTube Cashcow',
      year: '2024',
      duration: '1:33 min',
      aspectRatio: '16/9',
      role: 'Video Essayist & Post-Production Editor',
      director: 'Abhinay Yadav',
      synopsis: 'A fast-paced sports documentary breakdown analyzing the tactical turnaround, team chemistry, and high-stakes strategy behind the Brooklyn Nets.',
      details: 'Features dynamic map animations, sound foley layering, motion graphic stat cards, jump-cuts, and color grading tailored for high-retention YouTube audiences.',
      videoUrl: 'assets/videos/film-01.mp4',
      poster: 'assets/images/film-01-poster.jpg'
    },

    // 6. Long-Form Film 2 (16:9) - Bharat Ke Veer
    'film-02': {
      id: 'film-02',
      no: 'DOCUMENTARY 02',
      title: 'Bharat Ke Veer: Atal Bihari Vajpayee',
      category: 'Historical Biography Featurette',
      year: '2024',
      duration: '19:15 min',
      aspectRatio: '16/9',
      role: 'Lead Documentary Editor & Post Supervisor',
      director: 'Abhinay Yadav',
      synopsis: 'A grand historical documentary chronicles the monumental life, diplomacy, and enduring legacy of Atal Bihari Vajpayee.',
      details: '4K archival restoration with multi-layered foley, narrative pacing, and cinema grade in DaVinci Resolve.',
      videoUrl: 'assets/videos/doc-atal.mp4',
      poster: 'assets/images/doc-atal-poster.jpg'
    },

    // 7. Long-Form Film 3 (16:9) - B2B Brand Creative
    'film-03': {
      id: 'film-03',
      no: 'COMMERCIAL 03',
      title: 'B2B Brand Creative · Campaign',
      category: 'B2B Commercial / Brand Story',
      year: '2024',
      duration: '1:16 min',
      aspectRatio: '16/9',
      role: 'Commercial Editor & Sound Mixer',
      director: 'Abhinay Yadav',
      synopsis: 'Polished B2B commercial cut with crisp motion graphics, professional sound staging, and clean brand messaging.',
      details: 'High framerate 50fps corporate story cut for digital business campaigns and conference presentations.',
      videoUrl: 'assets/videos/film-03.mp4',
      poster: 'assets/images/film-03-poster.jpg'
    },

    // 8. Long-Form Film 4 (16:9) - Wedding Cinema
    'film-04': {
      id: 'film-04',
      no: 'CINEMA 04',
      title: 'Eternal Vows · Wedding Cinema',
      category: 'Wedding Cinema / Cinematic Teaser',
      year: '2024',
      duration: '0:31 min',
      aspectRatio: '16/9',
      role: 'Lead Video Editor & Colourist',
      director: 'Abhinay Yadav',
      synopsis: 'A lyrical, emotional wedding film capturing intimate vows, heritage rituals, and candid warmth in rich film tones.',
      details: 'Crafted with rhythmic acoustic pacing, gentle speed-ramped emotional beats, and warm Kodak film color grading in DaVinci Resolve.',
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

  // --- 4. Universal Video Modal (16:9 & 9:16 Smart Responsive) ---
  const modalBackdrop = document.getElementById('projectModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalTitle = document.getElementById('modalTitle');
  const modalNo = document.getElementById('modalNo');
  const modalType = document.getElementById('modalType');
  const modalYear = document.getElementById('modalYear');
  const modalRole = document.getElementById('modalRole');
  const modalDirector = document.getElementById('modalDirector');
  const modalCopy = document.getElementById('modalCopy');
  const modalDetails = document.getElementById('modalDetails');
  const modalMediaContainer = document.getElementById('modalMediaContainer');

  function openMediaModal(itemId) {
    const item = portfolioData[itemId];
    if (!item || !modalBackdrop) return;

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
    modalCloseBtn?.focus();
  }

  function closeMediaModal() {
    if (!modalBackdrop) return;
    modalBackdrop.classList.remove('active');
    document.body.style.overflow = '';
    // Stop audio/video immediately on close
    if (modalMediaContainer) {
      modalMediaContainer.innerHTML = '';
    }
  }

  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeMediaModal);

  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', e => {
      if (e.target === modalBackdrop) closeMediaModal();
    });
  }

  window.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modalBackdrop?.classList.contains('active')) {
      closeMediaModal();
    }
  });

  // Attach triggers for all video items
  document.querySelectorAll('[data-video-id]').forEach(element => {
    const videoId = element.getAttribute('data-video-id');
    element.addEventListener('click', e => {
      e.preventDefault();
      openMediaModal(videoId);
    });
    element.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openMediaModal(videoId);
      }
    });
  });

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

  // --- 6. Contact Form Processing & Mailto ---
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');

  if (contactForm && formStatus) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const name = contactForm.querySelector('[name="name"]')?.value.trim();
      const email = contactForm.querySelector('[name="email"]')?.value.trim();
      const project = contactForm.querySelector('[name="project"]')?.value.trim();
      const message = contactForm.querySelector('[name="message"]')?.value.trim();

      if (!name || !email || !message) {
        formStatus.textContent = 'Please fill out all required fields.';
        return;
      }

      formStatus.textContent = 'Opening email draft...';

      const subject = encodeURIComponent(`Project Collaboration Enquiry: ${project || 'Video Editing'} - ${name}`);
      const body = encodeURIComponent(
        `Hi Abhinay,\n\nName: ${name}\nEmail: ${email}\nProject Type: ${project}\n\nProject Brief & Timeline:\n${message}\n\nSent via your portfolio website.`
      );
      const mailtoUrl = `mailto:abhinaydev27@gmail.com?subject=${subject}&body=${body}`;

      setTimeout(() => {
        formStatus.innerHTML = `✓ Thank you, ${name}! If your email client didn't open automatically, <a href="${mailtoUrl}" style="color:#fff;text-decoration:underline;font-weight:600;">click here to send directly</a>.`;
        window.location.href = mailtoUrl;
        setTimeout(() => contactForm.reset(), 3500);
      }, 400);
    });
  }
});
