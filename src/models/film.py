"""Film buffer for pixel accumulation and PNG output."""

from __future__ import annotations

import numpy as np


class Film:
    """A pixel buffer where radiance values are accumulated.

    The film stores floating-point RGB values that are accumulated during
    rendering and later converted to uint8 for PNG output.

    Attributes:
        width: Horizontal pixel count.
        height: Vertical pixel count.
        pixels: Float buffer of shape (height, width, 3) for RGB accumulation.
        samples: Integer buffer tracking the number of samples per pixel.
    """

    __slots__ = ("width", "height", "pixels", "samples")

    def __init__(self, width: int = 512, height: int = 512) -> None:
        """Initialize a Film.

        Args:
            width: Film width in pixels.
            height: Film height in pixels.
        """
        self.width = width
        self.height = height
        self.pixels: np.ndarray = np.zeros((height, width, 3), dtype=np.float64)
        self.samples: np.ndarray = np.zeros((height, width), dtype=np.int32)

    def accumulate(self, x: int, y: int, color: tuple[float, float, float]) -> None:
        """Accumulate a color sample at the given pixel.

        Args:
            x: Horizontal pixel coordinate [0, width-1].
            y: Vertical pixel coordinate [0, height-1].
            color: RGB color tuple with components in [0, ∞).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y, x, 0] += color[0]
            self.pixels[y, x, 1] += color[1]
            self.pixels[y, x, 2] += color[2]
            self.samples[y, x] += 1

    def average(self) -> None:
        """Divide accumulated values by sample count (in-place).

        Pixels with zero samples remain black.
        """
        # Avoid division by zero
        valid = self.samples > 0
        for c in range(3):
            self.pixels[valid, c] /= self.samples[valid]

    def clamp(self, low: float = 0.0, high: float = 1.0) -> None:
        """Clamp pixel values to [low, high] (in-place).

        Args:
            low: Minimum value.
            high: Maximum value.
        """
        np.clip(self.pixels, low, high, out=self.pixels)

    def to_image_array(self) -> np.ndarray:
        """Convert the film buffer to a uint8 RGB array suitable for Pillow.

        Returns:
            NumPy array of shape (height, width, 3) with dtype uint8.
        """
        return (self.pixels * 255.0).astype(np.uint8)

    def clear(self) -> None:
        """Reset the film to all zeros."""
        self.pixels.fill(0.0)
        self.samples.fill(0)
