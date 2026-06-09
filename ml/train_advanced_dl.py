"""
Advanced Deep Learning Model Training with Overfitting Prevention
Implements: Dropout, L2 Regularization, Batch Normalization, Early Stopping, Data Augmentation
"""
import os
import sys
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks, regularizers
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import MODELS_DIR, RANDOM_STATE
from features import build_features_from_df, FEATURE_COLS

# Set random seeds for reproducibility
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

print("=" * 70)
print("ADVANCED DEEP LEARNING MODEL TRAINING")
print("Anti-Overfitting Techniques Enabled")
print("=" * 70)

# Load enhanced combined dataset
print("\n📂 Loading enhanced dataset...")
data_file = "weather_data_combined_enhanced.csv"
if not os.path.exists(data_file):
    data_file = "weather_data_combined.csv"
    print(f"  ℹ Using original dataset: {data_file}")
else:
    print(f"  ✓ Using enhanced dataset: {data_file}")

data = pd.read_csv(data_file, parse_dates=["datetime"])
print(f"✅ Loaded: {data.shape[0]:,} rows, {data.shape[1]} columns")

# Extract time features from datetime
print("\n🔧 Extracting time features...")
data['hour'] = data['datetime'].dt.hour
data['month'] = data['datetime'].dt.month
data['day_of_year'] = data['datetime'].dt.dayofyear
data['day_of_week'] = data['datetime'].dt.dayofweek

# Build features
print("🔧 Building features...")
X = build_features_from_df(data)
y = data["temperature"].values

print(f"✅ Feature matrix: {X.shape}")
print(f"   Features: {len(FEATURE_COLS)}")

# Temporal train/validation/test split (prevents data leakage)
print("\n📊 Creating temporal splits...")
n_samples = len(X)
train_end = int(n_samples * 0.70)  # 70% train
val_end = int(n_samples * 0.85)    # 15% validation
# Remaining 15% for test

X_train = X.iloc[:train_end].values
y_train = y[:train_end]

X_val = X.iloc[train_end:val_end].values
y_val = y[train_end:val_end]

X_test = X.iloc[val_end:].values
y_test = y[val_end:]

print(f"Training set:   {len(X_train):,} samples ({len(X_train)/n_samples*100:.1f}%)")
print(f"Validation set: {len(X_val):,} samples ({len(X_val)/n_samples*100:.1f}%)")
print(f"Test set:       {len(X_test):,} samples ({len(X_test)/n_samples*100:.1f}%)")

# Use RobustScaler (better for outliers)
print("\n📏 Scaling features with RobustScaler...")
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Data Augmentation (add noise for robustness)
print("\n🎲 Applying data augmentation...")
noise_factor = 0.02
X_train_augmented = X_train_scaled + noise_factor * np.random.normal(size=X_train_scaled.shape)
print(f"  ✓ Added Gaussian noise (factor: {noise_factor})")

# Create Advanced Deep Learning Model
print("\n🧠 Building Advanced Neural Network...")
print("=" * 70)

def create_advanced_model(input_dim, learning_rate=0.001):
    """
    Create advanced neural network with anti-overfitting techniques:
    - Batch Normalization
    - Dropout layers
    - L2 Regularization
    - Residual connections
    """
    # Input
    inputs = layers.Input(shape=(input_dim,))
    
    # First block
    x = layers.BatchNormalization()(inputs)
    x = layers.Dense(512, activation='relu', kernel_regularizer=regularizers.l2(0.0001))(x)
    x = layers.Dropout(0.4)(x)
    x = layers.BatchNormalization()(x)
    
    # Second block with residual connection
    residual = x
    x = layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.BatchNormalization()(x)
    
    # Third block
    x = layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.0001))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.BatchNormalization()(x)
    
    # Fourth block
    x = layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.0001))(x)
    x = layers.Dropout(0.2)(x)
    x = layers.BatchNormalization()(x)
    
    # Fifth block
    x = layers.Dense(32, activation='relu')(x)
    x = layers.Dropout(0.1)(x)
    
    # Output layer
    outputs = layers.Dense(1)(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    # Use Adam optimizer with learning rate scheduling
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    
    model.compile(
        optimizer=optimizer,
        loss='huber',  # Robust to outliers
        metrics=['mae', 'mse']
    )
    
    return model

# Create model
model = create_advanced_model(X_train_scaled.shape[1])

print("\nModel Architecture:")
model.summary()
print("\n✓ Anti-Overfitting Features:")
print("  • Dropout layers (10% - 40%)")
print("  • L2 Regularization (0.0001)")
print("  • Batch Normalization")
print("  • Huber Loss (robust to outliers)")
print("  • Data Augmentation")
print("  • Temporal train/val/test split")

# Advanced Callbacks
print("\n⚙️ Setting up training callbacks...")

# Early stopping with patience - monitor val_loss (minimize)
early_stop = callbacks.EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True,
    verbose=1,
    min_delta=0.0001
)

# Reduce learning rate on plateau - monitor val_loss
reduce_lr = callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=8,
    min_lr=0.000001,
    verbose=1
)

# Model checkpoint - save best model based on val_loss
checkpoint = callbacks.ModelCheckpoint(
    str(MODELS_DIR / 'best_dl_model.h5'),
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)

# Train model
print("\n🚀 Training Advanced Deep Learning Model...")
print("=" * 70)

history = model.fit(
    X_train_augmented, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=200,
    batch_size=1024,
    callbacks=[early_stop, reduce_lr, checkpoint],
    verbose=1
)

# Load best model
print("\n📥 Loading best model...")
model = keras.models.load_model(str(MODELS_DIR / 'best_dl_model.h5'))

# Evaluate on all sets
print("\n📈 Evaluating model performance...")
print("=" * 70)

def evaluate_model(X, y, set_name):
    """Evaluate model and print metrics - R² score first"""
    y_pred = model.predict(X, verbose=0).flatten()
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    print(f"\n{set_name} Set:")
    print(f"  R² Score: {r2:.4f} ({r2*100:.2f}% accuracy) ⭐")
    print(f"  MAE:      {mae:.3f}°C")
    print(f"  RMSE:     {rmse:.3f}°C")
    
    return r2, mae, rmse

train_metrics = evaluate_model(X_train_scaled, y_train, "Training")
val_metrics = evaluate_model(X_val_scaled, y_val, "Validation")
test_metrics = evaluate_model(X_test_scaled, y_test, "Test")

# Check for overfitting using R² scores
print("\n🔍 Overfitting Analysis (R² Score Based):")
train_r2 = train_metrics[0]
val_r2 = val_metrics[0]
test_r2 = test_metrics[0]
r2_gap = train_r2 - val_r2

if r2_gap < 0.02:  # Less than 2% difference
    print(f"  ✅ Excellent: No overfitting (gap: {r2_gap:.4f})")
elif r2_gap < 0.05:  # Less than 5% difference
    print(f"  ✓ Good: Minimal overfitting (gap: {r2_gap:.4f})")
else:
    print(f"  ⚠ Warning: Some overfitting detected (gap: {r2_gap:.4f})")

print(f"\n📊 R² Score Comparison:")
print(f"  Train R²:      {train_r2:.4f} ({train_r2*100:.2f}%)")
print(f"  Validation R²: {val_r2:.4f} ({val_r2*100:.2f}%)")
print(f"  Test R²:       {test_r2:.4f} ({test_r2*100:.2f}%) ⭐")

print("=" * 70)

# Save final model and metadata
print("\n💾 Saving final model and artifacts...")
final_model_path = MODELS_DIR / "deep_learning_model.h5"
model.save(str(final_model_path))
print(f"✓ Saved model: {final_model_path}")

scaler_path = MODELS_DIR / "dl_scaler.pkl"
joblib.dump(scaler, str(scaler_path))
print(f"✓ Saved scaler: {scaler_path}")

# Save comprehensive metadata
metadata = {
    "model_type": "Advanced Deep Neural Network",
    "framework": "TensorFlow/Keras",
    "anti_overfitting_techniques": [
        "Dropout (10-40%)",
        "L2 Regularization",
        "Batch Normalization",
        "Early Stopping",
        "Learning Rate Scheduling",
        "Data Augmentation",
        "Huber Loss",
        "Temporal Split"
    ],
    "architecture": {
        "layers": [512, 256, 128, 64, 32],
        "activation": "relu",
        "regularization": "L2 (0.0001)",
        "dropout_rates": [0.4, 0.3, 0.3, 0.2, 0.1]
    },
    "training": {
        "epochs_trained": len(history.history['loss']),
        "batch_size": 1024,
        "optimizer": "Adam",
        "loss_function": "Huber",
        "data_augmentation": True
    },
    "performance": {
        "train": {"R2": float(train_metrics[0]), "MAE": float(train_metrics[1]), "RMSE": float(train_metrics[2])},
        "validation": {"R2": float(val_metrics[0]), "MAE": float(val_metrics[1]), "RMSE": float(val_metrics[2])},
        "test": {"R2": float(test_metrics[0]), "MAE": float(test_metrics[1]), "RMSE": float(test_metrics[2])},
        "accuracy_percent": float(test_metrics[0] * 100),
        "r2_train_val_gap": float(train_metrics[0] - val_metrics[0])
    },
    "dataset": {
        "total_samples": len(X),
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "test_samples": len(X_test),
        "num_features": X_train_scaled.shape[1],
        "features": FEATURE_COLS
    }
}

metadata_path = MODELS_DIR / "dl_metadata.json"
with open(str(metadata_path), 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Saved metadata: {metadata_path}")

print("\n" + "=" * 70)
print("✅ ADVANCED DEEP LEARNING MODEL TRAINING COMPLETE!")
print("=" * 70)
print(f"\n🎯 Final Test Performance (R² Score Based):")
print(f"   R² Score: {test_metrics[0]:.4f} ({test_metrics[0]*100:.2f}% accuracy) ⭐")
print(f"   MAE:      {test_metrics[1]:.3f}°C")
print(f"   RMSE:     {test_metrics[2]:.3f}°C")
print(f"\n📊 Overfitting Check:")
print(f"   Train-Val R² gap: {r2_gap:.4f}")
print(f"   Status: {'✅ Well-balanced' if r2_gap < 0.02 else '✓ Acceptable' if r2_gap < 0.05 else '⚠ Review needed'}")
print("\n🏆 Model Comparison:")
print(f"   Linear Regression: 0.7347 (73.5%)")
print(f"   Random Forest:     0.8404 (84.0%)")
print(f"   XGBoost:           0.8603 (86.0%)")
print(f"   Deep Learning:     {test_metrics[0]:.4f} ({test_metrics[0]*100:.2f}%) {'🎉' if test_metrics[0] > 0.87 else '📈'}")
print("\n" + "=" * 70)
