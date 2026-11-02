import os
import sys

# Set matplotlib cache directory to local folder before import
os.environ['MPLCONFIGDIR'] = os.path.abspath('data/matplotlib_cache')
os.makedirs('data/matplotlib_cache', exist_ok=True)
os.makedirs('charts', exist_ok=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns

# Set global styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = False
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#E2E8F0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.6

# Palette definitions
NAVY = '#1E3A8A'
BLUE = '#2563EB'
TEAL = '#0D9488'
GREEN = '#10B981'
AMBER = '#F59E0B'
ROSE = '#E11D48'
PURPLE = '#7C3AED'
SLATE = '#475569'
LIGHT_BG = '#F8FAFC'

def load_data():
    college_df = pd.read_csv('data/college_placement_trends.csv')
    student_df = pd.read_csv('data/student_placement_records.csv')
    return college_df, student_df

# ==============================================================================
# DATASET 1: INSTITUTIONAL & MACRO PLACEMENT TRENDS (GRAPHS 1 - 8)
# ==============================================================================

def generate_chart1_pkg_trends(college_df):
    """Multi-Line Trend: Highest, Average, and Median Package LPA (2020-2026)"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    yearly = college_df.groupby('Graduation_Year').agg({
        'Highest_Package_LPA': ['mean', 'max'],
        'Average_Package_LPA': 'mean',
        'Median_Package_LPA': 'mean'
    }).reset_index()
    yearly.columns = ['Year', 'Highest_Avg', 'Highest_Peak', 'Average_Mean', 'Median_Mean']
    
    years = yearly['Year']
    ax.plot(years, yearly['Highest_Avg'], marker='o', lw=2.5, color=ROSE, label='Highest Package (Cohort Mean)')
    ax.plot(years, yearly['Average_Package_LPA' if 'Average_Package_LPA' in yearly else 'Average_Mean'], 
            marker='s', lw=2.5, color=BLUE, label='Average Package (Mean)')
    ax.plot(years, yearly['Median_Mean'], marker='^', lw=2.5, color=TEAL, label='Median Package (Mean)')
    
    # Peak highest package annotation
    max_row = college_df.loc[college_df['Highest_Package_LPA'].idxmax()]
    ax.scatter([max_row['Graduation_Year']], [max_row['Highest_Package_LPA']], color='#991B1B', s=90, zorder=5)
    ax.annotate(f"All-Time Peak: {max_row['Highest_Package_LPA']:.1f} LPA\n({max_row['College_Name']}, {max_row['Graduation_Year']})",
                xy=(max_row['Graduation_Year'], max_row['Highest_Package_LPA']),
                xytext=(max_row['Graduation_Year'] - 1.2, max_row['Highest_Package_LPA'] - 18),
                arrowprops=dict(facecolor='#991B1B', shrink=0.08, width=1.2, headwidth=6),
                fontsize=8, fontweight='bold', color='#991B1B',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEF2F2', edgecolor='#F87171', lw=0.8))
    
    ax.set_title('National Multi-Year Salary Package Evolution (2020 – 2026)', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Graduation Year', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Package (LPA in ₹ Lakhs)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_xticks(years)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8.5, loc='upper left')
    plt.tight_layout()
    fig.savefig('charts/chart1_pkg_trends.png')
    plt.close(fig)
    print("Generated chart1_pkg_trends.png")

def generate_chart2_stream_tier_placement_rate(college_df):
    """Grouped Bar Chart: Placement Rate % by Institution Tier & Academic Stream"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    pivot = college_df.groupby(['Institution_Tier', 'Stream'])['Placement_Rate_Pct'].mean().unstack()
    tiers = ['Tier 1', 'Tier 2', 'Tier 3']
    pivot = pivot.reindex(tiers)
    
    x = np.arange(len(tiers))
    width = 0.25
    
    streams = ['Engineering', 'Management', 'Arts/Commerce']
    colors = [NAVY, TEAL, AMBER]
    
    for i, stream in enumerate(streams):
        if stream in pivot.columns:
            vals = pivot[stream]
            rects = ax.bar(x + (i - 1) * width, vals, width, label=stream, color=colors[i], edgecolor='white', lw=1)
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f'{height:.1f}%',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points",
                            ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#1E293B')
                
    ax.set_title('Campus Placement Rate (%) Across Institution Tiers & Academic Streams', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(tiers, fontsize=9.5, fontweight='semibold')
    ax.set_ylabel('Average Placement Rate (%)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(title='Stream', frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8.5, title_fontsize=8.5)
    plt.tight_layout()
    fig.savefig('charts/chart2_stream_tier_placement_rate.png')
    plt.close(fig)
    print("Generated chart2_stream_tier_placement_rate.png")

def generate_chart3_tier_salary_boxplot(college_df):
    """Box-and-Whisker Plot: Average and Highest Package Distribution Across Tiers"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.6), dpi=300)
    
    tier_order = ['Tier 1', 'Tier 2', 'Tier 3']
    tier_palette = {'Tier 1': '#3B82F6', 'Tier 2': '#10B981', 'Tier 3': '#F59E0B'}
    
    sns.boxplot(data=college_df, x='Institution_Tier', y='Average_Package_LPA', order=tier_order,
                palette=tier_palette, ax=ax1, width=0.45, fliersize=2.5, boxprops=dict(alpha=0.85))
    ax1.set_title('Average Package Distribution', fontsize=10, fontweight='bold', color='#0F172A')
    ax1.set_xlabel('Institution Tier', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax1.set_ylabel('Average Package (LPA)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    sns.boxplot(data=college_df, x='Institution_Tier', y='Highest_Package_LPA', order=tier_order,
                palette=tier_palette, ax=ax2, width=0.45, fliersize=2.5, boxprops=dict(alpha=0.85))
    ax2.set_title('Highest Package Distribution (Ceilings)', fontsize=10, fontweight='bold', color='#0F172A')
    ax2.set_xlabel('Institution Tier', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax2.set_ylabel('Highest Package (LPA)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    fig.suptitle('Institutional Salary Dispersion & Outlier Spectrum by Tier', fontsize=11, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig('charts/chart3_tier_salary_boxplot.png', bbox_inches='tight')
    plt.close(fig)
    print("Generated chart3_tier_salary_boxplot.png")

def generate_chart4_top_recruiters_bar(college_df):
    """Horizontal Bar Chart: Top 15 Primary Recruiters by Institutional Hiring Reach"""
    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=300)
    
    top_rec = college_df['Primary_Recruiter'].value_counts().head(15).sort_values(ascending=True)
    
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(top_rec)))
    bars = ax.barh(top_rec.index, top_rec.values, color=colors, edgecolor='#1E3A8A', lw=0.6)
    
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f' {int(w)} cohorts',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    va='center', fontsize=7.5, fontweight='semibold', color='#1E293B')
        
    ax.set_title('Top 15 Primary Campus Recruiters by Institution Cohort Presence', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Number of Institutional Cohorts (Campus Hiring Engagements)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax.set_xlim(0, max(top_rec.values) * 1.15)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig.savefig('charts/chart4_top_recruiters_bar.png')
    plt.close(fig)
    print("Generated chart4_top_recruiters_bar.png")

def generate_chart5_stream_year_heatmap(college_df):
    """2D Heatmap Matrix: Average Package LPA across Streams and Graduation Years"""
    fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=300)
    
    pivot = college_df.pivot_table(index='Stream', columns='Graduation_Year', values='Average_Package_LPA', aggfunc='mean')
    
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='YlGnBu', cbar_kws={'label': 'Mean Package (LPA)'},
                linewidths=1, linecolor='white', ax=ax, annot_kws={'fontsize': 9, 'fontweight': 'bold'})
    
    ax.set_title('Heatmap: Mean Average Package (₹ LPA) by Stream & Graduation Year', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Graduation Year', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Academic Stream', fontsize=9, fontweight='semibold', color=SLATE)
    plt.tight_layout()
    fig.savefig('charts/chart5_stream_year_heatmap.png')
    plt.close(fig)
    print("Generated chart5_stream_year_heatmap.png")

def generate_chart6_scatter_placement_vs_avgpkg(college_df):
    """Scatter Plot with Linear Regression: Placement Rate vs Average Package"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    tier_palette = {'Tier 1': '#2563EB', 'Tier 2': '#0D9488', 'Tier 3': '#E11D48'}
    
    for tier in ['Tier 1', 'Tier 2', 'Tier 3']:
        sub = college_df[college_df['Institution_Tier'] == tier]
        ax.scatter(sub['Placement_Rate_Pct'], sub['Average_Package_LPA'], 
                   label=tier, color=tier_palette[tier], alpha=0.55, s=30, edgecolors='none')
        
    # Overall OLS Regression Line
    z = np.polyfit(college_df['Placement_Rate_Pct'], college_df['Average_Package_LPA'], 1)
    p = np.poly1d(z)
    corr = college_df['Placement_Rate_Pct'].corr(college_df['Average_Package_LPA'])
    x_range = np.linspace(college_df['Placement_Rate_Pct'].min(), college_df['Placement_Rate_Pct'].max(), 100)
    ax.plot(x_range, p(x_range), color='#0F172A', lw=2, linestyle='--', label=f'OLS Fit (r = {corr:.2f})')
    
    ax.set_title('Institutional Placement Rate (%) vs. Average Salary Realization (LPA)', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Placement Rate (%)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Average Package (LPA)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8.5, loc='upper left')
    plt.tight_layout()
    fig.savefig('charts/chart6_scatter_placement_vs_avgpkg.png')
    plt.close(fig)
    print("Generated chart6_scatter_placement_vs_avgpkg.png")

def generate_chart7_highest_pkg_area(college_df):
    """Area / Multi-Line Chart: Evolution of Median & Max Packages by Tier"""
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=300)
    
    tier_trends = college_df.groupby(['Graduation_Year', 'Institution_Tier'])['Median_Package_LPA'].mean().unstack()
    years = tier_trends.index
    
    ax.fill_between(years, 0, tier_trends['Tier 3'], color='#FDE68A', alpha=0.6, label='Tier 3 Range')
    ax.fill_between(years, tier_trends['Tier 3'], tier_trends['Tier 2'], color='#99F6E4', alpha=0.6, label='Tier 2 Delta')
    ax.fill_between(years, tier_trends['Tier 2'], tier_trends['Tier 1'], color='#BFDBFE', alpha=0.6, label='Tier 1 Delta')
    
    ax.plot(years, tier_trends['Tier 1'], marker='o', lw=2, color='#1D4ED8', label='Tier 1 Median')
    ax.plot(years, tier_trends['Tier 2'], marker='s', lw=2, color='#0F766E', label='Tier 2 Median')
    ax.plot(years, tier_trends['Tier 3'], marker='^', lw=2, color='#D97706', label='Tier 3 Median')
    
    ax.set_title('Cumulative Tier Median Package Strata Across Graduation Cohorts', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Graduation Year', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Median Package (LPA in ₹ Lakhs)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_xticks(years)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8, loc='upper left', ncol=2)
    plt.tight_layout()
    fig.savefig('charts/chart7_highest_pkg_area.png')
    plt.close(fig)
    print("Generated chart7_highest_pkg_area.png")

def generate_chart8_skills_demanded_bar(college_df):
    """Categorical Bar: Top Recruiter Competencies Demanded in Campus Hiring"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    # Split skills by comma and count
    all_skills = []
    for s in college_df['Skills_Demanded'].dropna():
        tokens = [t.strip() for t in s.split(',') if t.strip()]
        all_skills.extend(tokens)
    
    skill_counts = pd.Series(all_skills).value_counts().head(12).sort_values(ascending=True)
    
    colors = plt.cm.viridis(np.linspace(0.3, 0.85, len(skill_counts)))
    bars = ax.barh(skill_counts.index, skill_counts.values, color=colors, edgecolor='none')
    
    for bar in bars:
        w = bar.get_width()
        ax.annotate(f' {int(w)}',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    va='center', fontsize=7.5, fontweight='semibold', color='#1E293B')
        
    ax.set_title('Most Frequently Required Competencies by Primary Campus Recruiters', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Mention Frequency in Placement Specs', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax.set_xlim(0, max(skill_counts.values) * 1.15)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig.savefig('charts/chart8_skills_demanded_bar.png')
    plt.close(fig)
    print("Generated chart8_skills_demanded_bar.png")


# ==============================================================================
# DATASET 2: STUDENT PERFORMANCE & CAREER OUTCOMES (GRAPHS 9 - 19)
# ==============================================================================

def generate_chart9_donut_placement_status_and_domain(student_df):
    """Dual Donut Charts: (A) Placement Success Rate, (B) Placement Domain Allocation"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.4), dpi=300)
    
    # 1. Placement Status Donut
    status_counts = student_df['Placement Status'].value_counts()
    status_colors = ['#10B981', '#E11D48'] # Placed green, Not placed red
    wedges1, texts1, autotexts1 = ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%',
                                          startangle=90, colors=status_colors,
                                          wedgeprops=dict(width=0.45, edgecolor='white', lw=2),
                                          pctdistance=0.75, textprops=dict(fontsize=8, fontweight='semibold'))
    for at in autotexts1:
        at.set_color('white')
        at.set_fontsize(8.5)
    ax1.set_title(f'Overall Placement Rate\n(N = {len(student_df):,})', fontsize=9.5, fontweight='bold', color='#0F172A')
    
    # 2. Placement Domain Donut (Placed students only)
    placed_df = student_df[student_df['Placement Status'] == 'Placed']
    domain_counts = placed_df['Placement Domain'].value_counts()
    domain_colors = sns.color_palette('Set2', len(domain_counts))
    wedges2, texts2, autotexts2 = ax2.pie(domain_counts, labels=domain_counts.index, autopct='%1.1f%%',
                                          startangle=140, colors=domain_colors,
                                          wedgeprops=dict(width=0.45, edgecolor='white', lw=2),
                                          pctdistance=0.75, textprops=dict(fontsize=8))
    for at in autotexts2:
        at.set_fontsize(7.5)
        at.set_fontweight('bold')
    ax2.set_title(f'Hiring Domain Distribution\n(Placed Cohort: n = {len(placed_df):,})', fontsize=9.5, fontweight='bold', color='#0F172A')
    
    fig.suptitle('Student Placement Success Ratio & Functional Domain Allocation', fontsize=11, fontweight='bold', y=1.03)
    plt.tight_layout()
    fig.savefig('charts/chart9_donut_placement_status_and_domain.png', bbox_inches='tight')
    plt.close(fig)
    print("Generated chart9_donut_placement_status_and_domain.png")

def generate_chart10_ctc_and_gpa_histogram_kde(student_df):
    """Dual Histogram with KDE: CTC Distribution and Cumulative GPA Distribution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.5), dpi=300)
    
    placed = student_df[student_df['Placement Status'] == 'Placed']
    
    # CTC Histogram & KDE
    sns.histplot(placed['CTC (LPA)'], kde=True, ax=ax1, color='#2563EB', bins=18, edgecolor='white', alpha=0.6)
    ctc_mean = placed['CTC (LPA)'].mean()
    ctc_med = placed['CTC (LPA)'].median()
    ax1.axvline(ctc_mean, color='#DC2626', lw=1.8, linestyle='--', label=f'Mean: {ctc_mean:.2f}')
    ax1.axvline(ctc_med, color='#059669', lw=1.8, linestyle=':', label=f'Median: {ctc_med:.2f}')
    ax1.set_title('CTC Distribution for Placed Students', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax1.set_xlabel('Offered CTC (LPA in ₹ Lakhs)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax1.set_ylabel('Student Count', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax1.legend(fontsize=8, frameon=True, facecolor=LIGHT_BG)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Cumulative GPA Histogram & KDE
    sns.histplot(student_df['Average GPA'], kde=True, ax=ax2, color='#0D9488', bins=18, edgecolor='white', alpha=0.6)
    gpa_mean = student_df['Average GPA'].mean()
    gpa_med = student_df['Average GPA'].median()
    ax2.axvline(gpa_mean, color='#DC2626', lw=1.8, linestyle='--', label=f'Mean: {gpa_mean:.2f}')
    ax2.axvline(gpa_med, color='#1E3A8A', lw=1.8, linestyle=':', label=f'Median: {gpa_med:.2f}')
    ax2.set_title('Cumulative GPA Density (Entire Cohort)', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax2.set_xlabel('Average GPA (Scale of 10.0)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax2.set_ylabel('Student Count', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax2.legend(fontsize=8, frameon=True, facecolor=LIGHT_BG)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    fig.suptitle('Distributional Profiles: Offered Compensation & Academic Achievement', fontsize=11, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig('charts/chart10_ctc_and_gpa_histogram_kde.png', bbox_inches='tight')
    plt.close(fig)
    print("Generated chart10_ctc_and_gpa_histogram_kde.png")

def generate_chart11_branch_gpa_violin(student_df):
    """Split Violin Plot: GPA Distribution by Branch Stratified by Placement Status"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    branches = ['CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL']
    
    sns.violinplot(data=student_df, x='Branch', y='Average GPA', hue='Placement Status',
                   order=branches, split=True, inner='quart',
                   palette={'Placed': '#10B981', 'Not Placed': '#EF4444'},
                   cut=0, ax=ax)
    
    ax.set_title('Academic Performance (GPA) Split Violin by Engineering Branch & Placement Status', fontsize=10.5, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Engineering Department / Branch', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Average GPA (10-point scale)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(title='Placement Status', frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8.5)
    plt.tight_layout()
    fig.savefig('charts/chart11_branch_gpa_violin.png')
    plt.close(fig)
    print("Generated chart11_branch_gpa_violin.png")

def generate_chart12_attendance_vs_gpa_scatter(student_df):
    """Bivariate Scatter Plot: Attendance (%) vs Average GPA with Marginal Histograms"""
    g = sns.JointGrid(data=student_df, x='Attendance (%)', y='Average GPA', hue='Placement Status',
                      palette={'Placed': '#059669', 'Not Placed': '#DC2626'}, height=4.2, ratio=5)
    g.plot_joint(sns.scatterplot, alpha=0.55, s=28, edgecolors='none')
    g.plot_marginals(sns.histplot, multiple='stack', alpha=0.6, element='step')
    
    # Threshold lines
    g.ax_joint.axvline(75, color='#F59E0B', linestyle='--', lw=1.2, label='75% Mandatory Attendance')
    g.ax_joint.axhline(7.0, color='#6366F1', linestyle='--', lw=1.2, label='7.0 GPA Eligibility Cutoff')
    g.ax_joint.legend(fontsize=7.5, frameon=True, facecolor=LIGHT_BG, loc='lower left')
    
    g.fig.suptitle('Academic Bivariate Correlation: Attendance (%) vs. Cumulative GPA', fontsize=11, fontweight='bold', y=1.02)
    g.ax_joint.grid(True, linestyle='--', alpha=0.6)
    g.savefig('charts/chart12_attendance_vs_gpa_scatter.png', dpi=300, bbox_inches='tight')
    plt.close(g.fig)
    print("Generated chart12_attendance_vs_gpa_scatter.png")

def generate_chart13_backlogs_impact_barchart(student_df):
    """Bar Chart: Backlog Count vs Placement Rate and Average CTC"""
    fig, ax1 = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    backlog_stats = student_df.groupby('Backlogs').agg(
        Total=('Student ID', 'count'),
        Placed_Count=('Placement Status', lambda s: (s == 'Placed').sum()),
        Mean_CTC=('CTC (LPA)', lambda s: s[s > 0].mean())
    ).reset_index()
    backlog_stats['Placement_Rate'] = (backlog_stats['Placed_Count'] / backlog_stats['Total']) * 100
    
    x = backlog_stats['Backlogs']
    width = 0.38
    
    # Placement Rate Bar
    bars = ax1.bar(x - width/2, backlog_stats['Placement_Rate'], width=width, color=NAVY, label='Placement Rate (%)', edgecolor='white')
    ax1.set_xlabel('Number of Active / Historical Academic Backlogs', fontsize=9, fontweight='semibold', color=SLATE)
    ax1.set_ylabel('Placement Rate (%)', fontsize=9, fontweight='semibold', color=NAVY)
    ax1.set_ylim(0, 100)
    
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%',
                     xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 2), textcoords="offset points",
                     ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=NAVY)
        
    # CTC Bar on secondary axis
    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, backlog_stats['Mean_CTC'], width=width, color=TEAL, label='Mean CTC for Placed (LPA)', edgecolor='white')
    ax2.set_ylabel('Mean CTC of Placed Students (LPA)', fontsize=9, fontweight='semibold', color=TEAL)
    ax2.set_ylim(0, 18)
    
    for bar in bars2:
        h = bar.get_height()
        if not np.isnan(h):
            ax2.annotate(f'₹{h:.1f}L',
                         xy=(bar.get_x() + bar.get_width()/2, h),
                         xytext=(0, 2), textcoords="offset points",
                         ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=TEAL)
            
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, facecolor=LIGHT_BG, fontsize=8)
    
    ax1.set_title('Academic Backlogs Penalty: Placement Probability & Offered Compensation', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax1.set_xticks(x)
    ax1.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    fig.savefig('charts/chart13_backlogs_impact_barchart.png')
    plt.close(fig)
    print("Generated chart13_backlogs_impact_barchart.png")

def generate_chart14_internship_roi_groupedbar(student_df):
    """Grouped Bar: Placement Rate and Average CTC by Internship Status & Domain"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.6), dpi=300)
    
    # 1. Internship Done Yes vs No
    intern_stat = student_df.groupby('Internship Done').agg(
        Total=('Student ID', 'count'),
        Placed=('Placement Status', lambda s: (s == 'Placed').sum()),
        Mean_CTC=('CTC (LPA)', lambda s: s[s > 0].mean())
    )
    intern_stat['Placement_Rate'] = (intern_stat['Placed'] / intern_stat['Total']) * 100
    
    bars1 = ax1.bar(['No Internship', 'Internship Done'], intern_stat['Placement_Rate'], color=['#94A3B8', '#059669'], width=0.45, edgecolor='white')
    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
    ax1.set_title('Placement Success by Internship Status', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax1.set_ylabel('Placement Rate (%)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax1.set_ylim(0, 80)
    ax1.grid(axis='y', linestyle='--', alpha=0.6)
    
    # 2. Average CTC by Internship Domain
    domain_df = student_df[(student_df['Internship Done'] == 'Yes') & (student_df['Placement Status'] == 'Placed') & (student_df['Internship Domain'] != 'None')]
    domain_ctc = domain_df.groupby('Internship Domain')['CTC (LPA)'].mean().sort_values(ascending=False)
    
    colors = plt.cm.Blues(np.linspace(0.45, 0.9, len(domain_ctc)))
    bars2 = ax2.bar(domain_ctc.index, domain_ctc.values, color=colors, width=0.55, edgecolor='white')
    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f'₹{h:.1f}L', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax2.set_title('Offered CTC Across Internship Domains', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax2.set_ylabel('Average CTC (₹ LPA)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax2.set_xticklabels(domain_ctc.index, rotation=25, ha='right', fontsize=8)
    ax2.set_ylim(0, 16)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    
    fig.suptitle('Empirical Return on Investment (ROI) of Pre-Placement Internships', fontsize=11, fontweight='bold', y=1.02)
    plt.tight_layout()
    fig.savefig('charts/chart14_internship_roi_groupedbar.png', bbox_inches='tight')
    plt.close(fig)
    print("Generated chart14_internship_roi_groupedbar.png")

def generate_chart15_correlation_heatmap(student_df):
    """Correlation Matrix Heatmap: Academic and Placement Variables"""
    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=300)
    
    # Select key numerical columns
    cols = ['Age', 'Average GPA', 'Backlogs', 'Attendance (%)', 'CTC (LPA)', 
            'Sem1 GPA', 'Sem2 GPA', 'Sem3 GPA', 'Sem4 GPA', 'Sem5 GPA', 'Sem6 GPA', 'Sem7 GPA', 'Sem8 GPA']
    
    corr = student_df[cols].corr()
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap='vlag', vmin=-0.2, vmax=0.6, annot=True, fmt='.2f',
                linewidths=0.7, ax=ax, cbar_kws={'label': 'Pearson Correlation (r)'},
                annot_kws={'fontsize': 7, 'fontweight': 'semibold'})
    
    ax.set_title('Correlation Matrix: Demographics, Longitudinal Semesters & Compensation', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    plt.tight_layout()
    fig.savefig('charts/chart15_correlation_heatmap.png')
    plt.close(fig)
    print("Generated chart15_correlation_heatmap.png")

def generate_chart16_branch_radar_profile(student_df):
    """Spider / Radar Chart: Multi-Dimensional Performance Profiles of Departments"""
    fig, ax = plt.subplots(figsize=(7.5, 4.0), subplot_kw=dict(polar=True), dpi=300)
    
    categories = ['Average GPA', 'Attendance %', 'Placement Rate %', 'Internship %', 'Average CTC']
    num_vars = len(categories)
    
    branch_stats = []
    branches = ['CSE', 'IT', 'ECE', 'MECH'] # Select 4 major distinct branches for clarity
    
    # Precompute maximums for normalization
    for b in branches:
        sub = student_df[student_df['Branch'] == b]
        placed_sub = sub[sub['Placement Status'] == 'Placed']
        gpa = sub['Average GPA'].mean()
        att = sub['Attendance (%)'].mean()
        pl_rate = (len(placed_sub) / len(sub)) * 100
        intern_rate = (sub['Internship Done'] == 'Yes').mean() * 100
        ctc = placed_sub['CTC (LPA)'].mean()
        branch_stats.append({
            'Branch': b, 'Average GPA': gpa, 'Attendance %': att, 
            'Placement Rate %': pl_rate, 'Internship %': intern_rate, 'Average CTC': ctc
        })
    df_rad = pd.DataFrame(branch_stats)
    
    # Normalize each column 0.2 to 1.0 for aesthetic radar shape
    norm_df = df_rad.copy()
    norm_df['Average GPA'] = (df_rad['Average GPA'] - 6.5) / 1.5
    norm_df['Attendance %'] = (df_rad['Attendance %'] - 65) / 25
    norm_df['Placement Rate %'] = df_rad['Placement Rate %'] / 100
    norm_df['Internship %'] = df_rad['Internship %'] / 100
    norm_df['Average CTC'] = (df_rad['Average CTC'] - 5) / 10
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    colors = [BLUE, GREEN, ROSE, AMBER]
    for i, b in enumerate(branches):
        row = norm_df[norm_df['Branch'] == b].iloc[0]
        values = [row[c] for c in categories]
        values += values[:1]
        ax.plot(angles, values, color=colors[i], lw=2, label=b)
        ax.fill(angles, values, color=colors[i], alpha=0.15)
        
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), categories, fontsize=8.5, fontweight='semibold')
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=7, color=SLATE)
    ax.set_title('Radar Profile: Multi-Dimensional Branch Benchmarking (Normalized)', fontsize=11, fontweight='bold', color='#0F172A', pad=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), fontsize=8.5, frameon=True, facecolor=LIGHT_BG)
    plt.tight_layout()
    fig.savefig('charts/chart16_branch_radar_profile.png', bbox_inches='tight')
    plt.close(fig)
    print("Generated chart16_branch_radar_profile.png")

def generate_chart17_semester_gpa_progression(student_df):
    """Longitudinal Line Chart: Semester 1 to Semester 8 GPA Trajectory (Placed vs Unplaced)"""
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=300)
    
    sem_cols = [f'Sem{i} GPA' for i in range(1, 9)]
    sem_labels = [f'Sem {i}' for i in range(1, 9)]
    
    placed = student_df[student_df['Placement Status'] == 'Placed']
    unplaced = student_df[student_df['Placement Status'] == 'Not Placed']
    
    p_means = [placed[c].mean() for c in sem_cols]
    p_sems = [placed[c].sem() for c in sem_cols]
    u_means = [unplaced[c].mean() for c in sem_cols]
    u_sems = [unplaced[c].sem() for c in sem_cols]
    
    x = np.arange(1, 9)
    ax.plot(x, p_means, marker='o', lw=2.2, color='#059669', label='Placed Students (Cohort Mean)')
    ax.fill_between(x, np.array(p_means) - np.array(p_sems)*2, np.array(p_means) + np.array(p_sems)*2, color='#059669', alpha=0.15)
    
    ax.plot(x, u_means, marker='s', lw=2.2, color='#DC2626', label='Not Placed Students (Cohort Mean)')
    ax.fill_between(x, np.array(u_means) - np.array(u_sems)*2, np.array(u_means) + np.array(u_sems)*2, color='#DC2626', alpha=0.15)
    
    ax.set_title('Longitudinal Academic Trajectory: Semester 1 to 8 GPA Progression', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Curricular Semester', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Semester Grade Point Average (SGPA)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_xticks(x)
    ax.set_xticklabels(sem_labels, fontsize=8.5)
    ax.set_ylim(6.0, 8.0)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8.5, loc='lower right')
    plt.tight_layout()
    fig.savefig('charts/chart17_semester_gpa_progression.png')
    plt.close(fig)
    print("Generated chart17_semester_gpa_progression.png")

def generate_chart18_skills_vs_ctc_bar(student_df):
    """Bar Chart with Error Bars: Technical Skill Competencies vs Average CTC Realization"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    tech_skills = ['Python', 'SQL', 'C++', 'Java', 'Machine Learning', 'Web Development', 'Data Science']
    
    skill_stats = []
    for skill in tech_skills:
        # Check students who have this skill
        mask = student_df['Skills'].str.contains(skill, na=False, regex=False)
        sub_placed = student_df[mask & (student_df['Placement Status'] == 'Placed')]
        sub_all = student_df[mask]
        mean_ctc = sub_placed['CTC (LPA)'].mean()
        std_ctc = sub_placed['CTC (LPA)'].std()
        p_rate = (len(sub_placed) / len(sub_all)) * 100
        skill_stats.append({
            'Skill': skill,
            'Mean_CTC': mean_ctc,
            'Std_CTC': std_ctc,
            'Placement_Rate': p_rate,
            'Count': len(sub_all)
        })
    df_sk = pd.DataFrame(skill_stats).sort_values(by='Mean_CTC', ascending=True)
    
    colors = plt.cm.plasma(np.linspace(0.2, 0.75, len(df_sk)))
    bars = ax.barh(df_sk['Skill'], df_sk['Mean_CTC'], xerr=df_sk['Std_CTC']/3, capsize=4,
                   color=colors, edgecolor='none', height=0.6)
    
    for i, bar in enumerate(bars):
        w = bar.get_width()
        p_rate = df_sk['Placement_Rate'].iloc[i]
        ax.annotate(f' ₹{w:.2f} LPA  ({p_rate:.1f}% Placed)',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    va='center', fontsize=7.5, fontweight='semibold', color='#0F172A')
        
    ax.set_title('Offered CTC & Placement Rate by Core Technical Skill Competency', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Average Offered CTC (LPA in ₹ Lakhs with Standard Error)', fontsize=8.5, fontweight='semibold', color=SLATE)
    ax.set_xlim(0, max(df_sk['Mean_CTC']) * 1.35)
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig.savefig('charts/chart18_skills_vs_ctc_bar.png')
    plt.close(fig)
    print("Generated chart18_skills_vs_ctc_bar.png")

def generate_chart19_alumni_path_distribution(student_df):
    """Grouped Stacked Bar: Alumni Path Allocation across Placement Domains"""
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)
    
    placed = student_df[student_df['Placement Status'] == 'Placed']
    pivot = pd.crosstab(placed['Placement Domain'], placed['Alumni Path'], normalize='index') * 100
    
    paths = ['Job', 'Startup', 'Higher Studies', 'Research']
    path_colors = {'Job': '#1D4ED8', 'Startup': '#F59E0B', 'Higher Studies': '#10B981', 'Research': '#8B5CF6'}
    
    # Reindex columns
    pivot = pivot[[p for p in paths if p in pivot.columns]]
    
    pivot.plot(kind='bar', stacked=True, color=[path_colors[c] for c in pivot.columns], ax=ax, edgecolor='white', width=0.55)
    
    ax.set_title('Alumni Career Destinations by Functional Placement Domain (%)', fontsize=11, fontweight='bold', color='#0F172A', pad=10)
    ax.set_xlabel('Placement Functional Domain', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_ylabel('Proportion of Placed Graduates (%)', fontsize=9, fontweight='semibold', color=SLATE)
    ax.set_xticklabels(pivot.index, rotation=20, ha='right', fontsize=8.5)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.legend(title='Alumni Path', frameon=True, facecolor=LIGHT_BG, edgecolor='#CBD5E1', fontsize=8, loc='upper right')
    plt.tight_layout()
    fig.savefig('charts/chart19_alumni_path_distribution.png')
    plt.close(fig)
    print("Generated chart19_alumni_path_distribution.png")

def main():
    print("Loading datasets...")
    college_df, student_df = load_data()
    print(f"Loaded {len(college_df)} college rows and {len(student_df)} student records.")
    
    print("\n--- Generating Dataset 1 Institutional Visualizations ---")
    generate_chart1_pkg_trends(college_df)
    generate_chart2_stream_tier_placement_rate(college_df)
    generate_chart3_tier_salary_boxplot(college_df)
    generate_chart4_top_recruiters_bar(college_df)
    generate_chart5_stream_year_heatmap(college_df)
    generate_chart6_scatter_placement_vs_avgpkg(college_df)
    generate_chart7_highest_pkg_area(college_df)
    generate_chart8_skills_demanded_bar(college_df)
    
    print("\n--- Generating Dataset 2 Student Level Visualizations ---")
    generate_chart9_donut_placement_status_and_domain(student_df)
    generate_chart10_ctc_and_gpa_histogram_kde(student_df)
    generate_chart11_branch_gpa_violin(student_df)
    generate_chart12_attendance_vs_gpa_scatter(student_df)
    generate_chart13_backlogs_impact_barchart(student_df)
    generate_chart14_internship_roi_groupedbar(student_df)
    generate_chart15_correlation_heatmap(student_df)
    generate_chart16_branch_radar_profile(student_df)
    generate_chart17_semester_gpa_progression(student_df)
    generate_chart18_skills_vs_ctc_bar(student_df)
    generate_chart19_alumni_path_distribution(student_df)
    
    print("\nAll 19 high-resolution visualization charts generated successfully in 'charts/' directory!")

if __name__ == '__main__':
    main()
