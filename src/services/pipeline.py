"""Progressive rendering pipeline — orchestrates all 5 steps.

The pipeline can execute individual steps or all steps sequentially.
Each step produces a PNG output file.
"""

from __future__ import annotations

import time
from pathlib import Path

from src.models.film import Film
from src.models.scene import Scene
from src.services.renderer import Renderer
from src.utils.image_io import save_film_as_png

# Default step descriptions for logging
STEP_DESCRIPTIONS: dict[float, str] = {
    1: "Point light, flat red sphere, no shadows",
    1.5: "Point light, flat color with shadows (no Phong)",
    2: "Shadows + Phong illumination model",
    3: "Antialiasing with single point light",
    3.1: "Antialiasing with two point lights (left + right)",
    4: "Area light (rectangular) with uniform sampling (16 samples) + sphere",
    5: "Area light (rectangular) with uniform sampling (24 samples) + ellipsoid",
    6: "Area light (rectangular) with uniform sampling (24 samples) + sphere",
}

# Output filename mapping (descriptive names)
STEP_FILENAMES: dict[float, str] = {
    1: "step1_flat_color_no_shadows",
    1.5: "step1_5_flat_color_with_shadows",
    2: "step2_shadows_phong_illumination",
    3: "step3_antialiasing_single_light",
    3.1: "step3_antialiasing_dual_lights",
    4: "step4_sphere_area_light_uniform_16_samples",
    5: "step5_ellipsoid_area_light_uniform_24_samples",
    6: "step6_sphere_area_light_uniform_24_samples",
}

# Scene key mapping: maps float step number to int key used in scenes dictionary
SCENE_KEY_MAP: dict[float, int] = {
    1.5: 15,
    3.1: 31,
}


class Pipeline:
    """Orchestrates progressive rendering through all 5 steps.

    Attributes:
        output_dir: Directory to save PNG files.
        seed: Random seed for reproducibility.
    """

    def __init__(
        self,
        output_dir: str = "output",
        seed: int = 42,
    ) -> None:
        """Initialize the Pipeline.

        Args:
            output_dir: Directory for output PNG files.
            seed: Random seed.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.seed = seed

    def _auto_rays_per_pixel(self, step: int) -> int:
        """Determine default rays per pixel for a step."""
        if step >= 5:
            return 8  # Consistent with other area light steps
        if step >= 4:
            return 8  # Increased for step 4 to reduce noise
        if step >= 3:
            return 4
        return 1

    def _auto_light_samples(self, step: float) -> int:
        """Determine default light samples for a step."""
        if step in (5, 6):
            return 24  # Area light (rectangular) with uniform sampling
        if step == 4:
            return 16  # Area light (rectangular) with uniform sampling
        if step in (1.5, 3.1):
            return 1  # Point lights don't need multiple samples
        return 1

    def render_step(
        self,
        step: int,
        scene: Scene,
        rays_per_pixel: int | None = None,
        light_samples: int | None = None,
    ) -> Path:
        """Render a single step and save the PNG.

        Args:
            step: Step number (1-5).
            scene: Scene configuration for this step.
            rays_per_pixel: Override rays per pixel (uses auto default if None).
            light_samples: Override light samples (uses auto default if None).

        Returns:
            Path to the output PNG file.
        """
        rpp = (
            rays_per_pixel
            if rays_per_pixel is not None
            else self._auto_rays_per_pixel(step)
        )
        ls = (
            light_samples
            if light_samples is not None
            else self._auto_light_samples(step)
        )

        desc = STEP_DESCRIPTIONS.get(step, f"Step {step}")
        print(f"Rendering step {step}: {desc}")
        print(f"  Rays per pixel: {rpp}, Light samples: {ls}")

        start = time.perf_counter()

        film = Film(width=512, height=512)
        renderer = Renderer(
            scene=scene,
            film=film,
            step=step,
            rays_per_pixel=rpp,
            light_samples=ls,
            seed=self.seed,
        )
        renderer.render()

        output_filename = STEP_FILENAMES.get(step, f"step_{str(step).replace('.', '_')}")
        output_path = self.output_dir / f"{output_filename}.png"
        save_film_as_png(film, output_path)

        elapsed = time.perf_counter() - start
        print(f"  Saved to {output_path} ({elapsed:.2f}s)")

        return output_path

    def render_all(
        self,
        scenes: dict[float, Scene] | None = None,
        rays_per_pixel: int | None = None,
        light_samples: int | None = None,
    ) -> list[Path]:
        """Render all steps (1-5, with step 3 having dual output) sequentially.

        Args:
            scenes: Dictionary of step→Scene. Uses default scenes if None.
            rays_per_pixel: Override rays per pixel.
            light_samples: Override light samples.

        Returns:
            List of output PNG paths.
        """
        if scenes is None:
            scenes = Scene.default_steps()

        # Execute in order: 1, 1.5, 2, 3, 3.1, 4, 5, 6
        step_order = sorted(scenes.keys())
        paths = []
        
        # Render step 1 first
        if 1 in scenes:
            path = self.render_step(1, scenes[1], rays_per_pixel, light_samples)
            paths.append(path)
        
        # Render step 1.5
        if 15 in scenes:
            path_15 = self._render_custom_step(1.5, scenes[15], rays_per_pixel, light_samples)
            paths.append(path_15)
        
        # Render steps 2, 3, 3.1, 4, 5, 6
        for step in step_order:
            if step in (1, 1.5, 15, 31):
                continue  # Already rendered or will be handled
            
            scene = scenes[step]

            # Special handling for step 3: render both single and dual light variants
            if step == 3:
                # Render single light variant
                path = self.render_step(step, scene, rays_per_pixel, light_samples)
                paths.append(path)

                # Render dual light variant as step 3.1
                if 31 in scenes:
                    scene_31 = scenes[31]
                    path_31 = self._render_custom_step(3.1, scene_31, rays_per_pixel, light_samples)
                    paths.append(path_31)
            else:
                path = self.render_step(step, scene, rays_per_pixel, light_samples)
                paths.append(path)

        print(f"\nAll {len(paths)} steps rendered to: {self.output_dir}/")
        return paths
    
    def _render_custom_step(
        self,
        step: float,
        scene: Scene,
        rays_per_pixel: int | None = None,
        light_samples: int | None = None,
    ) -> Path:
        """Render a custom step with specific naming.

        Args:
            step: Step number (e.g., 3.1).
            scene: Scene configuration for this step.
            rays_per_pixel: Override rays per pixel (uses auto default if None).
            light_samples: Override light samples (uses auto default if None).

        Returns:
            Path to the output PNG file.
        """
        rpp = (
            rays_per_pixel
            if rays_per_pixel is not None
            else self._auto_rays_per_pixel(int(step))
        )
        ls = (
            light_samples
            if light_samples is not None
            else self._auto_light_samples(step)
        )

        desc = STEP_DESCRIPTIONS.get(step, f"Step {step}")
        print(f"Rendering step {step}: {desc}")
        print(f"  Rays per pixel: {rpp}, Light samples: {ls}")

        start = time.perf_counter()

        film = Film(width=512, height=512)
        
        # Map step 1.5 and 3.1 to their integer scene keys for the renderer
        renderer_step = SCENE_KEY_MAP.get(step, int(step))
        
        renderer = Renderer(
            scene=scene,
            film=film,
            step=renderer_step,
            rays_per_pixel=rpp,
            light_samples=ls,
            seed=self.seed,
        )
        renderer.render()

        output_filename = STEP_FILENAMES.get(step, f"step_{str(step).replace('.', '_')}")
        output_path = self.output_dir / f"{output_filename}.png"
        save_film_as_png(film, output_path)

        elapsed = time.perf_counter() - start
        print(f"  Saved to {output_path} ({elapsed:.2f}s)")

        return output_path
