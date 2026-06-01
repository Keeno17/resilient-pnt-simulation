"""
Simulated attack functions for testing purposes
"""

def apply_noise_attack(reading: dict, target_source_id: str, noise_level: float) -> dict:
    """Apply a noise attack to a specific source in the reading."""

    for source in reading["sources"]:
        if source["source_id"] == target_source_id:
            # Apply noise to the position
            source["position"] = (source["position"][0] + noise_level, source["position"][1] + noise_level)

            # Reduce confidence based on noise level
            source["confidence"] = max(0, source["confidence"] - (noise_level / 100))

            source["status"] = "noisy"
    return reading

def apply_spoofing_attack(reading: dict, target_source_id: str, spoofed_position: tuple) -> dict:
    """Apply a spoofing attack to a specific source in the reading."""

    for source in reading["sources"]:
        if source["source_id"] == target_source_id:
            # Spoof the position
            source["position"] = spoofed_position
            
            # Keep confidence high
            source["confidence"] = 0.9

            # Keep signal strength high
            source["signal_strength"] = 80

            source["status"] = "spoofed"
    return reading

def apply_jamming_attack(reading: dict, target_source_id: str) -> dict:
    """Apply a jamming attack to a specific source in the reading."""

    for source in reading["sources"]:
        if source["source_id"] == target_source_id:
            # Heavily reduce signal strength
            source["signal_strength"] = 1
            
            # Heavily reduce confidence
            source["confidence"] = 0.01

            source["status"] = "jammed"
    return reading

def apply_scenario(reading: dict, scenario: str) -> dict:
    """Apply a scenario to the readings."""

    if scenario == "noise":
        return apply_noise_attack(reading, target_source_id="GPS_1", noise_level=10)
    elif scenario == "spoofing":
        return apply_spoofing_attack(reading, target_source_id="GPS_2", spoofed_position=(35.6895, 139.6917))
    elif scenario == "jamming":
        return apply_jamming_attack(reading, target_source_id="GPS_3")
    elif scenario == "degraded":
        apply_noise_attack(reading, target_source_id="GPS_4", noise_level=20)
        apply_jamming_attack(reading, target_source_id="GPS_5")
        apply_spoofing_attack(reading, target_source_id="GPS_1", spoofed_position=(55.7558, 37.6173))
        return reading
    else:
        return reading  # No attack applied

