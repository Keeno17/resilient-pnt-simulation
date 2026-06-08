from typing import Tuple, List
from sources import NavigationSource


def calculate_consensus_position(readings) -> Tuple[float, float]:
    """Calculate a consensus (weighted average) position based on the readings from multiple sources."""

    weighted_x = 0.0
    weighted_y = 0.0
    total_confidence = 0.0

    for source in readings["sources"]:
        conf = float(source.get("confidence", 0.0))
        pos = source.get("position", (0.0, 0.0))
        weighted_x += pos[0] * conf
        weighted_y += pos[1] * conf
        total_confidence += conf

    if total_confidence == 0:
        # fallback to simple average if confidence sums to zero
        count = max(1, len(readings["sources"]))
        avg_x = (
            sum(s.get("position", (0.0, 0.0))[0] for s in readings["sources"]) / count
        )
        avg_y = (
            sum(s.get("position", (0.0, 0.0))[1] for s in readings["sources"]) / count
        )
        return (avg_x, avg_y)

    return (weighted_x / total_confidence, weighted_y / total_confidence)


def distance_between(pos1, pos2):
    """Calculate the distance between two positions."""

    from math import sqrt

    return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def detect_anomalies(
    readings, consensus_position=None
) -> Tuple[List[NavigationSource], List[NavigationSource]]:
    """Detect anomalies by comparing each source's position to the consensus position."""

    if consensus_position is None:
        consensus_position = calculate_consensus_position(readings)

    flagged: List[NavigationSource] = []
    trusted: List[NavigationSource] = []

    for source in readings["sources"]:
        distance = distance_between(
            source.get("position", (0.0, 0.0)), consensus_position
        )
        signal_strength = source.get("signal_strength", 0)
        confidence = source.get("confidence", 0.0)

        if signal_strength < 20:
            flagged.append(source)
        elif confidence < 0.2:
            flagged.append(source)
        elif distance > 0.1:
            flagged.append(source)
        else:
            trusted.append(source)

    return (flagged, trusted)


def calculate_trust_score(source) -> float:
    """Calculate a trust score for a source based on its properties."""

    signal_strength = source.get("signal_strength", 0)
    confidence = source.get("confidence", 0.0)
    noise_level = source.get("noise_level", 0.0)
    # Simple trust score calculation
    trust_score = (signal_strength * confidence) / (1 + noise_level)
    return trust_score
