"""Regression tests — verify output images against reference files."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from src.models.film import Film
from src.models.scene import Scene
from src.services.renderer import Renderer

REFERENCE_DIR = Path(__file__).parent.parent.parent / "assets" / "references"


class TestOutputRegression:
    """Regression tests comparing output against reference images."""

    @pytest.mark.skipif(
        not REFERENCE_DIR.exists(),
        reason="Reference images not available — run with --generate-references to create them",
    )
    def test_step1_regression(self) -> None:
        """Test step 1 output matches reference."""
        self._verify_step(1, tolerance=2)

    @pytest.mark.skipif(
        not REFERENCE_DIR.exists(),
        reason="Reference images not available",
    )
    def test_step2_regression(self) -> None:
        """Test step 2 output matches reference."""
        self._verify_step(2, tolerance=2)

    def _verify_step(self, step: int, tolerance: int = 2) -> None:
        """Verify a rendering step against its reference image.

        Args:
            step: Step number.
            tolerance: Allowed pixel difference tolerance.
        """
        scene = Scene.default_steps()[step]
        film = Film(width=64, height=64)
        renderer = Renderer(
            scene=scene,
            film=film,
            step=step,
            rays_per_pixel=1,
            light_samples=1,
            seed=42,
        )
        renderer.render()

        ref_path = REFERENCE_DIR / f"step_{step}_64x64.png"
        if not ref_path.exists():
            pytest.skip(f"Reference image not found: {ref_path}")

        ref_image = np.array(Image.open(str(ref_path))).astype(np.float64)
        output_array = film.to_image_array().astype(np.float64)

        # Allow small tolerance due to floating-point differences
        diff = np.abs(ref_image - output_array)
        assert np.all(diff <= tolerance), (
            f"Step {step} output differs from reference. Max diff: {diff.max():.2f}"
        )
