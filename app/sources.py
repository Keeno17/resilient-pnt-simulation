from dataclasses import dataclass
from math import sqrt
from typing import Tuple

@dataclass
class NavigationSource:
    source_id: str
    position: Tuple[float, float]  # (latitude, longitude)
    signal_strength: float
    confidence: float
    noise_level: float

    def generate_reading(self) -> dict:
        """Simulate a reading from the navigation source."""

        # Simulate signal strength with some noise
        noisy_signal = self.signal_strength + (self.noise_level * (0.5 - sqrt(2) * (self.confidence - 0.5)))
        return {
            "source_id": self.source_id,
            "position": self.position,
            "signal_strength": max(0, min(100, noisy_signal)),  # Ensure signal strength is between 0 and 100
            "confidence": self.confidence,
            "status": "normal",
        }

def create_navigation_sources() -> list:
    """Create a list of navigation sources with varying properties."""

    sources = [
        NavigationSource(source_id="GPS_1", position=(37.7749, -122.4194), signal_strength=80, confidence=0.9, noise_level=5),
        NavigationSource(source_id="GPS_2", position=(34.0522, -118.2437), signal_strength=70, confidence=0.8, noise_level=10),
        NavigationSource(source_id="GPS_3", position=(40.7128, -74.0060), signal_strength=60, confidence=0.7, noise_level=15),
        NavigationSource(source_id="GPS_4", position=(51.5074, -0.1278), signal_strength=50, confidence=0.6, noise_level=20),
        NavigationSource(source_id="GPS_5", position=(48.8566, 2.3522), signal_strength=90, confidence=0.95, noise_level=3),
    ]
    return sources

