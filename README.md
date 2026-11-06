# College Placement Analyzer & Analytics Pipeline

An end-to-end data science and analytics project designed to clean, harmonize, analyze, and visualize college placement data across institutional trends and individual student outcomes.

The project analyzes two datasets:
1. **Student Placement Records**: Micro-level academic, demographic, skill profile, internship, and CTC data for 1,984 engineering students.
2. **Institutional Placement Trends**: Macro-level placement rates, salary packages (Highest, Average, Median), and primary recruiters across 250 colleges over 7 graduation cohorts (2020–2026, 1,750 records).

---

## Deliverables & Submission Checklist

| Deliverable | File Name | Description |
| :--- | :--- | :--- |
| **1. Project Proposal** | `Project_Proposal.pdf` | Project concept, problem statement, objectives, and analytical scope |
| **2. Dataset** | `Dataset/` | Raw datasets (`students.xlsx`, `indian_college_placements_expanded_2020_2026.docx`, CSVs) |
| **3. Data Cleaning** | `data_cleaning.py` | End-to-end cleaning, anomaly detection, deduplication, and export pipeline |
| **4. Cleaned Dataset** | `clean_dataset.xlsx` | Multi-sheet cleaned workbook (`Cleaned_Students`, `Placement_Data`, `Combined_Data`, `Data_Quality_Summary`) |
| **5. Data Analysis** | `Data_analysis.py` | Statistical analysis, hypothesis testing, correlation metrics, and cohort evaluations |
| **6. Data Visualisation** | `Data_visualisation.py` | Publication-ready visual charts (19 figures) generated across both datasets |
| **7. Dashboard** | `DAV_Project.pbix` | Power BI dashboard template connected to the cleaned placement dataset |
| **Submission Archive** | `College_Placement_Project_Submission.zip` | Complete submission package containing all required deliverables |

---

## Project Structure

```
college-placement-tracker/
├── Project_Proposal.pdf                            # Project proposal document
├── clean_dataset.xlsx                              # Multi-sheet cleaned Excel dataset
├── data_cleaning.py                                # End-to-end data cleaning script
├── Data_analysis.py                                # Statistical and exploratory data analysis
├── Data_visualisation.py                           # Chart generation script (19 figures)
├── DAV_Project.pbix                                  # Power BI dashboard file
├── College_Placement_Comprehensive_Analytics_Report.pdf # 8-page compiled publication report
├── College_Placement_Project_Submission.zip        # Packaged zip containing all deliverables
├── requirements.txt                                # Python package dependencies
├── README.md                                       # Project documentation
│
├── Dataset/                                        # Raw and source datasets
│   ├── students.xlsx                               # Raw student records
│   ├── indian_college_placements_expanded_2020_2026.docx # Raw institutional records
│   ├── student_placement_records.csv               # Student CSV export
│   └── college_placement_trends.csv                # College trends CSV export
│
├── charts/                                         # 19 High-resolution visualization figures
│   ├── chart1_pkg_trends.png
│   ├── chart2_stream_tier_placement_rate.png
│   ├── chart3_tier_salary_boxplot.png
│   ├── chart4_top_recruiters_bar.png
│   ├── chart5_stream_year_heatmap.png
│   ├── chart6_scatter_placement_vs_avgpkg.png
│   ├── chart7_highest_pkg_area.png
│   ├── chart8_skills_demanded_bar.png
│   ├── chart9_donut_placement_status_and_domain.png
│   ├── chart10_ctc_and_gpa_histogram_kde.png
│   ├── chart11_branch_gpa_violin.png
│   ├── chart12_attendance_vs_gpa_scatter.png
│   ├── chart13_backlogs_impact_barchart.png
│   ├── chart14_internship_roi_groupedbar.png
│   ├── chart15_correlation_heatmap.png
│   ├── chart16_branch_radar_profile.png
│   ├── chart17_semester_gpa_progression.png
│   ├── chart18_skills_vs_ctc_bar.png
│   └── chart19_alumni_path_distribution.png
│
├── data/                                           # Processed data exports & cache
│   ├── clean_dataset.csv
│   ├── college_placement_trends.csv
│   └── student_placement_records.csv
│
└── scripts/                                        # Additional pipeline utilities
    ├── export_datasets.py
    ├── generate_charts.py
    └── generate_placement_report_pdf.py
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.10+ installed
- PowerShell, Command Prompt, or Terminal

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate.bat
# Linux/macOS:
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

---

## Execution Guide

### Step 1: Data Cleaning & Preprocessing
Cleans student records (removes invalid/corrupted records, removes duplicate profiles, formats missing fields) and parses 1,750 college placement records from the Word document.
```bash
python data_cleaning.py
```
**Outputs**:
- `clean_dataset.xlsx`
- `cleaned_combined_placement_data.xlsx`
- `data/student_placement_records.csv`
- `data/college_placement_trends.csv`

---

### Step 2: Statistical Data Analysis
Performs statistical summaries, department comparisons, academic performance impacts, recruiter share, and correlation testing.
```bash
python Data_analysis.py
```
**Options**:
```bash
# Save analysis text report to disk:
python Data_analysis.py --save-report
```

---

### Step 3: Data Visualisation
Generates all 19 charts covering institutional trends and student performance.
```bash
python Data_visualisation.py
```
**Outputs**: 19 high-resolution PNG charts in `charts/`.

---

### Step 4: Publication-Quality PDF Report Generation
Compiles all data tables, visualizations, executive summaries, and recommendations into an 8-page publication-ready PDF report.
```bash
python scripts/generate_placement_report_pdf.py
```
**Output**: `College_Placement_Comprehensive_Analytics_Report.pdf`

---

## Key Analytical Findings

### 1. Student Cohort Overview (N = 1,984)
- **Overall Placement Rate**: 51.61% (1,024 placed, 960 unplaced).
- **Salary Spectrum (Placed)**: Mean CTC of 11.22 LPA (Median: 11.12 LPA, Std: 4.75 LPA, Range: 3.04 – 19.99 LPA).
- **Academic Performance**: Mean GPA is 7.00 across branches; average attendance is 78.94%.
- **Branch Placement Rates**: EEE leads at 59.1%, followed by ECE (53.1%), IT (52.1%), CSE (49.7%), CIVIL (49.4%), and MECH (46.4%).

### 2. Institutional Trends (250 Colleges, 2020–2026)
- **Tier 1 Institutions**: Average placement rate of 91.31% with mean package of 21.58 LPA (peak package reaches 135.30 LPA).
- **Tier 2 Institutions**: Average placement rate of 79.63% with mean package of 9.95 LPA.
- **Tier 3 Institutions**: Average placement rate of 61.24% with mean package of 4.59 LPA.
- **Placement Rate vs. Package Correlation**: Strong positive correlation (Pearson $r = 0.683$, Spearman $\rho = 0.768$) between placement rate and average package.
- **Longitudinal Growth**: Institutional packages expanded at a 3.07% CAGR between 2020 and 2026.

---

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
