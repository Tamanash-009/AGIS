"""
AGIS Predictive Maintenance ML Pipeline
────────────────────────────────────────
Trains Random Forest + XGBoost models to predict:
1. Failure probability (0-100%)
2. Days to next failure
3. Recommended maintenance action

Usage:
    python python/ml/predictive_maintenance.py
    python python/ml/predictive_maintenance.py --evaluate
"""
import sys, os
import argparse
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, mean_absolute_error, r2_score)
from sklearn.preprocessing import LabelEncoder
import joblib
import json

from config.settings import RAW_DATA_DIR, PROCESSED_DIR, ML_MODEL_DIR, RANDOM_SEED

try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


def prepare_features(data_dir: str) -> pd.DataFrame:
    """Prepare feature matrix from raw data files."""
    print("  📊 Loading and preparing features...")

    # Load tables
    aircraft = pd.read_csv(os.path.join(data_dir, 'DimAircraft.csv'))
    maintenance = pd.read_csv(os.path.join(data_dir, 'FactMaintenance.csv'))
    failure_types = pd.read_csv(os.path.join(data_dir, 'DimFailureType.csv'))

    # Try loading processed telemetry summary if available, else compute from raw
    telemetry_path = os.path.join(data_dir, 'FactFlightTelemetry.csv')
    if os.path.exists(telemetry_path):
        telemetry = pd.read_csv(telemetry_path)
        # Aggregate telemetry per aircraft
        telem_agg = telemetry.groupby('AircraftID').agg(
            AvgStability=('StabilityScore', 'mean'),
            MaxTemp=('CoreTemp_C', 'max'),
            AvgEnergy=('EnergyConsumed_kW', 'mean'),
            AvgTurbulence=('Turbulence', 'mean'),
            FlightCount=('FlightID', 'nunique'),
            AvgAltitude=('Altitude_m', 'mean'),
            AvgVelocity=('Velocity_mps', 'mean'),
        ).reset_index()
    else:
        telem_agg = pd.DataFrame({'AircraftID': aircraft['AircraftID']})
        telem_agg['AvgStability'] = 75
        telem_agg['MaxTemp'] = 200
        telem_agg['AvgEnergy'] = 100
        telem_agg['AvgTurbulence'] = 0.2
        telem_agg['FlightCount'] = 50
        telem_agg['AvgAltitude'] = 10000
        telem_agg['AvgVelocity'] = 500

    # Aggregate maintenance per aircraft
    maint_agg = maintenance.groupby('AircraftID').agg(
        TotalFailures=('MaintenanceID', 'count'),
        AvgRepairCost=('RepairCost', 'mean'),
        TotalDowntime=('DowntimeHours', 'sum'),
        AvgSeverity=('FailureSeverity', 'mean'),
        MaxSeverity=('FailureSeverity', 'max'),
    ).reset_index()

    # Merge features
    features = aircraft[['AircraftID', 'Model', 'MaxAltitude', 'MaxVelocity',
                          'CoreHealthIndex', 'TotalFlightHours', 'Status']].copy()
    features = features.merge(telem_agg, on='AircraftID', how='left')
    features = features.merge(maint_agg, on='AircraftID', how='left')

    # Fill NaN
    features = features.fillna(0)

    # Create target: failure risk based on health + maintenance history
    # Uses a composite score to ensure class balance even on small datasets
    rng = np.random.default_rng(RANDOM_SEED)
    features['FailureScore'] = (
        (1 - features['CoreHealthIndex']) * 0.35 +
        (features['TotalFailures'] / max(features['TotalFailures'].max(), 1)) * 0.25 +
        (features['AvgSeverity'] / 5.0) * 0.20 +
        (features['TotalFlightHours'] / max(features['TotalFlightHours'].max(), 1)) * 0.20
    )
    # Add noise for realism
    features['FailureScore'] += rng.normal(0, 0.05, len(features))
    features['FailureScore'] = features['FailureScore'].clip(0, 1)
    
    # Threshold at median to ensure ~50/50 class split
    threshold = features['FailureScore'].median()
    features['WillFail'] = (features['FailureScore'] > threshold).astype(int)

    # Days to next failure (regression target) — correlated with failure score
    features['DaysToFailure'] = (
        (1 - features['FailureScore']) * 300 + rng.integers(5, 60, len(features))
    ).astype(int).clip(1, 365)

    print(f"    [OK] Feature matrix: {features.shape}")
    print(f"    [OK] Positive class (WillFail): {features['WillFail'].sum()} / {len(features)}")

    return features


def train_failure_classifier(features: pd.DataFrame, evaluate: bool = False):
    """Train failure prediction classifier (Random Forest + XGBoost ensemble)."""
    print("\n  🤖 Training Failure Prediction Classifier...")

    # Feature columns
    feature_cols = ['MaxAltitude', 'MaxVelocity', 'CoreHealthIndex', 'TotalFlightHours',
                    'AvgStability', 'MaxTemp', 'AvgEnergy', 'AvgTurbulence',
                    'FlightCount', 'AvgAltitude', 'AvgVelocity',
                    'TotalFailures', 'AvgRepairCost', 'TotalDowntime',
                    'AvgSeverity', 'MaxSeverity']

    # Encode model
    le = LabelEncoder()
    features['ModelEncoded'] = le.fit_transform(features['Model'])
    feature_cols.append('ModelEncoded')

    X = features[feature_cols].values
    y = features['WillFail'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_SEED, stratify=y
    )

    # Random Forest
    rf = RandomForestClassifier(
        n_estimators=200, max_depth=10, min_samples_leaf=2,
        random_state=RANDOM_SEED, n_jobs=-1, class_weight='balanced'
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_prob = rf.predict_proba(X_test)[:, 1]

    # Save model
    os.makedirs(str(ML_MODEL_DIR), exist_ok=True)
    joblib.dump(rf, os.path.join(str(ML_MODEL_DIR), 'rf_failure_classifier.joblib'))
    joblib.dump(le, os.path.join(str(ML_MODEL_DIR), 'model_encoder.joblib'))

    print(f"    ✓ Random Forest — AUC: {roc_auc_score(y_test, rf_prob):.4f}")

    # XGBoost (if available)
    if HAS_XGB:
        xgb_clf = xgb.XGBClassifier(
            n_estimators=200, max_depth=6, learning_rate=0.1,
            random_state=RANDOM_SEED, eval_metric='logloss',
            use_label_encoder=False, scale_pos_weight=sum(y == 0) / max(sum(y == 1), 1)
        )
        xgb_clf.fit(X_train, y_train)
        xgb_prob = xgb_clf.predict_proba(X_test)[:, 1]
        joblib.dump(xgb_clf, os.path.join(str(ML_MODEL_DIR), 'xgb_failure_classifier.joblib'))
        print(f"    ✓ XGBoost — AUC: {roc_auc_score(y_test, xgb_prob):.4f}")

        # Ensemble
        ensemble_prob = 0.5 * rf_prob + 0.5 * xgb_prob
        print(f"    ✓ Ensemble — AUC: {roc_auc_score(y_test, ensemble_prob):.4f}")
    else:
        ensemble_prob = rf_prob
        print("    ⚠ XGBoost not available, using Random Forest only")

    # Feature importance
    importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False)
    importance.to_csv(os.path.join(str(ML_MODEL_DIR), 'feature_importance.csv'), index=False)
    print(f"\n    📊 Top 5 Features:")
    for _, row in importance.head(5).iterrows():
        print(f"       {row['Feature']}: {row['Importance']:.4f}")

    if evaluate:
        print(f"\n    📋 Classification Report:")
        print(classification_report(y_test, rf_pred, target_names=['No Failure', 'Will Fail']))

    return rf, feature_cols


def train_rul_regressor(features: pd.DataFrame):
    """Train Remaining Useful Life regressor."""
    print("\n  ⏱️ Training RUL (Remaining Useful Life) Regressor...")

    feature_cols = ['CoreHealthIndex', 'TotalFlightHours', 'AvgStability',
                    'MaxTemp', 'AvgEnergy', 'TotalFailures', 'AvgSeverity',
                    'TotalDowntime', 'AvgTurbulence', 'FlightCount']

    X = features[feature_cols].values
    y = features['DaysToFailure'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=RANDOM_SEED
    )

    reg = GradientBoostingRegressor(
        n_estimators=150, max_depth=5, learning_rate=0.1,
        random_state=RANDOM_SEED
    )
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    joblib.dump(reg, os.path.join(str(ML_MODEL_DIR), 'rul_regressor.joblib'))

    print(f"    ✓ MAE: {mae:.1f} days")
    print(f"    ✓ R²: {r2:.4f}")

    return reg


def generate_predictions(features: pd.DataFrame, rf_model, feature_cols):
    """Generate predictions for all aircraft and save results."""
    print("\n  📈 Generating predictions for all aircraft...")

    # Encode model if needed
    le = joblib.load(os.path.join(str(ML_MODEL_DIR), 'model_encoder.joblib'))
    if 'ModelEncoded' not in features.columns:
        features['ModelEncoded'] = le.transform(features['Model'])

    X = features[feature_cols].values
    probs = rf_model.predict_proba(X)[:, 1]

    # Load RUL model
    rul_model_path = os.path.join(str(ML_MODEL_DIR), 'rul_regressor.joblib')
    if os.path.exists(rul_model_path):
        rul_model = joblib.load(rul_model_path)
        rul_cols = ['CoreHealthIndex', 'TotalFlightHours', 'AvgStability',
                    'MaxTemp', 'AvgEnergy', 'TotalFailures', 'AvgSeverity',
                    'TotalDowntime', 'AvgTurbulence', 'FlightCount']
        rul_preds = rul_model.predict(features[rul_cols].values)
    else:
        rul_preds = np.full(len(features), 180)

    # Build prediction table
    predictions = pd.DataFrame({
        'AircraftID': features['AircraftID'],
        'Model': features['Model'],
        'CoreHealthIndex': features['CoreHealthIndex'],
        'FailureProbability': (probs * 100).round(1),
        'RiskLevel': pd.cut(probs, bins=[0, 0.3, 0.6, 0.8, 1.0],
                            labels=['Low', 'Medium', 'High', 'Critical']),
        'PredictedDaysToFailure': rul_preds.round(0).astype(int),
        'RecommendedAction': pd.cut(probs, bins=[0, 0.3, 0.6, 0.8, 1.0],
                                    labels=['Monitor', 'Schedule Inspection',
                                            'Preventive Maintenance', 'Immediate Grounding']),
        'TotalFlightHours': features['TotalFlightHours'],
        'TotalFailures': features['TotalFailures'],
    })

    predictions = predictions.sort_values('FailureProbability', ascending=False)

    # Save
    pred_path = os.path.join(str(PROCESSED_DIR), 'MLPredictions_Maintenance.csv')
    os.makedirs(str(PROCESSED_DIR), exist_ok=True)
    predictions.to_csv(pred_path, index=False)
    print(f"    ✓ Saved predictions → {pred_path}")

    # Print top 10 highest risk
    print(f"\n    🚨 Top 10 Highest Risk Aircraft:")
    print(predictions.head(10).to_string(index=False))

    # Save model metrics summary
    metrics = {
        'total_aircraft': len(predictions),
        'high_risk_count': int((predictions['FailureProbability'] >= 60).sum()),
        'critical_count': int((predictions['FailureProbability'] >= 80).sum()),
        'avg_failure_probability': float(predictions['FailureProbability'].mean()),
        'avg_days_to_failure': float(predictions['PredictedDaysToFailure'].mean()),
    }
    with open(os.path.join(str(ML_MODEL_DIR), 'model_metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"\n    📊 Risk Summary:")
    print(f"       High Risk: {metrics['high_risk_count']} aircraft")
    print(f"       Critical:  {metrics['critical_count']} aircraft")
    print(f"       Avg Failure Prob: {metrics['avg_failure_probability']:.1f}%")

    return predictions


def main():
    parser = argparse.ArgumentParser(description='AGIS Predictive Maintenance')
    parser.add_argument('--evaluate', action='store_true', help='Print detailed evaluation')
    args = parser.parse_args()

    print("\n🔬 AGIS Predictive Maintenance Pipeline")
    print("=" * 60)

    # Check for data
    data_dir = str(RAW_DATA_DIR)
    if not os.path.exists(os.path.join(data_dir, 'DimAircraft.csv')):
        # Try processed dir
        data_dir = str(PROCESSED_DIR)
        if not os.path.exists(os.path.join(data_dir, 'DimAircraft.csv')):
            print("  ✗ No data found. Run data_generator.py first.")
            return

    features = prepare_features(data_dir)
    rf_model, feature_cols = train_failure_classifier(features, evaluate=args.evaluate)
    train_rul_regressor(features)
    generate_predictions(features, rf_model, feature_cols)

    print("\n" + "=" * 60)
    print("✅ Predictive Maintenance Pipeline Complete!")
    print("=" * 60)


if __name__ == '__main__':
    main()
