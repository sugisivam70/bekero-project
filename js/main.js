/* ============================================
   BAKERO — Animation & Interaction System
   GSAP + ScrollTrigger + Lenis
   ============================================ */

(function () {
  'use strict';

  // ---------- Register GSAP Plugins ----------
  gsap.registerPlugin(ScrollTrigger);

  // ---------- Lenis Smooth Scrolling ----------
  let lenis;

  function initLenis() {
    lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    });

    // Sync Lenis with GSAP ScrollTrigger
    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
      lenis.raf(time * 1000);
    });

    gsap.ticker.lagSmoothing(0);
  }

  // ---------- Preloader ----------
  function initPreloader() {
    const preloader = document.querySelector('.preloader');
    const barInner = document.querySelector('.preloader__bar-inner');
    if (!preloader) {
      initPageAnimations();
      return;
    }

    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 20 + 10;
      if (progress > 100) progress = 100;
      if (barInner) barInner.style.width = progress + '%';
      if (progress >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          preloader.classList.add('loaded');
          document.body.style.overflow = '';
          initPageAnimations();
        }, 300);
      }
    }, 80);

    // Safety fallback to guarantee preloader dismisses
    setTimeout(() => {
      if (!preloader.classList.contains('loaded')) {
        clearInterval(interval);
        preloader.classList.add('loaded');
        document.body.style.overflow = '';
        initPageAnimations();
      }
    }, 1500);
  }

  // ---------- Navigation ----------
  function initNavigation() {
    const nav = document.querySelector('.nav');
    const hamburger = document.querySelector('.nav__hamburger');
    const mobileMenu = document.querySelector('.nav__mobile-menu');
    if (!nav) return;

    // Scroll behavior: transparent → solid
    const heroSection = document.querySelector('.hero-cinematic, .hero, .page-hero');
    const heroHeight = heroSection ? heroSection.offsetHeight * 0.25 : 100;

    function updateNav() {
      const scrollY = window.scrollY || window.pageYOffset;
      if (scrollY > heroHeight) {
        nav.classList.remove('nav--transparent');
        nav.classList.add('nav--solid');
      } else {
        nav.classList.add('nav--transparent');
        nav.classList.remove('nav--solid');
      }
    }

    // If hero exists, start transparent
    if (heroSection) {
      nav.classList.add('nav--transparent');
    } else {
      nav.classList.add('nav--solid');
    }

    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();

    // Mobile menu
    if (hamburger && mobileMenu) {
      hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
      });

      // Close mobile menu on link click
      mobileMenu.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', () => {
          hamburger.classList.remove('active');
          mobileMenu.classList.remove('active');
          document.body.style.overflow = '';
        });
      });
    }
  }

  // ---------- Page Animations ----------
  function initPageAnimations() {
    initHeroAnimation();
    initScrollAnimations();
    initImageReveals();
    initParallax();
    initMarquee();
    initCinematicSection();
    initProductInteractions();
    initCounterAnimation();
  }

  // ---------- Hero Animation ----------
  function initHeroAnimation() {
    const heroCinematic = document.querySelector('.hero-cinematic');
    if (heroCinematic) {
      const bg = heroCinematic.querySelector('.hero-cinematic__bg');
      const badge = heroCinematic.querySelector('[data-hero-animate="badge"]');
      const title = heroCinematic.querySelector('[data-hero-animate="title"]');
      const subtitle = heroCinematic.querySelector('[data-hero-animate="subtitle"]');
      const cta = heroCinematic.querySelector('[data-hero-animate="cta"]');
      const stats = heroCinematic.querySelector('[data-hero-animate="stats"]');

      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

      // Initial state
      gsap.set([badge, title, subtitle, cta, stats].filter(Boolean), {
        opacity: 0,
        y: 40,
      });
      if (bg) {
        gsap.set(bg, { scale: 1.15, filter: 'brightness(0.7)' });
      }

      // Entrance Sequence
      if (bg) {
        tl.to(bg, { scale: 1.06, filter: 'brightness(1)', duration: 2.0, ease: 'power2.out' }, 0);
      }
      if (badge) tl.to(badge, { opacity: 1, y: 0, duration: 0.8 }, 0.25);
      if (title) tl.to(title, { opacity: 1, y: 0, duration: 1.1 }, 0.45);
      if (subtitle) tl.to(subtitle, { opacity: 1, y: 0, duration: 0.9 }, 0.7);
      if (cta) tl.to(cta, { opacity: 1, y: 0, duration: 0.8 }, 0.9);
      if (stats) tl.to(stats, { opacity: 1, y: 0, duration: 0.9 }, 1.1);

      // Continuous subtle ambient drift
      if (bg) {
        gsap.to(bg, {
          scale: 1.12,
          duration: 20,
          ease: 'sine.inOut',
          repeat: -1,
          yoyo: true,
        });

        // Parallax on scroll
        gsap.to(bg, {
          yPercent: 18,
          ease: 'none',
          scrollTrigger: {
            trigger: heroCinematic,
            start: 'top top',
            end: 'bottom top',
            scrub: true,
          },
        });
      }
      return;
    }

    const hero = document.querySelector('.hero');
    if (!hero) return;

    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    const heroBadge = hero.querySelector('.hero__badge, .hero__label');
    const heroTitle = hero.querySelector('.hero__title');
    const heroSubtitle = hero.querySelector('.hero__subtitle');
    const heroCTA = hero.querySelector('.hero__cta, .hero__cta-group');
    const heroImage = hero.querySelector('.hero__image-wrapper');
    const heroStats = hero.querySelector('.hero__stats');

    const elementsToAnimate = [heroBadge, heroTitle, heroSubtitle, heroCTA, heroImage, heroStats].filter(Boolean);

    tl.set(elementsToAnimate, {
      opacity: 0,
      y: 35,
    });

    if (heroBadge) tl.to(heroBadge, { opacity: 1, y: 0, duration: 0.8 }, 0.2);
    if (heroTitle) tl.to(heroTitle, { opacity: 1, y: 0, duration: 1 }, 0.35);
    if (heroSubtitle) tl.to(heroSubtitle, { opacity: 1, y: 0, duration: 0.8 }, 0.6);
    if (heroCTA) tl.to(heroCTA, { opacity: 1, y: 0, duration: 0.8 }, 0.75);
    if (heroImage) tl.to(heroImage, { opacity: 1, y: 0, duration: 1.1 }, 0.5);
    if (heroStats) tl.to(heroStats, { opacity: 1, y: 0, duration: 0.9 }, 0.9);

    // Hero image slow zoom
    if (heroImage) {
      const img = heroImage.querySelector('img');
      if (img) {
        gsap.to(img, {
          scale: 1.08,
          duration: 16,
          ease: 'sine.inOut',
          repeat: -1,
          yoyo: true,
        });
      }
    }
  }

  // ---------- Scroll-Triggered Animations ----------
  function initScrollAnimations() {
    // Fade-up elements
    const fadeUpElements = document.querySelectorAll('[data-animate="fade-up"]');
    fadeUpElements.forEach((el, i) => {
      gsap.fromTo(
        el,
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.9,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
        }
      );
    });

    // Fade-in elements
    const fadeInElements = document.querySelectorAll('[data-animate="fade-in"]');
    fadeInElements.forEach((el) => {
      gsap.fromTo(
        el,
        { opacity: 0 },
        {
          opacity: 1,
          duration: 1,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
        }
      );
    });

    // Scale-in elements
    const scaleElements = document.querySelectorAll('[data-animate="scale-in"]');
    scaleElements.forEach((el) => {
      gsap.fromTo(
        el,
        { opacity: 0, scale: 0.92 },
        {
          opacity: 1,
          scale: 1,
          duration: 1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
        }
      );
    });

    // Stagger groups
    const staggerGroups = document.querySelectorAll('[data-stagger]');
    staggerGroups.forEach((group) => {
      const children = group.children;
      gsap.fromTo(
        children,
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: group,
            start: 'top 80%',
            toggleActions: 'play none none none',
          },
        }
      );
    });

    // Clip-up animations
    const clipElements = document.querySelectorAll('[data-animate="clip-up"]');
    clipElements.forEach((el) => {
      gsap.fromTo(
        el,
        { clipPath: 'inset(100% 0 0 0)' },
        {
          clipPath: 'inset(0% 0 0 0)',
          duration: 1.2,
          ease: 'power3.inOut',
          scrollTrigger: {
            trigger: el,
            start: 'top 80%',
            toggleActions: 'play none none none',
          },
        }
      );
    });

    // Line-reveal text
    const lineReveals = document.querySelectorAll('.line-reveal');
    lineReveals.forEach((el) => {
      gsap.fromTo(
        el,
        { y: '100%', opacity: 0 },
        {
          y: '0%',
          opacity: 1,
          duration: 1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: el.parentElement || el,
            start: 'top 85%',
            toggleActions: 'play none none none',
          },
        }
      );
    });
  }

  // ---------- Image Reveals ----------
  function initImageReveals() {
    const reveals = document.querySelectorAll('.img-reveal');
    reveals.forEach((el) => {
      ScrollTrigger.create({
        trigger: el,
        start: 'top 80%',
        onEnter: () => el.classList.add('revealed'),
        once: true,
      });
    });
  }

  // ---------- Parallax Effects ----------
  function initParallax() {
    // The cinematic hero owns its scroll parallax in initHeroAnimation().
    // Excluding it here prevents two ScrollTriggers from competing to update
    // the same transform while the page scrolls.
    const parallaxImages = document.querySelectorAll(
      '[data-parallax]:not(.hero-cinematic__bg)'
    );
    parallaxImages.forEach((el) => {
      const speed = parseFloat(el.dataset.parallax) || 0.2;
      gsap.to(el, {
        yPercent: speed * 100,
        ease: 'none',
        scrollTrigger: {
          trigger: el.parentElement || el,
          start: 'top bottom',
          end: 'bottom top',
          scrub: 1,
        },
      });
    });

    // Cinematic bg zoom
    const cinematicBgs = document.querySelectorAll('.cinematic__bg img');
    cinematicBgs.forEach((img) => {
      gsap.fromTo(
        img,
        { scale: 1.15 },
        {
          scale: 1,
          ease: 'none',
          scrollTrigger: {
            trigger: img.closest('.cinematic'),
            start: 'top bottom',
            end: 'bottom top',
            scrub: 1.5,
          },
        }
      );
    });
  }

  // ---------- Marquee ----------
  function initMarquee() {
    const tracks = document.querySelectorAll('.marquee__track');
    tracks.forEach((track) => {
      // Duplicate items for seamless loop
      const items = track.innerHTML;
      track.innerHTML = items + items;
    });
  }

  // ---------- Cinematic Section ----------
  function initCinematicSection() {
    const cinematics = document.querySelectorAll('.cinematic');
    cinematics.forEach((section) => {
      const content = section.querySelector('.cinematic__content');
      if (content) {
        gsap.fromTo(
          content.children,
          { opacity: 0, y: 40 },
          {
            opacity: 1,
            y: 0,
            duration: 1,
            stagger: 0.2,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: section,
              start: 'top 60%',
              toggleActions: 'play none none none',
            },
          }
        );
      }
    });
  }

  // ---------- Product Interactions ----------
  function initProductInteractions() {
    const cards = document.querySelectorAll('.product-card, .category-card');
    cards.forEach((card) => {
      card.addEventListener('mouseenter', () => {
        gsap.to(card, { y: -4, duration: 0.4, ease: 'power2.out' });
      });
      card.addEventListener('mouseleave', () => {
        gsap.to(card, { y: 0, duration: 0.4, ease: 'power2.out' });
      });
    });
  }

  // ---------- Counter Animation ----------
  function initCounterAnimation() {
    const counters = document.querySelectorAll('[data-counter]');
    counters.forEach((counter) => {
      const target = parseInt(counter.dataset.counter, 10);
      const suffix = counter.dataset.suffix || '';
      const prefix = counter.dataset.prefix || '';

      ScrollTrigger.create({
        trigger: counter,
        start: 'top 80%',
        once: true,
        onEnter: () => {
          gsap.to(counter, {
            duration: 2.2,
            ease: 'power2.out',
            onUpdate: function () {
              const progress = this.progress();
              const val = Math.round(target * progress);
              counter.textContent = prefix + val.toLocaleString() + suffix;
            },
          });
        },
      });
    });
  }

  // ---------- Form Validation ----------
  function initFormValidation() {
    const form = document.querySelector('.contact-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let valid = true;

      // Clear previous errors
      form.querySelectorAll('.form-group').forEach((group) => {
        group.classList.remove('error');
      });

      // Validate required fields
      const requiredFields = form.querySelectorAll('[required]');
      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          field.closest('.form-group').classList.add('error');
          valid = false;
        }
      });

      // Validate email
      const emailField = form.querySelector('input[type="email"]');
      if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
          emailField.closest('.form-group').classList.add('error');
          valid = false;
        }
      }

      // Validate phone
      const phoneField = form.querySelector('input[type="tel"]');
      if (phoneField && phoneField.value) {
        const phoneRegex = /^[\d\s\-+()]{7,}$/;
        if (!phoneRegex.test(phoneField.value)) {
          phoneField.closest('.form-group').classList.add('error');
          valid = false;
        }
      }

      if (valid) {
        // Show success message
        form.style.display = 'none';
        const success = document.querySelector('.form-success');
        if (success) success.classList.add('active');

        // Build WhatsApp message
        const formData = new FormData(form);
        let message = 'New Enquiry from Bakero Website:%0A';
        formData.forEach((value, key) => {
          if (value) message += `${key}: ${value}%0A`;
        });

        // Log for integration
        console.log('Form submitted. Backend integration required.');
        console.log('WhatsApp message:', decodeURIComponent(message));
      }
    });
  }

  // ---------- Contact Details ----------
  // Add the shared social links to each page footer.
  function initContactDetails() {
    const whatsappNumber = '919042664066';
    const instagramUrl = 'https://www.instagram.com/varttaa_overseas?rpxt=NzdlNnVwZ3B0YWJ4';
    const facebookUrl = 'https://www.facebook.com/share/1CLM9X8hhy/';

    document.querySelectorAll('.footer__col').forEach((column) => {
      if (column.querySelector('h4')?.textContent.trim() !== 'Contact' || column.querySelector('.footer__social')) return;
      const socialLinks = document.createElement('div');
      socialLinks.className = 'footer__social';
      socialLinks.setAttribute('aria-label', 'Social media links');
      socialLinks.innerHTML = `
        <a href="https://wa.me/${whatsappNumber}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">WA</a>
        <a href="${instagramUrl}" target="_blank" rel="noopener noreferrer" aria-label="Instagram">IG</a>
        <a href="${facebookUrl}" target="_blank" rel="noopener noreferrer" aria-label="Facebook">FB</a>`;
      column.appendChild(socialLinks);
    });
  }

  // ---------- Smooth Anchor Navigation ----------
  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        if (targetId === '#') return;
        const target = document.querySelector(targetId);
        if (target && lenis) {
          e.preventDefault();
          lenis.scrollTo(target, { offset: -80 });
        }
      });
    });
  }

  // ---------- Lazy Loading ----------
  function initLazyLoad() {
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const img = entry.target;
              img.src = img.dataset.src;
              img.removeAttribute('data-src');
              observer.unobserve(img);
            }
          });
        },
        { rootMargin: '200px' }
      );
      images.forEach((img) => observer.observe(img));
    } else {
      images.forEach((img) => {
        img.src = img.dataset.src;
      });
    }
  }

  // ---------- Window Resize ----------
  function initResize() {
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        ScrollTrigger.refresh();
      }, 250);
    });
  }

  // ---------- Initialize Everything ----------
  function init() {
    initLenis();
    initNavigation();
    initPreloader();
    initFormValidation();
    initContactDetails();
    initSmoothAnchors();
    initLazyLoad();
    initResize();
  }

  // Start on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
