from dataclasses import dataclass
from typing import Tuple


@dataclass
class NavigationSource:
    source_id: str
    position: Tuple[float, float]  # (latitude, longitude)
    signal_strength: float
    confidence: float
    noise_level: float = 0.0

    def generate_reading(self) -> dict:
        """Simulate a reading from the navigation source."""

        # Simulate signal strength with some noise
        return {
            "source_id": self.source_id,
            "position": self.position,
            "signal_strength": max(
                0, min(100, self.signal_strength)
            ),  # Ensure signal strength is between 0 and 100
            "confidence": max(0, min(1, self.confidence)),
            "status": "normal",
        }


def create_navigation_sources() -> list:
    """Create a list of navigation sources with varying properties."""

    return [
        NavigationSource("GPS_1", (100.2, 99.9), 80, 0.90),
        NavigationSource("GPS_2", (99.8, 100.1), 70, 0.80),
        NavigationSource("GPS_3", (100.3, 100.0), 60, 0.70),
        NavigationSource("GPS_4", (99.9, 99.8), 50, 0.60),
        NavigationSource("GPS_5", (100.0, 100.2), 90, 0.95),
    ]
