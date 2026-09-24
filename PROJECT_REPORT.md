# Project Report: Global AI Agent Workforce Integration Analytics Dashboard

---

## 1. Project Overview

**Project Title:** Global AI Agent Workforce Integration Analytics Dashboard  
**Technology Stack:** Python, Flask, Pandas, Scikit-learn, HTML/CSS  
**Dataset:** Global_AI_Agent_Workforce_Integration_2026.csv  
**Objective:** Build a data-driven web application that analyses global enterprise AI agent adoption trends and predicts business outcomes (ROI timeline and productivity gains) based on company profiles.

---

## 2. Problem Statement

Organisations adopting autonomous AI agents face uncertainty around two key business questions:

1. **How long will it take to achieve a positive return on investment (ROI)?**
2. **What productivity gains can realistically be expected?**

These questions vary significantly by industry, company size, AI agent role, and governance maturity. This project addresses both questions using machine learning predictive models, backed by real-world 2026 data from companies across multiple sectors.

---

## 3. Dataset Description

**File:** `Global_AI_Agent_Workforce_Integration_2026.csv`

The dataset captures AI agent adoption metrics across global enterprises in 2026.

### Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `Company_ID` | String | Unique identifier per company |
| `Industry` | Categorical | Business sector |
| `Company_Size` | Categorical | Small / Medium / Large / Enterprise |
| `Primary_AI_Agent_Role` | Categorical | Core function of deployed AI agents |
| `Autonomous_Agents_Deployed` | Integer | Count of agents in production |
| `Avg_Agent_Cost_Per_Month_USD` | Float | Monthly cost per AI agent |
| `Human_Roles_Replaced` | Integer | Positions replaced by AI |
| `Human_Roles_Augmented` | Integer | Positions augmented by AI |
| `Productivity_Gain_Percent` | Float | **Target variable 1** — % productivity improvement |
| `Cybersecurity_Incidents_YTD` | Integer | Security incidents year-to-date |
| `Employee_Sentiment_Score_1_to_10` | Float | Staff morale score |
| `Months_To_Positive_ROI` | Float | **Target variable 2** — months to break even |
| `Has_Strict_AI_Governance` | Boolean | Whether formal AI governance exists |

### Sample Statistics

- Average Productivity Gain: ~25–30%
- Average Months to Positive ROI: ~12–18 months
- Industries covered: Education, Manufacturing, Retail, Healthcare, Finance, and more
- Company sizes: Small (1–50), Medium (51–500), Large (501–5000), Enterprise (5000+)

---

## 4. System Architecture

```
User Browser
     │
     ▼
Flask Web Server (app.py)
     │
     ├── GET  /              →  Home Dashboard (index.html)
     ├── POST /predict       →  ML Prediction Engine
     └── GET  /api/insights  →  Aggregated Analytics API
              │
              ├── model_roi.pkl   (ROI months predictor)
              ├── model_prod.pkl  (Productivity % predictor)
              ├── encoders.pkl    (Label encoders)
              └── CSV Dataset
```

---

## 5. Application Components

### 5.1 Home Dashboard (`/`)

- Loads the dataset and computes summary statistics:
  - Total number of companies in the dataset
  - Average productivity gain (%)
  - Average months to positive ROI
  - Total autonomous agents deployed
- Passes the first 10 records and filter options (industries, roles, sizes) to the frontend template.

### 5.2 Prediction Engine (`/predict`)

A POST endpoint that accepts a JSON payload describing a company profile and returns two ML predictions:

**Input Features:**
| Feature | Description |
|---------|-------------|
| `industry` | Company industry sector |
| `size` | Company size band |
| `role` | Primary AI agent role |
| `agents` | Number of autonomous agents to deploy |
| `cost` | Average monthly agent cost (USD) |
| `governance` | Whether strict AI governance exists (1/0) |

**Output:**
- `roi` — Predicted months to positive ROI
- `productivity` — Predicted productivity gain (%)

**ML Pipeline:**
1. Categorical inputs encoded using pre-fitted `LabelEncoder` objects (`encoders.pkl`)
2. Encoded feature vector passed to `model_roi.pkl` and `model_prod.pkl`
3. Both models return scalar predictions

### 5.3 Insights API (`/api/insights`)

Returns two aggregated JSON objects:
- **`by_industry`** — Mean productivity gain per industry
- **`by_governance`** — Mean cybersecurity incidents per year, grouped by governance strictness

---

## 6. Machine Learning Models

### Model 1: ROI Prediction (`model_roi.pkl`)
- **Target:** `Months_To_Positive_ROI`
- **Type:** Regression
- **Algorithm:** To be confirmed from training notebook

### Model 2: Productivity Prediction (`model_prod.pkl`)
- **Target:** `Productivity_Gain_Percent`
- **Type:** Regression
- **Algorithm:** To be confirmed from training notebook

### Feature Engineering
- `Industry`, `Company_Size`, and `Primary_AI_Agent_Role` are label-encoded
- `Autonomous_Agents_Deployed`, `Avg_Agent_Cost_Per_Month_USD`, and `Has_Strict_AI_Governance` are used as numeric inputs

---

## 7. Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `flask` | ≥ 2.3.0 | Web framework |
| `pandas` | ≥ 2.0.0 | Data loading and aggregation |
| `scikit-learn` | ≥ 1.3.0 | ML model training and inference |
| `joblib` | ≥ 1.3.0 | Model serialisation / deserialisation |
| `numpy` | ≥ 1.24.0 | Numerical operations |

---

## 8. How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python "code file.ipynb"

# Access the application
# Open browser → http://127.0.0.1:5000
```

---

## 9. Key Insights (from Dataset)

- **Governance Impact:** Companies with strict AI governance policies tend to report fewer cybersecurity incidents annually.
- **Industry Variation:** Productivity gains vary significantly by sector — some industries (e.g., Data Analytics roles) show higher gains.
- **Scale Effect:** Enterprise-sized companies deploy more agents but don't always achieve faster ROI due to higher integration complexity.
- **Augmentation vs Replacement:** Most companies augment more roles than they replace, suggesting AI is being used as a collaborative tool.

---

## 10. Future Enhancements

| Enhancement | Description |
|-------------|-------------|
| Model retraining UI | Allow admin users to retrain models via the dashboard |
| Interactive charts | Add Chart.js / Plotly visualisations for trends |
| Filter & search | Enable CSV data browsing with filters by industry/size |
| Authentication | Add login/logout for secure access to predictions |
| Export reports | Allow users to download prediction results as PDF/CSV |
| Docker support | Containerise the app for easy deployment |

---

## 11. Conclusion

This project demonstrates how enterprise AI adoption data can be transformed into actionable predictions using a lightweight Flask API backed by scikit-learn models. The dashboard gives decision-makers a fast, evidence-based way to estimate ROI timelines and productivity improvements before committing to AI agent deployment — reducing uncertainty and supporting informed investment decisions.

---

*Report generated for: Global AI Agent Workforce Integration Analytics Dashboard*  
*Dataset Year: 2026*
