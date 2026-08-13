// Chart.js Visualizations Manager for Campus Placement Analytics

let chartInstances = {};

function initPlacementCharts() {
  if (typeof Chart === 'undefined') {
    console.error("Chart.js library is missing!");
    return;
  }

  // Global Chart Defaults
  Chart.defaults.color = '#9ca3af';
  Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.08)';
  Chart.defaults.font.family = "'Outfit', 'Inter', sans-serif";

  renderPlacementTrendChart();
  renderDepartmentCompareChart();
  renderCompanyHiringChart();
  renderSalaryDistChart();
  renderSkillDemandChart();
}

// 1. Placement Percentage Trend (Line Chart)
function renderPlacementTrendChart() {
  const ctx = document.getElementById('trendChartCanvas');
  if (!ctx) return;

  if (chartInstances.trend) chartInstances.trend.destroy();

  chartInstances.trend = new Chart(ctx, {
    type: 'line',
    data: {
      labels: PlacementData.placementTrend.map(d => d.month),
      datasets: [
        {
          label: 'Placement Rate (%)',
          data: PlacementData.placementTrend.map(d => d.percentage),
          borderColor: '#6366f1',
          backgroundColor: 'rgba(99, 102, 241, 0.15)',
          fill: true,
          tension: 0.35,
          borderWidth: 3,
          pointBackgroundColor: '#818cf8',
          pointRadius: 5
        },
        {
          label: 'Total Offers Issued',
          data: PlacementData.placementTrend.map(d => d.offers),
          borderColor: '#06b6d4',
          backgroundColor: 'transparent',
          borderDash: [5, 5],
          tension: 0.35,
          borderWidth: 2,
          pointRadius: 4,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      scales: {
        y: {
          min: 0,
          max: 100,
          ticks: { callback: v => v + '%' }
        },
        y1: {
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { callback: v => v + ' offers' }
        }
      },
      plugins: {
        legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8 } }
      }
    }
  });
}

// 2. Department Performance Comparison (Grouped Bar Chart)
function renderDepartmentCompareChart() {
  const ctx = document.getElementById('deptCompareCanvas');
  if (!ctx) return;

  if (chartInstances.dept) chartInstances.dept.destroy();

  chartInstances.dept = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: PlacementData.departmentStats.map(d => d.code),
      datasets: [
        {
          label: 'Placement %',
          data: PlacementData.departmentStats.map(d => d.rate),
          backgroundColor: 'rgba(99, 102, 241, 0.85)',
          borderRadius: 6
        },
        {
          label: 'Avg CTC (LPA)',
          data: PlacementData.departmentStats.map(d => d.avgPackage),
          backgroundColor: 'rgba(6, 182, 212, 0.85)',
          borderRadius: 6,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          max: 100,
          ticks: { callback: v => v + '%' }
        },
        y1: {
          position: 'right',
          grid: { drawOnChartArea: false },
          ticks: { callback: v => v + ' LPA' }
        }
      },
      plugins: {
        legend: { position: 'top' }
      }
    }
  });
}

// 3. Company-Wise Hiring (Horizontal Bar)
function renderCompanyHiringChart() {
  const ctx = document.getElementById('companyHiringCanvas');
  if (!ctx) return;

  if (chartInstances.company) chartInstances.company.destroy();

  const sorted = [...PlacementData.companyHiring].sort((a, b) => b.offers - a.offers);

  chartInstances.company = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sorted.map(c => c.company),
      datasets: [{
        label: 'Number of Hires',
        data: sorted.map(c => c.offers),
        backgroundColor: sorted.map((c, i) => i < 4 ? 'rgba(139, 92, 246, 0.85)' : 'rgba(99, 102, 241, 0.6)'),
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { ticks: { precision: 0 } }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

// 4. Salary Distribution Spectrum (Doughnut & Bar)
function renderSalaryDistChart() {
  const ctx = document.getElementById('salaryDistCanvas');
  if (!ctx) return;

  if (chartInstances.salary) chartInstances.salary.destroy();

  chartInstances.salary = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: PlacementData.salaryDistribution.map(s => s.bracket),
      datasets: [{
        data: PlacementData.salaryDistribution.map(s => s.count),
        backgroundColor: [
          '#64748b',
          '#06b6d4',
          '#6366f1',
          '#8b5cf6',
          '#10b981'
        ],
        borderWidth: 2,
        borderColor: '#111827'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { padding: 15 } }
      },
      cutout: '65%'
    }
  });
}

// 5. Skill Demand & Proficiency Radar Chart
function renderSkillDemandChart() {
  const ctx = document.getElementById('skillDemandCanvas');
  if (!ctx) return;

  if (chartInstances.skill) chartInstances.skill.destroy();

  chartInstances.skill = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: PlacementData.skillDemand.map(s => s.skill),
      datasets: [
        {
          label: 'Recruiter Demand Index',
          data: PlacementData.skillDemand.map(s => s.demandScore),
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.2)',
          borderWidth: 2,
          pointBackgroundColor: '#ef4444'
        },
        {
          label: 'Student Skill Index',
          data: PlacementData.skillDemand.map(s => s.studentProficiency),
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.2)',
          borderWidth: 2,
          pointBackgroundColor: '#10b981'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
          grid: { color: 'rgba(255, 255, 255, 0.1)' },
          pointLabels: { font: { size: 11 } },
          min: 0,
          max: 100
        }
      },
      plugins: {
        legend: { position: 'top' }
      }
    }
  });
}
