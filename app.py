from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# ── Load dataset ──────────────────────────────────────────────────────────────
CSV_PATH = os.path.join('data', 'Global_AI_Agent_Workforce_Integration_2026.csv')
df = pd.read_csv(CSV_PATH)

# ── Load trained models & encoders ───────────────────────────────────────────
model_roi  = joblib.load('model_roi.pkl')
model_prod = joblib.load('model_prod.pkl')
encoders   = joblib.load('encoders.pkl')


# ── Helper: encode a single prediction request ───────────────────────────────
def build_feature_vector(d):
    """Encode categorical inputs and return a single-row feature list."""
    industry = encoders['industry'].transform([d['industry']])[0]
    size     = encoders['size'].transform([d['size']])[0]
    role     = encoders['role'].transform([d['role']])[0]
    agents   = int(d['agents'])
    cost     = float(d['cost'])
    gov      = int(d['governance'])
    return [[industry, size, role, agents, cost, gov]]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    """Dashboard home page with summary statistics."""
    stats = {
        "total":        len(df),
        "avg_prod":     round(df['Productivity_Gain_Percent'].mean(), 2),
        "avg_roi":      round(df['Months_To_Positive_ROI'].mean(), 2),
        "total_agents": int(df['Autonomous_Agents_Deployed'].sum()),
        "avg_sentiment":round(df['Employee_Sentiment_Score_1_to_10'].mean(), 2),
        "total_replaced":   int(df['Human_Roles_Replaced'].sum()),
        "total_augmented":  int(df['Human_Roles_Augmented'].sum()),
        "industries":   sorted(df['Industry'].unique().tolist()),
        "roles":        sorted(df['Primary_AI_Agent_Role'].unique().tolist()),
        "sizes":        sorted(df['Company_Size'].unique().tolist()),
    }
    records = df.head(10).to_dict('records')
    return render_template('index.html', stats=stats, data=records)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict ROI months and productivity gain for a company profile.

    Expected JSON body:
        {
            "industry":   "Manufacturing",
            "size":       "Medium (51-500)",
            "role":       "Data Analytics",
            "agents":     10,
            "cost":       500.00,
            "governance": 1
        }

    Returns:
        { "roi": <float>, "productivity": <float> }
    """
    data = request.get_json(force=True)

    required = ['industry', 'size', 'role', 'agents', 'cost', 'governance']
    missing  = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        X = build_feature_vector(data)
    except Exception as e:
        return jsonify({"error": f"Encoding error: {str(e)}"}), 422

    roi  = round(float(model_roi.predict(X)[0]),  2)
    prod = round(float(model_prod.predict(X)[0]), 2)

    return jsonify({"roi": roi, "productivity": prod})


@app.route('/api/insights')
def insights():
    """Aggregated insights for the dashboard charts."""
    by_industry = (
        df.groupby('Industry')['Productivity_Gain_Percent']
        .mean().round(2).to_dict()
    )
    by_governance = (
        df.groupby('Has_Strict_AI_Governance')['Cybersecurity_Incidents_YTD']
        .mean().round(2)
        .rename(index={True: 'Strict Governance', False: 'No Governance'})
        .to_dict()
    )
    by_role = (
        df.groupby('Primary_AI_Agent_Role')['Productivity_Gain_Percent']
        .mean().round(2).to_dict()
    )
    by_size = (
        df.groupby('Company_Size')['Months_To_Positive_ROI']
        .mean().round(2).to_dict()
    )
    return jsonify({
        "by_industry":   by_industry,
        "by_governance": by_governance,
        "by_role":       by_role,
        "by_size":       by_size,
    })


@app.route('/api/data')
def data_table():
    """Return paginated dataset records as JSON."""
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    industry = request.args.get('industry', '')
    size     = request.args.get('size', '')

    filtered = df.copy()
    if industry:
        filtered = filtered[filtered['Industry'] == industry]
    if size:
        filtered = filtered[filtered['Company_Size'] == size]

    total   = len(filtered)
    start   = (page - 1) * per_page
    records = filtered.iloc[start: start + per_page].to_dict('records')

    return jsonify({"total": total, "page": page, "records": records})


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
