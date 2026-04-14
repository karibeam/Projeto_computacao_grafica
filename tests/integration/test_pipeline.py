"""Integration tests for the full rendering pipeline."""

from src.models.film import Film
from src.models.scene import Scene
from src.services.pipeline import Pipeline
from src.services.renderer import Renderer


class TestPipelineIntegration:
    """Integration tests for the full rendering pipeline."""

    def test_render_step1_produces_image(self) -> None:
        """Test that step 1 renders without errors."""
        scene = Scene.default_steps()[1]
        film = Film(width=64, height=64)  # Small for test speed
        renderer = Renderer(
            scene=scene,
            film=film,
            step=1,
            rays_per_pixel=1,
            light_samples=1,
            seed=42,
        )
        result = renderer.render()

        assert result is not None
        # At least some pixels should be non-black (sphere and plane should be visible)
        assert result.pixels.sum() > 0

    def test_render_step2_phong(self) -> None:
        """Test that step 2 (Phong) produces different output than step 1."""
        scene1 = Scene.default_steps()[1]
        scene2 = Scene.default_steps()[2]

        film1 = Film(width=64, height=64)
        renderer1 = Renderer(
            scene=scene1,
            film=film1,
            step=1,
            rays_per_pixel=1,
            light_samples=1,
            seed=42,
        )
        renderer1.render()

        film2 = Film(width=64, height=64)
        renderer2 = Renderer(
            scene=scene2,
            film=film2,
            step=2,
            rays_per_pixel=1,
            light_samples=1,
            seed=42,
        )
        renderer2.render()

        # Step 2 should have different pixel values (Phong shading)
        diff = abs(film1.pixels - film2.pixels).sum()
        assert diff > 0

    def test_render_all_steps(self) -> None:
        """Test that all 5 steps can be rendered."""
        Pipeline(output_dir="output", seed=42)
        scenes = Scene.default_steps()

        # Use small film for speed
        for step in range(1, 6):
            film = Film(width=32, height=32)
            renderer = Renderer(
                scene=scenes[step],
                film=film,
                step=step,
                rays_per_pixel=1,
                light_samples=1,
                seed=42,
            )
            result = renderer.render()
            assert result is not None
            assert result.pixels.sum() > 0

    def test_deterministic_output(self) -> None:
        """Test that identical inputs produce identical outputs."""
        scene = Scene.default_steps()[3]

        film1 = Film(width=32, height=32)
        renderer1 = Renderer(
            scene=scene,
            film=film1,
            step=3,
            rays_per_pixel=4,
            light_samples=1,
            seed=123,
        )
        renderer1.render()

        film2 = Film(width=32, height=32)
        renderer2 = Renderer(
            scene=scene,
            film=film2,
            step=3,
            rays_per_pixel=4,
            light_samples=1,
            seed=123,
        )
        renderer2.render()

        # Outputs should be identical
        import numpy as np

        np.testing.assert_array_almost_equal(film1.pixels, film2.pixels, decimal=10)
