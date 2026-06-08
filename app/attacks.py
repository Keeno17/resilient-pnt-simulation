"""
Simulated attack functions for testing the Mini Resilient PNT Simulation.

These are not real RF attacks. They only modify simulated source readings.
"""

NOISE_POSITION_OFFSET = 6.0
NOISE_SIGNAL_STRENGTH_DROP = 35
NOISE_CONFIDENCE_DROP = 0.40

JAMMED_SIGNAL_STRENGTH = 1
JAMMED_CONFIDENCE = 0.01

SPOOFED_SIGNAL_STRENGTH = 85
SPOOFED_CONFIDENCE = 0.95


def apply_noise_attack(
    reading: dict,
    target_source_id: str,
    position_offset: float = NOISE_POSITION_OFFSET,
    signal_drop: float = NOISE_SIGNAL_STRENGTH_DROP,
    confidence_drop: float = NOISE_CONFIDENCE_DROP,
) -> dict:
    """Apply a noise attack to a specific source in the reading."""

    for source in reading["sources"]:
        if source["source_id"] == target_source_id:
            x, y = source["position"]

            source["position"] = (x + position_offset, y - position_offset)

            source["signal_strength"] = max(0, source["signal_strength"] - signal_drop)
            source["confidence"] = max(0, source["confidence"] - confidence_drop)

            source["status"] = "noisy"

    return reading


def apply_spoofing_attack(
    reading: dict,
    target_source_id: str,
    spoofed_position: tuple = (250.0, 300.0),
) -> dict:
    """Apply a spoofing attack to a specific source in the reading."""

    for source in reading["sources"]:
        if source["source_id"] == target_source_id:
            # Spoof the position
            source["position"] = spoofed_position

            # Keep confidence high
            source["confidence"] = SPOOFED_CONFIDENCE

            # Keep signal strength high
            source["signal_strength"] = SPOOFED_SIGNAL_STRENGTH

            source["status"] = "spoofed"
    return reading


def apply_jamming_attack(reading: dict, target_source_id: str) -> dict:
    """Apply a jamming attack to a specific source in the reading."""

    for source in reading["sources"]:
        if source["source_id"] == target_source_id:
            # Heavily reduce signal strength
            source["signal_strength"] = JAMMED_SIGNAL_STRENGTH

            # Heavily reduce confidence
            source["confidence"] = JAMMED_CONFIDENCE

            source["status"] = "jammed"
    return reading


def apply_scenario(reading: dict, scenario: str) -> dict:
    """Apply a scenario to the readings."""

    if scenario == "noise":
        return apply_noise_attack(
            reading,
            target_source_id="GPS_1",
            position_offset=6.0,
            signal_drop=35,
            confidence_drop=0.40,
        )
    elif scenario == "spoofing":
        return apply_spoofing_attack(
            reading,
            target_source_id="GPS_2",
            spoofed_position=(250.0, 300.0),
        )
    elif scenario == "jamming":
        return apply_jamming_attack(
            reading,
            target_source_id="GPS_3",
        )
    elif scenario == "degraded":
        apply_spoofing_attack(
            reading,
            target_source_id="GPS_1",
            spoofed_position=(250.0, 300.0),
        )
        apply_spoofing_attack(
            reading,
            target_source_id="GPS_2",
            spoofed_position=(230.0, 280.0),
        )
        apply_noise_attack(
            reading,
            target_source_id="GPS_4",
            position_offset=18.0,
            signal_drop=40,
            confidence_drop=0.45,
        )
        apply_jamming_attack(
            reading,
            target_source_id="GPS_5",
        )
        return reading

    return reading  # No attack applied
