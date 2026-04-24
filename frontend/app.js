/* ====================================================
   APP.JS - MADHAVI ENTERPRISES FRONTEND LOGIC
   ==================================================== */

const API_BASE = 'http://127.0.0.1:5001';  // Flask serves from same origin

// ===== STATE =====
let allProperties = [];
let currentFilter = 'all';
let galleryImages  = [];
let galleryVisible = [];
let lbIndex        = 0;
const GALLERY_PAGE = 20;
let galleryOffset  = 0;

// ===== DOM READY =====
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initParticles();
  initScrollAnimations();
  initCounters();
  initCarousel();
  loadProperties();
  initPropTabs();
  loadGallery();
  initGalleryFilters();
  // Lightbox keyboard
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeLightbox(); closeModal(); }
    if (e.key === 'ArrowLeft')  lightboxNav(-1);
    if (e.key === 'ArrowRight') lightboxNav(1);
  });
});

/* 
   NAVBAR
 */
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const navMobile = document.getElementById('nav-mobile');

  if (!navbar) return;

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  });

  if (hamburger && navMobile) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      navMobile.classList.toggle('open');
    });
    navMobile.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navMobile.classList.remove('open');
      });
    });
  }
}

/* 
   PARTICLES
 */
function initParticles() {
  const container = document.getElementById('particles');
  if (!container) return;
  const count = window.innerWidth > 768 ? 25 : 10;
  for (let i = 0; i < count; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    p.style.cssText = `
      left: ${Math.random() * 100}%;
      top: ${Math.random() * 100}%;
      width: ${Math.random() * 3 + 1}px;
      height: ${Math.random() * 3 + 1}px;
      animation-duration: ${Math.random() * 15 + 10}s;
      animation-delay: ${Math.random() * -15}s;
      opacity: ${Math.random() * 0.5 + 0.1};
    `;
    container.appendChild(p);
  }
}

/* 
   SCROLL ANIMATIONS (LEVITATE)
 */
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.levitate').forEach(el => observer.observe(el));
}

/* 
   COUNTER ANIMATION
 */
function initCounters() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
}

function animateCounter(el) {
  const target = parseInt(el.dataset.count);
  const suffix = el.dataset.suffix || '+';
  const duration = 1800;
  const start = performance.now();

  const tick = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target) + (progress >= 1 ? suffix : '');
    if (progress < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

/* 
   TESTIMONIAL CAROUSEL
 */
function initCarousel() {
  const track = document.getElementById('testi-track');
  const dotsEl = document.getElementById('carousel-dots');
  if (!track) return;

  const cards = track.querySelectorAll('.testimonial-card');
  if (!cards.length) return;

  let currentIdx = 0;
  const total = cards.length;
  let autoTimer;

  // Build dots
  if (dotsEl) {
    cards.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = `carousel-dot${i === 0 ? ' active' : ''}`;
      dot.setAttribute('aria-label', `Slide ${i + 1}`);
      dot.addEventListener('click', () => goTo(i));
      dotsEl.appendChild(dot);
    });
  }

  function goTo(idx) {
    currentIdx = (idx + total) % total;
    const cardWidth = cards[0].offsetWidth + 24; // gap
    track.style.transform = `translateX(-${currentIdx * cardWidth}px)`;
    document.querySelectorAll('.carousel-dot').forEach((d, i) => {
      d.classList.toggle('active', i === currentIdx);
    });
  }

  function next() { goTo(currentIdx + 1); }

  function startAuto() {
    autoTimer = setInterval(next, 4000);
  }

  function stopAuto() { clearInterval(autoTimer); }

  track.addEventListener('mouseenter', stopAuto);
  track.addEventListener('mouseleave', startAuto);

  // Touch swipe
  let touchStart = 0;
  track.addEventListener('touchstart', e => { touchStart = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend', e => {
    const diff = touchStart - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) { diff > 0 ? next() : goTo(currentIdx - 1); }
  });

  startAuto();
  window.addEventListener('resize', () => goTo(currentIdx));
}

/* 
   PROPERTIES - LOAD & RENDER
 */
async function loadProperties() {
  const grid = document.getElementById('props-grid');
  if (!grid) return;

  try {
    const res = await fetch(`${API_BASE}/api/properties`);
    if (!res.ok) throw new Error('Server error');
    const data = await res.json();
    allProperties = Array.isArray(data) ? data : [];
  } catch (err) {
    console.warn('Could not load properties from API, using demo data.');
    allProperties = getDemoProperties();
  }

  renderProperties(allProperties);
}

function getDemoProperties() {
  return [
    {
      id: 'kammapadu', title: 'Kammapadu Premium Plots', type: 'Plot',
      price: 'Rs. 15,000', location: 'Kammapadu, AP',
      description: 'DTCP-approved gated community with excellent connectivity.',
      images: ['https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&q=80'],
      featured: true
    },
    {
      id: 'lemalle', title: 'Lemalle Venture', type: 'Plot',
      price: 'Rs. 17,000', location: 'Lemalle, AP',
      description: 'RERA-registered plots with highway access.',
      images: ['https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=600&q=80'],
      featured: true
    },
    {
      id: 'kanchincharla', title: 'Kanchincharla Exclusive', type: 'Plot',
      price: 'Rs. 18,000', location: 'Kanchincharla, AP',
      description: 'River view plots - investment hotspot.',
      images: ['https://images.unsplash.com/photo-1560493676-04071c5f467b?w=600&q=80'],
      featured: true
    },
    {
      id: 'villa-1', title: 'Heritage Villa', type: 'Villa',
      price: 'Rs. 1.8 Cr', location: 'Vijayawada, AP',
      description: 'Luxury 4BHK villa with smart home features and landscaped garden.',
      images: ['https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=600&q=80'],
      featured: false
    },
    {
      id: 'apt-1', title: 'Skyline Apartments', type: 'Apartment',
      price: 'Rs. 85 Lakhs', location: 'Guntur, AP',
      description: 'Modern 3BHK apartments with rooftop amenities in the heart of Guntur.',
      images: ['https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600&q=80'],
      featured: false
    },
    {
      id: 'house-1', title: 'Riverside House', type: 'House',
      price: 'Rs. 65 Lakhs', location: 'Krishna District, AP',
      description: 'Spacious individual house with 2400 sqft, near the Krishna river.',
      images: ['https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=600&q=80'],
      featured: false
    }
  ];
}

function renderProperties(props) {
  const grid = document.getElementById('props-grid');
  const noProps = document.getElementById('no-props');
  if (!grid) return;

  const filtered = currentFilter === 'all' ? props : props.filter(p => p.type === currentFilter);

  if (!filtered.length) {
    grid.innerHTML = '';
    if (noProps) noProps.style.display = 'block';
    return;
  }
  if (noProps) noProps.style.display = 'none';

  grid.innerHTML = filtered.map((p, i) => {
    const img = (p.images && p.images[0]) || (p.image_urls && p.image_urls.split(',')[0]) || 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&q=80';
    const isVenture = ['kammapadu', 'lemalle', 'kanchincharla'].includes(String(p.id));
    const href = isVenture
      ? `property.html?venture=${p.id}`
      : `property.html?id=${p.id}`;
    return `
    <div class="ag-card property-card levitate levitate-delay-${Math.min(i % 3 + 1, 5)}" onclick="window.location.href='${href}'" id="prop-card-${p.id}">
      <div class="prop-img-wrap">
        <img src="${img}" alt="${p.title}" loading="lazy"/>
        <div class="prop-badge">${p.type || 'Property'}</div>
        ${p.featured ? '<div class="prop-featured"> Featured</div>' : ''}
      </div>
      <div class="prop-body">
        <h3>${p.title}</h3>
        <div class="prop-location"> ${p.location}</div>
        <div class="prop-price">${p.price} <span>${p.type === 'Plot' ? '/sq.yard' : ''}</span></div>
        <div class="prop-cta">
          <button class="btn btn-glass" style="font-size:0.78rem;padding:8px 18px;" onclick="event.stopPropagation();openLeadModal('${p.title}','${p.id}','${p.price}')">
            <i class="fa-solid fa-robot"></i>  Quick Enquiry
          </button>
          <div class="prop-view">View Details </div>
        </div>
      </div>
    </div>`;
  }).join('');

  // Re-observe new elements
  initScrollAnimations();
}

/* 
   PROPERTY TABS / FILTER
 */
function initPropTabs() {
  const tabs = document.querySelectorAll('.prop-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentFilter = tab.dataset.filter;
      renderProperties(allProperties);
    });
  });
}

/* 
   LEAD MODAL
 */
function openLeadModal(propertyTitle, propertyId, price) {
  document.getElementById('lead-property').value = propertyTitle || '';
  document.getElementById('lead-property-id').value = propertyId || '';
  const form = document.getElementById('lead-form');
  if (form) form.reset();
  document.getElementById('lead-modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('lead-modal').classList.remove('open');
  document.body.style.overflow = '';
}

// Close modal on overlay click
document.addEventListener('click', (e) => {
  const modal = document.getElementById('lead-modal');
  if (e.target === modal) closeModal();
});

// Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

/* 
   LEAD SUBMISSION  AI CALL + WHATSAPP
 */
async function submitLead(e) {
  e.preventDefault();
  const btn = document.getElementById('lead-submit-btn');
  btn.textContent = ' Connecting AI Agent...';
  btn.disabled = true;

  const name       = document.getElementById('lead-name').value.trim();
  const phone      = document.getElementById('lead-phone').value.trim();
  const budget     = document.getElementById('lead-budget')?.value || '';
  const property   = document.getElementById('lead-property').value || 'General Inquiry';
  const propertyId = document.getElementById('lead-property-id').value || '';

  const payload = {
    name,
    phone,
    budget,
    property,
    property_id: propertyId,
    location: 'Andhra Pradesh'
  };

  try {
    const res = await fetch(`${API_BASE}/enquiry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    closeModal();
    showToast();
  } catch (err) {
    console.error('Lead submission error:', err);
    // Still show success toast - lead may be saved
    closeModal();
    showToast();
  }

  btn.textContent = '<i class="fa-solid fa-rocket"></i>  Get My AI Call Now';
  btn.disabled = false;
}

function showToast() {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 5000);
}

/* 
   PROPERTY NAVIGATION
 */
function goToProperty(ventureName) {
  window.location.href = `property.html?venture=${ventureName}`;
}

/* 
   CLOUDINARY INTERIOR GALLERY
 */
async function loadGallery() {
  const grid    = document.getElementById('interior-gallery');
  const loader  = document.getElementById('gallery-loader');
  const empty   = document.getElementById('gallery-empty');
  if (!grid) return;

  try {
    const res  = await fetch(`${API_BASE}/api/cloudinary/images?max=80`);
    const data = await res.json();
    galleryImages = data.images || [];
  } catch (err) {
    console.warn('Cloudinary gallery load error:', err);
    galleryImages = [];
  }

  if (loader) loader.style.display = 'none';

  if (!galleryImages.length) {
    if (empty) empty.style.display = 'block';
    return;
  }

  galleryVisible = [...galleryImages];
  galleryOffset  = 0;
  grid.style.display = 'block';
  renderGalleryChunk();
}

function renderGalleryChunk() {
  const grid     = document.getElementById('interior-gallery');
  const loadMore = document.getElementById('gallery-load-more');
  if (!grid) return;

  const chunk = galleryVisible.slice(galleryOffset, galleryOffset + GALLERY_PAGE);
  chunk.forEach((img, i) => {
    const idx  = galleryOffset + i;
    const item = document.createElement('div');
    item.className = 'gallery-item';
    item.dataset.folder = img.folder || '';
    item.innerHTML = `
      <img src="${img.url}" alt="Interior Design" loading="lazy"/>
      <div class="gal-overlay">
        <span class="gal-label">${img.folder ? img.folder.replace('madhavi_', '').replace('_', ' ') : 'Design Portfolio'}</span>
      </div>`;
    item.addEventListener('click', () => openLightbox(idx));
    grid.appendChild(item);
  });

  galleryOffset += chunk.length;

  if (loadMore) {
    loadMore.style.display = galleryOffset < galleryVisible.length ? 'flex' : 'none';
  }
  initScrollAnimations();
}

function loadMoreGallery() {
  renderGalleryChunk();
}

/*  Gallery Filters  */
function initGalleryFilters() {
  document.querySelectorAll('.gal-filter').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.gal-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.galFilter;

      if (f === 'all') {
        galleryVisible = [...galleryImages];
      } else {
        galleryVisible = galleryImages.filter(img =>
          (img.folder || '').toLowerCase().includes(f) ||
          (img.public_id || '').toLowerCase().includes(f)
        );
        // If Cloudinary has no folder-based match, show all (fallback)
        if (!galleryVisible.length) galleryVisible = [...galleryImages];
      }

      const grid = document.getElementById('interior-gallery');
      if (grid) { grid.innerHTML = ''; }
      galleryOffset = 0;
      if (galleryVisible.length) {
        renderGalleryChunk();
      } else {
        const empty = document.getElementById('gallery-empty');
        if (empty) empty.style.display = 'block';
      }
    });
  });
}

/*  Lightbox  */
function openLightbox(idx) {
  lbIndex = idx;
  const lb  = document.getElementById('lightbox');
  const img = document.getElementById('lightbox-img');
  if (!lb || !img) return;
  img.src = galleryVisible[lbIndex]?.url || '';
  lb.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  const lb = document.getElementById('lightbox');
  if (lb) lb.classList.remove('open');
  document.body.style.overflow = '';
}

function lightboxNav(dir) {
  if (!galleryVisible.length) return;
  lbIndex = (lbIndex + dir + galleryVisible.length) % galleryVisible.length;
  const img = document.getElementById('lightbox-img');
  if (img) {
    img.style.opacity = '0';
    setTimeout(() => {
      img.src = galleryVisible[lbIndex]?.url || '';
      img.style.opacity = '1';
    }, 150);
  }
}

// Close lightbox on backdrop click
document.addEventListener('click', e => {
  const lb = document.getElementById('lightbox');
  if (e.target === lb) closeLightbox();
});
