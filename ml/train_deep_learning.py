"""
Train Deep Learning Model for Weather Forecasting
Uses TensorFlow/Keras Neural Network for improved accuracy
"""
import os
import sys
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import MODELS_DIR, TRAIN_TEST_SPLIT, RANDOM_STATE
from features import build_features_from_df, FEATURE_COLS

# Set random seeds for reproducibility
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

print("=" * 70)
print("DEEP LEARNING MODEL TRAINING")
print("=" * 70)

# Load combined dataset
print("\n📂 Loading weather_data_combined.csv...")
data = pd.read_csv("weather_data_combined.csv", parse_dates=["datetime"])
print(f"✅ Loaded: {data.shape}")

# Build features
print("\n🔧 Building features...")
X = build_features_from_df(data)
y = data["temperature"].values

print(f"✅ Feature matrix: {X.shape}")

# Temporal train/test split
print("\n📊 Train/Test Split...")
cutoff = int(len(X) * TRAIN_TEST_SPLIT)
X_train, X_test = X.iloc[:cutoff].values, X.iloc[cutoff:].values
y_train, y_test = y[:cutoff], y[cutoff:]

print(f"Training set: {len(X_train):,} samples")
print(f"Test set: {len(X_test):,} samples")

# Scale features
print("\n📏 Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create Deep Learning Model
print("\n🧠 Building Neural Network Architecture...")
print("=" * 70)

def create_model(input_dim):
    """Create deep neural network model"""
    model = keras.Sequential([
        # Input layer with batch normalization
        layers.Input(shape=(input_dim,)),
        layers.BatchNormalization(),
        
        # First hidden layer - 256 neurons
        layers.Dense(256, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dropout(0.3),
        layers.BatchNormalization(),
        
        # Second hidden layer - 128 neurons
        layers.Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dropout(0.2),
        layers.BatchNormalization(),
        
        # Third hidden layer - 64 neurons
        layers.Dense(64, activation='relu', kernel_regularizer=keras.regularizers.l2(0.001)),
        layers.Dropout(0.2),
        layers.BatchNormalization(),
        
        # Fourth hidden layer - 32 neurons
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.1),
        
        # Output layer
        layers.Dense(1)
    ])
    
    return model

# Create model
model = create_model(X_train_scaled.shape[1])

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='mse',
    metrics=['mae']
)

# Model summary
print("\nModel Architecture:")
model.summary()

# Callbacks
early_stopping = callbacks.EarlyStopping(
    monitor='val_loss',
    patience=15,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=0.00001,
    verbose=1
)

# Train model
print("\n🚀 Training Deep Learning Model...")
print("=" * 70)

history = model.fit(
    X_train_scaled, y_train,
    validation_split=0.2,
    epochs=100,
    batch_size=512,
    callbacks=[early_stopping, reduce_lr],
    verbose=1
)

# Evaluate on test set
print("\n📈 Evaluating on test set...")
y_pred = model.predict(X_test_scaled, verbose=0).flatten()

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n" + "=" * 70)
print("DEEP LEARNING MODEL RESULTS")
print("=" * 70)
print(f"MAE:  {mae:.3f}°C")
print(f"RMSE: {rmse:.3f}°C")
print(f"R²:   {r2:.4f}")
print(f"Accuracy: {r2*100:.2f}%")
print("=" * 70)

# Save model
print("\n💾 Saving Deep Learning Model...")
model_path = os.path.join(MODELS_DIR, "deep_learning_model.h5")
model.save(model_path)
print(f"✓ Saved model to: {model_path}")

# Save scaler (reuse existing one or save new)
scaler_path = os.path.join(MODELS_DIR, "dl_scaler.pkl")
joblib.dump(scaler, scaler_path)
print(f"✓ Saved scaler to: {scaler_path}")

# Save metadata
metadata = {
    "model_type": "Deep Neural Network",
    "framework": "TensorFlow/Keras",
    "architecture": {
        "layers": [256, 128, 64, 32],
        "activation": "relu",
        "dropout": [0.3, 0.2, 0.2, 0.1],
        "regularization": "L2 (0.001)"
    },
    "training": {
        "epochs_trained": len(history.history['loss']),
        "batch_size": 512,
        "optimizer": "Adam",
        "learning_rate": 0.001
    },
    "performance": {
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
        "accuracy_percent": float(r2 * 100)
    },
    "num_features": X_train_scaled.shape[1],
    "features": FEATURE_COLS,
    "training_samples": len(X_train),
    "test_samples": len(X_test)
}

metadata_path = os.path.join(MODELS_DIR, "dl_metadata.json")
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Saved metadata to: {metadata_path}")

print("\n" + "=" * 70)
print("✅ DEEP LEARNING MODEL TRAINING COMPLETE!")
print("=" * 70)
print(f"\n🎯 Final Performance:")
print(f"   MAE: {mae:.3f}°C (Mean Absolute Error)")
print(f"   R²: {r2:.4f} ({r2*100:.2f}% accuracy)")
print(f"\n📊 Comparison with XGBoost:")
print(f"   XGBoost MAE: 2.819°C")
print(f"   Deep Learning MAE: {mae:.3f}°C")
print(f"   Improvement: {((2.819 - mae) / 2.819 * 100):.1f}%")
print("\n" + "=" * 70)
