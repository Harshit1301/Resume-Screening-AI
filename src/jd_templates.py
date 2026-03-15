from __future__ import annotations

from typing import Dict, List

JOB_CATALOG: Dict[str, Dict[str, List[str]]] = {
    "Technology": {
        "Software Development": [
            "Junior Software Engineer",
            "Software Engineer",
            "Senior Software Engineer",
            "Backend Developer",
            "Frontend Developer",
            "Full Stack Developer",
            "API Developer",
            "Systems Engineer",
        ],
        "Web Development": [
            "Web Developer",
            "Senior Web Developer",
            "WordPress Developer",
            "React Developer",
            "Next.js Developer",
            "PHP Developer",
        ],
        "Mobile Development": [
            "Android Developer",
            "iOS Developer",
            "Flutter Developer",
            "React Native Developer",
            "Mobile Architect",
        ],
        "Cloud Engineering": [
            "Cloud Engineer",
            "Cloud Architect",
            "Site Reliability Engineer",
            "Platform Engineer",
            "Infrastructure Engineer",
        ],
        "DevOps": [
            "DevOps Engineer",
            "Release Engineer",
            "CI/CD Engineer",
            "Automation Engineer",
            "Build Engineer",
        ],
        "Cybersecurity": [
            "Security Analyst",
            "Security Engineer",
            "Penetration Tester",
            "SOC Analyst",
            "Application Security Engineer",
        ],
        "Game Development": [
            "Game Developer",
            "Unity Developer",
            "Unreal Engine Developer",
            "Gameplay Programmer",
            "Game Tools Engineer",
        ],
    },
    "Data & AI": {
        "Data Science": [
            "Data Scientist",
            "Senior Data Scientist",
            "Applied Scientist",
            "Quantitative Analyst",
            "Experimentation Scientist",
        ],
        "Machine Learning": [
            "ML Engineer",
            "AI Engineer",
            "NLP Engineer",
            "Computer Vision Engineer",
            "Deep Learning Engineer",
            "Applied AI Scientist",
        ],
        "Data Engineering": [
            "Data Engineer",
            "Senior Data Engineer",
            "Analytics Engineer",
            "ETL Developer",
            "Streaming Data Engineer",
        ],
        "AI Research": [
            "AI Research Scientist",
            "Research Engineer",
            "LLM Engineer",
            "Generative AI Engineer",
            "Prompt Engineer",
        ],
        "Business Intelligence": [
            "BI Analyst",
            "BI Developer",
            "Dashboard Engineer",
            "Data Visualization Specialist",
            "Reporting Analyst",
        ],
    },
    "Product & Management": {
        "Product Management": [
            "Associate Product Manager",
            "Product Manager",
            "Senior Product Manager",
            "Group Product Manager",
            "Technical Product Manager",
        ],
        "Project Management": [
            "Project Manager",
            "Program Manager",
            "Delivery Manager",
            "Scrum Master",
            "PMO Analyst",
        ],
        "Business Analysis": [
            "Business Analyst",
            "Senior Business Analyst",
            "Requirements Analyst",
            "Process Analyst",
            "Strategy Analyst",
        ],
        "Operations Management": [
            "Operations Manager",
            "Business Operations Manager",
            "Process Improvement Manager",
            "Workforce Planning Manager",
            "Service Delivery Manager",
        ],
    },
    "Design & Creative": {
        "UI/UX Design": [
            "UI Designer",
            "UX Designer",
            "Product Designer",
            "Interaction Designer",
            "UX Researcher",
        ],
        "Graphic Design": [
            "Graphic Designer",
            "Visual Designer",
            "Brand Designer",
            "Illustrator",
            "Creative Designer",
        ],
        "Product Design": [
            "Product Design Lead",
            "Design Systems Designer",
            "Service Designer",
            "Experience Designer",
            "Prototype Designer",
        ],
        "Motion Design": [
            "Motion Designer",
            "2D Animator",
            "3D Animator",
            "Motion Graphics Artist",
            "Storyboard Artist",
        ],
        "Video Production": [
            "Video Editor",
            "Video Producer",
            "Videographer",
            "Post Production Specialist",
            "Content Video Strategist",
        ],
    },
    "Marketing & Sales": {
        "Digital Marketing": [
            "Digital Marketing Specialist",
            "Marketing Analyst",
            "Growth Marketer",
            "Campaign Manager",
            "Demand Generation Specialist",
        ],
        "Content Marketing": [
            "Content Strategist",
            "Content Marketing Manager",
            "Copywriter",
            "Technical Content Writer",
            "Editorial Manager",
        ],
        "SEO": [
            "SEO Specialist",
            "SEO Manager",
            "Technical SEO Analyst",
            "SEO Content Specialist",
            "Organic Growth Analyst",
        ],
        "Performance Marketing": [
            "PPC Manager",
            "Performance Marketing Manager",
            "Paid Media Specialist",
            "Acquisition Manager",
            "Conversion Rate Optimization Specialist",
        ],
        "Social Media Marketing": [
            "Social Media Manager",
            "Community Manager",
            "Influencer Marketing Specialist",
            "Social Content Creator",
            "Engagement Strategist",
        ],
        "Sales Development": [
            "Sales Executive",
            "Sales Development Representative",
            "Account Executive",
            "Business Development Manager",
            "Inside Sales Specialist",
        ],
    },
    "Finance & Accounting": {
        "Corporate Finance": [
            "Finance Manager",
            "Corporate Finance Analyst",
            "Treasury Analyst",
            "Investment Analyst",
            "Capital Planning Analyst",
        ],
        "Accounting": [
            "Accountant",
            "Senior Accountant",
            "Accounts Payable Specialist",
            "Accounts Receivable Specialist",
            "General Ledger Accountant",
        ],
        "FP&A": [
            "FP&A Analyst",
            "Senior FP&A Analyst",
            "Budget Analyst",
            "Financial Planning Manager",
            "Forecasting Analyst",
        ],
        "Audit & Compliance": [
            "Internal Auditor",
            "Compliance Analyst",
            "Risk Analyst",
            "SOX Compliance Specialist",
            "Governance Analyst",
        ],
    },
    "Human Resources": {
        "Talent Acquisition": [
            "Talent Acquisition Specialist",
            "Technical Recruiter",
            "Recruitment Coordinator",
            "Executive Recruiter",
            "Sourcing Specialist",
        ],
        "People Operations": [
            "HR Manager",
            "HR Generalist",
            "People Operations Specialist",
            "Compensation and Benefits Analyst",
            "Employee Relations Partner",
        ],
        "Learning & Development": [
            "L&D Specialist",
            "Instructional Designer",
            "Training Manager",
            "Learning Program Manager",
            "Organizational Development Analyst",
        ],
    },
    "Healthcare": {
        "Clinical Operations": [
            "Clinical Coordinator",
            "Clinical Operations Manager",
            "Nursing Supervisor",
            "Patient Care Manager",
            "Healthcare Administrator",
        ],
        "Medical Research": [
            "Clinical Research Associate",
            "Research Coordinator",
            "Biostatistician",
            "Medical Writer",
            "Regulatory Affairs Specialist",
        ],
        "Health Informatics": [
            "Health Informatics Analyst",
            "EHR Specialist",
            "Healthcare Data Analyst",
            "Clinical Data Manager",
            "Interoperability Specialist",
        ],
    },
    "Education": {
        "Teaching": [
            "Teacher",
            "Senior Teacher",
            "Subject Matter Expert",
            "Academic Coordinator",
            "Instructional Coach",
        ],
        "Curriculum Design": [
            "Curriculum Designer",
            "Assessment Designer",
            "Learning Experience Designer",
            "Education Content Specialist",
            "Program Designer",
        ],
        "EdTech Operations": [
            "EdTech Program Manager",
            "Learning Platform Specialist",
            "Education Operations Manager",
            "Student Success Manager",
            "Academic Technology Specialist",
        ],
    },
    "Customer Support": {
        "Technical Support": [
            "Technical Support Engineer",
            "Support Specialist",
            "Tier 2 Support Engineer",
            "Application Support Analyst",
            "Support Escalation Engineer",
        ],
        "Customer Success": [
            "Customer Success Manager",
            "Customer Onboarding Specialist",
            "Implementation Specialist",
            "Account Success Manager",
            "Renewals Manager",
        ],
        "Support Operations": [
            "Support Operations Analyst",
            "Knowledge Base Manager",
            "Quality Assurance Specialist",
            "Support Team Lead",
            "Service Desk Manager",
        ],
    },
    "Operations & Logistics": {
        "Supply Chain": [
            "Supply Chain Analyst",
            "Supply Chain Manager",
            "Inventory Planner",
            "Demand Planner",
            "Procurement Planner",
        ],
        "Logistics": [
            "Logistics Coordinator",
            "Logistics Manager",
            "Warehouse Manager",
            "Transportation Analyst",
            "Fulfillment Manager",
        ],
        "Procurement": [
            "Procurement Specialist",
            "Sourcing Manager",
            "Vendor Manager",
            "Contract Procurement Analyst",
            "Category Manager",
        ],
    },
    "Legal": {
        "Corporate Law": [
            "Corporate Counsel",
            "Legal Counsel",
            "Contract Manager",
            "Paralegal",
            "Legal Analyst",
        ],
        "Compliance": [
            "Compliance Manager",
            "Regulatory Compliance Specialist",
            "Data Privacy Officer",
            "AML Analyst",
            "Policy Analyst",
        ],
        "Legal Operations": [
            "Legal Operations Manager",
            "eDiscovery Specialist",
            "Legal Project Manager",
            "Litigation Support Specialist",
            "Contract Operations Analyst",
        ],
    },
    "Construction & Engineering": {
        "Civil Engineering": [
            "Civil Engineer",
            "Structural Engineer",
            "Transportation Engineer",
            "Geotechnical Engineer",
            "Site Engineer",
        ],
        "Construction Management": [
            "Construction Manager",
            "Project Engineer",
            "Estimator",
            "Site Supervisor",
            "Construction Planner",
        ],
        "Mechanical Engineering": [
            "Mechanical Engineer",
            "Design Engineer",
            "Maintenance Engineer",
            "Manufacturing Engineer",
            "Quality Engineer",
        ],
    },
}

SUBCATEGORY_SKILLS: Dict[str, List[str]] = {
    "Software Development": ["Python", "Java", "APIs", "SQL", "Git"],
    "Web Development": ["HTML", "CSS", "JavaScript", "React", "Web Performance"],
    "Mobile Development": ["Android", "iOS", "Flutter", "React Native", "Mobile UI"],
    "Cloud Engineering": ["AWS", "Azure", "GCP", "Terraform", "Kubernetes"],
    "DevOps": ["CI/CD", "Docker", "Kubernetes", "Linux", "Monitoring"],
    "Cybersecurity": ["Network Security", "Threat Detection", "SIEM", "OWASP", "Incident Response"],
    "Game Development": ["Unity", "Unreal", "C#", "C++", "Gameplay Systems"],
    "Data Science": ["Python", "Statistics", "Machine Learning", "SQL", "Visualization"],
    "Machine Learning": ["PyTorch", "TensorFlow", "NLP", "Computer Vision", "MLOps"],
    "Data Engineering": ["ETL", "Data Pipelines", "Spark", "Airflow", "SQL"],
    "AI Research": ["Transformers", "LLMs", "Deep Learning", "Experiment Design", "Python"],
    "Business Intelligence": ["Power BI", "Tableau", "SQL", "Data Modeling", "Reporting"],
    "Product Management": ["Roadmapping", "User Research", "Analytics", "Prioritization", "A/B Testing"],
    "Project Management": ["Planning", "Risk Management", "Stakeholder Management", "Agile", "Jira"],
    "Business Analysis": ["Requirements Gathering", "Process Mapping", "SQL", "Documentation", "UAT"],
    "Operations Management": ["Process Optimization", "KPI Tracking", "Workforce Planning", "SOPs", "Reporting"],
    "UI/UX Design": ["Figma", "Wireframing", "User Research", "Prototyping", "Design Systems"],
    "Graphic Design": ["Adobe Illustrator", "Photoshop", "Branding", "Typography", "Layout Design"],
    "Product Design": ["Design Systems", "Interaction Design", "Prototyping", "Usability Testing", "Figma"],
    "Motion Design": ["After Effects", "Animation", "Storyboarding", "Video Editing", "3D Motion"],
    "Video Production": ["Premiere Pro", "Storytelling", "Scripting", "Color Grading", "Audio Editing"],
    "Digital Marketing": ["Campaign Management", "Email Marketing", "Google Analytics", "Lead Generation", "CRM"],
    "Content Marketing": ["SEO Writing", "Editorial Planning", "Copywriting", "Content Strategy", "Analytics"],
    "SEO": ["Keyword Research", "On-page SEO", "Technical SEO", "Google Search Console", "Content Optimization"],
    "Performance Marketing": ["PPC", "Meta Ads", "Google Ads", "Conversion Optimization", "Attribution"],
    "Social Media Marketing": ["Social Strategy", "Community Management", "Content Planning", "Influencer Outreach", "Analytics"],
    "Sales Development": ["Prospecting", "Lead Qualification", "CRM", "Negotiation", "Pipeline Management"],
    "Corporate Finance": ["Financial Modeling", "Budgeting", "Forecasting", "Excel", "Capital Planning"],
    "Accounting": ["Bookkeeping", "GAAP", "Reconciliation", "Excel", "ERP"],
    "FP&A": ["Forecasting", "Variance Analysis", "Budgeting", "Scenario Modeling", "Excel"],
    "Audit & Compliance": ["Internal Controls", "Regulatory Compliance", "Risk Assessment", "SOX", "Documentation"],
    "Talent Acquisition": ["Sourcing", "Interviewing", "ATS", "Employer Branding", "Candidate Experience"],
    "People Operations": ["HR Policies", "Performance Management", "Employee Engagement", "HRIS", "Compensation"],
    "Learning & Development": ["Instructional Design", "Training Delivery", "LMS", "Program Evaluation", "Coaching"],
    "Clinical Operations": ["Patient Care", "Clinical Workflow", "Documentation", "Coordination", "Compliance"],
    "Medical Research": ["Clinical Trials", "Protocol Management", "Medical Writing", "Regulatory Knowledge", "Data Integrity"],
    "Health Informatics": ["EHR", "Healthcare Analytics", "Interoperability", "HIPAA", "Data Governance"],
    "Teaching": ["Lesson Planning", "Classroom Management", "Assessment", "Student Engagement", "Communication"],
    "Curriculum Design": ["Curriculum Mapping", "Assessment Design", "Instructional Design", "Learning Outcomes", "Pedagogy"],
    "EdTech Operations": ["LMS", "Student Success", "Program Operations", "Reporting", "Stakeholder Communication"],
    "Technical Support": ["Troubleshooting", "Ticketing Systems", "Customer Communication", "SLA Management", "Root Cause Analysis"],
    "Customer Success": ["Onboarding", "Renewals", "Product Adoption", "Relationship Management", "QBRs"],
    "Support Operations": ["Helpdesk Metrics", "Knowledge Base", "QA", "Escalation Management", "Process Improvement"],
    "Supply Chain": ["Inventory Management", "Demand Planning", "Supplier Management", "ERP", "Forecasting"],
    "Logistics": ["Transportation", "Warehouse Operations", "Route Optimization", "Dispatch", "Fleet Management"],
    "Procurement": ["Vendor Negotiation", "Contract Management", "Spend Analysis", "Sourcing", "Procurement Tools"],
    "Corporate Law": ["Contract Review", "Legal Drafting", "Regulatory Review", "Negotiation", "Legal Research"],
    "Compliance": ["Policy Compliance", "Risk Controls", "Regulatory Reporting", "Data Privacy", "Audits"],
    "Legal Operations": ["Matter Management", "eDiscovery", "Contract Lifecycle", "Legal Analytics", "Workflow Automation"],
    "Civil Engineering": ["AutoCAD", "Structural Design", "Site Planning", "Project Documentation", "Safety Standards"],
    "Construction Management": ["Project Scheduling", "Cost Estimation", "Site Supervision", "Contractor Coordination", "Safety Compliance"],
    "Mechanical Engineering": ["CAD", "Manufacturing Processes", "Maintenance", "Quality Control", "Root Cause Analysis"],
}

ROLE_TEMPLATE_DATA: Dict[str, Dict[str, object]] = {
    "Software Engineer": {
        "overview": "Build scalable software products and maintain reliable services across the stack.",
        "responsibilities": [
            "Design and implement production-grade features.",
            "Collaborate with cross-functional teams to deliver releases.",
            "Improve code quality, testing, and observability.",
        ],
        "required_skills": ["Python", "APIs", "SQL", "Git", "System Design"],
        "preferred_qualifications": ["Bachelor's degree in Computer Science or equivalent", "Cloud experience", "Agile delivery experience"],
        "experience": "2-5 years preferred",
        "tools": ["Python", "PostgreSQL", "Docker", "GitHub Actions", "AWS"],
    },
    "Senior Software Engineer": {
        "overview": "Lead architecture decisions and build highly reliable software systems.",
        "responsibilities": ["Own end-to-end technical delivery", "Mentor engineers and review code", "Drive performance and reliability initiatives"],
        "required_skills": ["System Design", "Python", "Distributed Systems", "Databases", "CI/CD"],
        "preferred_qualifications": ["6+ years engineering experience", "Leadership in production environments", "Cloud-native development"],
        "experience": "5-8 years preferred",
        "tools": ["Python", "Kubernetes", "Redis", "Prometheus", "AWS/GCP"],
    },
    "Backend Developer": {
        "overview": "Develop secure backend services and APIs powering customer-facing applications.",
        "responsibilities": ["Build APIs and services", "Optimize database performance", "Implement auth and monitoring controls"],
        "required_skills": ["Python", "Node.js", "REST APIs", "SQL", "Docker"],
        "preferred_qualifications": ["Experience with microservices", "Knowledge of caching and queues", "Cloud platform familiarity"],
        "experience": "2-6 years preferred",
        "tools": ["FastAPI", "PostgreSQL", "Redis", "Docker", "AWS"],
    },
    "Frontend Developer": {
        "overview": "Create responsive and accessible web interfaces with modern frontend frameworks.",
        "responsibilities": ["Build reusable components", "Integrate APIs", "Improve UX performance and accessibility"],
        "required_skills": ["JavaScript", "TypeScript", "React", "HTML", "CSS"],
        "preferred_qualifications": ["Experience with design systems", "Frontend testing exposure", "Performance optimization experience"],
        "experience": "2-5 years preferred",
        "tools": ["React", "Next.js", "Tailwind", "Jest", "Figma"],
    },
    "Full Stack Developer": {
        "overview": "Deliver complete features across backend services and frontend interfaces.",
        "responsibilities": ["Build APIs and UI workflows", "Own feature lifecycle from design to deployment", "Maintain test coverage and reliability"],
        "required_skills": ["Python", "React", "APIs", "SQL", "Git"],
        "preferred_qualifications": ["Experience with cloud deployment", "Knowledge of DevOps practices", "System design understanding"],
        "experience": "3-6 years preferred",
        "tools": ["Python", "React", "PostgreSQL", "Docker", "AWS"],
    },
    "DevOps Engineer": {
        "overview": "Automate delivery pipelines and improve infrastructure reliability at scale.",
        "responsibilities": ["Manage CI/CD pipelines", "Improve observability and alerts", "Optimize infrastructure security and cost"],
        "required_skills": ["CI/CD", "Docker", "Kubernetes", "Linux", "Terraform"],
        "preferred_qualifications": ["Cloud certification", "SRE exposure", "Incident response experience"],
        "experience": "3-7 years preferred",
        "tools": ["Jenkins", "GitHub Actions", "Terraform", "Kubernetes", "Prometheus"],
    },
    "Security Engineer": {
        "overview": "Protect applications and infrastructure through proactive security engineering.",
        "responsibilities": ["Implement security controls", "Perform threat modeling", "Drive vulnerability remediation"],
        "required_skills": ["Application Security", "SIEM", "Threat Detection", "OWASP", "Cloud Security"],
        "preferred_qualifications": ["Security certifications", "Pen-testing exposure", "Incident response experience"],
        "experience": "3-6 years preferred",
        "tools": ["Splunk", "Burp Suite", "AWS Security Hub", "Nessus", "WAF"],
    },
    "Data Scientist": {
        "overview": "Analyze complex datasets and build predictive models for product and business decisions.",
        "responsibilities": ["Build and validate models", "Communicate insights to stakeholders", "Deploy and monitor model performance"],
        "required_skills": ["Python", "Statistics", "Machine Learning", "SQL", "Visualization"],
        "preferred_qualifications": ["Graduate degree in quantitative field", "Experimentation experience", "MLOps familiarity"],
        "experience": "2-6 years preferred",
        "tools": ["Python", "scikit-learn", "Pandas", "SQL", "Tableau"],
    },
    "ML Engineer": {
        "overview": "Productionize ML models and build robust machine learning pipelines.",
        "responsibilities": ["Train and deploy models", "Build reusable ML services", "Monitor drift and quality"],
        "required_skills": ["PyTorch", "TensorFlow", "MLOps", "Python", "Model Serving"],
        "preferred_qualifications": ["Experience with distributed training", "Feature store knowledge", "Cloud ML platforms"],
        "experience": "3-7 years preferred",
        "tools": ["PyTorch", "MLflow", "Docker", "Kubernetes", "Airflow"],
    },
    "AI Engineer": {
        "overview": "Develop AI-powered applications using modern NLP and generative AI techniques.",
        "responsibilities": ["Integrate LLM workflows", "Optimize prompts and retrieval", "Evaluate model quality and latency"],
        "required_skills": ["LLMs", "Python", "Prompt Engineering", "Vector Databases", "APIs"],
        "preferred_qualifications": ["NLP background", "Model evaluation experience", "RAG architecture exposure"],
        "experience": "2-6 years preferred",
        "tools": ["Transformers", "LangChain", "FAISS", "Python", "Docker"],
    },
    "NLP Engineer": {
        "overview": "Design NLP systems for text understanding, classification, and generation.",
        "responsibilities": ["Build NLP pipelines", "Fine-tune language models", "Evaluate linguistic quality and bias"],
        "required_skills": ["NLP", "Transformers", "Python", "Text Preprocessing", "Model Evaluation"],
        "preferred_qualifications": ["Research publications", "Multilingual NLP experience", "LLM fine-tuning"],
        "experience": "3-6 years preferred",
        "tools": ["Hugging Face", "spaCy", "PyTorch", "Weights & Biases", "FastAPI"],
    },
    "Data Engineer": {
        "overview": "Build reliable data pipelines and platform infrastructure for analytics and ML use cases.",
        "responsibilities": ["Develop ETL jobs", "Maintain data quality checks", "Optimize warehouse performance"],
        "required_skills": ["SQL", "ETL", "Python", "Spark", "Data Warehousing"],
        "preferred_qualifications": ["Streaming systems experience", "Cloud data tooling", "Strong data modeling"],
        "experience": "3-7 years preferred",
        "tools": ["Airflow", "Spark", "dbt", "Snowflake", "Python"],
    },
    "BI Analyst": {
        "overview": "Translate business questions into dashboards and data-driven reporting insights.",
        "responsibilities": ["Create KPI dashboards", "Analyze trends and anomalies", "Collaborate with business teams"],
        "required_skills": ["SQL", "Power BI", "Tableau", "Data Modeling", "Communication"],
        "preferred_qualifications": ["Experience in stakeholder-facing analytics", "Domain expertise", "Strong storytelling"],
        "experience": "2-5 years preferred",
        "tools": ["Power BI", "Tableau", "SQL", "Excel", "Python"],
    },
    "Product Manager": {
        "overview": "Drive product strategy and execution to deliver measurable business outcomes.",
        "responsibilities": ["Define product roadmap", "Prioritize initiatives", "Coordinate cross-functional delivery"],
        "required_skills": ["Product Strategy", "User Research", "Analytics", "Roadmapping", "Communication"],
        "preferred_qualifications": ["SaaS product experience", "Technical fluency", "Growth experimentation"],
        "experience": "3-7 years preferred",
        "tools": ["Jira", "Notion", "Amplitude", "Figma", "Miro"],
    },
    "Technical Product Manager": {
        "overview": "Bridge product strategy and technical implementation for complex platforms.",
        "responsibilities": ["Define technical requirements", "Align engineering priorities", "Manage roadmap execution"],
        "required_skills": ["API Products", "System Thinking", "Roadmapping", "Stakeholder Management", "Data Analysis"],
        "preferred_qualifications": ["Engineering background", "Platform product experience", "Enterprise product exposure"],
        "experience": "4-8 years preferred",
        "tools": ["Jira", "Confluence", "Postman", "SQL", "Roadmapping Tools"],
    },
    "Project Manager": {
        "overview": "Plan and deliver projects on time, within scope, and with strong cross-team coordination.",
        "responsibilities": ["Manage project plans", "Track risks and dependencies", "Report delivery status"],
        "required_skills": ["Project Planning", "Agile", "Stakeholder Management", "Risk Management", "Communication"],
        "preferred_qualifications": ["PMP or Agile certification", "Software delivery experience", "Process improvement mindset"],
        "experience": "3-6 years preferred",
        "tools": ["Jira", "MS Project", "Confluence", "Asana", "Excel"],
    },
    "Business Analyst": {
        "overview": "Analyze business needs and convert them into actionable requirements and workflows.",
        "responsibilities": ["Gather and document requirements", "Map business processes", "Support UAT and release planning"],
        "required_skills": ["Requirements Analysis", "Process Mapping", "Stakeholder Interviews", "Documentation", "SQL"],
        "preferred_qualifications": ["Domain expertise", "Agile environment experience", "Strong facilitation skills"],
        "experience": "2-5 years preferred",
        "tools": ["Jira", "Confluence", "Visio", "SQL", "Excel"],
    },
    "UI Designer": {
        "overview": "Design polished interface systems with strong visual hierarchy and consistency.",
        "responsibilities": ["Create high-fidelity UI designs", "Maintain design library", "Collaborate with developers"],
        "required_skills": ["Figma", "Visual Design", "Typography", "Layout", "Design Systems"],
        "preferred_qualifications": ["Portfolio of shipped products", "Accessibility knowledge", "SaaS design exposure"],
        "experience": "2-5 years preferred",
        "tools": ["Figma", "Adobe XD", "Illustrator", "Maze", "Notion"],
    },
    "UX Designer": {
        "overview": "Shape user journeys and interaction models that improve usability and adoption.",
        "responsibilities": ["Conduct UX research", "Build wireframes and prototypes", "Run usability tests"],
        "required_skills": ["User Research", "Wireframing", "Prototyping", "Interaction Design", "Usability Testing"],
        "preferred_qualifications": ["Research portfolio", "Cross-platform product experience", "Design system collaboration"],
        "experience": "2-6 years preferred",
        "tools": ["Figma", "Miro", "Hotjar", "Maze", "Notion"],
    },
    "Product Designer": {
        "overview": "Own end-to-end product design from discovery through shipped experiences.",
        "responsibilities": ["Define user flows", "Create interactive prototypes", "Partner on product strategy"],
        "required_skills": ["Product Thinking", "Interaction Design", "Figma", "UX Writing", "Usability Testing"],
        "preferred_qualifications": ["Experience in B2B SaaS", "Strong collaboration with PM/Engineering", "Data-informed design"],
        "experience": "3-7 years preferred",
        "tools": ["Figma", "FigJam", "Notion", "Maze", "Loom"],
    },
    "Digital Marketing Specialist": {
        "overview": "Execute digital campaigns to drive acquisition, engagement, and conversion growth.",
        "responsibilities": ["Run multi-channel campaigns", "Analyze funnel performance", "Optimize campaign ROI"],
        "required_skills": ["Digital Marketing", "Analytics", "Campaign Management", "Email", "Lead Gen"],
        "preferred_qualifications": ["B2B marketing experience", "Marketing automation exposure", "Strong copywriting"],
        "experience": "2-5 years preferred",
        "tools": ["Google Analytics", "HubSpot", "Meta Ads", "Google Ads", "SEMrush"],
    },
    "SEO Specialist": {
        "overview": "Improve organic visibility through technical SEO and content optimization strategies.",
        "responsibilities": ["Conduct keyword research", "Perform technical SEO audits", "Drive on-page optimizations"],
        "required_skills": ["SEO", "Keyword Research", "Technical SEO", "Content Optimization", "Analytics"],
        "preferred_qualifications": ["Hands-on SEO growth results", "CMS familiarity", "Link building experience"],
        "experience": "2-5 years preferred",
        "tools": ["Ahrefs", "SEMrush", "Google Search Console", "GA4", "Screaming Frog"],
    },
    "PPC Manager": {
        "overview": "Manage paid acquisition channels with a focus on ROI and conversion growth.",
        "responsibilities": ["Build paid campaigns", "Monitor CAC and ROAS", "Optimize ad creatives and landing pages"],
        "required_skills": ["Google Ads", "Meta Ads", "Bid Optimization", "Attribution", "A/B Testing"],
        "preferred_qualifications": ["Performance marketing certifications", "Budget ownership experience", "Analytics proficiency"],
        "experience": "3-6 years preferred",
        "tools": ["Google Ads", "Meta Business Suite", "Looker Studio", "Hotjar", "GA4"],
    },
    "Social Media Manager": {
        "overview": "Develop social channels to strengthen brand presence and community engagement.",
        "responsibilities": ["Plan social content calendars", "Track engagement metrics", "Manage community interactions"],
        "required_skills": ["Social Strategy", "Content Creation", "Community Management", "Analytics", "Brand Voice"],
        "preferred_qualifications": ["Experience with B2B/B2C growth", "Video-first content exposure", "Influencer collaboration"],
        "experience": "2-5 years preferred",
        "tools": ["Buffer", "Hootsuite", "Canva", "Instagram", "LinkedIn"],
    },
    "Sales Executive": {
        "overview": "Drive pipeline growth and close opportunities through consultative selling.",
        "responsibilities": ["Prospect and qualify leads", "Run discovery and demos", "Close and expand accounts"],
        "required_skills": ["Prospecting", "Negotiation", "CRM", "Pipeline Management", "Communication"],
        "preferred_qualifications": ["SaaS sales experience", "Quota attainment history", "Enterprise sales exposure"],
        "experience": "2-6 years preferred",
        "tools": ["Salesforce", "HubSpot", "LinkedIn Sales Navigator", "Zoom", "Apollo"],
    },
    "Finance Manager": {
        "overview": "Lead financial planning, reporting, and strategic budgeting initiatives.",
        "responsibilities": ["Manage financial statements", "Drive budget cycles", "Support strategic decisions with analysis"],
        "required_skills": ["Financial Analysis", "Budgeting", "Forecasting", "Excel", "Stakeholder Communication"],
        "preferred_qualifications": ["CPA/CFA preferred", "Leadership experience", "ERP experience"],
        "experience": "5-8 years preferred",
        "tools": ["Excel", "Power BI", "NetSuite", "SAP", "Tableau"],
    },
    "Accountant": {
        "overview": "Maintain accurate financial records and ensure accounting compliance.",
        "responsibilities": ["Prepare reconciliations", "Manage monthly close", "Support statutory reporting"],
        "required_skills": ["Accounting", "Reconciliation", "GAAP", "Excel", "ERP"],
        "preferred_qualifications": ["Accounting certification", "Audit support experience", "Detail orientation"],
        "experience": "2-5 years preferred",
        "tools": ["Excel", "QuickBooks", "SAP", "Oracle", "Power BI"],
    },
    "FP&A Analyst": {
        "overview": "Build forecasts and financial models to support operational and strategic planning.",
        "responsibilities": ["Develop budget models", "Analyze variances", "Prepare planning insights"],
        "required_skills": ["FP&A", "Financial Modeling", "Forecasting", "Excel", "Communication"],
        "preferred_qualifications": ["Strong business partnering", "Scenario modeling expertise", "BI tooling experience"],
        "experience": "2-5 years preferred",
        "tools": ["Excel", "Adaptive Planning", "Power BI", "SQL", "Anaplan"],
    },
    "Talent Acquisition Specialist": {
        "overview": "Own end-to-end recruitment for priority hiring pipelines.",
        "responsibilities": ["Source and screen candidates", "Coordinate interviews", "Manage hiring funnel metrics"],
        "required_skills": ["Sourcing", "Interviewing", "ATS", "Employer Branding", "Stakeholder Management"],
        "preferred_qualifications": ["Technical hiring experience", "Diversity hiring exposure", "Strong communication"],
        "experience": "2-6 years preferred",
        "tools": ["LinkedIn Recruiter", "Greenhouse", "Lever", "Gem", "Notion"],
    },
    "HR Manager": {
        "overview": "Lead people operations, policies, and employee engagement programs.",
        "responsibilities": ["Manage HR operations", "Partner with managers on performance", "Ensure policy compliance"],
        "required_skills": ["HR Operations", "Employee Relations", "Performance Management", "Compliance", "Communication"],
        "preferred_qualifications": ["HR certification", "HRIS expertise", "Leadership skills"],
        "experience": "5-8 years preferred",
        "tools": ["BambooHR", "Workday", "Excel", "Lattice", "Slack"],
    },
    "Customer Success Manager": {
        "overview": "Drive retention and product adoption by partnering closely with customers.",
        "responsibilities": ["Manage onboarding and adoption", "Run business reviews", "Reduce churn risk"],
        "required_skills": ["Customer Management", "Onboarding", "Renewals", "Communication", "Analytics"],
        "preferred_qualifications": ["B2B SaaS customer success experience", "Escalation handling", "Strategic account planning"],
        "experience": "3-6 years preferred",
        "tools": ["Gainsight", "HubSpot", "Salesforce", "Zendesk", "Looker"],
    },
    "Technical Support Engineer": {
        "overview": "Resolve technical customer issues and improve support knowledge workflows.",
        "responsibilities": ["Troubleshoot product issues", "Document solutions", "Collaborate with engineering on escalations"],
        "required_skills": ["Troubleshooting", "API Debugging", "Logs Analysis", "Customer Communication", "Ticketing"],
        "preferred_qualifications": ["SaaS technical support experience", "SQL familiarity", "Incident management exposure"],
        "experience": "2-5 years preferred",
        "tools": ["Zendesk", "Postman", "Datadog", "SQL", "Confluence"],
    },
    "Supply Chain Analyst": {
        "overview": "Optimize inventory and supply planning using data-driven analysis.",
        "responsibilities": ["Track supply metrics", "Analyze demand trends", "Recommend planning improvements"],
        "required_skills": ["Supply Chain", "Forecasting", "Excel", "ERP", "Data Analysis"],
        "preferred_qualifications": ["Inventory optimization experience", "Cross-functional operations collaboration", "Strong modeling skills"],
        "experience": "2-5 years preferred",
        "tools": ["SAP", "Excel", "Power BI", "Oracle", "SQL"],
    },
    "Compliance Manager": {
        "overview": "Establish and monitor compliance programs aligned with regulatory requirements.",
        "responsibilities": ["Maintain compliance controls", "Coordinate audits", "Update policy frameworks"],
        "required_skills": ["Compliance", "Risk Management", "Policy Drafting", "Auditing", "Regulatory Reporting"],
        "preferred_qualifications": ["Industry certifications", "Cross-border compliance exposure", "Legal collaboration experience"],
        "experience": "4-8 years preferred",
        "tools": ["GRC Platform", "Excel", "Policy Management Tools", "Jira", "Confluence"],
    },
    "Civil Engineer": {
        "overview": "Design and oversee infrastructure projects with safety and quality standards.",
        "responsibilities": ["Prepare technical drawings", "Coordinate site execution", "Ensure design compliance"],
        "required_skills": ["Civil Design", "AutoCAD", "Project Planning", "Site Coordination", "Safety Standards"],
        "preferred_qualifications": ["Licensed engineer preferred", "Large infrastructure experience", "Regulatory knowledge"],
        "experience": "3-7 years preferred",
        "tools": ["AutoCAD", "Civil 3D", "MS Project", "Primavera", "Excel"],
    },
    "Construction Manager": {
        "overview": "Lead end-to-end construction project execution across schedule, quality, and cost.",
        "responsibilities": ["Plan site operations", "Manage contractors", "Track budget and progress"],
        "required_skills": ["Construction Planning", "Site Management", "Cost Estimation", "Contractor Coordination", "Safety Compliance"],
        "preferred_qualifications": ["PMP/Construction certification", "Multi-site experience", "Regulatory compliance knowledge"],
        "experience": "5-10 years preferred",
        "tools": ["Primavera", "MS Project", "AutoCAD", "Procore", "Excel"],
    },
}

QUICK_INSERT_BLOCKS: Dict[str, str] = {
    "Role Overview": "Role Overview\nProvide a concise summary of the role's mission, team context, and expected business impact.\n",
    "Responsibilities": "Key Responsibilities\n- Own and deliver measurable outcomes\n- Collaborate cross-functionally with stakeholders\n- Improve process efficiency and quality\n",
    "Required Skills": "Required Skills\n- Core technical/functional competency\n- Problem-solving and communication\n- Relevant tools and workflows\n",
    "Preferred Qualifications": "Preferred Qualifications\n- Bachelor's degree or equivalent practical experience\n- Industry certifications (if relevant)\n- Experience in fast-paced environments\n",
}


def get_job_categories() -> List[str]:
    return list(JOB_CATALOG.keys())


def get_subcategories(category: str) -> List[str]:
    return list(JOB_CATALOG.get(category, {}).keys())


def get_roles(category: str, subcategory: str) -> List[str]:
    return JOB_CATALOG.get(category, {}).get(subcategory, [])


def get_total_roles() -> int:
    return sum(len(roles) for category in JOB_CATALOG.values() for roles in category.values())


def get_role_skills(category: str, subcategory: str, role: str) -> List[str]:
    template = ROLE_TEMPLATE_DATA.get(role)
    if template and isinstance(template.get("required_skills"), list):
        return list(template["required_skills"])
    return SUBCATEGORY_SKILLS.get(subcategory, ["Communication", "Problem Solving", "Collaboration", "Domain Knowledge"])


def _format_template(
    role: str,
    category: str,
    subcategory: str,
    overview: str,
    responsibilities: List[str],
    required_skills: List[str],
    preferred_qualifications: List[str],
    experience: str,
    tools: List[str],
) -> str:
    responsibilities_block = "\n".join([f"- {item}" for item in responsibilities])
    skills_block = "\n".join([f"- {item}" for item in required_skills])
    preferred_block = "\n".join([f"- {item}" for item in preferred_qualifications])
    tools_block = "\n".join([f"- {item}" for item in tools])

    return f"""Role: {role}
Industry: {category}
Specialization: {subcategory}

Role Overview
{overview}

Key Responsibilities
{responsibilities_block}

Required Skills
{skills_block}

Preferred Qualifications
{preferred_block}

Experience Level
{experience}

Tools & Technologies
{tools_block}
"""


def generate_job_description_template(category: str, subcategory: str, role: str) -> str:
    """Generate a structured job description template for a selected role."""
    template = ROLE_TEMPLATE_DATA.get(role)
    if template:
        return _format_template(
            role=role,
            category=category,
            subcategory=subcategory,
            overview=str(template["overview"]),
            responsibilities=list(template["responsibilities"]),
            required_skills=list(template["required_skills"]),
            preferred_qualifications=list(template["preferred_qualifications"]),
            experience=str(template["experience"]),
            tools=list(template["tools"]),
        )

    fallback_skills = get_role_skills(category, subcategory, role)
    return _format_template(
        role=role,
        category=category,
        subcategory=subcategory,
        overview=f"We are hiring a {role} to contribute to high-impact {subcategory.lower()} initiatives in our {category} team.",
        responsibilities=[
            "Deliver role-specific outcomes aligned with team goals.",
            "Collaborate with stakeholders to improve quality and execution speed.",
            "Track performance and continuously optimize workflows.",
        ],
        required_skills=fallback_skills,
        preferred_qualifications=[
            "Bachelor's degree or equivalent practical experience.",
            "Strong communication and cross-functional collaboration.",
            "Proven ability to manage priorities in a fast-paced environment.",
        ],
        experience="2-5 years preferred",
        tools=fallback_skills,
    )
