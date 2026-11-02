# College Placement Tracker & Analytics Command Center

An institutional-grade placement management and analytics platform for colleges and universities to track student applications, recruiter pipelines, interview stages, offer statuses, and department-level placement statistics.

---

## 📁 Project Structure

```
college-placement-tracker/
├── College_Placement_Comprehensive_Analytics_Report.pdf  # Comprehensive 8-page multi-dataset analytics report
├── charts/                          # 19 High-resolution publication-quality visualization figures
├── data/                            # Processed & cleaned CSV datasets
│   ├── college_placement_trends.csv # Institutional trends (250 Colleges, 7 Cohorts 2020-2026, 1,750 records)
│   └── student_placement_records.csv# Student records (1,999 Engineers, 24 academic/placement variables)
├── scripts/                         # Pipeline scripts for dataset parsing, charting & PDF generation
│   ├── export_datasets.py           # Extracts and validates both datasets from source files
│   ├── generate_charts.py           # Generates all 19 chart figures across both datasets
│   └── generate_placement_report_pdf.py # Compiles the multi-page styled analytical PDF report
├── assets/                          # Student photos and image assets
│   ├── student_alex.jpg
│   ├── student_david.jpg
│   └── student_priya.jpg
├── css/
│   └── styles.css                   # Custom responsive stylesheet & dark theme
├── js/
│   ├── app.js                       # UI interactions, modals, filtering & application logic
│   ├── charts.js                    # Chart.js visualizations (trends, salary spectrum, department breakdown)
│   └── data.js                      # Core placement data and student records
├── index.html                       # Main interactive dashboard & student application tracker
├── server.py                        # Lightweight Python local HTTP server (port 8000)
├── start_server.bat                 # One-click Windows batch file to start the server
├── open_in_browser.bat              # One-click Windows batch file to open directly in web browser
├── .gitignore                       # Git ignore file
└── README.md                        # Documentation
```

---

## 🚀 How to Run

### Method 1: Direct File Launch (No setup required)
- Double-click `open_in_browser.bat` or double-click `index.html` to open directly in your web browser.

### Method 2: Local Python Server (Recommended)
- Double-click `start_server.bat` OR run:
  ```bash
  python server.py
  ```
- Open your browser at:
  ```
  http://localhost:8000
  ```

---

## ✨ Features

- **Executive Overview Dashboard**: Real-time KPI metrics (Placement Rate, Average CTC, Total Offers, Active Recruiters).
- **Interactive Student Application Tracker**:
  - Live filtering by student, branch, company, status, and salary bracket.
  - Color-coded status tags (Green: Shortlisted/Offer, Yellow: Pending/Interview, Red: Rejected).
  - Interview date & time tracking with resume version tracking.
  - Quick action to add new student applications with real-time updates.
- **Department Performance Analytics**: Comparative placement rates, average and highest packages across departments (CSE, AI/DS, ECE, IT, ME, CE).
- **Recruiter & Salary Spectrum**: Distribution charts showing package brackets (<5 LPA, 5-8 LPA, 8-14 LPA, 14-25 LPA, 25+ LPA).
- **Skill Demand Radar**: Industry demand scores vs student proficiency.

---

## 📊 Comprehensive Placement Analytics PDF Report

The repository includes an institutional-grade, publication-quality 8-page analytical report:  
**[`College_Placement_Comprehensive_Analytics_Report.pdf`](./College_Placement_Comprehensive_Analytics_Report.pdf)**

It features **19 distinct visualization figures** synthesizing both datasets:

### Part 1: Macro & Institutional Placement Trends (Dataset 1 — 250 Colleges, 1,750 Records)
1. **Multi-Line Time Series**: Longitudinal Evolution of Highest, Average, and Median Package (2020–2026).
2. **Grouped Bar Chart**: Campus Placement Rate (%) by Institution Tier and Academic Stream.
3. **Box-and-Whisker Plots**: Salary Dispersion and Outlier Spectrum across Tiers 1, 2, and 3.
4. **Horizontal Bar Chart**: Top 15 Primary Campus Recruiters by Institutional Cohort Presence.
5. **2D Heatmap Matrix**: Mean Average Package (₹ LPA) by Stream and Graduation Year.
6. **Scatter Plot with OLS Fit**: Placement Rate (%) vs. Average Salary Realization (r = +0.84).
7. **Stacked Area Strata**: Tier Median Package Evolution Across Graduation Cohorts.
8. **Categorical Competency Bar Chart**: Most Frequently Required Skills by Primary Recruiters.

### Part 2: Student Academic & Placement Outcomes (Dataset 2 — 1,999 Engineering Records)
9. **Dual Donut Charts**: Overall Placement Success Ratio (51.6%) and Hiring Functional Domain Allocation.
10. **Dual Histograms with KDE**: Offered Compensation Density (Mean ₹11.23L) and GPA Distribution.
11. **Split Violin Plot**: Academic GPA Distributions across Branches stratified by Placement Status.
12. **Bivariate Scatter Plot**: Attendance (%) vs Cumulative GPA with 75% attendance / 7.0 GPA threshold quadrant.
13. **Dual-Axis Bar Chart**: Impact of Academic Backlogs (0–5) on Placement Probability & Realized CTC.
14. **Grouped Bar ROI**: Placement Success and Offered CTC by Internship Status and Domain.
15. **Correlation Matrix Heatmap**: Pearson correlations among demographics, cumulative GPA, attendance, CTC, and Semesters 1–8.
16. **Radar / Spider Chart**: 5-Axis Normalized Departmental Benchmarking Profile (CSE, IT, ECE, MECH).
17. **Longitudinal Trajectory Plot**: Semester 1 to 8 SGPA Progression comparing placed vs unplaced cohorts.
18. **Skill Valuation Error Bar Chart**: Offered CTC and Placement Rate by Core Technical Skill.
19. **Stacked Alluvial Distribution**: Alumni Post-Graduation Career Destinations across Hiring Domains.

---

## 🛠️ Data Pipeline & Report Regeneration

To re-extract datasets, re-render visualization figures, and re-compile the PDF report:

```bash
# 1. Extract and clean datasets
python scripts/export_datasets.py

# 2. Render all 19 high-resolution chart images
python scripts/generate_charts.py

# 3. Compile the 8-page analytical PDF report
python scripts/generate_placement_report_pdf.py
```

