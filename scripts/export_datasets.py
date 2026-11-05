import os
import zipfile
import xml.etree.ElementTree as ET
import re
import pandas as pd

def parse_college_dataset(docx_path):
    with zipfile.ZipFile(docx_path) as z:
        tree = ET.fromstring(z.read('word/document.xml'))
        paras = tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')

    raw_blocks = []
    cur_pre = []
    for p in paras[1:]:
        texts = []
        for child in p.iter():
            tag = child.tag.split('}')[-1]
            if tag == 't' and child.text:
                texts.append(child.text)
            elif tag == 'tab':
                texts.append('\t')
        line = ''.join(texts).strip()
        if not line:
            continue
        parts = [pt.strip() for pt in line.split('\t') if pt.strip()]
        if any(re.match(r'^202[0-6]$', pt) for pt in parts):
            raw_blocks.append((cur_pre, line))
            cur_pre = []
        else:
            cur_pre.append(line)

    assert len(raw_blocks) == 1750, f"Expected 1750 blocks, got {len(raw_blocks)}"

    SIGNATURES = [
        (['Verilog', 'CUDA', 'Hardware Engineer', 'NVIDIA'], 'NVIDIA', 'Hardware Engineer', 'Verilog, Computer Architecture, CUDA, C++'),
        (['Stochastic', 'High-Frequency', 'Quant Analyst', 'Tower Research'], 'Tower Research', 'Quant Analyst', 'Stochastic Calculus, C++, High-Frequency Trading'),
        (['Data Structures', 'System Design', 'Algorithms, C++', 'Google'], 'Google', 'Software Engineer (SDE)', 'Data Structures, Algorithms, C++, System Design'),
        (['Machine Learning, SQL, PyTorch', 'PyTorch', 'Data Scientist', 'Microsoft'], 'Microsoft', 'Data Scientist', 'Python, Machine Learning, SQL, PyTorch'),
        (['Agile, Analytics', 'UX Design', 'Product Strategy', 'Amazon\tProduct Manager'], 'Amazon', 'Product Manager', 'Product Strategy, Agile, Analytics, UX Design'),
        (['Growth Hacking', 'Agile Development', 'Uber'], 'Uber', 'Product Manager', 'Growth Hacking, Data Analytics, Agile Development'),
        (['Brand Strategy', 'Consumer Insights', 'Market Research', 'HUL', 'Brand Manager'], 'HUL', 'Brand Manager', 'Market Research, Brand Strategy, Consumer Insights'),
        (['Operations Strategy', 'Change Management', 'Boston', 'Operations Chief'], 'Boston Consulting Group', 'Strategy & Operations Chief', 'Operations Strategy, Supply Chain, Change Management'),
        (['Strategic Frameworks', 'Case Analysis', 'Frameworks,', 'McKinsey', 'Consultant\tAnalysis'], 'McKinsey & Co', 'Management Consultant', 'Strategic Frameworks, Financial Modeling, Case Analysis'),
        (['Corporate Finance', 'Valuation, M&A', 'Goldman Sachs', 'Investment Banking'], 'Goldman Sachs', 'Investment Banking Analyst', 'Corporate Finance, Valuation, M&A'),
        (['Excel, Tableau', 'Capgemini'], 'Capgemini', 'Data Analyst', 'Excel, Tableau, Python, SQL'),
        (['Spring Boot', 'Object Oriented', 'TCS Digital', 'SDE-1'], 'TCS Digital', 'SDE-1', 'Java, Spring Boot, SQL, Object Oriented Programming'),
        (['Docker', 'Kubernetes', 'Power Programmer', 'Cloud Engineer'], 'Infosys Power Programmer', 'Cloud Engineer', 'AWS, Docker, Kubernetes, Linux'),
        (['React.js', 'Node.js', 'MongoDB', 'Cognizant CTS', 'Full Stack'], 'Cognizant CTS', 'Full Stack Developer', 'React.js, Node.js, MongoDB, JavaScript'),
        (['Selenium', 'Jenkins', 'Wipro Turbo', 'QA Automation'], 'Wipro Turbo', 'QA Automation Engineer', 'Selenium, Java, Jenkins, Testing'),
        (['Basic Java', 'HTML/CSS', 'TCS Ninja', 'System Engineer'], 'TCS Ninja', 'System Engineer', 'Basic Java, SQL, HTML/CSS'),
        (['PHP, HTML', 'WordPress', 'Tech Mahindra', 'Web Developer'], 'Tech Mahindra', 'Web Developer', 'PHP, HTML, WordPress, MySQL'),
        (['Core Java', 'Database Basics', 'Cognizant\tTrainee', 'Graduate Engineer'], 'Cognizant', 'Graduate Engineer Trainee', 'Core Java, Database Basics'),
        (['Technical Support', 'Troubleshooting', 'Wipro\tExecutive'], 'Wipro', 'Technical Support Executive', 'Networking, Linux, Customer Troubleshooting'),
        (['Manual Testing', 'Associate Software', 'Infosys\tEngineer'], 'Infosys', 'Associate Software Engineer', 'JavaScript, Python, Manual Testing'),
        (['B2B Sales', 'CRM Tools', 'ICICI Bank', 'Marketing Associate'], 'ICICI Bank', 'Marketing Associate', 'B2B Sales, CRM Tools, Digital Marketing'),
        (['Logistics', 'Operations Research', 'SAP ERP', 'Planning, SAP', 'Supply Chain\tERP'], 'EY', 'Supply Chain Consultant', 'Logistics Planning, SAP ERP, Operations Research'),
        (['Financial Statement', 'Tax Strategy', 'Deloitte', 'Financial Analyst'], 'Deloitte', 'Financial Analyst', 'Financial Statement Analysis, Advanced Excel, Tax Strategy'),
        (['Client Acquisition', 'Portfolio Management', 'HDFC Bank', 'Acquisition,', 'Business\tNegotiation'], 'HDFC Bank', 'Business Development Manager', 'Client Acquisition, Negotiation, Portfolio Management'),
        (['Talent Acquisition', 'Strategic HR', 'Employee Relations', 'Accenture', 'HR Business'], 'Accenture', 'HR Business Partner', 'Talent Acquisition, Strategic HR, Employee Relations'),
        (['Sourcing, Screening', 'Screening,', 'TeamLease', 'HR Recruiter'], 'TeamLease', 'HR Recruiter', 'Sourcing, Screening, Communication Skills'),
        (['Muthoot', 'Banking Loans', 'Customer Service, Retail'], 'Muthoot Finance', 'Customer Relationship Manager', 'Customer Service, Retail Banking Loans'),
        (['Customer Journey Mapping', 'Teleperformance', 'Basic Data Entry', 'Journey'], 'Teleperformance', 'Operations Executive', 'Customer Journey Mapping, Basic Data Entry'),
        (['Process Optimization', 'Genpact', 'Assistant Manager Trainee', 'Optimization,'], 'Genpact', 'Assistant Manager Trainee', 'Process Optimization, Excel, Reporting'),
        (['Cold Calling', 'Justdial', 'Lead Generation'], 'Justdial', 'Sales Executive', 'Cold Calling, Lead Generation, Field Sales'),
        (['Copywriting', 'Public Relations, Content Strategy', 'Meesho', 'Corporate\tCommunications', 'Communications\tSpecialist'], 'Meesho', 'Corporate Communications Specialist', 'Public Relations, Content Strategy, Copywriting'),
        (['Problem Solving', 'Market Sizing', 'Bain', 'Associate\tConsultant', 'Presentation Skills'], 'Bain & Company', 'Associate Consultant', 'Problem Solving, Market Sizing, Presentation Skills'),
        (['Financial Risk', 'Auditing, Financial Accounting', 'KPMG', 'Financial Risk\tAnalyst'], 'KPMG', 'Financial Risk Analyst', 'Auditing, Financial Accounting, Risk Management'),
        (['Macroeconomics', 'Python for Finance', 'J.P. Morgan', 'Investment Analyst'], 'J.P. Morgan', 'Investment Analyst', 'Macroeconomics, Financial Valuation, Python for Finance'),
        (['Statistical Analytics', 'Risk Probability', 'PwC', 'Actuarial Analyst'], 'PwC', 'Actuarial Analyst', 'Statistical Analytics, R programming, Risk Probability'),
        (['Media Relations', 'Crisis Management', 'Ogilvy', 'Public Relations\tOfficer'], 'Ogilvy', 'Public Relations Officer', 'Media Relations, Event Planning, Crisis Management'),
        (['GST Compliance', 'SAP Financials', 'Reliance Retail', 'Accounts Executive'], 'Reliance Retail', 'Accounts Executive', 'Bookkeeping, GST Compliance, SAP Financials'),
        (['Industry Analysis', 'Report Writing', 'Crisil', 'Research Analyst'], 'Crisil', 'Research Analyst', 'Industry Analysis, Data Mining, Report Writing'),
        (['SEO Optimization', 'Creative Writing', 'Zomato', 'Content\tCreator'], 'Zomato', 'Content Creator/Strategist', 'SEO Optimization, Social Media Analytics, Creative Writing'),
        (['Statutory Audit', 'Tally Prime', 'Tax Planning', 'Audit Associate'], 'EY', 'Audit Associate', 'Statutory Audit, Tax Planning, Tally Prime'),
        (['Blog Writing', 'Freelance Agency', 'Keyword Research', 'Content Writer'], 'Freelance Agency', 'Content Writer', 'Blog Writing, Basic Keyword Research'),
        (['Spoken English', 'Customer Empathy', 'Amazon CS', 'Ticketing Tools'], 'Amazon CS', 'Customer Relationship Associate', 'Spoken English, Customer Empathy, Ticketing Tools'),
        (['Direct Sales', 'Byju', 'Lead Conversion', 'Sales Representative'], 'Byju\'s', 'Sales Representative', 'Direct Sales, Lead Conversion, Persuasion'),
        (['Typing Speed', 'WNS', 'Attention to Detail', 'Data Entry\tSpecialist'], 'WNS', 'Data Entry Specialist', 'Typing Speed, MS Office, Attention to Detail'),
        (['Tax Filing', 'Local CA Firm', 'Voucher Entry', 'Accounts Trainee'], 'Local CA Firm', 'Accounts Trainee', 'Tax Filing, Voucher Entry, Tally'),
    ]

    named_list = [
        'IIIT Hyderabad', 'IIIT Bangalore', 'IIT Bombay', 'IIT Delhi', 'IIT Madras',
        'IIT Kharagpur', 'IIT Kanpur', 'IIT Roorkee', 'IIT Guwahati', 'IIT Hyderabad',
        'BITS Pilani', 'NIT Trichy', 'NIT Surathkal', 'NIT Rourkela', 'DTU Delhi',
        'NSUT Delhi', 'Jadavpur University', 'COEP Pune', 'VIT Vellore', 'SRM Chennai',
        'Manipal MIT', 'Thapar University', 'RVCE Bangalore', 'BMSCE Bangalore',
        'PES University', 'LNMIIT Jaipur', 'PSG Tech Coimbatore', 'VJTI Mumbai',
        'TIET Patiala', 'Amity University', 'LPU Punjab', 'CU Chandigarh',
        'Chitkara University', 'SRM Sonepat', 'Techno India Kolkata', 'IEM Kolkata',
        'KIIT Bhubaneswar', 'SOA Bhubaneswar', 'GALGOTIAS Noida', 'GL Bajaj Noida',
        'IIM Ahmedabad', 'IIM Bangalore', 'IIM Calcutta', 'IIM Lucknow', 'IIM Kozhikode',
        'IIM Indore', 'FMS Delhi', 'XLRI Jamshedpur', 'SPJIMR Mumbai', 'JBIMS Mumbai',
        'MDI Gurgaon', 'IIFT Delhi', 'NMIMS Mumbai', 'IMT Ghaziabad', 'IMI Delhi',
        'XIMB Bhubaneswar', 'TAPMI Manipal', 'GIM Goa', 'FORE School Delhi',
        'KJ Somaiya Mumbai', 'LBSIM Delhi', 'BIMTECH Noida', 'SIBM Pune', 'SCMHRD Pune',
        'IIM Kashipur', 'IIM Raipur', 'IIM Ranchi', 'IIM Trichy', 'IIM Udaipur',
        'IIM Amritsar', 'St. Stephen\'s College Delhi', 'SRCC Delhi', 'LSR Delhi',
        'Hindu College Delhi', 'Hansraj College Delhi', 'Miranda House Delhi',
        'Loyola College Chennai', 'St. Xavier\'s Mumbai', 'St. Xavier\'s Kolkata',
        'Christ University Bangalore', 'Symbiosis Pune', 'NM College Mumbai',
        'Mithibai College Mumbai', 'MCC Chennai', 'Mount Carmel Bangalore',
        'Fergusson College Pune', 'SXUK Kolkata', 'GGDSD Chandigarh', 'KJC Bangalore',
        'Jai Hind Mumbai'
    ]

    college_meta = []
    for c_idx in range(250):
        block = raw_blocks[c_idx * 7 : (c_idx + 1) * 7]
        text_corpus = ' \n '.join([' \n '.join(p[0]) + ' \n ' + p[1] for p in block])
        
        stream_m = re.search(r'(Engineering|Management|Arts/Commerce)', text_corpus)
        stream = stream_m.group(1) if stream_m else 'Engineering'
        
        tier_m = re.search(r'(Tier\s*[123])', text_corpus)
        tier = tier_m.group(1).replace('Tier', 'Tier ').strip() if tier_m else 'Tier 1'
        tier = ' '.join(tier.split()) # normalize whitespace to 'Tier X'
        
        name = None
        if 'State' in text_corpus and 'Technical' in text_corpus:
            num_m = re.search(r'Institute\s*(\d+)', text_corpus)
            if not num_m:
                for p, l in block:
                    m_start = re.match(r'^(?:Institute\s*)?(\d+)\b', l)
                    if m_start:
                        num_m = m_start
                        break
            if not num_m:
                num_m = re.search(r'\b(\d+)\s*(?:Engineering|Tier)', text_corpus)
            if num_m:
                name = f'State Technical Institute {num_m.group(1)}'
            else:
                name = 'State Technical Institute'

        elif 'Global' in text_corpus and 'Business' in text_corpus:
            num_m = re.search(r'(?:of\s*Business|Global\s*School)[\s\n\t]*(\d+)', text_corpus)
            if not num_m:
                for p, l in block:
                    m_start = re.match(r'^(\d+)\b', l)
                    if m_start:
                        num_m = m_start
                        break
            if not num_m:
                num_m = re.search(r'\b(\d+)\s*(?:Management|Tier)', text_corpus)
            if num_m:
                name = f'Global School of Business {num_m.group(1)}'
            else:
                name = 'Global School of Business'
                
        elif 'National' in text_corpus and 'Commerce' in text_corpus:
            num_m = re.search(r'(?:&|and)\s*Commerce[\s\n\t]*(\d+)', text_corpus)
            if not num_m:
                for p, l in block:
                    m_start = re.match(r'^(\d+)\b', l)
                    if m_start:
                        num_m = m_start
                        break
            if not num_m:
                num_m = re.search(r'\b(\d+)\s*(?:Arts/Commerce|Tier)', text_corpus)
            if num_m:
                name = f'National College of Arts & Commerce {num_m.group(1)}'
            else:
                name = 'National College of Arts & Commerce'
                
        if not name:
            for nl in named_list:
                parts = nl.split()
                if all(pt in text_corpus for pt in parts):
                    name = nl
                    break
        
        college_meta.append((name, stream, tier))

    records = []
    for c_idx in range(250):
        c_name, c_stream, c_tier = college_meta[c_idx]
        block = raw_blocks[c_idx * 7 : (c_idx + 1) * 7]
        for yr_idx, (pre, line) in enumerate(block):
            grad_year = 2020 + yr_idx
            m = re.search(r'\b(202[0-6])[\s\t]+([\d\.]+)[\s\t]+([\d\.]+)[\s\t]+([\d\.]+)[\s\t]+([\d\.]+)', line)
            if m:
                placement_rate = float(m.group(2))
                highest_pkg = float(m.group(3))
                avg_pkg = float(m.group(4))
                median_pkg = float(m.group(5))
            else:
                raise ValueError(f"Could not parse metrics in row: {line}")
            
            full_text = ' '.join(pre) + ' ' + line
            found_mapping = None
            for kw_list, rec, role, skills in SIGNATURES:
                if any(kw in full_text for kw in kw_list):
                    found_mapping = (rec, role, skills)
                    break
            
            if not found_mapping:
                raise ValueError(f"Could not match recruiter signature: {full_text[:100]}")
            
            rec, role, skills = found_mapping
            records.append({
                'College_Name': c_name,
                'Stream': c_stream,
                'Institution_Tier': c_tier,
                'Graduation_Year': grad_year,
                'Placement_Rate_Pct': placement_rate,
                'Highest_Package_LPA': highest_pkg,
                'Average_Package_LPA': avg_pkg,
                'Median_Package_LPA': median_pkg,
                'Primary_Recruiter': rec,
                'Dominant_Job_Role': role,
                'Skills_Demanded': skills
            })

    df = pd.DataFrame(records)
    return df

def parse_student_dataset(xlsx_path):
    df = pd.read_excel(xlsx_path)
    df = df.dropna(subset=['Student ID', 'Branch'])
    int_cols = ['Age', 'Backlogs']
    for col in int_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)
    
    df['Placement Domain'] = df['Placement Domain'].fillna('None')
    df['Alumni Path'] = df['Alumni Path'].fillna('None')
    df['Internship Domain'] = df['Internship Domain'].fillna('None')
    return df

if __name__ == '__main__':
    uploaded_dir = r'C:\Users\gaura\.gemini\antigravity\brain\b212c85c-9cd5-450d-a447-f2007f59381b\.user_uploaded'
    docx_file = os.path.join(uploaded_dir, 'media_1793623104661_a2a3bcf7.docx')
    xlsx_file = os.path.join(uploaded_dir, 'media_1793623104676_a355955e.xlsx')
    
    print("Parsing College Placement Trends dataset...")
    df_college = parse_college_dataset(docx_file)
    os.makedirs('data', exist_ok=True)
    college_out = os.path.join('data', 'college_placement_trends.csv')
    df_college.to_csv(college_out, index=False)
    print(f"Saved {len(df_college)} rows to {college_out}")
    print(df_college.info())
    print("\nSample:\n", df_college.head(3))
    
    print("\nParsing Student Placement Records dataset...")
    df_student = parse_student_dataset(xlsx_file)
    student_out = os.path.join('data', 'student_placement_records.csv')
    df_student.to_csv(student_out, index=False)
    print(f"Saved {len(df_student)} rows to {student_out}")
    print(df_student.info())
    print("\nSample:\n", df_student.head(3))

