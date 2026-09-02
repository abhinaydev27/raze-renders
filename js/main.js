/**
 * Portfolio Interactive Core
 * Abhinay Yadav — Independent Video Editor
 */

document.addEventListener('DOMContentLoaded', () => {
  // Enhanced Project Database
  const portfolioData = {
    // 1. Short-Form Video 1 (9:16 Reel) - MWM
    'reel-01': {
      id: 'reel-01',
      no: 'REEL 01',
      title: 'MWM · High Retention Edit',
      category: 'Talking Head / High Retention Cut',
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

    // 2. Short-Form Video 2 (9:16 Reel) - Meta Ad
    'reel-02': {
      id: 'reel-02',
      no: 'REEL 02',
      title: 'Direct Response · Meta Ad Creative',
      category: 'Paid Social / Performance Ad',
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

    // 3. Short-Form Video 3 (9:16 Reel) - Anime Explainer
    'reel-03': {
      id: 'reel-03',
      no: 'REEL 03',
      title: 'Halkenburg · Anime Breakdown',
      category: 'Anime Explainer / Viral Short',
      year: '2024',
      duration: '0:51 sec',
      aspectRatio: '9/16',
      role: 'Video Essayist & Anime Editor',
      director: 'Abhinay (RaZe Renders)',
      metrics: '60 FPS · Viral Storytelling',
      synopsis: 'Fast-paced anime narrative breakdown analyzing pivotal Hunter x Hunter plot twists with beat-matched cutaways, voice sync, and high-impact sound design.',
      details: 'Crafted for anime and pop culture communities with seamless loop transitions and tension-building audio.',
      videoUrl: 'assets/videos/reel-03.mp4',
      poster: 'assets/images/reel-03-poster.jpg'
    },

    // 4. Short-Form Video 4 (9:16 Reel) - Gaming Edit
    'reel-gaming': {
      id: 'reel-gaming',
      no: 'REEL 04',
      title: 'Clutch · Gaming Breakdown',
      category: 'Gaming Highlights / High Intensity',
      year: '2024',
      duration: '0:30 sec',
      aspectRatio: '9/16',
      role: 'Gaming Video Editor & SFX Designer',
      director: 'Abhinay (RaZe Renders)',
      metrics: 'High Impact · Sound Synced',
      synopsis: 'Intense, beat-synced gaming highlights montage cut with impact camera shakes, velocity speed ramps, and multi-layered combat sound effects.',
      details: 'Designed for esports channels and gaming community feeds to deliver maximum punch in under 30 seconds.',
      videoUrl: 'assets/videos/reel-gaming.mp4',
      poster: 'assets/images/reel-gaming.jpg'
    },

    // 5. Long-Form Film 1 (16:9) - The Secret To The Nets (HIGHLIGHT 1)
    'film-01': {
      id: 'film-01',
      no: 'FEATURED 01',
      title: 'The Secret To The Nets',
      category: 'Sports Documentary / YouTube Cashcow',
      year: '2024',
      duration: '1:33 min',
      aspectRatio: '16/9',
      role: 'Video Essayist & Lead Editor',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'A high-energy sports documentary breakdown analyzing the tactical turnaround, team chemistry, and high-stakes roster moves behind the Brooklyn Nets.',
      details: 'Engineered for top-tier YouTube retention with dynamic player stat graphics, animated tactical overlays, fast voiceover pacing, and multi-track stadium sound foley.',
      videoUrl: 'assets/videos/film-01.mp4',
      poster: 'assets/images/film-01-poster.jpg'
    },

    // 6. Long-Form Film 2 (16:9) - Bharat Ke Veer (HIGHLIGHT 2)
    'film-02': {
      id: 'film-02',
      no: 'FEATURED 02',
      title: 'Bharat Ke Veer: Atal Bihari Vajpayee',
      category: '4K Historical Biography Documentary',
      year: '2024',
      duration: '19:15 min',
      aspectRatio: '16/9',
      role: 'Lead Documentary Editor & Post Supervisor',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'A grand historical documentary chronicling the monumental life, diplomatic milestones, and enduring national legacy of Atal Bihari Vajpayee.',
      details: 'Features archival photo restoration, vintage paper & map route motion design, authentic historical sound architecture, and cinema color grading in Premiere Pro & After Effects.',
      videoUrl: 'assets/videos/doc-atal.mp4',
      poster: 'assets/images/doc-atal-poster.jpg'
    },

    // 7. Long-Form Film 3 (16:9) - B2B Brand Creative (HIGHLIGHT 3)
    'film-03': {
      id: 'film-03',
      no: 'FEATURED 03',
      title: 'B2B Brand Creative · Campaign',
      category: 'B2B Commercial / Corporate Storytelling',
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
      title: 'Every World Where Humanity Was Completely Erased',
      category: 'Long-Form Anime Essay / Fiction Deep Dive',
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
      title: 'Eternal Vows · Wedding Cinema',
      category: 'Wedding Cinema / Cinematic Teaser',
      year: '2024',
      duration: '0:31 min',
      aspectRatio: '16/9',
      role: 'Lead Video Editor & Colourist',
      director: 'Abhinay (RaZe Renders)',
      synopsis: 'A lyrical, emotional wedding film capturing intimate vows, heritage rituals, and candid warmth in rich film tones.',
      details: 'Crafted with rhythmic acoustic pacing, gentle speed-ramped emotional beats, and warm Kodak film color grading in Premiere Pro.',
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
