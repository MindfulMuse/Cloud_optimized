# 💰 Cloud Cost Optimizer – AI-Powered LLM-Driven System

An intelligent cloud cost optimization tool that uses **Large Language Models (LLMs)** to analyze project requirements, generate synthetic billing data, and provide actionable **multi-cloud cost optimization recommendations**.

> 📊 Analyze. 💡 Optimize. 💸 Save.

---

## 📑 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Example Files](#-example-files)
- [Architecture](#-system-architecture)
- [Optimization Logic ](#-Optimization-Logic)
- [Use Cases](#-use-cases)

---

## ✨ Features

### 🔹 Core Capabilities

- **AI-Powered Profile Extraction**  
  Automatically extracts structured project profiles from free-form text descriptions.

- **Synthetic Billing Generation**  
  Creates realistic, budget-aware cloud billing data (12–20 records).

- **Multi-Cloud Cost Analysis**  
  Analyzes costs across **AWS**, **Azure**, and **GCP**.

- **Optimization Recommendations**  
  Provides **6–10 actionable cost-saving recommendations**.

- **Alternative Solutions**  
  Suggests open-source and free-tier alternatives.

- **Report Generation**  
  Exports detailed reports in **JSON** and **human-readable formatted text**.

### ✅ Key Features

- Free-form text input (no strict format required)
- Budget-aware cost generation
- Multi-cloud provider support (AWS, Azure, GCP)
- Open-source alternative recommendations
- Risk and effort assessment for each recommendation
- Step-by-step implementation guides
- CLI-based interface (Windows, macOS, Linux)

---

## 📁 Project Structure

```text
cloud-cost-optimizer/
├── main.py                          # Main CLI application
├── profile_extractor.py             # LLM-based profile extraction
├── billing_generator.py             # Synthetic billing generation
├── cost_analyzer.py                 # Cost analysis & recommendations
├── utils.py                         # Utility functions
├── requirements.txt                 # Python dependencies
├── .env                             # API keys (not tracked in git)
├── .env.example                     # Environment template
├── README.md                        # This file
├── data/                            # Generated data files
│   ├── project_description.txt
│   ├── project_profile.json
│   ├── mock_billing.json
│   ├── cost_optimization_report.json
│   └── cost_optimization_report_formatted.txt
└── examples/                        # Example files
    ├── example_description.txt
    ├── example_profile.json
    ├── example_billing.json
    └── example_report.json

```

## 🔧 Prerequisites

### Required Software

- **Python**: 3.9 or higher  
- **pip**: Python package installer  
- **Git**: For cloning the repository  

### 🔑 API Requirements


Groq API Key: Free account at https://console.groq.com

Sign up for free
Generate an API key
Free tier includes generous quota for testing




## 📥 Installation

- Step 1: Clone the Repository
bashgit clone https://github.com/yourusername/cloud-cost-optimizer.git
cd cloud-cost-optimizer
- Step 2: Create Virtual Environment
Windows:
bashpython -m venv venv
venv\Scripts\activate
Mac/Linux:
bashpython3 -m venv venv
source venv/bin/activate
- Step 3: Install Dependencies
bashpip install -r requirements.txt
Dependencies installed:

requests: HTTP library for API calls
python-dotenv: Environment variable management
groq: Groq LLM API client


## ⚙️ Configuration
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

## Mac/Linux
cp .env.example .env
Step 3: Add Your API Key
Open .env and add your key:
envGROQ_API_KEY=gsk_your_actual_api_key_here
⚠️ Important:

No quotes around the API key
No spaces before or after =
Never commit .env to version control


## 🚀 Usage

Starting the Application
bashpython main.py


## 🚀 Getting Started

### 1️⃣ Run the Python File

```bash
python main.py
```

📸 **CLI Startup Screen**

![Run Python File](https://github.com/user-attachments/assets/bc2c7b5a-bdb9-47eb-8fbb-bdcfc7f8d2fb)

---

### 2️⃣ Run Complete Analysis

Select **Option 1** from the menu to perform a full cost analysis.

📸 **Running Analysis**

![Run Analysis](https://github.com/user-attachments/assets/104336c0-0611-43d0-8a6b-0d376c0e0dcf)

📸 **Analysis Output**

![Output 1](https://github.com/user-attachments/assets/3841f024-759a-4910-99db-7eb364ddf4fc)

![Output 2](https://github.com/user-attachments/assets/b75af61c-0bc1-4af0-ba0c-87f1a5bce21e)

---

### 3️⃣ Analysis Summary

After analysis completion, a detailed **summary view** is displayed including:

* 💰 Total monthly cloud spend
* 📉 Cost distribution by service
* ⚠️ Inefficient resource flags
* 📌 Optimization suggestions

📸 **Summary Screens**

![Summary 1](https://github.com/user-attachments/assets/0f09e116-1bea-4d11-8f5d-59e3189fc3d2)

![Summary 2](https://github.com/user-attachments/assets/166e5351-dc92-40b4-92a6-37a870f0395e)

---

### 4️⃣ Export Report

Select **Option 4** to export a formatted cost optimization report.

📄 The report is saved as a `.txt` file inside the `reports/` directory.

📸 **Export Option**

![Export Report](https://github.com/user-attachments/assets/87ee5b01-88c0-42a8-a96d-a2981bfd0a2f)

---

### 5️⃣ Exit Application

Select **Option 5** to safely exit the program.

📸 **Exit Screens**

![Exit 1](https://github.com/user-attachments/assets/79877f3a-db7f-4055-90e3-28494f781320)

![Exit 2](https://github.com/user-attachments/assets/88fae00d-c536-454d-9470-62cc7358a8c8)

---

## 🧪 Example Files

📸 **Sample Analysis Result**

![Example Output](https://github.com/user-attachments/assets/6f814774-bbb7-4467-882f-379c7637c511)

---

## 📄 Input & Output Files

### 🔹 `mock_billing.json`

Simulated cloud billing data used for analysis.

![mock\_billing.json](https://github.com/user-attachments/assets/3445cb97-da4f-479a-b101-656f13760252)

---

### 🔹 `project_profile.json`

Defines project metadata and environment details.

![project\_profile.json](https://github.com/user-attachments/assets/390024c4-3caf-4b0e-84b9-8a72354161b0)

---

### 🔹 `cost_optimization_report.json`

Structured output containing optimization recommendations.

![cost\_optimization\_report.json](https://github.com/user-attachments/assets/3f9df6e6-6961-4550-b1c1-1801cb700319)


---

## 🏗️ System Architecture

```text
┌─────────────────────┐
│  User Input         │
│  (Free-form text)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Profile Extractor  │ ──► Groq LLM API
│  (AI Extraction)    │     (Llama-3.1-8b-instant)
└──────────┬──────────┘
           │
           ▼
     project_profile.json
           │
           ▼
┌─────────────────────┐
│  Billing Generator  │ ──► Groq LLM API
│  (Synthetic Data)   │     (Context-aware)
└──────────┬──────────┘
           │
           ▼
     mock_billing.json
           │
           ▼
┌─────────────────────┐
│  Cost Analyzer      │ ──► Groq LLM API
│  (Recommendations)  │     (Expert analysis)
└──────────┬──────────┘
           │
           ▼
  cost_optimization_report.json
           │
           ▼
┌─────────────────────┐
│  Output Reports     │
│  (JSON + TXT)       │
└─────────────────────┘

```
## 📈 Optimization Logic (Highlights)

* Identifies **idle or low-utilization services**
* Flags **over-provisioned compute resources**
* Suggests **downsizing & cleanup actions**
* Estimates **potential monthly savings**

---

## 📌 Use Cases

* Reduces cloud costs by identifying waste and overprovisioned resources.
* Provides actionable optimization recommendations across AWS, Azure, and GCP.
* Helps plan cost-efficient architectures before deployment.
* Supports continuous cost monitoring and multi-cloud decision-making.

---
