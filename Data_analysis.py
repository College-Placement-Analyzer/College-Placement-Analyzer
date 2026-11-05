import os
import sys
import math
import argparse
import pandas as pd
import numpy as np

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


def load_datasets():
    student_df = None
    college_df = None

    excel_path = 'cleaned_combined_placement_data.xlsx'
    if os.path.exists(excel_path):
        try:
            xl = pd.ExcelFile(excel_path)
            if 'Cleaned_Students' in xl.sheet_names:
                student_df = pd.read_excel(excel_path, sheet_name='Cleaned_Students')
            if 'Placement_Data' in xl.sheet_names:
                college_df = pd.read_excel(excel_path, sheet_name='Placement_Data')
        except Exception:
            pass

    if student_df is None and os.path.exists('data/student_placement_records.csv'):
        student_df = pd.read_csv('data/student_placement_records.csv')
    if college_df is None and os.path.exists('data/college_placement_trends.csv'):
        college_df = pd.read_csv('data/college_placement_trends.csv')

    if student_df is None and os.path.exists('students.xlsx'):
        student_df = pd.read_excel('students.xlsx').dropna(subset=['Student ID', 'Branch'])

    if student_df is None or college_df is None:
        raise FileNotFoundError("Placement datasets not found.")

    student_df['Placement Status'] = student_df['Placement Status'].fillna('Not Placed')
    student_df['Placement Domain'] = student_df['Placement Domain'].fillna('None').replace('', 'None')
    student_df['Internship Done'] = student_df['Internship Done'].fillna('No')
    student_df['Internship Domain'] = student_df['Internship Domain'].fillna('None').replace('', 'None')
    student_df['Alumni Path'] = student_df['Alumni Path'].fillna('None').replace('', 'None')
    student_df['CTC (LPA)'] = pd.to_numeric(student_df['CTC (LPA)'], errors='coerce').fillna(0.0)

    return student_df, college_df


def compute_t_test(sample1, sample2):
    s1 = np.array(sample1, dtype=float)
    s2 = np.array(sample2, dtype=float)
    s1 = s1[~np.isnan(s1)]
    s2 = s2[~np.isnan(s2)]
    
    n1, n2 = len(s1), len(s2)
    if n1 < 2 or n2 < 2:
        return 0.0, 1.0, 0.0
    
    m1, m2 = np.mean(s1), np.mean(s2)
    v1, v2 = np.var(s1, ddof=1), np.var(s2, ddof=1)
    
    pooled_sd = math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2)) if (n1 + n2 - 2) > 0 else 1.0
    cohens_d = (m1 - m2) / pooled_sd if pooled_sd > 0 else 0.0
    
    if SCIPY_AVAILABLE:
        res = stats.ttest_ind(s1, s2, equal_var=False)
        return float(res.statistic), float(res.pvalue), cohens_d
    else:
        se_diff = math.sqrt(v1 / n1 + v2 / n2)
        if se_diff == 0:
            return 0.0, 1.0, cohens_d
        t_stat = (m1 - m2) / se_diff
        df = ((v1/n1 + v2/n2)**2) / (((v1/n1)**2)/(n1-1) + ((v2/n2)**2)/(n2-1))
        p_val = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_stat) / math.sqrt(2))))
        return float(t_stat), float(p_val), cohens_d


def compute_anova(groups):
    valid_groups = [np.array(g[~np.isnan(g)], dtype=float) for g in groups if len(g) > 1]
    k = len(valid_groups)
    if k < 2:
        return 0.0, 1.0
    
    if SCIPY_AVAILABLE:
        res = stats.f_oneway(*valid_groups)
        return float(res.statistic), float(res.pvalue)
    
    all_data = np.concatenate(valid_groups)
    n_total = len(all_data)
    grand_mean = np.mean(all_data)
    
    ssb = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in valid_groups)
    ssw = sum(sum((val - np.mean(g))**2 for val in g) for g in valid_groups)
    
    df_between = k - 1
    df_within = n_total - k
    
    msb = ssb / df_between if df_between > 0 else 0
    msw = ssw / df_within if df_within > 0 else 1.0
    f_stat = msb / msw if msw > 0 else 0.0
    
    z = (f_stat**(1/3) - (1 - 2/(9*df_within))) / math.sqrt(2/(9*df_within) + (f_stat**(2/3))*(2/(9*df_between))) if df_between > 0 and df_within > 0 else 0
    p_val = 1.0 - 0.5 * (1.0 + math.erf(z / math.sqrt(2)))
    p_val = max(0.0, min(1.0, p_val))
    return float(f_stat), float(p_val)


def compute_chi2(contingency_matrix):
    obs = np.array(contingency_matrix, dtype=float)
    if SCIPY_AVAILABLE:
        chi2, p, dof, _ = stats.chi2_contingency(obs)
        return float(chi2), float(p), int(dof)
    
    row_sums = obs.sum(axis=1)
    col_sums = obs.sum(axis=0)
    total = obs.sum()
    if total == 0:
        return 0.0, 1.0, 0
    
    expected = np.outer(row_sums, col_sums) / total
    chi2 = np.sum((obs - expected)**2 / np.where(expected > 0, expected, 1.0))
    dof = (obs.shape[0] - 1) * (obs.shape[1] - 1)
    
    if dof > 0:
        z = ((chi2 / dof)**(1/3) - (1 - 2/(9*dof))) / math.sqrt(2/(9*dof))
        p_val = 1.0 - 0.5 * (1.0 + math.erf(z / math.sqrt(2)))
        p_val = max(0.0, min(1.0, p_val))
    else:
        p_val = 1.0
    return float(chi2), float(p_val), int(dof)


class StudentPlacementAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        self.placed_df = self.df[self.df['Placement Status'] == 'Placed'].copy()
        self.unplaced_df = self.df[self.df['Placement Status'] == 'Not Placed'].copy()

    def get_cohort_overview(self):
        total = len(self.df)
        placed_count = len(self.placed_df)
        unplaced_count = len(self.unplaced_df)
        placement_rate = (placed_count / total) * 100 if total > 0 else 0.0
        ctc_series = self.placed_df['CTC (LPA)']
        
        return {
            'Total Students': total,
            'Placed Count': placed_count,
            'Not Placed Count': unplaced_count,
            'Placement Rate (%)': round(placement_rate, 2),
            'Mean CTC (LPA)': round(ctc_series.mean(), 2),
            'Median CTC (LPA)': round(ctc_series.median(), 2),
            'Std Dev CTC (LPA)': round(ctc_series.std(), 2),
            'Min CTC (LPA)': round(ctc_series.min(), 2),
            'Max CTC (LPA)': round(ctc_series.max(), 2),
            'IQR CTC (LPA)': round(ctc_series.quantile(0.75) - ctc_series.quantile(0.25), 2),
            'Mean GPA': round(self.df['Average GPA'].mean(), 2),
            'Median GPA': round(self.df['Average GPA'].median(), 2),
            'Mean Attendance (%)': round(self.df['Attendance (%)'].mean(), 2),
            'Total Backlogs Logged': int(self.df['Backlogs'].sum()),
        }

    def analyze_by_branch(self):
        records = []
        for branch, grp in self.df.groupby('Branch'):
            placed_grp = grp[grp['Placement Status'] == 'Placed']
            n_total = len(grp)
            n_placed = len(placed_grp)
            p_rate = (n_placed / n_total) * 100 if n_total > 0 else 0.0
            ctc_s = placed_grp['CTC (LPA)']
            records.append({
                'Branch': branch,
                'Total Candidates': n_total,
                'Placed': n_placed,
                'Placement Rate (%)': round(p_rate, 1),
                'Mean GPA': round(grp['Average GPA'].mean(), 2),
                'Mean Attendance (%)': round(grp['Attendance (%)'].mean(), 1),
                'Mean CTC (LPA)': round(ctc_s.mean(), 2) if len(ctc_s) > 0 else 0.0,
                'Median CTC (LPA)': round(ctc_s.median(), 2) if len(ctc_s) > 0 else 0.0,
                'Max CTC (LPA)': round(ctc_s.max(), 2) if len(ctc_s) > 0 else 0.0,
                'Backlogs per Student': round(grp['Backlogs'].mean(), 2)
            })
        return pd.DataFrame(records).sort_values(by='Placement Rate (%)', ascending=False)

    def analyze_by_gender(self):
        records = []
        for gender, grp in self.df.groupby('Gender'):
            placed_grp = grp[grp['Placement Status'] == 'Placed']
            p_rate = (len(placed_grp) / len(grp)) * 100
            ctc_s = placed_grp['CTC (LPA)']
            records.append({
                'Gender': gender,
                'Total Candidates': len(grp),
                'Placed': len(placed_grp),
                'Placement Rate (%)': round(p_rate, 1),
                'Mean GPA': round(grp['Average GPA'].mean(), 2),
                'Mean Attendance (%)': round(grp['Attendance (%)'].mean(), 1),
                'Mean CTC (LPA)': round(ctc_s.mean(), 2) if len(ctc_s) > 0 else 0.0,
                'Median CTC (LPA)': round(ctc_s.median(), 2) if len(ctc_s) > 0 else 0.0,
            })
        return pd.DataFrame(records)

    def analyze_backlogs_impact(self):
        records = []
        for bl, grp in self.df.groupby('Backlogs'):
            placed_grp = grp[grp['Placement Status'] == 'Placed']
            p_rate = (len(placed_grp) / len(grp)) * 100
            ctc_s = placed_grp['CTC (LPA)']
            records.append({
                'Backlogs Count': int(bl),
                'Students Count': len(grp),
                'Placement Rate (%)': round(p_rate, 1),
                'Mean GPA': round(grp['Average GPA'].mean(), 2),
                'Mean Attendance (%)': round(grp['Attendance (%)'].mean(), 1),
                'Mean Placed CTC (LPA)': round(ctc_s.mean(), 2) if len(ctc_s) > 0 else 0.0,
            })
        return pd.DataFrame(records).sort_values(by='Backlogs Count')

    def analyze_attendance_brackets(self):
        bins = [0, 65, 75, 85, 95, 100]
        labels = ['<65%', '65-75%', '75-85%', '85-95%', '95-100%']
        self.df['Attendance_Bracket'] = pd.cut(self.df['Attendance (%)'], bins=bins, labels=labels, right=True)
        
        records = []
        for brk, grp in self.df.groupby('Attendance_Bracket', observed=False):
            placed_grp = grp[grp['Placement Status'] == 'Placed']
            p_rate = (len(placed_grp) / len(grp)) * 100 if len(grp) > 0 else 0.0
            ctc_s = placed_grp['CTC (LPA)']
            records.append({
                'Attendance Tier': str(brk),
                'Candidates': len(grp),
                'Placement Rate (%)': round(p_rate, 1),
                'Mean GPA': round(grp['Average GPA'].mean(), 2) if len(grp) > 0 else 0.0,
                'Mean CTC (LPA)': round(ctc_s.mean(), 2) if len(ctc_s) > 0 else 0.0,
            })
        return pd.DataFrame(records)

    def analyze_internship_roi(self):
        records = []
        for status, grp in self.df.groupby('Internship Done'):
            placed_grp = grp[grp['Placement Status'] == 'Placed']
            p_rate = (len(placed_grp) / len(grp)) * 100
            ctc_s = placed_grp['CTC (LPA)']
            records.append({
                'Internship Completed': status,
                'Candidates': len(grp),
                'Placed Count': len(placed_grp),
                'Placement Rate (%)': round(p_rate, 1),
                'Mean CTC (LPA)': round(ctc_s.mean(), 2),
                'Median CTC (LPA)': round(ctc_s.median(), 2),
            })
        df_status = pd.DataFrame(records)

        domain_records = []
        intern_df = self.df[self.df['Internship Done'] == 'Yes']
        for domain, grp in intern_df.groupby('Internship Domain'):
            if domain in ['None', '', np.nan]:
                continue
            placed_grp = grp[grp['Placement Status'] == 'Placed']
            p_rate = (len(placed_grp) / len(grp)) * 100
            ctc_s = placed_grp['CTC (LPA)']
            domain_records.append({
                'Internship Domain': domain,
                'Total Interns': len(grp),
                'Placement Rate (%)': round(p_rate, 1),
                'Mean CTC (LPA)': round(ctc_s.mean(), 2) if len(ctc_s) > 0 else 0.0,
                'Median CTC (LPA)': round(ctc_s.median(), 2) if len(ctc_s) > 0 else 0.0,
            })
        df_domain = pd.DataFrame(domain_records).sort_values(by='Mean CTC (LPA)', ascending=False)
        return df_status, df_domain

    def analyze_technical_skills(self):
        core_skills = ['Python', 'Machine Learning', 'Data Science', 'SQL', 'C++', 'Java', 'Web Development']
        records = []
        for skill in core_skills:
            mask = self.df['Skills'].str.contains(skill, na=False, regex=False)
            sub_all = self.df[mask]
            sub_placed = self.df[mask & (self.df['Placement Status'] == 'Placed')]
            
            p_rate = (len(sub_placed) / len(sub_all)) * 100 if len(sub_all) > 0 else 0.0
            ctc_s = sub_placed['CTC (LPA)']
            records.append({
                'Technical Competency': skill,
                'Candidate Count': len(sub_all),
                'Market Penetration (%)': round((len(sub_all) / len(self.df)) * 100, 1),
                'Placement Rate (%)': round(p_rate, 1),
                'Mean CTC (LPA)': round(ctc_s.mean(), 2) if len(ctc_s) > 0 else 0.0,
                'Median CTC (LPA)': round(ctc_s.median(), 2) if len(ctc_s) > 0 else 0.0,
                'Standard Deviation CTC': round(ctc_s.std(), 2) if len(ctc_s) > 0 else 0.0,
            })
        return pd.DataFrame(records).sort_values(by='Mean CTC (LPA)', ascending=False)

    def analyze_semester_progression(self):
        sem_cols = [f'Sem{i} GPA' for i in range(1, 9)]
        records = []
        for i, col in enumerate(sem_cols, 1):
            p_mean = self.placed_df[col].mean()
            p_std = self.placed_df[col].std()
            u_mean = self.unplaced_df[col].mean()
            u_std = self.unplaced_df[col].std()
            diff = p_mean - u_mean
            records.append({
                'Semester': f'Sem {i}',
                'Placed Mean SGPA': round(p_mean, 2),
                'Placed SGPA Std': round(p_std, 2),
                'Unplaced Mean SGPA': round(u_mean, 2),
                'Unplaced SGPA Std': round(u_std, 2),
                'Delta (Placed - Unplaced)': round(diff, 2)
            })
        return pd.DataFrame(records)

    def perform_hypothesis_tests(self):
        results = {}
        
        placed_gpa = self.placed_df['Average GPA'].dropna()
        unplaced_gpa = self.unplaced_df['Average GPA'].dropna()
        t_stat, p_val, d = compute_t_test(placed_gpa, unplaced_gpa)
        results['GPA_Difference_TTest'] = {
            'T-Statistic': round(t_stat, 4),
            'P-Value': p_val,
            'Significant': p_val < 0.05,
            'Cohen d': round(d, 4)
        }
        
        branch_groups = [grp['CTC (LPA)'].dropna().values for _, grp in self.placed_df.groupby('Branch')]
        f_stat, anova_p = compute_anova(branch_groups)
        results['Branch_CTC_ANOVA'] = {
            'F-Statistic': round(f_stat, 4),
            'P-Value': anova_p,
            'Significant': anova_p < 0.05
        }
        
        ct_backlogs = pd.crosstab(self.df['Backlogs'], self.df['Placement Status'])
        chi2, p_chi, dof = compute_chi2(ct_backlogs.values)
        results['Backlogs_Placement_Chi2'] = {
            'Chi2-Statistic': round(chi2, 4),
            'P-Value': p_chi,
            'Degrees of Freedom': dof,
            'Significant': p_chi < 0.05
        }
        
        return results


class InstitutionalPlacementAnalyzer:
    def __init__(self, df):
        self.df = df.copy()

    def get_institutional_overview(self):
        total_obs = len(self.df)
        colleges = self.df['College_Name'].nunique()
        years = sorted(self.df['Graduation_Year'].unique())
        
        return {
            'Total Cohort Observations': total_obs,
            'Unique Institutions': colleges,
            'Year Horizon': f"{min(years)} - {max(years)} ({len(years)} batches)",
            'National Mean Placement Rate (%)': round(self.df['Placement_Rate_Pct'].mean(), 2),
            'National Mean Package (LPA)': round(self.df['Average_Package_LPA'].mean(), 2),
            'National Median Package (LPA)': round(self.df['Median_Package_LPA'].mean(), 2),
            'All-Time Peak Ceiling (LPA)': round(self.df['Highest_Package_LPA'].max(), 2),
            'Mean Package Ceiling (LPA)': round(self.df['Highest_Package_LPA'].mean(), 2),
        }

    def analyze_by_tier(self):
        records = []
        for tier in ['Tier 1', 'Tier 2', 'Tier 3']:
            grp = self.df[self.df['Institution_Tier'] == tier]
            if len(grp) == 0:
                continue
            records.append({
                'Institution Tier': tier,
                'Cohorts Count': len(grp),
                'Mean Placement Rate (%)': round(grp['Placement_Rate_Pct'].mean(), 2),
                'Placement Rate Std (%)': round(grp['Placement_Rate_Pct'].std(), 2),
                'Mean Package (LPA)': round(grp['Average_Package_LPA'].mean(), 2),
                'Median Package (LPA)': round(grp['Median_Package_LPA'].mean(), 2),
                'Package Std (LPA)': round(grp['Average_Package_LPA'].std(), 2),
                'Max Peak Ceiling (LPA)': round(grp['Highest_Package_LPA'].max(), 2),
                'Mean Package Ceiling (LPA)': round(grp['Highest_Package_LPA'].mean(), 2)
            })
        return pd.DataFrame(records)

    def analyze_by_stream(self):
        records = []
        for stream in ['Engineering', 'Management', 'Arts/Commerce']:
            grp = self.df[self.df['Stream'] == stream]
            if len(grp) == 0:
                continue
            records.append({
                'Academic Stream': stream,
                'Cohorts Count': len(grp),
                'Mean Placement Rate (%)': round(grp['Placement_Rate_Pct'].mean(), 2),
                'Mean Package (LPA)': round(grp['Average_Package_LPA'].mean(), 2),
                'Median Package (LPA)': round(grp['Median_Package_LPA'].mean(), 2),
                'Max Package Recorded (LPA)': round(grp['Highest_Package_LPA'].max(), 2),
            })
        return pd.DataFrame(records).sort_values(by='Mean Package (LPA)', ascending=False)

    def analyze_longitudinal_growth(self):
        records = []
        for yr, grp in self.df.groupby('Graduation_Year'):
            records.append({
                'Year': int(yr),
                'Cohorts Tracked': len(grp),
                'Mean Placement Rate (%)': round(grp['Placement_Rate_Pct'].mean(), 2),
                'Highest Package Mean (LPA)': round(grp['Highest_Package_LPA'].mean(), 2),
                'Highest Package Max (LPA)': round(grp['Highest_Package_LPA'].max(), 2),
                'Average Package Mean (LPA)': round(grp['Average_Package_LPA'].mean(), 2),
                'Median Package Mean (LPA)': round(grp['Median_Package_LPA'].mean(), 2),
            })
        df_yr = pd.DataFrame(records).sort_values(by='Year')
        
        base_avg = df_yr.iloc[0]['Average Package Mean (LPA)']
        final_avg = df_yr.iloc[-1]['Average Package Mean (LPA)']
        cagr = ((final_avg / base_avg)**(1.0 / (len(df_yr) - 1)) - 1.0) * 100
        
        return df_yr, round(cagr, 2)

    def analyze_top_recruiters(self, top_n=15):
        counts = self.df['Primary_Recruiter'].value_counts().head(top_n)
        records = []
        for rec, cnt in counts.items():
            sub = self.df[self.df['Primary_Recruiter'] == rec]
            records.append({
                'Primary Recruiter': rec,
                'Hiring Cohorts Engaged': cnt,
                'Market Footprint (%)': round((cnt / len(self.df)) * 100, 2),
                'Mean Offered Package (LPA)': round(sub['Average_Package_LPA'].mean(), 2),
                'Associated Dominant Role': sub['Dominant_Job_Role'].mode().iloc[0] if len(sub) > 0 else 'Various'
            })
        return pd.DataFrame(records)

    def compute_placement_correlation(self):
        r_pearson = self.df['Placement_Rate_Pct'].corr(self.df['Average_Package_LPA'], method='pearson')
        r_spearman = self.df['Placement_Rate_Pct'].rank().corr(self.df['Average_Package_LPA'].rank())
        return round(r_pearson, 3), round(r_spearman, 3)


def generate_full_report(student_df, college_df, output_path=None):
    stu_analyzer = StudentPlacementAnalyzer(student_df)
    inst_analyzer = InstitutionalPlacementAnalyzer(college_df)
    
    lines = []
    def log(msg=""):
        lines.append(msg)
        print(msg)

    log("=" * 80)
    log("COLLEGE PLACEMENT DATA ANALYSIS")
    log("=" * 80)
    
    log("\n[1] Student Cohort Metrics:")
    stu_meta = stu_analyzer.get_cohort_overview()
    for k, v in stu_meta.items():
        log(f"  {k:<28}: {v}")

    log("\n[2] Branch Analysis:")
    df_branch = stu_analyzer.analyze_by_branch()
    log(df_branch.to_string(index=False))

    log("\n[3] Gender Breakdown:")
    df_gender = stu_analyzer.analyze_by_gender()
    log(df_gender.to_string(index=False))

    log("\n[4] Backlogs Impact:")
    df_backlogs = stu_analyzer.analyze_backlogs_impact()
    log(df_backlogs.to_string(index=False))

    log("\n[5] Attendance Brackets:")
    df_att = stu_analyzer.analyze_attendance_brackets()
    log(df_att.to_string(index=False))

    log("\n[6] Internship Analysis:")
    df_intern_status, df_intern_domain = stu_analyzer.analyze_internship_roi()
    log(df_intern_status.to_string(index=False))
    log("\nDomain Breakdown:")
    log(df_intern_domain.to_string(index=False))

    log("\n[7] Technical Skills:")
    df_skills = stu_analyzer.analyze_technical_skills()
    log(df_skills.to_string(index=False))

    log("\n[8] Semester Progression:")
    df_sem = stu_analyzer.analyze_semester_progression()
    log(df_sem.to_string(index=False))

    log("\n[9] Hypothesis Tests:")
    tests = stu_analyzer.perform_hypothesis_tests()
    for test_name, res in tests.items():
        log(f"  {test_name}: {res}")

    log("\n" + "=" * 80)
    log("[10] Institutional Metrics:")
    inst_meta = inst_analyzer.get_institutional_overview()
    for k, v in inst_meta.items():
        log(f"  {k:<32}: {v}")

    log("\n[11] Tier Comparison:")
    df_tier = inst_analyzer.analyze_by_tier()
    log(df_tier.to_string(index=False))

    log("\n[12] Stream Comparison:")
    df_stream = inst_analyzer.analyze_by_stream()
    log(df_stream.to_string(index=False))

    df_years, cagr = inst_analyzer.analyze_longitudinal_growth()
    log(f"\n[13] Longitudinal Growth (2020-2026, CAGR: {cagr}%):")
    log(df_years.to_string(index=False))

    log("\n[14] Top Recruiters:")
    df_top_rec = inst_analyzer.analyze_top_recruiters()
    log(df_top_rec.to_string(index=False))

    r_p, r_s = inst_analyzer.compute_placement_correlation()
    log(f"\n[15] Placement Rate vs Package Correlation: Pearson={r_p}, Spearman={r_s}")
    log("=" * 80)

    if output_path:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines) + "\n")

    return {
        'student_overview': stu_meta,
        'branch_stats': df_branch,
        'tier_stats': df_tier,
        'skill_stats': df_skills,
        'hypothesis_tests': tests,
        'longitudinal_trends': df_years
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save-report', type=str, default='data_analysis_report.txt')
    parser.add_argument('--export-tables', action='store_true')
    args = parser.parse_args()

    student_df, college_df = load_datasets()
    results = generate_full_report(student_df, college_df, output_path=args.save_report)

    if args.export_tables:
        out_dir = 'data/analysis_metrics'
        os.makedirs(out_dir, exist_ok=True)
        results['branch_stats'].to_csv(os.path.join(out_dir, 'branch_placement_metrics.csv'), index=False)
        results['tier_stats'].to_csv(os.path.join(out_dir, 'tier_placement_metrics.csv'), index=False)
        results['skill_stats'].to_csv(os.path.join(out_dir, 'skill_valuation_metrics.csv'), index=False)
        results['longitudinal_trends'].to_csv(os.path.join(out_dir, 'longitudinal_salary_trends.csv'), index=False)


if __name__ == '__main__':
    main()
