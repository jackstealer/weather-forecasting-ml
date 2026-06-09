"""
Train ML models on weather data - Using Combined Dataset
"""
import os
import json
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
import sklearn
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

from config.config import MODELS_DIR, TRAIN_TEST_SPLIT, RANDOM_STATE
from features import build_features_from_df, FEATURE_COLS

print("=" * 70)
print("WEATHER FORECASTING - MODEL TRAINING")
print("=" * 70)

# Load combined dataset
print("\n📂 Loading weather_data_combined.csv...")
try:
    data = pd.read_csv("weather_data_combined.csv", parse_dates=["datetime"])
    print(f"✅ Loaded: {data.shape}")
    print(f"   Cities: {data['city'].nunique()}")
    print(f"   Date range: {data['datetime'].min()} to {data['datetime'].max()}")
except FileNotFoundError:
    print("❌ weather_data_combined.csv not found!")
    print("\nPlease ensure the combined dataset exists.")
    exit(1)
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit(1)

# Build features
print("\n" + "=" * 70)
print("FEATURE ENGINEERING")
print("=" * 70)

X = build_features_from_df(data)
y = data["temperature"]

print(f"✅ Feature matrix: {X.shape}")
print(f"   Features: {len(FEATURE_COLS)}")

# Temporal train/test split
print("\n" + "=" * 70)
print("TRAIN/TEST SPLIT (Temporal)")
print("=" * 70)

cutoff = int(len(X) * TRAIN_TEST_SPLIT)
X_train, X_test = X.iloc[:cutoff], X.iloc[cutoff:]
y_train, y_test = y.iloc[:cutoff], y.iloc[cutoff:]

print(f"Training set: {len(X_train):,} samples")
print(f"Test set: {len(X_test):,} samples")

# Scale features
print("\n📏 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
print("\n" + "=" * 70)
print("TRAINING MODELS")
print("=" * 70)

models = {}
results = {}

# 1. Linear Regression
print("\n[1/3] Training Linear Regression...")
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
lr_pred = lr.predict(X_test_scaled)

mae = mean_absolute_error(y_test, lr_pred)
rmse = np.sqrt(mean_squared_error(y_test, lr_pred))
r2 = r2_score(y_test, lr_pred)

models["Linear Regression"] = lr
results["Linear Regression"] = {"MAE": mae, "RMSE": rmse, "R2": r2}
print(f"  MAE: {mae:.3f}°C | RMSE: {rmse:.3f}°C | R²: {r2:.4f}")

# 2. Random Forest
print("\n[2/3] Training Random Forest...")
rf = RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    verbose=0
)
rf.fit(X_train_scaled, y_train)
rf_pred = rf.predict(X_test_scaled)

mae = mean_absolute_error(y_test, rf_pred)
rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
r2 = r2_score(y_test, rf_pred)

models["Random Forest"] = rf
results["Random Forest"] = {"MAE": mae, "RMSE": rmse, "R2": r2}
print(f"  MAE: {mae:.3f}°C | RMSE: {rmse:.3f}°C | R²: {r2:.4f}")

# 3. XGBoost
print("\n[3/3] Training XGBoost...")
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=10,
    learning_rate=0.1,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    verbosity=0
)
xgb_model.fit(X_train_scaled, y_train)
xgb_pred = xgb_model.predict(X_test_scaled)

mae = mean_absolute_error(y_test, xgb_pred)
rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
r2 = r2_score(y_test, xgb_pred)

models["XGBoost"] = xgb_model
results["XGBoost"] = {"MAE": mae, "RMSE": rmse, "R2": r2}
print(f"  MAE: {mae:.3f}°C | RMSE: {rmse:.3f}°C | R²: {r2:.4f}")

# Results summary
print("\n" + "=" * 70)
print("RESULTS SUMMARY")
print("=" * 70)

best_model = max(results.items(), key=lambda x: x[1]["R2"])
for name, metrics in results.items():
    marker = " 🏆" if name == best_model[0] else ""
    print(f"{name:<22} MAE: {metrics['MAE']:.3f}°C | RMSE: {metrics['RMSE']:.3f}°C | R²: {metrics['R2']:.4f}{marker}")

# Save models
print("\n" + "=" * 70)
print("SAVING MODELS")
print("=" * 70)

os.makedirs(MODELS_DIR, exist_ok=True)

for name, model in models.items():
    filename = name.lower().replace(' ', '_') + '_model.pkl'
    filepath = os.path.join(MODELS_DIR, filename)
    joblib.dump(model, filepath)
    print(f"✓ Saved {name}")

joblib.dump(scaler, os.path.join(MODELS_DIR, "scaler.pkl"))
joblib.dump(FEATURE_COLS, os.path.join(MODELS_DIR, "feature_names.pkl"))
print(f"✓ Saved scaler and feature names")

# Save metadata
metadata = {
    "trained_at": datetime.now().isoformat(),
    "sklearn_version": sklearn.__version__,
    "xgboost_version": xgb.__version__,
    "num_features": len(FEATURE_COLS),
    "features": FEATURE_COLS,
    "split_type": "temporal",
    "test_split": TRAIN_TEST_SPLIT,
    "random_state": RANDOM_STATE,
    "cities": data['city'].unique().tolist(),
    "num_cities": data['city'].nunique(),
    "results": results,
}

with open(os.path.join(MODELS_DIR, "metadata.json"), 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Saved metadata")

print("\n" + "=" * 70)
print("✅ TRAINING COMPLETE!")
print("=" * 70)
print(f"\n📊 Dataset: weather_data_combined.csv ({len(data):,} rows)")
print(f"📁 Models saved to: {MODELS_DIR}/")
print("\n🚀 Next: streamlit run app.py")
print("=" * 70)
