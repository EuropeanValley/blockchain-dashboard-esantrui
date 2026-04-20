"""Starter file for module M1."""

from datetime import datetime, timezone

import streamlit as st

from api.blockchain_client import get_block, get_latest_block


def _block_age_minutes(block_time: int) -> float:
    """Return elapsed time since the block timestamp in minutes."""
    now = datetime.now(timezone.utc).timestamp()
    return max(0.0, (now - block_time) / 60.0)


def render() -> None:
    """Render the M1 panel."""
    st.header("M1 - Proof of Work Monitor")
    st.write("Live view of the newest mined block and its proof-of-work fields.")

    if st.button("Fetch latest block", key="m1_fetch"):
        with st.spinner("Fetching data..."):
            try:
                latest = get_latest_block()
                block = get_block(latest["hash"])

                age_minutes = _block_age_minutes(int(block.get("time", 0)))

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Height", block.get("height", "-"))
                col2.metric("Transactions", block.get("n_tx", "-"))
                col3.metric("Nonce", block.get("nonce", "-"))
                col4.metric("Bits", block.get("bits", "-"))

                col5, col6 = st.columns(2)
                col5.metric("Block Age (min)", f"{age_minutes:,.2f}")
                col6.metric("Size (bytes)", block.get("size", "-"))

                st.write(f"**Block hash:** {block.get('hash', '-')}")
                st.write(f"**Previous block:** {block.get('prev_block', '-')}")

                with st.expander("Raw block data"):
                    st.json(block)
            except Exception as exc:
                st.error(f"Error fetching data: {exc}")
    else:
        st.info("Click the button to test the API connection.")
