"""Starter file for module M3."""

import pandas as pd
import plotly.express as px
import streamlit as st

from api.blockchain_client import get_difficulty_history


def render() -> None:
    """Render the M3 panel."""
    st.header("M3 - Difficulty History")
    st.write("Plot and analyze Bitcoin mining difficulty over time.")

    n_points = st.slider("Number of data points", min_value=10, max_value=365, value=100, key="m3_n")
    show_ma = st.checkbox("Show moving average (14)", value=True, key="m3_ma")
    log_scale = st.checkbox("Use logarithmic scale", value=False, key="m3_log")

    if st.button("Load difficulty chart", key="m3_load"):
        with st.spinner("Fetching data..."):
            try:
                values = get_difficulty_history(n_points)
                if not values:
                    st.warning("No difficulty data was returned by the API.")
                    return

                df = pd.DataFrame(values)
                df["x"] = pd.to_datetime(df["x"], unit="s")
                df = df.rename(columns={"x": "Date", "y": "Difficulty"})

                if show_ma:
                    df["MA14"] = df["Difficulty"].rolling(14).mean()

                first_value = float(df["Difficulty"].iloc[0])
                last_value = float(df["Difficulty"].iloc[-1])
                pct_change = ((last_value - first_value) / first_value) * 100 if first_value else 0.0

                c1, c2, c3 = st.columns(3)
                c1.metric("Latest", f"{last_value:,.2f}")
                c2.metric("Earliest", f"{first_value:,.2f}")
                c3.metric("Period change", f"{pct_change:,.2f}%")

                fig = px.line(df, x="Date", y="Difficulty", title="Bitcoin Mining Difficulty")
                if show_ma:
                    fig.add_scatter(x=df["Date"], y=df["MA14"], mode="lines", name="MA14")
                if log_scale:
                    fig.update_yaxes(type="log")
                st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.error(f"Error loading chart: {exc}")
    else:
        st.info("Click Load difficulty chart to display the chart.")
