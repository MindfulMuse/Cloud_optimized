💰 Cloud Cost Optimizer - AI-Powered LLM-Driven System
An intelligent cloud cost optimization tool that uses Large Language Models (LLMs) to analyze project requirements, generate synthetic billing data, and provide actionable multi-cloud cost optimization recommendations.
Show Image
Show Image
Show Image

📑 Table of Contents

Features
Project Structure
Prerequisites
Installation
Configuration
Usage
Example Files
How It Works
Architecture
Tools Used
Troubleshooting
Contributing
License


✨ Features
Core Capabilities

-- AI-Powered Profile Extraction: Automatically extracts structured project profiles from free-form text descriptions
-- Synthetic Billing Generation: Creates realistic, budget-aware cloud billing data (12-20 records)
-- Multi-Cloud Cost Analysis: Analyzes costs across AWS, Azure, and GCP
-- Optimization Recommendations: Provides 6-10 actionable cost-saving recommendations
-- Alternative Solutions: Suggests open-source and free-tier alternatives
-- Report Generation: Exports detailed reports in JSON and formatted text

Key Features

✅ Free-form text input (no strict format required)
✅ Budget-aware cost generation
✅ Multi-cloud provider support (AWS, Azure, GCP)
✅ Open-source alternative recommendations
✅ Risk and effort assessment for each recommendation
✅ Step-by-step implementation guides
✅ CLI-based interface (Windows, Mac, Linux compatible)


📁 Project Structure
cloud-cost-optimizer/
├── main.py                          # Main CLI application
├── profile_extractor.py             # LLM-based profile extraction
├── billing_generator.py             # Synthetic billing generation
├── cost_analyzer.py                 # Cost analysis & recommendations
├── utils.py                         # Utility functions
├── requirements.txt                 # Python dependencies
├── .env                            # API keys (not tracked in git)
├── .env.example                    # Environment template
├── README.md                       # This file
├── data/                           # Generated data files
│   ├── project_description.txt     # User's project description
│   ├── project_profile.json        # Extracted project profile
│   ├── mock_billing.json          # Generated billing records
│   ├── cost_optimization_report.json       # Full analysis report
│   └── cost_optimization_report_formatted.txt  # Human-readable report
└── examples/                       # Example files
    ├── example_description.txt
    ├── example_profile.json
    ├── example_billing.json
    └── example_report.json

🔧 Prerequisites
Required Software

Python: 3.9 or higher
pip: Python package installer
Git: For cloning the repository

 -------------------
| API Requirements  |
 -------------------

Groq API Key: Free account at https://console.groq.com

Sign up for free
Generate an API key
Free tier includes generous quota for testing




📥 Installation
Step 1: Clone the Repository
bashgit clone https://github.com/yourusername/cloud-cost-optimizer.git
cd cloud-cost-optimizer
Step 2: Create Virtual Environment
Windows:
bashpython -m venv venv
venv\Scripts\activate
Mac/Linux:
bashpython3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bashpip install -r requirements.txt
Dependencies installed:

requests: HTTP library for API calls
python-dotenv: Environment variable management
groq: Groq LLM API client


⚙️ Configuration
Step 1: Get Groq API Key

Go to https://console.groq.com
Sign up / Log in
Navigate to API Keys section
Click Create API Key
Copy the generated key (starts with gsk_)

Step 2: Create .env File
Create a .env file in the project root:
bash# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
Step 3: Add Your API Key
Open .env and add your key:
envGROQ_API_KEY=gsk_your_actual_api_key_here
⚠️ Important:

No quotes around the API key
No spaces before or after =
Never commit .env to version control


🚀 Usage
Starting the Application
bashpython main.py

1️⃣ Run the python file

<img width="947" height="521" alt="image" src="https://github.com/user-attachments/assets/bc2c7b5a-bdb9-47eb-8fbb-bdcfc7f8d2fb" />



2️⃣ Run Complete Analysis

<img width="967" height="517" alt="image" src="https://github.com/user-attachments/assets/104336c0-0611-43d0-8a6b-0d376c0e0dcf" />

Output:

<img width="882" height="640" alt="image" src="https://github.com/user-attachments/assets/3841f024-759a-4910-99db-7eb364ddf4fc" />

<img width="875" height="542" alt="image" src="https://github.com/user-attachments/assets/b75af61c-0bc1-4af0-ba0c-87f1a5bce21e" />



3️⃣ ##ANALYSIS SUMMARY

<img width="848" height="425" alt="image" src="https://github.com/user-attachments/assets/0f09e116-1bea-4d11-8f5d-59e3189fc3d2" />


<img width="743" height="621" alt="image" src="https://github.com/user-attachments/assets/166e5351-dc92-40b4-92a6-37a870f0395e" />

4️⃣ Export Report
Select Option 4 to save a formatted text report.
5️⃣ Exit
Select Option 5 to close the application.


Example output :
<img width="838" height="441" alt="image" src="https://github.com/user-attachments/assets/6f814774-bbb7-4467-882f-379c7637c511" />

##mock_billing.json

<img width="1341" height="498" alt="image" src="https://github.com/user-attachments/assets/3445cb97-da4f-479a-b101-656f13760252" />

##cost_optimization_report.json 
<img width="820" height="912" alt="image" src="https://github.com/user-attachments/assets/3f9df6e6-6961-4550-b1c1-1801cb700319" />

##project_profile.json
<img width="1292" height="667" alt="image" src="https://github.com/user-attachments/assets/390024c4-3caf-4b0e-84b9-8a72354161b0" />

