"""Starter file for module M4."""

import math

import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX

from api.blockchain_client import get_difficulty_history


def _fit_and_forecast(train: pd.Series, horizon: int, model_name: str) -> tuple[list[float], str]:
    """Fit selected time-series model and return forecast values and model label."""
    if model_name == "ARIMA":
        model = ARIMA(train, order=(1, 2, 1))
        fitted = model.fit()
        yhat = fitted.forecast(steps=horizon)
        return [max(0.0, float(v)) for v in yhat], "ARIMA(1,2,1)"

    if model_name == "SARIMA":
        try:
            model = SARIMAX(
                train,
                order=(0, 2, 1),
                seasonal_order=(0, 1, 1, 7),
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            fitted = model.fit(disp=False)
            yhat = fitted.forecast(steps=horizon)
            return [max(0.0, float(v)) for v in yhat], "SARIMA(0,2,1)x(0,1,1,7)"
        except Exception:
            model = SARIMAX(
                train,
                order=(1, 1, 1),
                seasonal_order=(0, 1, 1, 7),
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            fitted = model.fit(disp=False)
            yhat = fitted.forecast(steps=horizon)
            return [max(0.0, float(v)) for v in yhat], "SARIMA(1,1,1)x(0,1,1,7) [stable]"

    model = ExponentialSmoothing(
        train,
        trend="add",
        seasonal="add",
        seasonal_periods=7,
        initialization_method="estimated",
    )
    fitted = model.fit(optimized=True)
    yhat = fitted.forecast(horizon)
    return [max(0.0, float(v)) for v in yhat], "Holt-Winters(add,add,7)"


def _mae(y_true: pd.Series, y_pred: list[float]) -> float:
    errors = [abs(float(a) - float(b)) for a, b in zip(y_true.tolist(), y_pred)]
    return sum(errors) / len(errors) if errors else 0.0


def _rmse(y_true: pd.Series, y_pred: list[float]) -> float:
    sq_errors = [(float(a) - float(b)) ** 2 for a, b in zip(y_true.tolist(), y_pred)]
    if not sq_errors:
        return 0.0
    return math.sqrt(sum(sq_errors) / len(sq_errors))


def _detect_anomalies_zscore(series: pd.Series, threshold: float = 2.0) -> pd.Series:
    """Return a mask of anomaly points based on absolute z-score."""
    mean = series.mean()
    std = series.std(ddof=0)
    if std == 0:
        return pd.Series([False] * len(series), index=series.index)
    zscores = (series - mean) / std
    return zscores.abs() >= threshold


def render() -> None:
    """Render the M4 panel."""
    st.header("M4 - AI Component")
    st.write("Forecasting with ARIMA, SARIMA, or Holt-Winters plus anomaly detection.")

    history_points = st.slider("Training points", min_value=30, max_value=365, value=180, key="m4_hist")
    forecast_horizon = st.slider("Forecast horizon (days)", min_value=7, max_value=60, value=30, key="m4_horizon")
    model_choice = st.selectbox(
        "Forecasting model",
        ["ARIMA", "SARIMA", "Holt-Winters"],
        index=1,
        key="m4_model",
    )

    if st.button("Run AI analysis", key="m4_run"):
        with st.spinner("Running model..."):
            try:
                values = get_difficulty_history(history_points)
                if not values:
                    st.warning("No difficulty data was returned by the API.")
                    return

                df = pd.DataFrame(values)
                df["x"] = pd.to_datetime(df["x"], unit="s")
                df = df.rename(columns={"x": "Date", "y": "Difficulty"})

                holdout_size = max(7, min(30, len(df) // 5))
                if len(df) <= holdout_size + 14:
                    st.warning("Not enough points for robust holdout evaluation. Increase training points.")
                    return

                train_series = df["Difficulty"].iloc[:-holdout_size]
                holdout_series = df["Difficulty"].iloc[-holdout_size:]

                holdout_pred, model_label = _fit_and_forecast(train_series, holdout_size, model_choice)
                holdout_mae = _mae(holdout_series, holdout_pred)
                holdout_rmse = _rmse(holdout_series, holdout_pred)

                full_series = df["Difficulty"]
                forecast, model_label = _fit_and_forecast(full_series, forecast_horizon, model_choice)
                last_date = df["Date"].iloc[-1]
                future_dates = pd.date_range(
                    last_date + pd.Timedelta(days=1),
                    periods=forecast_horizon,
                    freq="D",
                )

                history_df = df[["Date", "Difficulty"]].copy()
                history_df["Type"] = "History"
                forecast_df = pd.DataFrame(
                    {"Date": future_dates, "Difficulty": forecast, "Type": "Forecast"}
                )
                merged_df = pd.concat([history_df, forecast_df], ignore_index=True)

                fig = px.line(
                    merged_df,
                    x="Date",
                    y="Difficulty",
                    color="Type",
                    title="Difficulty: history vs forecast",
                )
                st.plotly_chart(fig, use_container_width=True)

                anomalies = _detect_anomalies_zscore(df["Difficulty"], threshold=2.0)
                anomaly_df = df.loc[anomalies, ["Date", "Difficulty"]]

                c1, c2, c3 = st.columns(3)
                c1.metric("Latest value", f"{float(df['Difficulty'].iloc[-1]):,.2f}")
                c2.metric("Forecast end", f"{float(forecast[-1]):,.2f}")
                c3.metric("Anomalies", int(anomaly_df.shape[0]))

                c4, c5 = st.columns(2)
                c4.metric("Holdout MAE", f"{holdout_mae:,.2f}")
                c5.metric("Holdout RMSE", f"{holdout_rmse:,.2f}")

                if anomaly_df.empty:
                    st.success("No strong anomalies detected in the selected period.")
                else:
                    st.warning("Anomalies detected (z-score >= 2).")
                    st.dataframe(anomaly_df, use_container_width=True, hide_index=True)

                st.caption(f"Model used: {model_label}")
            except Exception as exc:
                st.error(f"Error in AI component: {exc}")
    else:
        st.info("Select parameters and click Run AI analysis.")
