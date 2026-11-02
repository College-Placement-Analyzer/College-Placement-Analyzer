# College Placement Tracker & Analytics Command Center

An institutional-grade placement management and analytics platform for colleges and universities to track student applications, recruiter pipelines, interview stages, offer statuses, and department-level placement statistics.

---

## 📁 Project Structure

```
college-placement-tracker/
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
