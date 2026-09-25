/**
 * File Integrity Checker — Frontend Client Controller
 * Manages tab views, asynchronous API operations, file analysis,
 * baseline creation, cryptographic verification, and audit reports.
 */

document.addEventListener('DOMContentLoaded', () => {
  // ---------------------------------------------------------------------------
  // State Management
  // ---------------------------------------------------------------------------
  const state = {
    currentAnalysis: null, // { metadata, sha256, has_baseline, baseline }
    lastVerificationResult: null, // VerificationResult object
    currentHistoryId: null,
  };

  // ---------------------------------------------------------------------------
  // DOM Element Selectors
  // ---------------------------------------------------------------------------
  // Navigation tabs
  const navTabs = document.querySelectorAll('.nav-tab');
  const screens = document.querySelectorAll('.screen-view');

  // Home Screen Elements
  const statTotalBaselines = document.getElementById('statTotalBaselines');
  const statTotalVerifications = document.getElementById('statTotalVerifications');
  const statMatched = document.getElementById('statMatched');
  const statModified = document.getElementById('statModified');
  const homeRecentActivityList = document.getElementById('homeRecentActivityList');
  const quickFilePathInput = document.getElementById('quickFilePathInput');
  const btnQuickVerify = document.getElementById('btnQuickVerify');
  const quickFileInput = document.getElementById('quickFileInput');
  const btnRefreshStats = document.getElementById('btnRefreshStats');
  const btnHeroAnalyze = document.getElementById('btnHeroAnalyze');
  const btnHeroHistory = document.getElementById('btnHeroHistory');

  // File Analysis Elements
  const tabInputPath = document.getElementById('tabInputPath');
  const tabInputUpload = document.getElementById('tabInputUpload');
  const subtabPathContent = document.getElementById('subtabPathContent');
  const subtabUploadContent = document.getElementById('subtabUploadContent');
  const analyzeFilePathInput = document.getElementById('analyzeFilePathInput');
  const btnRunAnalysis = document.getElementById('btnRunAnalysis');
  const fileDropzone = document.getElementById('fileDropzone');
  const analyzeFileInput = document.getElementById('analyzeFileInput');
  const analysisResultCard = document.getElementById('analysisResultCard');
  const anaFileName = document.getElementById('anaFileName');
  const anaBaselineStatusBadge = document.getElementById('anaBaselineStatusBadge');
  const btnCreateBaseline = document.getElementById('btnCreateBaseline');
  const btnVerifyAnalyzedFile = document.getElementById('btnVerifyAnalyzedFile');
  const anaFilePath = document.getElementById('anaFilePath');
  const anaFileSize = document.getElementById('anaFileSize');
  const anaLastModified = document.getElementById('anaLastModified');
  const anaAnalysisTime = document.getElementById('anaAnalysisTime');
  const anaSha256 = document.getElementById('anaSha256');
  const btnCopyHash = document.getElementById('btnCopyHash');
  const anaBaselinePreview = document.getElementById('anaBaselinePreview');
  const anaBaselineCreated = document.getElementById('anaBaselineCreated');
  const anaBaselineHashVal = document.getElementById('anaBaselineHashVal');
  const anaCurrentHashVal = document.getElementById('anaCurrentHashVal');

  // Verification Result Elements
  const resultEmptyState = document.getElementById('resultEmptyState');
  const resultCard = document.getElementById('resultCard');
  const resultStatusBanner = document.getElementById('resultStatusBanner');
  const resultStatusIcon = document.getElementById('resultStatusIcon');
  const resultStatusText = document.getElementById('resultStatusText');
  const resultExplanation = document.getElementById('resultExplanation');
  const resFileName = document.getElementById('resFileName');
  const resFilePath = document.getElementById('resFilePath');
  const resVerifiedAt = document.getElementById('resVerifiedAt');
  const resBaselineCreated = document.getElementById('resBaselineCreated');
  const resBaselineHash = document.getElementById('resBaselineHash');
  const resCurrentHash = document.getElementById('resCurrentHash');
  const btnCopyBaselineHash = document.getElementById('btnCopyBaselineHash');
  const btnCopyCurrentHash = document.getElementById('btnCopyCurrentHash');
  const btnDownloadReport = document.getElementById('btnDownloadReport');
  const btnGoToAnalyze = document.getElementById('btnGoToAnalyze');

  // History & Baselines Elements
  const tabSubHistory = document.getElementById('tabSubHistory');
  const tabSubBaselines = document.getElementById('tabSubBaselines');
  const historyLogsView = document.getElementById('historyLogsView');
  const historyBaselinesView = document.getElementById('historyBaselinesView');
  const historyFilters = document.getElementById('historyFilters');
  const filterStatus = document.getElementById('filterStatus');
  const btnReloadHistory = document.getElementById('btnReloadHistory');
  const historyTableBody = document.getElementById('historyTableBody');
  const baselinesTableBody = document.getElementById('baselinesTableBody');

  // Modal & Toast Elements
  const reportModal = document.getElementById('reportModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const modalReportContent = document.getElementById('modalReportContent');
  const btnCopyModalReport = document.getElementById('btnCopyModalReport');
  const btnDownloadModalReport = document.getElementById('btnDownloadModalReport');
  const toastContainer = document.getElementById('toastContainer');

  // ---------------------------------------------------------------------------
  // Helper: Toast Notifications
  // ---------------------------------------------------------------------------
  function showToast(message, type = 'info', duration = 3500) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(30px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // ---------------------------------------------------------------------------
  // Helper: Tab Switching
  // ---------------------------------------------------------------------------
  function switchTab(targetTabId) {
    navTabs.forEach((tab) => {
      const isTarget = tab.dataset.tab === targetTabId;
      tab.classList.toggle('active', isTarget);
      tab.setAttribute('aria-selected', isTarget);
    });

    screens.forEach((screen) => {
      const match = screen.id.toLowerCase() === `screen${targetTabId}`;
      screen.classList.toggle('active', match);
      screen.hidden = !match;
    });

    // Refresh view data if required
    if (targetTabId === 'home') {
      loadStats();
    } else if (targetTabId === 'history') {
      loadHistory();
      loadBaselines();
    }
  }

  navTabs.forEach((tab) => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });

  if (btnHeroAnalyze) btnHeroAnalyze.addEventListener('click', () => switchTab('analyze'));
  if (btnHeroHistory) btnHeroHistory.addEventListener('click', () => switchTab('history'));
  if (btnGoToAnalyze) btnGoToAnalyze.addEventListener('click', () => switchTab('analyze'));

  // ---------------------------------------------------------------------------
  // Helper: Clipboard Copy
  // ---------------------------------------------------------------------------
  function copyTextToClipboard(text, successMessage = 'Copied to clipboard!') {
    if (!text || text === '-' || text === 'N/A') return;
    navigator.clipboard.writeText(text).then(
      () => showToast(successMessage, 'success'),
      () => showToast('Failed to copy text', 'error')
    );
  }

  // ---------------------------------------------------------------------------
  // API: Dashboard Stats (Screen 1)
  // ---------------------------------------------------------------------------
  async function loadStats() {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      if (!data.success) return;

      const { stats } = data;
      if (statTotalBaselines) statTotalBaselines.textContent = stats.total_baselines;
      if (statTotalVerifications) statTotalVerifications.textContent = stats.total_verifications;
      if (statMatched) statMatched.textContent = stats.matched_count;
      if (statModified) statModified.textContent = stats.modified_count;

      renderRecentActivity(stats.recent_verifications || []);
    } catch (err) {
      console.error('Error fetching dashboard stats:', err);
    }
  }

  function renderRecentActivity(records) {
    if (!homeRecentActivityList) return;
    if (!records || records.length === 0) {
      homeRecentActivityList.innerHTML = `<div class="empty-state-sm">No recent verification activity recorded yet.</div>`;
      return;
    }

    homeRecentActivityList.innerHTML = records
      .map((r) => {
        const badgeClass = getBadgeClass(r.status);
        const timeFormatted = r.verified_at ? r.verified_at.replace('T', ' ').slice(0, 19) : '-';
        return `
          <div class="recent-item">
            <div class="recent-info">
              <span class="recent-name">${escapeHtml(r.file_name)}</span>
              <span class="recent-time">${timeFormatted} UTC</span>
            </div>
            <span class="badge ${badgeClass}">${r.status}</span>
          </div>
        `;
      })
      .join('');
  }

  if (btnRefreshStats) {
    btnRefreshStats.addEventListener('click', () => {
      loadStats();
      showToast('Dashboard stats updated', 'info', 2000);
    });
  }

  // ---------------------------------------------------------------------------
  // Quick Verification from Home Screen
  // ---------------------------------------------------------------------------
  async function executeQuickVerification(filePath) {
    if (!filePath) {
      showToast('Please enter a file path to verify.', 'error');
      return;
    }
    showToast('Executing verification check...', 'info', 1500);
    try {
      const res = await fetch('/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath }),
      });
      const data = await res.json();
      if (!data.success) {
        showToast(data.error || 'Verification request failed.', 'error');
        return;
      }
      displayVerificationResult(data.result);
      switchTab('result');
    } catch (err) {
      showToast(`Network error: ${err.message}`, 'error');
    }
  }

  if (btnQuickVerify) {
    btnQuickVerify.addEventListener('click', () => {
      const path = quickFilePathInput.value.trim();
      executeQuickVerification(path);
    });
  }

  if (quickFilePathInput) {
    quickFilePathInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const path = quickFilePathInput.value.trim();
        executeQuickVerification(path);
      }
    });
  }

  if (quickFileInput) {
    quickFileInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      uploadAndAnalyze(file, true);
    });
  }

  // ---------------------------------------------------------------------------
  // File Analysis Subtabs (Path vs Drag & Drop)
  // ---------------------------------------------------------------------------
  if (tabInputPath && tabInputUpload) {
    tabInputPath.addEventListener('click', () => {
      tabInputPath.classList.add('active');
      tabInputUpload.classList.remove('active');
      subtabPathContent.classList.add('active');
      subtabUploadContent.classList.remove('active');
    });

    tabInputUpload.addEventListener('click', () => {
      tabInputUpload.classList.add('active');
      tabInputPath.classList.remove('active');
      subtabUploadContent.classList.add('active');
      subtabPathContent.classList.remove('active');
    });
  }

  // ---------------------------------------------------------------------------
  // Drag & Drop Handling
  // ---------------------------------------------------------------------------
  if (fileDropzone && analyzeFileInput) {
    fileDropzone.addEventListener('click', () => analyzeFileInput.click());

    ['dragenter', 'dragover'].forEach((eventName) => {
      fileDropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        fileDropzone.classList.add('drag-active');
      });
    });

    ['dragleave', 'drop'].forEach((eventName) => {
      fileDropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        fileDropzone.classList.remove('drag-active');
      });
    });

    fileDropzone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const file = dt.files[0];
      if (file) {
        uploadAndAnalyze(file, false);
      }
    });

    analyzeFileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        uploadAndAnalyze(file, false);
      }
    });
  }

  async function uploadAndAnalyze(file, autoVerify = false) {
    const formData = new FormData();
    formData.append('file', file);

    showToast(`Uploading and calculating SHA-256 for "${file.name}"...`, 'info', 2000);

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (!data.success) {
        showToast(data.error || 'Upload and analysis failed.', 'error');
        return;
      }

      state.currentAnalysis = data;
      renderAnalysisCard(data);

      if (autoVerify) {
        if (data.has_baseline) {
          executeQuickVerification(data.metadata.file_path);
        } else {
          showToast(`No baseline found for "${file.name}". Switched to File Analysis screen to establish one.`, 'info', 4000);
          switchTab('analyze');
        }
      }
    } catch (err) {
      showToast(`Error uploading file: ${err.message}`, 'error');
    }
  }

  // ---------------------------------------------------------------------------
  // File Analysis (Path Input)
  // ---------------------------------------------------------------------------
  async function analyzeFilePath(filePath) {
    if (!filePath) {
      showToast('Please specify a valid file path.', 'error');
      return;
    }

    showToast('Reading file and computing SHA-256 digest...', 'info', 1500);

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath }),
      });
      const data = await res.json();

      if (!data.success) {
        showToast(data.error || 'Analysis failed.', 'error', 4500);
        return;
      }

      state.currentAnalysis = data;
      renderAnalysisCard(data);
      showToast('File analyzed successfully!', 'success');
    } catch (err) {
      showToast(`Network error: ${err.message}`, 'error');
    }
  }

  if (btnRunAnalysis) {
    btnRunAnalysis.addEventListener('click', () => {
      const path = analyzeFilePathInput.value.trim();
      analyzeFilePath(path);
    });
  }

  if (analyzeFilePathInput) {
    analyzeFilePathInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const path = analyzeFilePathInput.value.trim();
        analyzeFilePath(path);
      }
    });
  }

  function renderAnalysisCard(data) {
    const { metadata, sha256, has_baseline, baseline } = data;

    analysisResultCard.style.display = 'block';
    anaFileName.textContent = metadata.file_name;
    anaFilePath.textContent = metadata.file_path;
    anaFileSize.textContent = `${metadata.file_size_human} (${metadata.file_size.toLocaleString()} bytes)`;
    anaLastModified.textContent = metadata.last_modified
      ? metadata.last_modified.replace('T', ' ').slice(0, 19) + ' UTC'
      : 'N/A';
    anaAnalysisTime.textContent = new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
    anaSha256.textContent = sha256;

    if (has_baseline && baseline) {
      anaBaselineStatusBadge.className = 'badge badge-matched';
      anaBaselineStatusBadge.textContent = 'Baseline Active';

      anaBaselinePreview.style.display = 'block';
      anaBaselineCreated.textContent = `Established: ${baseline.created_at.replace('T', ' ').slice(0, 19)} UTC`;
      anaBaselineHashVal.textContent = baseline.sha256;
      anaCurrentHashVal.textContent = sha256;

      if (baseline.sha256.toLowerCase() === sha256.toLowerCase()) {
        anaCurrentHashVal.style.color = '#3fb950';
      } else {
        anaCurrentHashVal.style.color = '#d29922';
      }
    } else {
      anaBaselineStatusBadge.className = 'badge badge-neutral';
      anaBaselineStatusBadge.textContent = 'No Stored Baseline';
      anaBaselinePreview.style.display = 'none';
    }
  }

  if (btnCopyHash) {
    btnCopyHash.addEventListener('click', () => {
      if (state.currentAnalysis && state.currentAnalysis.sha256) {
        copyTextToClipboard(state.currentAnalysis.sha256, 'SHA-256 hash copied!');
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Action: Create / Update Baseline
  // ---------------------------------------------------------------------------
  if (btnCreateBaseline) {
    btnCreateBaseline.addEventListener('click', async () => {
      if (!state.currentAnalysis) {
        showToast('Please analyze a file first.', 'error');
        return;
      }

      const filePath = state.currentAnalysis.metadata.file_path;
      showToast('Persisting baseline in SQLite database...', 'info', 1500);

      try {
        const res = await fetch('/api/baseline', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ file_path: filePath }),
        });
        const data = await res.json();

        if (!data.success) {
          showToast(data.error || 'Failed to establish baseline.', 'error');
          return;
        }

        showToast('Trusted baseline established and saved!', 'success');
        // Re-analyze to refresh preview badge
        analyzeFilePath(filePath);
        loadStats();
      } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Action: Verify Analyzed File
  // ---------------------------------------------------------------------------
  if (btnVerifyAnalyzedFile) {
    btnVerifyAnalyzedFile.addEventListener('click', async () => {
      if (!state.currentAnalysis) {
        showToast('Please analyze a file first.', 'error');
        return;
      }
      const filePath = state.currentAnalysis.metadata.file_path;
      executeQuickVerification(filePath);
    });
  }

  // ---------------------------------------------------------------------------
  // Screen 3: Verification Result Rendering
  // ---------------------------------------------------------------------------
  function displayVerificationResult(result) {
    state.lastVerificationResult = result;

    resultEmptyState.style.display = 'none';
    resultCard.style.display = 'block';

    const status = result.status.toUpperCase();
    resultStatusText.textContent = status;
    resultExplanation.textContent = result.explanation;

    // Reset status classes
    resultStatusBanner.className = 'result-banner';
    resultStatusBanner.classList.add(`status-${status.toLowerCase()}`);

    // Update banner icon
    if (status === 'MATCHED') {
      resultStatusIcon.innerHTML = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`;
    } else if (status === 'MODIFIED') {
      resultStatusIcon.innerHTML = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`;
    } else if (status === 'MISSING') {
      resultStatusIcon.innerHTML = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`;
    } else {
      resultStatusIcon.innerHTML = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
    }

    // Metadata
    resFileName.textContent = result.file_name;
    resFilePath.textContent = result.file_path;
    resVerifiedAt.textContent = result.verified_at ? result.verified_at.replace('T', ' ').slice(0, 19) + ' UTC' : 'N/A';
    resBaselineCreated.textContent = result.baseline_created_at
      ? result.baseline_created_at.replace('T', ' ').slice(0, 19) + ' UTC'
      : 'N/A';

    // Hash comparison
    resBaselineHash.textContent = result.baseline_hash || 'NO_BASELINE_STORED';
    resCurrentHash.textContent = result.current_hash || 'NOT_CALCULATED';

    if (result.current_hash && result.baseline_hash) {
      if (result.current_hash.toLowerCase() === result.baseline_hash.toLowerCase()) {
        resCurrentHash.style.color = '#3fb950';
      } else {
        resCurrentHash.style.color = '#d29922';
      }
    } else {
      resCurrentHash.style.color = 'var(--text-main)';
    }

    loadStats();
  }

  if (btnCopyBaselineHash) {
    btnCopyBaselineHash.addEventListener('click', () => {
      if (state.lastVerificationResult && state.lastVerificationResult.baseline_hash) {
        copyTextToClipboard(state.lastVerificationResult.baseline_hash, 'Baseline hash copied!');
      }
    });
  }

  if (btnCopyCurrentHash) {
    btnCopyCurrentHash.addEventListener('click', () => {
      if (state.lastVerificationResult && state.lastVerificationResult.current_hash) {
        copyTextToClipboard(state.lastVerificationResult.current_hash, 'Current hash copied!');
      }
    });
  }

  if (btnDownloadReport) {
    btnDownloadReport.addEventListener('click', async () => {
      if (!state.lastVerificationResult) return;
      const historyId = state.lastVerificationResult.history_id;
      if (historyId) {
        openReportModal(historyId);
      } else {
        showToast('Report unavailable: no history record ID.', 'error');
      }
    });
  }

  // ---------------------------------------------------------------------------
  // Screen 4: History & Baselines
  // ---------------------------------------------------------------------------
  if (tabSubHistory && tabSubBaselines) {
    tabSubHistory.addEventListener('click', () => {
      tabSubHistory.classList.add('active');
      tabSubBaselines.classList.remove('active');
      historyLogsView.style.display = 'block';
      historyBaselinesView.style.display = 'none';
      historyFilters.style.display = 'flex';
      loadHistory();
    });

    tabSubBaselines.addEventListener('click', () => {
      tabSubBaselines.classList.add('active');
      tabSubHistory.classList.remove('active');
      historyLogsView.style.display = 'none';
      historyBaselinesView.style.display = 'block';
      historyFilters.style.display = 'none';
      loadBaselines();
    });
  }

  if (filterStatus) {
    filterStatus.addEventListener('change', () => loadHistory());
  }

  if (btnReloadHistory) {
    btnReloadHistory.addEventListener('click', () => {
      loadHistory();
      loadBaselines();
      showToast('Refreshed audit history and baselines', 'info', 1500);
    });
  }

  async function loadHistory() {
    const status = filterStatus ? filterStatus.value : '';
    const url = status ? `/api/history?status=${encodeURIComponent(status)}` : '/api/history';

    try {
      const res = await fetch(url);
      const data = await res.json();
      if (!data.success) return;

      renderHistoryTable(data.history || []);
    } catch (err) {
      console.error('Error loading history:', err);
    }
  }

  function renderHistoryTable(records) {
    if (!historyTableBody) return;
    if (!records || records.length === 0) {
      historyTableBody.innerHTML = `<tr><td colspan="6" class="text-center">No verification audit records matching criteria.</td></tr>`;
      return;
    }

    historyTableBody.innerHTML = records
      .map((r) => {
        const badgeClass = getBadgeClass(r.status);
        const timeFormatted = r.verified_at ? r.verified_at.replace('T', ' ').slice(0, 19) : '-';
        const hashShort = r.current_hash ? r.current_hash.slice(0, 16) + '...' : '-';

        return `
          <tr>
            <td>#${r.id}</td>
            <td><span class="badge ${badgeClass}">${r.status}</span></td>
            <td><strong title="${escapeHtml(r.file_path)}">${escapeHtml(r.file_name)}</strong></td>
            <td>${timeFormatted} UTC</td>
            <td class="mono" title="${r.current_hash || ''}">${hashShort}</td>
            <td>
              <button class="btn btn-secondary btn-xs" onclick="window.viewReport(${r.id})">Report</button>
              <button class="btn btn-primary btn-xs" onclick="window.reverifyPath('${escapeJsString(r.file_path)}')">Verify</button>
            </td>
          </tr>
        `;
      })
      .join('');
  }

  async function loadBaselines() {
    try {
      const res = await fetch('/api/baselines');
      const data = await res.json();
      if (!data.success) return;

      renderBaselinesTable(data.baselines || []);
    } catch (err) {
      console.error('Error loading baselines:', err);
    }
  }

  function renderBaselinesTable(baselines) {
    if (!baselinesTableBody) return;
    if (!baselines || baselines.length === 0) {
      baselinesTableBody.innerHTML = `<tr><td colspan="7" class="text-center">No trusted baselines established yet.</td></tr>`;
      return;
    }

    baselinesTableBody.innerHTML = baselines
      .map((b) => {
        const createdFormatted = b.created_at ? b.created_at.replace('T', ' ').slice(0, 19) : '-';
        const lastVerFormatted = b.last_verified_at ? b.last_verified_at.replace('T', ' ').slice(0, 19) : 'Never';
        const hashShort = b.sha256 ? b.sha256.slice(0, 16) + '...' : '-';
        const sizeFormatted = formatBytes(b.file_size);

        return `
          <tr>
            <td>#${b.id}</td>
            <td><strong title="${escapeHtml(b.file_path)}">${escapeHtml(b.file_name)}</strong></td>
            <td>${sizeFormatted}</td>
            <td>${createdFormatted}</td>
            <td>${lastVerFormatted}</td>
            <td class="mono" title="${b.sha256}">${hashShort}</td>
            <td>
              <button class="btn btn-primary btn-xs" onclick="window.reverifyPath('${escapeJsString(b.file_path)}')">Verify</button>
              <button class="btn btn-danger btn-xs" onclick="window.deleteBaseline(${b.id})">Delete</button>
            </td>
          </tr>
        `;
      })
      .join('');
  }

  // ---------------------------------------------------------------------------
  // Global Actions (Exposed to inline button handlers)
  // ---------------------------------------------------------------------------
  window.reverifyPath = function (filePath) {
    executeQuickVerification(filePath);
  };

  window.deleteBaseline = async function (baselineId) {
    if (!confirm(`Are you sure you want to remove baseline #${baselineId}?`)) return;

    try {
      const res = await fetch(`/api/baselines/${baselineId}`, { method: 'DELETE' });
      const data = await res.json();
      if (data.success) {
        showToast(`Baseline #${baselineId} deleted.`, 'success');
        loadBaselines();
        loadStats();
      } else {
        showToast(data.error || 'Failed to delete baseline.', 'error');
      }
    } catch (err) {
      showToast(`Error: ${err.message}`, 'error');
    }
  };

  window.viewReport = function (historyId) {
    openReportModal(historyId);
  };

  // ---------------------------------------------------------------------------
  // Report Modal
  // ---------------------------------------------------------------------------
  async function openReportModal(historyId) {
    state.currentHistoryId = historyId;
    modalReportContent.textContent = 'Generating security audit report...';
    reportModal.style.display = 'flex';

    try {
      const res = await fetch(`/api/report/${historyId}?format=text`);
      if (!res.ok) {
        modalReportContent.textContent = 'Failed to load report from server.';
        return;
      }
      const textReport = await res.text();
      modalReportContent.textContent = textReport;
    } catch (err) {
      modalReportContent.textContent = `Error loading report: ${err.message}`;
    }
  }

  function closeReportModal() {
    reportModal.style.display = 'none';
  }

  if (btnCloseModal) btnCloseModal.addEventListener('click', closeReportModal);
  if (reportModal) {
    reportModal.addEventListener('click', (e) => {
      if (e.target === reportModal) closeReportModal();
    });
  }

  if (btnCopyModalReport) {
    btnCopyModalReport.addEventListener('click', () => {
      const text = modalReportContent.textContent;
      copyTextToClipboard(text, 'Report text copied to clipboard!');
    });
  }

  if (btnDownloadModalReport) {
    btnDownloadModalReport.addEventListener('click', () => {
      const text = modalReportContent.textContent;
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `integrity_audit_report_${state.currentHistoryId || Date.now()}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('Audit report downloaded successfully.', 'success');
    });
  }

  // ---------------------------------------------------------------------------
  // Utility Functions
  // ---------------------------------------------------------------------------
  function getBadgeClass(status) {
    switch ((status || '').toUpperCase()) {
      case 'MATCHED':
        return 'badge-matched';
      case 'MODIFIED':
        return 'badge-modified';
      case 'MISSING':
        return 'badge-missing';
      case 'ERROR':
        return 'badge-error';
      default:
        return 'badge-neutral';
    }
  }

  function formatBytes(bytes) {
    if (!bytes || bytes <= 0) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB'];
    let i = 0;
    let size = bytes;
    while (size >= 1024 && i < units.length - 1) {
      size /= 1024;
      i++;
    }
    return `${size.toFixed(i > 0 ? 1 : 0)} ${units[i]}`;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function escapeJsString(str) {
    if (!str) return '';
    return str.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
  }

  // Initial Load
  loadStats();
});
