# 🤖 Global AI Agent Workforce Integration — Analytics Dashboard

A Flask-based web application that provides predictive analytics and insights on AI agent adoption across global enterprises (2026 dataset).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Dataset](#dataset)

---

## Overview

This application analyses how organisations worldwide are integrating autonomous AI agents into their workforce. It uses machine learning models to predict **ROI timelines** and **productivity gains** based on company profile inputs, and provides a dashboard with industry-level insights.

---

## Features

- 📊 **Dashboard** — Summary statistics on AI agent adoption (avg productivity gain, ROI months, total agents deployed)
- 🔮 **Prediction Engine** — Predict ROI months and productivity gain for a given company profile
- 📡 **Insights API** — Aggregated analytics by industry and AI governance strictness
- 🗃️ **CSV-powered** — Backed by the `Global_AI_Agent_Workforce_Integration_2026.csv` dataset

---

## Project Structure

```
project/
│
├── code file.ipynb                              # Flask application entry point
├── data/
│   └── Global_AI_Agent_Workforce_Integration_2026.csv
├── model_roi.pkl                                # Trained ROI prediction model
├── model_prod.pkl                               # Trained productivity prediction model
├── encoders.pkl                                 # Label encoders for categorical features
├── templates/
│   └── index.html                               # Frontend dashboard template
├── requirements.txt                             # Python dependencies
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone the repository
git clone <repository-url>
cd <project-folder>

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
# Run the Flask development server
python "code file.ipynb"
```

Open your browser at `http://127.0.0.1:5000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home dashboard with summary statistics |
| POST | `/predict` | Predict ROI and productivity for a company profile |
| GET | `/api/insights` | Aggregated insights by industry and governance |

### `/predict` — Request Body (JSON)

```json
{
  "industry":   "Manufacturing",
  "size":       "Medium (51-500)",
  "role":       "Data Analytics",
  "agents":     10,
  "cost":       500.00,
  "governance": 1
}
```

### `/predict` — Response

```json
{
  "roi": 12.45,
  "productivity": 28.73
}
```

---

## Dataset

**File:** `Global_AI_Agent_Workforce_Integration_2026.csv`

| Column | Description |
|--------|-------------|
| `Company_ID` | Unique company identifier |
| `Industry` | Sector (Education, Manufacturing, Retail, etc.) |
| `Company_Size` | Small / Medium / Large / Enterprise |
| `Primary_AI_Agent_Role` | Main function of AI agents deployed |
| `Autonomous_Agents_Deployed` | Number of agents in production |
| `Avg_Agent_Cost_Per_Month_USD` | Monthly cost per agent |
| `Human_Roles_Replaced` | Headcount replaced by AI |
| `Human_Roles_Augmented` | Headcount augmented by AI |
| `Productivity_Gain_Percent` | % improvement in productivity |
| `Cybersecurity_Incidents_YTD` | Security incidents year-to-date |
| `Employee_Sentiment_Score_1_to_10` | Staff sentiment rating |
| `Months_To_Positive_ROI` | Months until investment breaks even |
| `Has_Strict_AI_Governance` | Whether strict AI governance is in place |

---

## License

MIT License
