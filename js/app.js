// Main Application Logic for Campus Placement Analytics

document.addEventListener('DOMContentLoaded', () => {
  initApp();
});

function initApp() {
  renderSummaryKPIs();
  initTabNavigation();
  renderStudentTable();
  initTableFilters();
  initModalHandlers();

  // Initialize Chart.js visualizations
  setTimeout(() => {
    initPlacementCharts();
  }, 100);
}

// 1. Render Summary KPI Cards
function renderSummaryKPIs() {
  const summary = PlacementData.summary;
  
  const kpiPlacementRate = document.getElementById('kpiPlacementRate');
  const kpiAvgPackage = document.getElementById('kpiAvgPackage');
  const kpiTotalOffers = document.getElementById('kpiTotalOffers');
  const kpiRecruiters = document.getElementById('kpiRecruiters');

  if (kpiPlacementRate) kpiPlacementRate.innerText = summary.placementPercentage + '%';
  if (kpiAvgPackage) kpiAvgPackage.innerText = summary.averagePackage + ' LPA';
  if (kpiTotalOffers) kpiTotalOffers.innerText = summary.totalOffers;
  if (kpiRecruiters) kpiRecruiters.innerText = summary.activeRecruiters;
}

// 2. Tab Navigation Handler
function initTabNavigation() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const activeContent = document.getElementById(targetTab);
      if (activeContent) activeContent.classList.add('active');

      // Re-trigger chart resize when switching tabs
      window.dispatchEvent(new Event('resize'));
    });
  });
}

// 3. Render Student Application Tracker Table (Implementing reference image columns & status color coding)
function renderStudentTable(filteredStudents = null) {
  const tbody = document.getElementById('studentTableBody');
  if (!tbody) return;

  const dataToRender = filteredStudents || PlacementData.students;
  tbody.innerHTML = '';

  if (dataToRender.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" style="text-align: center; padding: 2rem; color: var(--text-muted);">
          <i class="fas fa-search" style="font-size: 1.5rem; margin-bottom: 0.5rem; display: block;"></i>
          No student application records found matching your filters.
        </td>
      </tr>
    `;
    return;
  }

  dataToRender.forEach(stu => {
    const tr = document.createElement('tr');

    // Determine status badge color class as required by prompt reference
    let badgeClass = 'status-yellow';
    let iconClass = 'fa-clock';
    
    if (stu.status === 'Offer' || stu.status === 'Shortlisted') {
      badgeClass = 'status-green';
      iconClass = 'fa-check-circle';
    } else if (stu.status === 'Rejected') {
      badgeClass = 'status-red';
      iconClass = 'fa-times-circle';
    } else if (stu.status === 'Interview') {
      badgeClass = 'status-yellow';
      iconClass = 'fa-calendar-alt';
    }

    tr.innerHTML = `
      <td>
        <div class="student-cell">
          <img src="${stu.avatar}" alt="${stu.name}" class="student-avatar" onerror="this.src='https://via.placeholder.com/40'">
          <div>
            <div class="student-name">${stu.name}</div>
            <div class="student-dept">${stu.rollNo} • <span class="badge-dept">${stu.dept}</span></div>
          </div>
        </div>
      </td>
      <td>
        <strong style="color: #f3f4f6;">${stu.company}</strong>
      </td>
      <td>
        <span style="color: var(--text-muted);">${stu.role}</span>
      </td>
      <td>
        <span style="color: var(--text-dim); font-size: 0.85rem;">${stu.appDate}</span>
      </td>
      <td>
        <span class="status-badge ${badgeClass}">
          <i class="fas ${iconClass}"></i> ${stu.status}
        </span>
      </td>
      <td>
        <div style="font-size: 0.85rem; color: #e2e8f0;">
          <i class="far fa-clock" style="color: var(--accent-cyan); margin-right: 0.3rem;"></i>
          ${stu.testDate}
        </div>
      </td>
      <td>
        <span class="resume-pill" title="Click to view resume details">
          <i class="far fa-file-pdf" style="color: #ef4444; margin-right: 0.3rem;"></i>
          ${stu.resumeVersion}
        </span>
      </td>
      <td>
        <button class="action-btn" onclick="openStudentModal('${stu.id}')" title="View Profile">
          <i class="fas fa-id-card"></i>
        </button>
        <button class="action-btn" onclick="syncCalendar('${stu.id}')" title="Sync to Calendar Alert">
          <i class="fas fa-calendar-plus" style="color: var(--accent-cyan);"></i>
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}

// 4. Live Table Search & Filter Handlers
function initTableFilters() {
  const searchInput = document.getElementById('studentSearchInput');
  const deptFilter = document.getElementById('deptFilterSelect');
  const statusFilter = document.getElementById('statusFilterSelect');

  function applyFilters() {
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const deptVal = deptFilter ? deptFilter.value : 'ALL';
    const statusVal = statusFilter ? statusFilter.value : 'ALL';

    const filtered = PlacementData.students.filter(stu => {
      const matchesSearch = 
        stu.name.toLowerCase().includes(query) ||
        stu.company.toLowerCase().includes(query) ||
        stu.role.toLowerCase().includes(query) ||
        stu.resumeVersion.toLowerCase().includes(query) ||
        stu.rollNo.toLowerCase().includes(query);

      const matchesDept = (deptVal === 'ALL' || stu.dept === deptVal);
      const matchesStatus = (statusVal === 'ALL' || stu.status === statusVal);

      return matchesSearch && matchesDept && matchesStatus;
    });

    renderStudentTable(filtered);
  }

  if (searchInput) searchInput.addEventListener('input', applyFilters);
  if (deptFilter) deptFilter.addEventListener('change', applyFilters);
  if (statusFilter) statusFilter.addEventListener('change', applyFilters);
}

// 5. Open Individual Student Profile Card Modal
function openStudentModal(studentId) {
  const stu = PlacementData.students.find(s => s.id === studentId);
  if (!stu) return;

  const modalOverlay = document.getElementById('studentProfileModal');
  const modalContent = document.getElementById('studentProfileContent');

  if (!modalOverlay || !modalContent) return;

  let badgeClass = 'status-yellow';
  if (stu.status === 'Offer' || stu.status === 'Shortlisted') badgeClass = 'status-green';
  if (stu.status === 'Rejected') badgeClass = 'status-red';

  modalContent.innerHTML = `
    <div style="display: flex; gap: 1.5rem; align-items: center; margin-bottom: 1.5rem;">
      <img src="${stu.avatar}" alt="${stu.name}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 3px solid var(--accent-primary);">
      <div>
        <h2 style="font-size: 1.4rem; font-weight: 700;">${stu.name}</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">${stu.rollNo} • Department of ${stu.dept}</p>
        <p style="color: var(--text-dim); font-size: 0.85rem;">CGPA: <strong style="color: var(--accent-cyan);">${stu.cgpa}</strong> | ${stu.email}</p>
      </div>
    </div>

    <div style="background: rgba(0,0,0,0.3); padding: 1.25rem; border-radius: 12px; border: 1px solid var(--border-color); margin-bottom: 1.5rem;">
      <h3 style="font-size: 1rem; color: var(--text-muted); margin-bottom: 0.75rem; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;">Current Application Details</h3>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
          <span style="color: var(--text-dim); font-size: 0.8rem; display: block;">Target Company</span>
          <strong style="font-size: 1.1rem; color: white;">${stu.company}</strong>
        </div>
        <div>
          <span style="color: var(--text-dim); font-size: 0.8rem; display: block;">Applied Role</span>
          <strong style="color: var(--text-main);">${stu.role}</strong>
        </div>
        <div>
          <span style="color: var(--text-dim); font-size: 0.8rem; display: block;">Application Status</span>
          <span class="status-badge ${badgeClass}" style="margin-top: 0.2rem;">${stu.status}</span>
        </div>
        <div>
          <span style="color: var(--text-dim); font-size: 0.8rem; display: block;">Test / Interview Schedule</span>
          <span style="color: var(--accent-cyan); font-weight: 600; font-size: 0.9rem;">${stu.testDate}</span>
        </div>
      </div>
    </div>

    <div style="margin-bottom: 1.5rem;">
      <h3 style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem;">Submitted Resume Version</h3>
      <div style="background: rgba(255,255,255,0.05); padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between;">
        <span><i class="far fa-file-pdf" style="color: #ef4444; margin-right: 0.5rem;"></i> ${stu.resumeVersion}</span>
        <button class="btn-secondary" onclick="alert('Viewing document version: ${stu.resumeVersion}')">Preview Resume</button>
      </div>
    </div>

    <div>
      <h3 style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 0.5rem;">Verified Skills & Proficiencies</h3>
      <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
        ${stu.skills.map(sk => `<span style="background: rgba(99, 102, 241, 0.15); color: #a5b4fc; padding: 0.3rem 0.7rem; border-radius: 20px; font-size: 0.8rem; border: 1px solid rgba(99, 102, 241, 0.3);">${sk}</span>`).join('')}
      </div>
    </div>
  `;

  modalOverlay.classList.add('active');
}

// 6. Sync Interview/Test Dates with Google Calendar / ICS Download (Prompt feature requirement)
function syncCalendar(studentId) {
  const stu = PlacementData.students.find(s => s.id === studentId);
  if (!stu) return;

  const eventTitle = encodeURIComponent(`Interview/Test: ${stu.company} (${stu.role}) - ${stu.name}`);
  const eventDetails = encodeURIComponent(`Campus Placement Selection Round for ${stu.name}\nCompany: ${stu.company}\nRole: ${stu.role}\nResume: ${stu.resumeVersion}`);
  const googleCalUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${eventTitle}&details=${eventDetails}`;

  const userChoice = confirm(`Sync interview reminder for ${stu.name} with Google Calendar?\n\nCompany: ${stu.company}\nTest Date: ${stu.testDate}`);
  if (userChoice) {
    window.open(googleCalUrl, '_blank');
  }
}

// 7. Modal Handlers (Close & Add Entry)
function initModalHandlers() {
  const addBtn = document.getElementById('addApplicationBtn');
  const addModal = document.getElementById('addApplicationModal');
  const closeBtns = document.querySelectorAll('.close-modal-trigger');
  const addForm = document.getElementById('addApplicationForm');

  if (addBtn && addModal) {
    addBtn.addEventListener('click', () => {
      addModal.classList.add('active');
    });
  }

  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
    });
  });

  // Handle outside click to close modal
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
      }
    });
  });

  // Handle Form Submission
  if (addForm) {
    addForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('inputStudentName').value;
      const dept = document.getElementById('inputDept').value;
      const company = document.getElementById('inputCompany').value;
      const role = document.getElementById('inputRole').value;
      const status = document.getElementById('inputStatus').value;
      const testDate = document.getElementById('inputTestDate').value;
      const resumeVersion = document.getElementById('inputResumeVersion').value;

      const newStudent = {
        id: 'STU-' + (1000 + PlacementData.students.length + 1),
        name: name,
        avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80',
        rollNo: `21${dept}0` + (PlacementData.students.length + 10),
        dept: dept,
        cgpa: 8.5,
        email: `${name.toLowerCase().replace(/\s+/g, '.')}@college.edu`,
        company: company,
        role: role,
        appDate: new Date().toISOString().split('T')[0],
        status: status,
        testDate: testDate || 'TBD',
        resumeVersion: resumeVersion || 'Resume_v1_General.pdf',
        skills: ["Problem Solving", "Communication"]
      };

      PlacementData.students.unshift(newStudent);
      renderStudentTable();
      
      addModal.classList.remove('active');
      addForm.reset();
      alert(`Successfully added application record for ${name}!`);
    });
  }
}
