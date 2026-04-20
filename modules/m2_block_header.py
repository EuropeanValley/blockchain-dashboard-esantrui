"""Starter file for module M2."""

from datetime import datetime, timezone

import streamlit as st

from api.blockchain_client import get_block, get_latest_block


def _to_utc(unix_ts: int) -> str:
    """Format UNIX timestamp as UTC datetime string."""
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def render() -> None:
    """Render the M2 panel."""
    st.header("M2 - Block Header Analyzer")
    st.write("Inspect one Bitcoin block header and summarize its key fields.")

    if st.button("Use latest block hash", key="m2_latest"):
        try:
            latest = get_latest_block()
            st.session_state["m2_hash"] = latest.get("hash", "")
        except Exception as exc:
            st.error(f"Could not fetch latest block hash: {exc}")

    block_hash = st.text_input(
        "Block hash",
        placeholder="Enter a block hash",
        key="m2_hash",
    )
    block_hash = block_hash.strip()

    if st.button("Look up block", key="m2_lookup") and block_hash:
        with st.spinner("Fetching data..."):
            try:
                block = get_block(block_hash)
                st.subheader("Block header fields")

                cols = st.columns(4)
                cols[0].metric("Height", block.get("height", "-"))
                cols[1].metric("Nonce", block.get("nonce", "-"))
                cols[2].metric("Bits", block.get("bits", "-"))
                cols[3].metric("Transactions", block.get("n_tx", "-"))

                st.write(f"**Hash:** {block.get('hash', '-')}")
                st.write(f"**Previous block:** {block.get('prev_block', '-')}")
                st.write(f"**Merkle root:** {block.get('mrkl_root', '-')}")
                st.write(f"**Time (raw):** {block.get('time', '-')}")

                if block.get("time") is not None:
                    st.write(f"**Time (UTC):** {_to_utc(int(block['time']))}")

                with st.expander("Raw block data"):
                    st.json(block)
            except Exception as exc:
                st.error(f"Error fetching block: {exc}")
    elif not block_hash:
        st.info("Enter a block hash and click Look up block.")
