// Mock Dataset for Campus Placement Analytics Dashboard

const PlacementData = {
  summary: {
    totalStudents: 560,
    placedStudents: 484,
    placementPercentage: 86.4,
    highestPackage: 44.5, // LPA
    averagePackage: 12.8, // LPA
    medianPackage: 10.2, // LPA
    totalOffers: 612,
    activeRecruiters: 94,
    topSector: "Software & Product Tech",
    year: "2025 - 2026 Batch"
  },

  departmentStats: [
    { name: "Computer Science & Eng (CSE)", code: "CSE", total: 150, placed: 142, rate: 94.7, avgPackage: 16.5, maxPackage: 44.5 },
    { name: "AI & Data Science (AI/DS)", code: "AIDS", total: 80, placed: 74, rate: 92.5, avgPackage: 15.2, maxPackage: 38.0 },
    { name: "Electronics & Comm (ECE)", code: "ECE", total: 110, placed: 96, rate: 87.3, avgPackage: 11.8, maxPackage: 28.5 },
    { name: "Information Tech (IT)", code: "IT", total: 90, placed: 79, rate: 87.8, avgPackage: 13.4, maxPackage: 32.0 },
    { name: "Mechanical Eng (ME)", code: "ME", total: 70, placed: 53, rate: 75.7, avgPackage: 8.5, maxPackage: 18.0 },
    { name: "Civil Eng (CE)", code: "CE", total: 60, placed: 40, rate: 66.7, avgPackage: 7.2, maxPackage: 14.5 }
  ],

  companyHiring: [
    { company: "Google", offers: 18, avgCTC: 38.0, sector: "Product Tech", tier: "Tier 1" },
    { company: "Microsoft", offers: 24, avgCTC: 34.5, sector: "Product Tech", tier: "Tier 1" },
    { company: "Amazon", offers: 32, avgCTC: 28.0, sector: "E-Commerce / Cloud", tier: "Tier 1" },
    { company: "Goldman Sachs", offers: 14, avgCTC: 24.0, sector: "FinTech / Banking", tier: "Tier 1" },
    { company: "Deloitte", offers: 45, avgCTC: 11.5, sector: "Consulting", tier: "Tier 2" },
    { company: "Texas Instruments", offers: 12, avgCTC: 22.0, sector: "Semiconductors", tier: "Tier 1" },
    { company: "TCS Digital", offers: 65, avgCTC: 7.5, sector: "IT Services", tier: "Tier 2" },
    { company: "Infosys Specialist", offers: 52, avgCTC: 9.5, sector: "IT Services", tier: "Tier 2" },
    { company: "Tata Motors", offers: 16, avgCTC: 10.2, sector: "Automotive / Core", tier: "Tier 2" },
    { company: "L&T Engineering", offers: 19, avgCTC: 8.0, sector: "Infrastructure", tier: "Tier 2" }
  ],

  salaryDistribution: [
    { bracket: "< 5 LPA", count: 48, percentage: 9.9 },
    { bracket: "5 - 8 LPA", count: 142, percentage: 29.3 },
    { bracket: "8 - 14 LPA", count: 186, percentage: 38.4 },
    { bracket: "14 - 25 LPA", count: 76, percentage: 15.7 },
    { bracket: "25+ LPA", count: 32, percentage: 6.6 }
  ],

  skillDemand: [
    { skill: "Python & Data Science", demandScore: 95, studentProficiency: 82 },
    { skill: "Data Analytics & SQL", demandScore: 92, studentProficiency: 88 },
    { skill: "Full-Stack (React/Node)", demandScore: 89, studentProficiency: 76 },
    { skill: "Machine Learning / AI", demandScore: 86, studentProficiency: 68 },
    { skill: "Cloud & DevOps (AWS)", demandScore: 80, studentProficiency: 58 },
    { skill: "DSA & System Design", demandScore: 94, studentProficiency: 81 },
    { skill: "Embedded & IoT", demandScore: 65, studentProficiency: 70 }
  ],

  placementTrend: [
    { month: "Aug", offers: 45, percentage: 8.0 },
    { month: "Sep", offers: 110, percentage: 27.6 },
    { month: "Oct", offers: 195, percentage: 62.5 },
    { month: "Nov", offers: 280, percentage: 74.3 },
    { month: "Dec", offers: 360, percentage: 80.1 },
    { month: "Jan", offers: 435, percentage: 84.2 },
    { month: "Feb", offers: 484, percentage: 86.4 }
  ],

  // Individual Student Application Tracker Records (as per reference screenshot)
  students: [
    {
      id: "STU-1001",
      name: "Ananya Sharma",
      avatar: "assets/student_alex.jpg",
      rollNo: "21CSE042",
      dept: "CSE",
      cgpa: 9.2,
      email: "ananya.sharma@college.edu",
      company: "Google",
      role: "Software Development Engineer",
      appDate: "2025-09-12",
      status: "Offer", // Offer / Shortlisted / Interview / Pending / Rejected
      statusType: "success", // Green
      testDate: "2025-10-05 10:00 AM",
      resumeVersion: "Resume_v2_SoftwareDev.pdf",
      packageOffered: "38.5 LPA",
      skills: ["Python", "C++", "System Design", "React"]
    },
    {
      id: "STU-1002",
      name: "David Miller",
      avatar: "assets/student_david.jpg",
      rollNo: "21AIDS018",
      dept: "AIDS",
      cgpa: 8.8,
      email: "david.miller@college.edu",
      company: "Goldman Sachs",
      role: "Data Analyst & Quantitative Trader",
      appDate: "2025-09-18",
      status: "Shortlisted",
      statusType: "success", // Green
      testDate: "2025-10-22 02:30 PM",
      resumeVersion: "Resume_v1_DataAnalytics.pdf",
      packageOffered: "24.0 LPA",
      skills: ["Python", "SQL", "Pandas", "Statistics"]
    },
    {
      id: "STU-1003",
      name: "Priya Patel",
      avatar: "assets/student_priya.jpg",
      rollNo: "21ECE089",
      dept: "ECE",
      cgpa: 8.5,
      email: "priya.patel@college.edu",
      company: "Texas Instruments",
      role: "Embedded Systems Hardware Engineer",
      appDate: "2025-10-01",
      status: "Interview",
      statusType: "warning", // Yellow
      testDate: "2025-10-28 11:00 AM",
      resumeVersion: "Resume_v3_EmbeddedSystems.pdf",
      packageOffered: "Pending",
      skills: ["C/C++", "Verilog", "Embedded Systems", "Microcontrollers"]
    },
    {
      id: "STU-1004",
      name: "Rohan Mehta",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
      rollNo: "21IT024",
      dept: "IT",
      cgpa: 7.9,
      email: "rohan.mehta@college.edu",
      company: "Amazon",
      role: "Cloud Operations Associate",
      appDate: "2025-09-25",
      status: "Pending",
      statusType: "warning", // Yellow
      testDate: "2025-11-04 03:00 PM",
      resumeVersion: "Resume_v2_CloudDevOps.pdf",
      packageOffered: "Pending",
      skills: ["AWS", "Docker", "Linux", "Python"]
    },
    {
      id: "STU-1005",
      name: "Sneha Reddy",
      avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80",
      rollNo: "21CSE110",
      dept: "CSE",
      cgpa: 8.1,
      email: "sneha.reddy@college.edu",
      company: "Microsoft",
      role: "Front-End Engineer",
      appDate: "2025-09-10",
      status: "Rejected",
      statusType: "danger", // Red
      testDate: "2025-09-30 09:30 AM",
      resumeVersion: "Resume_v1_WebDevelopment.pdf",
      packageOffered: "N/A",
      skills: ["JavaScript", "React", "CSS3", "HTML5"]
    },
    {
      id: "STU-1006",
      name: "Aditya Nair",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
      rollNo: "21ME035",
      dept: "ME",
      cgpa: 8.4,
      email: "aditya.nair@college.edu",
      company: "Tata Motors",
      role: "Graduate Engineer Trainee (R&D)",
      appDate: "2025-10-05",
      status: "Offer",
      statusType: "success", // Green
      testDate: "2025-10-18 02:00 PM",
      resumeVersion: "Resume_v1_CoreMechanical.pdf",
      packageOffered: "10.5 LPA",
      skills: ["SolidWorks", "ANSYS", "Thermodynamics", "AutoCAD"]
    },
    {
      id: "STU-1007",
      name: "Kavya Joshi",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
      rollNo: "21AIDS052",
      dept: "AIDS",
      cgpa: 9.0,
      email: "kavya.joshi@college.edu",
      company: "Deloitte",
      role: "AI & Cognitive Technology Analyst",
      appDate: "2025-09-29",
      status: "Shortlisted",
      statusType: "success", // Green
      testDate: "2025-11-02 10:00 AM",
      resumeVersion: "Resume_v2_AIMLConsulting.pdf",
      packageOffered: "11.8 LPA",
      skills: ["PyTorch", "NLP", "Python", "PowerBI"]
    },
    {
      id: "STU-1008",
      name: "Vikram Singh",
      avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
      rollNo: "21CE015",
      dept: "CE",
      cgpa: 7.6,
      email: "vikram.singh@college.edu",
      company: "L&T Engineering",
      role: "Assistant Structural Engineer",
      appDate: "2025-10-08",
      status: "Interview",
      statusType: "warning", // Yellow
      testDate: "2025-11-10 11:30 AM",
      resumeVersion: "Resume_v1_CivilDesign.pdf",
      packageOffered: "Pending",
      skills: ["STAAD Pro", "AutoCAD", "Structural Analysis", "Revit"]
    },
    {
      id: "STU-1009",
      name: "Meera Gupta",
      avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150&auto=format&fit=crop&q=80",
      rollNo: "21CSE091",
      dept: "CSE",
      cgpa: 8.9,
      email: "meera.gupta@college.edu",
      company: "Amazon",
      role: "Software Development Engineer 1",
      appDate: "2025-09-14",
      status: "Offer",
      statusType: "success", // Green
      testDate: "2025-10-12 01:00 PM",
      resumeVersion: "Resume_v2_SoftwareDev.pdf",
      packageOffered: "28.5 LPA",
      skills: ["Java", "Data Structures", "System Design", "AWS"]
    },
    {
      id: "STU-1010",
      name: "Arjun Das",
      avatar: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150&auto=format&fit=crop&q=80",
      rollNo: "21ECE044",
      dept: "ECE",
      cgpa: 7.8,
      email: "arjun.das@college.edu",
      company: "TCS Digital",
      role: "Digital Systems Engineer",
      appDate: "2025-10-02",
      status: "Pending",
      statusType: "warning", // Yellow
      testDate: "2025-11-05 02:00 PM",
      resumeVersion: "Resume_v1_ITSystems.pdf",
      packageOffered: "Pending",
      skills: ["Java", "SQL", "Networking", "Python"]
    }
  ]
};
