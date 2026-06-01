from typing import Tuple, List
from sources import NavigationSource

def fuse_positions(trusted_readings: List):
    """Fuse the positions from trusted readings to produce a final estimated reading."""

    if not trusted_readings:
        return {
            "position": (0.0, 0.0),
            "confidence": 0.0,
            "status": "unavailable",
        }

    weighted_x = 0.0
    weighted_y = 0.0
    total_weight = 0.0

    for source in trusted_readings:
        weight = source["confidence"] * source["signal_strength"]

        weighted_x += source["position"][0] * weight
        weighted_y += source["position"][1] * weight

        total_weight += weight

    final_x = weighted_x / total_weight if total_weight > 0 else 0.0
    final_y = weighted_y / total_weight if total_weight > 0 else 0.0

    overall_confidence = total_weight / len(trusted_readings) if trusted_readings else 0.0

    if len(trusted_readings) < 2:
        status = "degraded"
    else:
        status = "normal"

    return {
        "position": (final_x, final_y),
        "confidence": overall_confidence,
        "status": status,
    }