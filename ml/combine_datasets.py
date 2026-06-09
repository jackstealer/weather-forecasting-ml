"""
Combine multiple weather datasets for improved model training
Handles Kaggle Weather Prediction dataset + existing data
"""
import os
import pandas as pd
import numpy as np
from pathlib import Path
import glob

print("=" * 70)
print("DATASET COMBINATION AND PREPROCESSING")
print("=" * 70)

# Find all CSV files in the project
base_dir = Path(__file__).parent.parent
data_files = []

# Look for existing weather data
existing_data = base_dir / "weather_data_combined.csv"
if existing_data.exists():
    print(f"\n✓ Found existing data: {existing_data}")
    data_files.append(existing_data)

# Look for new Kaggle dataset
kaggle_patterns = [
    "weather_prediction*.csv",
    "weather*.csv",
    "*prediction*.csv"
]

print("\n🔍 Searching for new weather datasets...")
for pattern in kaggle_patterns:
    found = list(base_dir.glob(pattern))
    for f in found:
        if f != existing_data and f.stat().st_size > 1000:  # At least 1KB
            print(f"✓ Found: {f.name} ({f.stat().st_size / 1024 / 1024:.1f} MB)")
            data_files.append(f)

if len(data_files) == 0:
    print("❌ No dataset files found!")
    exit(1)

print(f"\n📊 Total datasets found: {len(data_files)}")

# Load and combine all datasets
combined_data = []
total_rows = 0

for idx, file_path in enumerate(data_files, 1):
    print(f"\n[{idx}/{len(data_files)}] Loading {file_path.name}...")
    try:
        df = pd.read_csv(file_path)
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)[:5]}..." if len(df.columns) > 5 else f"  Columns: {list(df.columns)}")
        
        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Look for essential columns with different possible names
        column_mappings = {
            'temperature': ['temperature', 'temp', 'temperature_c', 'temperature_celsius', 't', 'air_temperature'],
            'humidity': ['humidity', 'relative_humidity', 'rh', 'humidity_%'],
            'pressure': ['pressure', 'sea_level_pressure', 'slp', 'pressure_hpa', 'atmospheric_pressure'],
            'wind_speed': ['wind_speed', 'windspeed', 'wind', 'ws', 'wind_speed_m/s'],
            'wind_direction': ['wind_direction', 'wind_dir', 'wd', 'wind_deg'],
            'latitude': ['latitude', 'lat', 'y'],
            'longitude': ['longitude', 'lon', 'long', 'x'],
            'datetime': ['datetime', 'date', 'time', 'timestamp', 'dt'],
            'city': ['city', 'location', 'station', 'place']
        }
        
        # Rename columns to standard names
        for standard_name, possible_names in column_mappings.items():
            for col in df.columns:
                if col in possible_names:
                    df.rename(columns={col: standard_name}, inplace=True)
                    break
        
        # Keep only relevant columns
        required_cols = ['temperature', 'humidity', 'pressure', 'wind_speed']
        available_cols = [col for col in required_cols if col in df.columns]
        
        if len(available_cols) >= 3:  # At least 3 required columns
            # Select columns to keep
            cols_to_keep = available_cols.copy()
            for optional in ['wind_direction', 'latitude', 'longitude', 'datetime', 'city']:
                if optional in df.columns:
                    cols_to_keep.append(optional)
            
            df = df[cols_to_keep]
            
            # Remove duplicates and nulls
            df = df.drop_duplicates()
            df = df.dropna(subset=available_cols)
            
            print(f"  ✓ Kept {len(df):,} valid rows")
            combined_data.append(df)
            total_rows += len(df)
        else:
            print(f"  ⚠ Skipped: Missing required columns")
            
    except Exception as e:
        print(f"  ❌ Error loading file: {e}")
        continue

if len(combined_data) == 0:
    print("\n❌ No valid data could be loaded!")
    exit(1)

# Combine all dataframes
print(f"\n🔄 Combining {len(combined_data)} datasets...")
final_df = pd.concat(combined_data, ignore_index=True)

# Add missing columns with reasonable defaults
if 'wind_direction' not in final_df.columns:
    final_df['wind_direction'] = 180  # Default direction
if 'latitude' not in final_df.columns:
    final_df['latitude'] = 40.0  # Default coordinates
if 'longitude' not in final_df.columns:
    final_df['longitude'] = -100.0

# Parse datetime if available
if 'datetime' in final_df.columns:
    try:
        final_df['datetime'] = pd.to_datetime(final_df['datetime'], errors='coerce')
        # Extract time features if datetime is valid
        valid_datetime = final_df['datetime'].notna()
        if valid_datetime.sum() > 0:
            print("  ✓ Extracting datetime features...")
    except:
        pass

# If no datetime column, create one
if 'datetime' not in final_df.columns or final_df['datetime'].isna().all():
    print("  ℹ Creating synthetic datetime...")
    final_df['datetime'] = pd.date_range(start='2010-01-01', periods=len(final_df), freq='1H')

# Data quality checks
print("\n🔍 Data Quality Checks...")

# Remove outliers using IQR method
for col in ['temperature', 'humidity', 'pressure', 'wind_speed']:
    if col in final_df.columns:
        Q1 = final_df[col].quantile(0.01)
        Q3 = final_df[col].quantile(0.99)
        IQR = Q3 - Q1
        lower = Q1 - 3 * IQR
        upper = Q3 + 3 * IQR
        before = len(final_df)
        final_df = final_df[(final_df[col] >= lower) & (final_df[col] <= upper)]
        removed = before - len(final_df)
        if removed > 0:
            print(f"  ✓ Removed {removed:,} {col} outliers")

# Final cleanup
final_df = final_df.drop_duplicates()
final_df = final_df.reset_index(drop=True)

# Save combined dataset
output_path = base_dir / "weather_data_combined_enhanced.csv"
print(f"\n💾 Saving combined dataset to: {output_path.name}")
final_df.to_csv(output_path, index=False)

# Print statistics
print("\n" + "=" * 70)
print("COMBINED DATASET SUMMARY")
print("=" * 70)
print(f"Total rows: {len(final_df):,}")
print(f"Total columns: {len(final_df.columns)}")
print(f"Date range: {final_df['datetime'].min()} to {final_df['datetime'].max()}")
print(f"\nColumn Statistics:")
print(final_df.describe())

print("\n" + "=" * 70)
print("✅ DATASET COMBINATION COMPLETE!")
print("=" * 70)
print(f"\n📁 Enhanced dataset saved: {output_path}")
print(f"📊 Ready for training with {len(final_df):,} samples")
