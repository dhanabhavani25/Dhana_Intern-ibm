"""
train_models.py
───────────────
Trains two Random Forest regression models on the
Global AI Agent Workforce Integration 2026 dataset and saves:
    • model_roi.pkl   — predicts Months_To_Positive_ROI
    • model_prod.pkl  — predicts Productivity_Gain_Percent
    • encoders.pkl    — LabelEncoders for Industry, Company_Size, Primary_AI_Agent_Role

Run:
    python train_models.py
"""

import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# ── 1. Load data ──────────────────────────────────────────────────────────────
CSV_PATH = os.path.join('data', 'Global_AI_Agent_Workforce_Integration_2026.csv')
df = pd.read_csv(CSV_PATH)

print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")

# ── 2. Encode categorical features ───────────────────────────────────────────
encoders = {
    'industry': LabelEncoder(),
    'size':     LabelEncoder(),
    'role':     LabelEncoder(),
}

df['Industry_enc']     = encoders['industry'].fit_transform(df['Industry'])
df['Size_enc']         = encoders['size'].fit_transform(df['Company_Size'])
df['Role_enc']         = encoders['role'].fit_transform(df['Primary_AI_Agent_Role'])
df['Governance_enc']   = df['Has_Strict_AI_Governance'].astype(int)

# ── 3. Define features & targets ─────────────────────────────────────────────
FEATURES = [
    'Industry_enc',
    'Size_enc',
    'Role_enc',
    'Autonomous_Agents_Deployed',
    'Avg_Agent_Cost_Per_Month_USD',
    'Governance_enc',
]

TARGET_ROI  = 'Months_To_Positive_ROI'
TARGET_PROD = 'Productivity_Gain_Percent'

X      = df[FEATURES]
y_roi  = df[TARGET_ROI]
y_prod = df[TARGET_PROD]

# ── 4. Train / test split ─────────────────────────────────────────────────────
X_train, X_test, y_roi_train, y_roi_test = train_test_split(
    X, y_roi, test_size=0.2, random_state=42
)
_, _, y_prod_train, y_prod_test = train_test_split(
    X, y_prod, test_size=0.2, random_state=42
)

# ── 5. Train models ───────────────────────────────────────────────────────────
print("\nTraining ROI model ...")
model_roi = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model_roi.fit(X_train, y_roi_train)

print("Training Productivity model ...")
model_prod = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model_prod.fit(X_train, y_prod_train)

# ── 6. Evaluate ───────────────────────────────────────────────────────────────
def evaluate(model, X_test, y_test, label):
    preds = model.predict(X_test)
    mae   = mean_absolute_error(y_test, preds)
    r2    = r2_score(y_test, preds)
    print(f"\n{label}")
    print(f"  MAE : {mae:.3f}")
    print(f"  R²  : {r2:.3f}")

evaluate(model_roi,  X_test, y_roi_test,  "ROI Model")
evaluate(model_prod, X_test, y_prod_test, "Productivity Model")

# ── 7. Save artefacts ─────────────────────────────────────────────────────────
joblib.dump(model_roi,  'model_roi.pkl')
joblib.dump(model_prod, 'model_prod.pkl')
joblib.dump(encoders,   'encoders.pkl')

print("\n✓ Saved: model_roi.pkl, model_prod.pkl, encoders.pkl")
print("Run `python app.py` to start the Flask server.")
