/**
 * NexusAI - Modal Dialogs Management (Tool Details & Tool Submission)
 */

document.addEventListener('DOMContentLoaded', () => {
  // Modal Elements
  const detailModalOverlay = document.getElementById('detail-modal-overlay');
  const detailModalCloseBtn = document.getElementById('detail-modal-close');
  const detailModalContent = document.getElementById('detail-modal-content');

  const submitModalOverlay = document.getElementById('submit-modal-overlay');
  const submitModalCloseBtn = document.getElementById('submit-modal-close');
  const btnOpenSubmit = document.getElementById('btn-open-submit');
  const submitForm = document.getElementById('submit-tool-form');
  const submitSubmitBtn = document.getElementById('btn-submit-form-action');

  // ==========================================
  // Tool Detail Modal
  // ==========================================

  window.openToolDetailModal = async function(toolId) {
    if (!detailModalOverlay || !detailModalContent) return;

    // Show modal in loading state
    detailModalOverlay.classList.add('active');
    document.body.style.overflow = 'hidden';

    detailModalContent.innerHTML = `
      <div style="text-align: center; padding: 60px 20px; color: var(--text-muted);">
        <div style="display: inline-block; width: 36px; height: 36px; border: 3px solid var(--border-glow); border-top-color: var(--accent-primary); border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
        <p style="margin-top: 14px; font-size: 0.95rem;">Loading tool specifications...</p>
      </div>
    `;

    try {
      const response = await fetch(`/api/tools/${toolId}`);
      const data = await response.json();

      if (data.status === 'success' && data.tool) {
        renderDetailModal(data.tool);
      } else {
        detailModalContent.innerHTML = `
          <div style="text-align: center; padding: 40px;">
            <h3>Error loading tool</h3>
            <p style="color: var(--text-secondary); margin-top: 8px;">Tool could not be found.</p>
          </div>
        `;
      }
    } catch (err) {
      console.error('Error opening tool modal:', err);
      detailModalContent.innerHTML = `
        <div style="text-align: center; padding: 40px;">
          <h3>Connection Error</h3>
          <p style="color: var(--text-secondary); margin-top: 8px;">Failed to fetch tool details.</p>
        </div>
      `;
    }
  };

  function renderDetailModal(tool) {
    const isBookmarked = window.isToolBookmarked ? window.isToolBookmarked(tool.id) : false;
    const isUpvoted = window.isToolUpvoted ? window.isToolUpvoted(tool.id) : false;
    const pricingClass = `pricing-${tool.pricing_type.replace(/\s+/g, '-')}`;

    const featuresHTML = (tool.features || []).map(feat => `
      <li class="detail-feature-item">
        <svg class="feature-check-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <span>${escapeHTML(feat)}</span>
      </li>
    `).join('');

    const tagsHTML = (tool.tags || []).map(tag => `
      <span class="tag-pill">#${escapeHTML(tag)}</span>
    `).join('');

    detailModalContent.innerHTML = `
      <div class="detail-header">
        <img src="${escapeHTML(tool.logo_url)}" alt="${escapeHTML(tool.name)} Logo" class="detail-logo" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&auto=format&fit=crop&q=80'">
        <div class="detail-title-block">
          <div class="detail-name-row">
            <h2 class="detail-name">${escapeHTML(tool.name)}</h2>
            ${tool.is_verified ? `
              <span class="badge-verified" title="Verified AI Tool">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </span>
            ` : ''}
          </div>
          <div class="detail-badges">
            <span class="badge-category">
              <span class="category-dot" style="background: ${escapeHTML(tool.category_color || '#6366f1')}"></span>
              ${escapeHTML(tool.category_name)}
            </span>
            <span class="badge-pricing ${pricingClass}">${escapeHTML(tool.pricing_type)}</span>
            <span style="font-size: 0.85rem; color: #fbbf24; font-weight: 700;">★ ${tool.rating || '4.8'}</span>
            ${tool.is_featured ? '<span class="badge-featured">★ Featured</span>' : ''}
          </div>
        </div>
      </div>

      <div class="detail-tagline">${escapeHTML(tool.tagline)}</div>

      <div class="detail-section">
        <div class="detail-section-title">Overview</div>
        <p class="detail-desc">${escapeHTML(tool.description)}</p>
      </div>

      ${tool.features && tool.features.length > 0 ? `
        <div class="detail-section">
          <div class="detail-section-title">Key Capabilities & Features</div>
          <ul class="detail-features-list">
            ${featuresHTML}
          </ul>
        </div>
      ` : ''}

      <div class="detail-pricing-box">
        <div class="detail-pricing-info">
          <span class="detail-pricing-model">Pricing Model: ${escapeHTML(tool.pricing_type)}</span>
          <span class="detail-pricing-sub">${escapeHTML(tool.pricing_details || 'Check official website for tier plans.')}</span>
        </div>
      </div>

      <div class="detail-section">
        <div class="detail-section-title">Tags & Keywords</div>
        <div class="card-tags">
          ${tagsHTML}
        </div>
      </div>

      <div class="detail-actions-footer">
        <div class="detail-left-actions">
          <button id="modal-btn-upvote" class="btn-upvote ${isUpvoted ? 'upvoted' : ''}" title="Upvote Tool">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="${isUpvoted ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 19V5M5 12l7-7 7 7"/>
            </svg>
            <span id="modal-upvote-count">${tool.upvotes || 0}</span>
          </button>

          <button id="modal-btn-bookmark" class="card-bookmark-btn ${isBookmarked ? 'saved' : ''}" title="Bookmark Tool">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="${isBookmarked ? '#fbbf24' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </button>
        </div>

        <a href="${escapeHTML(tool.website_url)}" target="_blank" rel="noopener noreferrer" class="detail-visit-btn">
          Visit Official Tool Website
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="21" y1="3" x2="14" y2="10"></line>
          </svg>
        </a>
      </div>
    `;

    // Modal action listeners
    const modalUpvoteBtn = document.getElementById('modal-btn-upvote');
    if (modalUpvoteBtn) {
      modalUpvoteBtn.addEventListener('click', () => {
        if (window.nexusHandleUpvote) {
          window.nexusHandleUpvote(tool.id, modalUpvoteBtn);
        }
      });
    }

    const modalBookmarkBtn = document.getElementById('modal-btn-bookmark');
    if (modalBookmarkBtn) {
      modalBookmarkBtn.addEventListener('click', () => {
        if (window.nexusToggleBookmark) {
          window.nexusToggleBookmark(tool.id);
          const savedNow = window.isToolBookmarked ? window.isToolBookmarked(tool.id) : false;
          modalBookmarkBtn.classList.toggle('saved', savedNow);
          modalBookmarkBtn.querySelector('svg').setAttribute('fill', savedNow ? '#fbbf24' : 'none');
        }
      });
    }
  }

  function closeDetailModal() {
    if (detailModalOverlay) {
      detailModalOverlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  if (detailModalCloseBtn) {
    detailModalCloseBtn.addEventListener('click', closeDetailModal);
  }

  if (detailModalOverlay) {
    detailModalOverlay.addEventListener('click', (e) => {
      if (e.target === detailModalOverlay) {
        closeDetailModal();
      }
    });
  }

  // ==========================================
  // Submit Tool Modal
  // ==========================================

  function openSubmitModal() {
    if (submitModalOverlay) {
      submitModalOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
      const firstInput = submitModalOverlay.querySelector('input');
      if (firstInput) setTimeout(() => firstInput.focus(), 100);
    }
  }

  function closeSubmitModal() {
    if (submitModalOverlay) {
      submitModalOverlay.classList.remove('active');
      document.body.style.overflow = '';
      if (submitForm) submitForm.reset();
    }
  }

  if (btnOpenSubmit) {
    btnOpenSubmit.addEventListener('click', (e) => {
      e.preventDefault();
      openSubmitModal();
    });
  }

  if (submitModalCloseBtn) {
    submitModalCloseBtn.addEventListener('click', closeSubmitModal);
  }

  if (submitModalOverlay) {
    submitModalOverlay.addEventListener('click', (e) => {
      if (e.target === submitModalOverlay) {
        closeSubmitModal();
      }
    });
  }

  // Handle Form Submission
  if (submitForm) {
    submitForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const name = document.getElementById('submit-name').value.trim();
      const website_url = document.getElementById('submit-url').value.trim();
      const category_id = document.getElementById('submit-category').value;
      const pricing_type = document.getElementById('submit-pricing').value;
      const tagline = document.getElementById('submit-tagline').value.trim();
      const description = document.getElementById('submit-description').value.trim();
      const featuresRaw = document.getElementById('submit-features').value.trim();
      const tagsRaw = document.getElementById('submit-tags').value.trim();
      const logo_url = document.getElementById('submit-logo').value.trim();

      if (!name || !website_url || !category_id || !tagline) {
        if (window.nexusShowToast) {
          window.nexusShowToast('⚠️ Please fill in all required fields.');
        }
        return;
      }

      const payload = {
        name,
        website_url,
        category_id,
        pricing_type,
        tagline,
        description: description || tagline,
        features: featuresRaw ? featuresRaw.split('\n').filter(f => f.trim().length > 0) : [],
        tags: tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(t => t.length > 0) : [],
        logo_url: logo_url || 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&auto=format&fit=crop&q=80'
      };

      if (submitSubmitBtn) {
        submitSubmitBtn.disabled = true;
        submitSubmitBtn.innerHTML = 'Submitting Tool...';
      }

      try {
        const response = await fetch('/api/tools/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const resData = await response.json();

        if (response.ok && resData.status === 'success') {
          closeSubmitModal();
          if (window.nexusShowToast) {
            window.nexusShowToast(`🎉 "${name}" added to directory successfully!`);
          }
          if (window.refreshToolsDirectory) {
            window.refreshToolsDirectory();
          }
        } else {
          if (window.nexusShowToast) {
            window.nexusShowToast(`❌ Submission failed: ${resData.message || 'Error'}`);
          }
        }
      } catch (err) {
        console.error('Error submitting tool:', err);
        if (window.nexusShowToast) {
          window.nexusShowToast('❌ Network error submitting tool.');
        }
      } finally {
        if (submitSubmitBtn) {
          submitSubmitBtn.disabled = false;
          submitSubmitBtn.innerHTML = `
            <span>Submit AI Tool</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          `;
        }
      }
    });
  }

  // Global Escape key listener to close active modal
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDetailModal();
      closeSubmitModal();
    }
  });

  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});
