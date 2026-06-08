import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from attacks import apply_scenario
from detection import calculate_consensus_position, detect_anomalies
from fusion import fuse_positions
from sources import create_navigation_sources


def build_reading() -> dict:
    """
    Create a reading dictionary from all navigation sources.
    This converts your NavigationSource objects into dictionaries.
    """
    sources = create_navigation_sources()
    readings = [source.generate_reading() for source in sources]

    return {"sources": readings}


def prepare_dataframe(reading: dict, trusted: list, flagged: list) -> pd.DataFrame:
    """
    Convert source readings into a DataFrame for Streamlit tables.
    """
    trusted_ids = {source["source_id"] for source in trusted}
    flagged_ids = {source["source_id"] for source in flagged}

    rows = []

    for source in reading["sources"]:
        x, y = source["position"]

        if source["source_id"] in trusted_ids:
            decision = "trusted"
        elif source["source_id"] in flagged_ids:
            decision = "flagged"
        else:
            decision = "unknown"

        rows.append(
            {
                "source_id": source["source_id"],
                "x_position": x,
                "y_position": y,
                "signal_strength": round(source["signal_strength"], 2),
                "confidence": round(source["confidence"], 2),
                "source_status": source.get("status", "normal"),
                "decision": decision,
            }
        )

    return pd.DataFrame(rows)


def plot_navigation_sources(
    reading: dict,
    trusted: list,
    flagged: list,
    consensus_position: tuple,
    fused_result: dict,
):
    """
    Plot trusted sources, flagged sources, consensus position and fused position.
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    trusted_ids = {source["source_id"] for source in trusted}
    flagged_ids = {source["source_id"] for source in flagged}

    for source in reading["sources"]:
        x, y = source["position"]

        if source["source_id"] in trusted_ids:
            ax.scatter(x, y, marker="o", s=100, label="Trusted source")
        elif source["source_id"] in flagged_ids:
            ax.scatter(x, y, marker="x", s=120, label="Flagged source")
        else:
            ax.scatter(x, y, marker=".", s=80, label="Unknown source")

        ax.annotate(
            source["source_id"],
            (x, y),
            textcoords="offset points",
            xytext=(5, 5),
            ha="left",
        )

    consensus_x, consensus_y = consensus_position
    ax.scatter(consensus_x, consensus_y, marker="D", s=140, label="Consensus position")
    ax.annotate(
        "Consensus",
        (consensus_x, consensus_y),
        textcoords="offset points",
        xytext=(5, 5),
        ha="left",
    )

    fused_x, fused_y = fused_result["position"]
    ax.scatter(fused_x, fused_y, marker="*", s=220, label="Fused position")
    ax.annotate(
        "Fused",
        (fused_x, fused_y),
        textcoords="offset points",
        xytext=(5, 5),
        ha="left",
    )

    ax.set_title("Mini Resilient PNT Source Visualisation")
    ax.set_xlabel("Latitude / X position")
    ax.set_ylabel("Longitude / Y position")
    ax.grid(True)

    # Remove duplicate legend labels
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    ax.legend(unique.values(), unique.keys())

    return fig


def render_status(fused_result: dict, trusted: list, flagged: list):
    """
    Display a simple operational status.
    """
    status = fused_result["status"]

    if status == "normal":
        st.success("GREEN: Reliable fix available")
    elif status == "degraded":
        st.warning("AMBER: Degraded fix — limited trusted sources")
    else:
        st.error("RED: Unavailable — system should refuse certainty")

    st.write(f"Trusted sources: **{len(trusted)}**")
    st.write(f"Flagged sources: **{len(flagged)}**")
    st.write(f"Fused confidence: **{round(fused_result['confidence'], 2)}**")


def run_visualisation_app():
    """
    Main Streamlit visualisation function.
    """
    st.set_page_config(page_title="Mini Resilient PNT Simulation", layout="wide")

    st.title("Mini Resilient PNT Simulation")
    st.write(
        "A small-scale simulation of resilient navigation source fusion, "
        "showing how the system reacts to clean, noisy, spoofed, jammed and degraded inputs."
    )

    scenario = st.sidebar.selectbox(
        "Choose attack scenario", ["clean", "noise", "spoofing", "jamming", "degraded"]
    )

    reading = build_reading()
    reading = apply_scenario(reading, scenario)

    consensus_position = calculate_consensus_position(reading)
    flagged, trusted = detect_anomalies(reading, consensus_position)
    fused_result = fuse_positions(trusted)

    left_col, right_col = st.columns([2, 1])

    with left_col:
        fig = plot_navigation_sources(
            reading=reading,
            trusted=trusted,
            flagged=flagged,
            consensus_position=consensus_position,
            fused_result=fused_result,
        )
        st.pyplot(fig)

    with right_col:
        st.subheader("System status")
        render_status(fused_result, trusted, flagged)

        st.subheader("Fused estimate")
        st.json(fused_result)

    st.subheader("Source readings")
    df = prepare_dataframe(reading, trusted, flagged)
    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    run_visualisation_app()
