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
Main Menu
======================================================================
                      Cloud Cost Optimizer
======================================================================

🤖 AI-Powered Cloud Cost Analysis & Optimization

Please select an option:

  1. Enter New Project Description
  2. Run Complete Cost Analysis
  3. View Recommendations
  4. Export Report
  5. Exit

Enter your choice (1-5):
Workflow
1️⃣ Enter Project Description
Select Option 1, then type your project description:
I want to build an e-commerce platform for selling handmade crafts.
The frontend will use React with Next.js, backend with Node.js.
MongoDB for database, Nginx as reverse proxy.
Hosting on AWS with Docker containers.
My budget is 8000 rupees per month.
The system needs to be highly available and scalable.
DONE
Press Enter after typing DONE.
2️⃣ Run Complete Analysis
Select Option 2 to:

Extract project profile using AI
Generate realistic billing records (12-20)
Analyze costs and create recommendations
Display summary results

Expected output:
======================================================================
STEP 1/3: Extracting Project Profile
======================================================================

Analyzing: I want to build an e-commerce platform...
  ✓ Extracted profile for: Handmade Crafts E-commerce Platform
  ✓ Budget: ₹8,000.00/month

✅ Project profile extracted and saved

======================================================================
STEP 2/3: Generating Synthetic Billing Data
======================================================================

  → Generating billing data for AWS...
  ✓ Generated 15 billing records
  ✓ Total monthly cost: ₹8,450.00

✅ Mock billing data generated and saved

======================================================================
STEP 3/3: Analyzing Costs & Generating Recommendations
======================================================================

  📊 Analyzing costs...
  🤖 Generating recommendations with AI...
  ✅ Generated 8 recommendations

✅ Cost optimization report generated and saved

======================================================================
📊 ANALYSIS SUMMARY
======================================================================

💰 Cost Overview:
   Total Monthly Cost: ₹8,450.00
   Budget:             ₹8,000.00
   Variance:           ₹450.00
   Status:             ⚠️  OVER BUDGET

💡 Optimization Potential:
   Total Savings:      ₹3,200.00
   Savings %:          37.9%
   Recommendations:    8
3️⃣ View Recommendations
Select Option 3 to see detailed recommendations:
======================================================================
#1: Migrate MongoDB to Self-Hosted Open Source
======================================================================
Service:            MongoDB
Current Cost:       ₹1,200.00
Potential Savings:  ₹600.00
Type:               open_source
Implementation:     MEDIUM effort
Risk Level:         MEDIUM

📝 Description:
   Migrate from managed MongoDB service to self-hosted open-source
   MongoDB on EC2, reducing costs while maintaining functionality.

☁️  Cloud Providers: AWS, Azure, GCP

📋 Implementation Steps:
   1. Set up EC2 instance with MongoDB
   2. Configure backup and monitoring
   3. Migrate data from managed service
   4. Update application connection strings
   5. Test thoroughly before switching
4️⃣ Export Report
Select Option 4 to save a formatted text report.
5️⃣ Exit
Select Option 5 to close the application.