"""
features.py — Single source of truth for feature engineering.

Both training (train_complete.py) and inference (predict_weather.py, app_clean.py,
realtime_weather_api.py) must import and call build_features() from here.
This eliminates the critical feature-mismatch bug where training and inference
were computing completely different columns.
"""

import numpy as np
import pandas as pd

# ── Canonical ordered feature list ──────────────────────────────────────────
# This list is saved alongside the model (feature_names.pkl) and must never
# be changed without retraining.
FEATURE_COLS = [
    "humidity",
    "pressure",
    "wind_speed",
    "wind_direction",
    "latitude",
    "longitude",
    "hour",
    "month",
    "day_of_year",
    "day_of_week",
    "month_sin",
    "month_cos",
    "hour_sin",
    "hour_cos",
    "day_sin",
    "day_cos",
    "day_of_week_sin",
    "day_of_week_cos",
    "humidity_pressure",
    "wind_speed_squared",
    "dewpoint_approx",
]


def build_features(
    humidity: float,
    pressure: float,
    wind_speed: float,
    wind_direction: float,
    latitude: float,
    longitude: float,
    hour: int,
    month: int,
    day_of_year: int,
    day_of_week: int,
) -> pd.DataFrame:
    """
    Build the canonical feature DataFrame for a single observation.

    Returns a one-row DataFrame with columns in FEATURE_COLS order, ready to
    be passed directly to scaler.transform() and then model.predict().

    Parameters
    ----------
    humidity      : 0–100 %
    pressure      : hPa (typically 950–1050)
    wind_speed    : m/s (0–50)
    wind_direction: degrees (0–360)
    latitude      : decimal degrees
    longitude     : decimal degrees
    hour          : 0–23
    month         : 1–12
    day_of_year   : 1–365
    day_of_week   : 0 (Mon) – 6 (Sun)
    """
    # ── Cyclical encodings ────────────────────────────────────────────────
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)
    hour_sin  = np.sin(2 * np.pi * hour / 24)
    hour_cos  = np.cos(2 * np.pi * hour / 24)
    # Wrap day_of_year so values beyond 365 (e.g. during multi-day forecast)
    # stay within [0, 2π) instead of drifting out of the trained range.
    doy_wrapped = ((day_of_year - 1) % 365) + 1
    day_sin = np.sin(2 * np.pi * doy_wrapped / 365)
    day_cos = np.cos(2 * np.pi * doy_wrapped / 365)
    dow_sin = np.sin(2 * np.pi * day_of_week / 7)
    dow_cos = np.cos(2 * np.pi * day_of_week / 7)

    # ── Interaction / derived features ───────────────────────────────────
    humidity_pressure = humidity * pressure / 1000   # scale to ~65
    wind_speed_squared = wind_speed ** 2
    # Magnus-formula approximation for dew point (°C) — useful signal for
    # temperature without requiring current_temp as input (avoids leakage).
    # Valid for humidity > 0.
    h = max(humidity, 1e-6)
    dewpoint_approx = (243.04 * (np.log(h / 100) + 17.625 * 20 / (243.04 + 20))) / \
                      (17.625 - (np.log(h / 100) + 17.625 * 20 / (243.04 + 20)))

    row = {
        "humidity":          humidity,
        "pressure":          pressure,
        "wind_speed":        wind_speed,
        "wind_direction":    wind_direction,
        "latitude":          latitude,
        "longitude":         longitude,
        "hour":              hour,
        "month":             month,
        "day_of_year":       doy_wrapped,
        "day_of_week":       day_of_week,
        "month_sin":         month_sin,
        "month_cos":         month_cos,
        "hour_sin":          hour_sin,
        "hour_cos":          hour_cos,
        "day_sin":           day_sin,
        "day_cos":           day_cos,
        "day_of_week_sin":   dow_sin,
        "day_of_week_cos":   dow_cos,
        "humidity_pressure": humidity_pressure,
        "wind_speed_squared": wind_speed_squared,
        "dewpoint_approx":   dewpoint_approx,
    }

    # Return columns in the exact canonical order
    return pd.DataFrame([row])[FEATURE_COLS]


def build_features_from_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vectorised version of build_features for use during training.

    Expects df to already have columns:
        humidity, pressure, wind_speed, wind_direction,
        latitude, longitude, hour, month, day_of_year, day_of_week

    Returns a DataFrame with exactly the FEATURE_COLS columns.
    """
    out = df.copy()

    # Cyclical encodings
    out["month_sin"] = np.sin(2 * np.pi * out["month"] / 12)
    out["month_cos"] = np.cos(2 * np.pi * out["month"] / 12)
    out["hour_sin"]  = np.sin(2 * np.pi * out["hour"] / 24)
    out["hour_cos"]  = np.cos(2 * np.pi * out["hour"] / 24)
    doy = ((out["day_of_year"] - 1) % 365) + 1
    out["day_sin"] = np.sin(2 * np.pi * doy / 365)
    out["day_cos"] = np.cos(2 * np.pi * doy / 365)
    out["day_of_year"] = doy  # store wrapped version
    out["day_of_week_sin"] = np.sin(2 * np.pi * out["day_of_week"] / 7)
    out["day_of_week_cos"] = np.cos(2 * np.pi * out["day_of_week"] / 7)

    # Interaction / derived
    out["humidity_pressure"]  = out["humidity"] * out["pressure"] / 1000
    out["wind_speed_squared"] = out["wind_speed"] ** 2
    h = out["humidity"].clip(lower=1e-6)
    out["dewpoint_approx"] = (
        243.04 * (np.log(h / 100) + 17.625 * 20 / (243.04 + 20))
    ) / (
        17.625 - (np.log(h / 100) + 17.625 * 20 / (243.04 + 20))
    )

    return out[FEATURE_COLS]


def validate_inputs(
    humidity: float,
    pressure: float,
    wind_speed: float,
    wind_direction: float,
    latitude: float,
    longitude: float,
) -> list[str]:
    """
    Return a list of validation error strings (empty list = all OK).
    Call this before build_features() in any user-facing code path.
    """
    errors = []
    if not (0 <= humidity <= 100):
        errors.append(f"Humidity must be 0–100 %, got {humidity}")
    if not (900 <= pressure <= 1100):
        errors.append(f"Pressure must be 900–1100 hPa, got {pressure}")
    if not (0 <= wind_speed <= 50):
        errors.append(f"Wind speed must be 0–50 m/s, got {wind_speed}")
    if not (0 <= wind_direction <= 360):
        errors.append(f"Wind direction must be 0–360°, got {wind_direction}")
    if not (-90 <= latitude <= 90):
        errors.append(f"Latitude must be -90–90, got {latitude}")
    if not (-180 <= longitude <= 180):
        errors.append(f"Longitude must be -180–180, got {longitude}")
    return errors
