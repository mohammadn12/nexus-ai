/**
 * NexusAI - Main Frontend Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // State Management
  const state = {
    searchQuery: '',
    currentCategory: 'all',
    currentPricing: 'all',
    currentSort: 'popular',
    currentTab: 'all', // 'all', 'featured', 'bookmarks'
    tools: [],
    bookmarks: JSON.parse(localStorage.getItem('nexusai_bookmarks') || '[]'),
    upvotedTools: JSON.parse(localStorage.getItem('nexusai_upvotes') || '[]')
  };

  // DOM Elements
  const searchInput = document.getElementById('search-input');
  const searchClearBtn = document.getElementById('search-clear-btn');
  const categoryPills = document.querySelectorAll('.category-pill');
  const pricingFilter = document.getElementById('pricing-filter');
  const sortFilter = document.getElementById('sort-filter');
  const tabButtons = document.querySelectorAll('.tab-btn');
  const toolsGrid = document.getElementById('tools-grid');
  const resultsCount = document.getElementById('results-count');
  const favCountNav = document.getElementById('fav-count-nav');
  const favCountTab = document.getElementById('fav-count-tab');
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const toastContainer = document.getElementById('toast-container');

  // Initialize
  initTheme();
  updateBookmarkBadges();
  fetchAndRenderTools();

  // Search Debounce Handler
  let debounceTimeout;
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const val = e.target.value;
      state.searchQuery = val;
      if (searchClearBtn) {
        searchClearBtn.classList.toggle('visible', val.length > 0);
      }
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(() => {
        fetchAndRenderTools();
      }, 250);
    });

    // Keyboard shortcut '/' to focus search
    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== searchInput && !isModalOpen()) {
        e.preventDefault();
        searchInput.focus();
      }
    });
  }

  if (searchClearBtn) {
    searchClearBtn.addEventListener('click', () => {
      searchInput.value = '';
      state.searchQuery = '';
      searchClearBtn.classList.remove('visible');
      fetchAndRenderTools();
      searchInput.focus();
    });
  }

  // Category Pill Filter
  categoryPills.forEach(pill => {
    pill.addEventListener('click', () => {
      categoryPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      state.currentCategory = pill.dataset.category || 'all';
      fetchAndRenderTools();
    });
  });

  // Pricing Filter
  if (pricingFilter) {
    pricingFilter.addEventListener('change', (e) => {
      state.currentPricing = e.target.value;
      fetchAndRenderTools();
    });
  }

  // Sort Filter
  if (sortFilter) {
    sortFilter.addEventListener('change', (e) => {
      state.currentSort = e.target.value;
      fetchAndRenderTools();
    });
  }

  // Tab View Switcher (All, Featured, Bookmarks)
  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.currentTab = btn.dataset.tab;
      fetchAndRenderTools();
    });
  });

  // Theme Management
  function initTheme() {
    const savedTheme = localStorage.getItem('nexusai_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    if (themeToggleBtn) {
      themeToggleBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('nexusai_theme', newTheme);
        updateThemeIcon(newTheme);
        showToast(newTheme === 'dark' ? '🌙 Dark theme enabled' : '☀️ Light theme enabled');
      });
    }
  }

  function updateThemeIcon(theme) {
    if (!themeToggleBtn) return;
    if (theme === 'light') {
      themeToggleBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>`;
    } else {
      themeToggleBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>`;
    }
  }

  // Fetch & Render Tools
  async function fetchAndRenderTools() {
    if (!toolsGrid) return;
    toolsGrid.innerHTML = `
      <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted);">
        <div style="display: inline-block; width: 32px; height: 32px; border: 3px solid var(--border-glow); border-top-color: var(--accent-primary); border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
        <p style="margin-top: 12px; font-size: 0.9rem;">Finding top AI tools...</p>
      </div>
    `;

    try {
      const params = new URLSearchParams();
      if (state.searchQuery) params.append('q', state.searchQuery);
      if (state.currentCategory !== 'all') params.append('category', state.currentCategory);
      if (state.currentPricing !== 'all') params.append('pricing', state.currentPricing);
      if (state.currentTab === 'featured') params.append('featured', '1');
      params.append('sort', state.currentSort);

      const response = await fetch(`/api/tools?${params.toString()}`);
      const data = await response.json();

      if (data.status === 'success') {
        let tools = data.tools;

        // If bookmarks tab active, filter locally by bookmarks state
        if (state.currentTab === 'bookmarks') {
          tools = tools.filter(t => state.bookmarks.includes(t.id));
        }

        state.tools = tools;
        renderToolsGrid(tools);
        updateResultsCount(tools.length);
      }
    } catch (err) {
      console.error('Error fetching tools:', err);
      toolsGrid.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-title">Failed to load tools</div>
          <p class="empty-state-desc">There was an issue connecting to the server. Please refresh or try again.</p>
        </div>
      `;
    }
  }

  // Render Grid
  function renderToolsGrid(tools) {
    if (!toolsGrid) return;
    if (tools.length === 0) {
      toolsGrid.innerHTML = `
        <div class="empty-state">
          <div class="empty-state-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </div>
          <div class="empty-state-title">No AI Tools Found</div>
          <p class="empty-state-desc">
            ${state.currentTab === 'bookmarks' 
              ? "You haven't saved any AI tools to your bookmarks yet. Click the star icon on any tool card to save it here!" 
              : "We couldn't find any tools matching your active filters. Try searching with different keywords or resetting filters."}
          </p>
          <button id="btn-reset-filters" class="btn-reset-filters">Reset All Filters</button>
        </div>
      `;

      const resetBtn = document.getElementById('btn-reset-filters');
      if (resetBtn) {
        resetBtn.addEventListener('click', resetAllFilters);
      }
      return;
    }

    toolsGrid.innerHTML = tools.map(tool => createToolCardHTML(tool)).join('');

    // Attach card event listeners
    attachCardListeners();
  }

  // Create Card HTML
  function createToolCardHTML(tool) {
    const isBookmarked = state.bookmarks.includes(tool.id);
    const isUpvoted = state.upvotedTools.includes(tool.id);
    const pricingClass = `pricing-${tool.pricing_type.replace(/\s+/g, '-')}`;

    const tagsHTML = (tool.tags || []).slice(0, 3).map(tag => 
      `<span class="tag-pill">#${escapeHTML(tag)}</span>`
    ).join('');

    return `
      <div class="tool-card" data-id="${tool.id}">
        <div class="card-header">
          <div class="card-brand">
            <img src="${escapeHTML(tool.logo_url)}" alt="${escapeHTML(tool.name)} Logo" class="tool-logo" onerror="this.src='https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=128&auto=format&fit=crop&q=80'">
            <div class="tool-identity">
              <div class="tool-name-row">
                <span class="tool-name">${escapeHTML(tool.name)}</span>
                ${tool.is_verified ? `
                  <span class="badge-verified" title="Verified AI Tool">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                  </span>
                ` : ''}
              </div>
              ${tool.is_featured ? `
                <span class="badge-featured" style="width: fit-content; margin-top: 4px;">
                  ★ Featured
                </span>
              ` : ''}
            </div>
          </div>
          <button class="card-bookmark-btn ${isBookmarked ? 'saved' : ''}" data-id="${tool.id}" title="${isBookmarked ? 'Remove Bookmark' : 'Bookmark Tool'}">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="${isBookmarked ? '#fbbf24' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </button>
        </div>

        <p class="tool-tagline">${escapeHTML(tool.tagline)}</p>

        <div class="card-tags">
          ${tagsHTML}
        </div>

        <div class="card-meta">
          <div class="badge-category">
            <span class="category-dot" style="background: ${escapeHTML(tool.category_color || '#6366f1')}"></span>
            ${escapeHTML(tool.category_name)}
          </div>
          <span class="badge-pricing ${pricingClass}">${escapeHTML(tool.pricing_type)}</span>
        </div>

        <div class="card-actions">
          <button class="btn-upvote ${isUpvoted ? 'upvoted' : ''}" data-id="${tool.id}" title="Upvote Tool">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="${isUpvoted ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 19V5M5 12l7-7 7 7"/>
            </svg>
            <span class="upvote-count">${tool.upvotes || 0}</span>
          </button>
          
          <button class="btn-details" data-id="${tool.id}">Details</button>

          <a href="${escapeHTML(tool.website_url)}" target="_blank" rel="noopener noreferrer" class="btn-visit" title="Visit ${escapeHTML(tool.name)}">
            Visit
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="21" y1="3" x2="14" y2="10"></line>
            </svg>
          </a>
        </div>
      </div>
    `;
  }

  // Attach card event listeners (Bookmarks, Upvotes, Details)
  function attachCardListeners() {
    // Bookmark toggles
    document.querySelectorAll('.card-bookmark-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const toolId = parseInt(btn.dataset.id, 10);
        toggleBookmark(toolId);
      });
    });

    // Upvotes
    document.querySelectorAll('.btn-upvote').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const toolId = parseInt(btn.dataset.id, 10);
        handleUpvote(toolId, btn);
      });
    });

    // Details Modal
    document.querySelectorAll('.btn-details').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const toolId = parseInt(btn.dataset.id, 10);
        if (window.openToolDetailModal) {
          window.openToolDetailModal(toolId);
        }
      });
    });
  }

  // Toggle Bookmark
  function toggleBookmark(toolId) {
    const idx = state.bookmarks.indexOf(toolId);
    if (idx > -1) {
      state.bookmarks.splice(idx, 1);
      showToast('Removed from bookmarks');
    } else {
      state.bookmarks.push(toolId);
      showToast('⭐ Saved to bookmarks!');
    }
    localStorage.setItem('nexusai_bookmarks', JSON.stringify(state.bookmarks));
    updateBookmarkBadges();

    // If currently on bookmarks tab, re-render to reflect removal
    if (state.currentTab === 'bookmarks') {
      fetchAndRenderTools();
    } else {
      // Update icon in current card
      const btn = document.querySelector(`.card-bookmark-btn[data-id="${toolId}"]`);
      if (btn) {
        const isSaved = state.bookmarks.includes(toolId);
        btn.classList.toggle('saved', isSaved);
        btn.querySelector('svg').setAttribute('fill', isSaved ? '#fbbf24' : 'none');
      }
    }
  }

  function updateBookmarkBadges() {
    const count = state.bookmarks.length;
    if (favCountNav) favCountNav.textContent = count;
    if (favCountTab) favCountTab.textContent = count;
  }

  // Handle Upvote
  async function handleUpvote(toolId, btnElement) {
    if (state.upvotedTools.includes(toolId)) {
      showToast('You already upvoted this tool!');
      return;
    }

    try {
      const res = await fetch(`/api/tools/${toolId}/upvote`, { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        state.upvotedTools.push(toolId);
        localStorage.setItem('nexusai_upvotes', JSON.stringify(state.upvotedTools));

        btnElement.classList.add('upvoted');
        btnElement.querySelector('.upvote-count').textContent = data.upvotes;
        btnElement.querySelector('svg').setAttribute('fill', 'currentColor');
        showToast('🚀 Upvoted successfully!');
      }
    } catch (err) {
      console.error('Error upvoting tool:', err);
    }
  }

  function updateResultsCount(count) {
    if (resultsCount) {
      resultsCount.innerHTML = `Showing <strong>${count}</strong> AI tools`;
    }
  }

  function resetAllFilters() {
    state.searchQuery = '';
    state.currentCategory = 'all';
    state.currentPricing = 'all';
    state.currentSort = 'popular';
    state.currentTab = 'all';

    if (searchInput) searchInput.value = '';
    if (searchClearBtn) searchClearBtn.classList.remove('visible');
    if (pricingFilter) pricingFilter.value = 'all';
    if (sortFilter) sortFilter.value = 'popular';

    categoryPills.forEach(p => {
      p.classList.toggle('active', p.dataset.category === 'all');
    });

    tabButtons.forEach(b => {
      b.classList.toggle('active', b.dataset.tab === 'all');
    });

    fetchAndRenderTools();
    showToast('Filters reset');
  }

  // Toast Notification Function
  function showToast(message) {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <span>${escapeHTML(message)}</span>
    `;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('toast-fadeout');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Helper: Escape HTML
  function escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function isModalOpen() {
    return document.querySelector('.modal-overlay.active') !== null;
  }

  // Expose global methods for modal integration
  window.refreshToolsDirectory = fetchAndRenderTools;
  window.nexusShowToast = showToast;
  window.nexusToggleBookmark = toggleBookmark;
  window.nexusHandleUpvote = handleUpvote;
  window.isToolBookmarked = (id) => state.bookmarks.includes(id);
  window.isToolUpvoted = (id) => state.upvotedTools.includes(id);
});

// Keyframe animation for spinner
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);
