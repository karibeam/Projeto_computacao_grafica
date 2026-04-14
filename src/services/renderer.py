"""Core ray tracer — primary ray tracing and shadow rays."""

from __future__ import annotations

import random

from pyglm import glm

from src.models.film import Film
from src.models.ray import Ray
from src.models.scene import Scene
from src.services.intersection import find_closest_hit
from src.services.shading import compute_flat_color, compute_phong


class Renderer:
    """Core ray tracing engine.

    Traces rays from the camera through the film plane, computes
    intersections, and evaluates shading.

    Attributes:
        scene: The scene to render.
        film: The film buffer to accumulate pixels.
        step: The rendering step (1-5), which determines which features are active.
        rays_per_pixel: Number of primary rays per pixel (antialiasing).
        light_samples: Number of shadow rays per area light sample.
        seed: Random seed for reproducibility.
    """

    __slots__ = (
        "scene",
        "film",
        "step",
        "rays_per_pixel",
        "light_samples",
        "seed",
        "_rng",
    )

    def __init__(
        self,
        scene: Scene,
        film: Film,
        step: int = 1,
        rays_per_pixel: int = 1,
        light_samples: int = 1,
        seed: int = 42,
    ) -> None:
        """Initialize the Renderer.

        Args:
            scene: Scene to render.
            film: Film buffer for output.
            step: Rendering step number (1-5).
            rays_per_pixel: Primary rays per pixel.
            light_samples: Shadow rays per area light.
            seed: Random seed.
        """
        self.scene = scene
        self.film = film
        self.step = step
        self.rays_per_pixel = rays_per_pixel
        self.light_samples = light_samples
        self.seed = seed
        self._rng = random.Random(seed)

    def trace_ray(self, ray: Ray, depth: int = 0) -> glm.vec3:
        """Trace a single ray and compute its color.

        Args:
            ray: The ray to trace.
            depth: Recursion depth (for future extensions, currently always 0).

        Returns:
            RGB color for this ray.
        """
        hit = find_closest_hit(ray, scene=self.scene)

        if hit is None:
            # Background color (dark gradient)
            return glm.vec3(0.02, 0.02, 0.05)

        # Determine shading model based on step
        if self.step == 1:
            # Step 1: flat color, no shadows
            return compute_flat_color(hit, self.scene, use_shadows=False)
        elif self.step == 15:
            # Step 1.5: flat color with shadows (no Phong)
            return compute_flat_color(hit, self.scene, use_shadows=True)
        else:
            # Steps 2+: Phong model
            view_dir = glm.normalize(self.scene.camera.eye - hit.point)
            use_shadows = self.step >= 2

            return compute_phong(
                hit,
                self.scene,
                view_dir,
                use_shadows=use_shadows,
                light_samples=self.light_samples,
                rng=self._rng,
            )

    def render(self) -> Film:
        """Execute the full rendering pass.

        Iterates over every pixel, generates rays, traces them,
        and accumulates results in the film buffer.

        Returns:
            The film buffer with accumulated pixel values.
        """
        camera = self.scene.camera
        film = self.film

        for y in range(film.height):
            for x in range(film.width):
                if self.rays_per_pixel <= 1:
                    # Single ray per pixel
                    u = (x + 0.5) / film.width
                    v = (film.height - y - 0.5) / film.height
                    ray = camera.generate_ray(u, v)
                    color = self.trace_ray(ray)
                    film.accumulate(x, y, (color[0], color[1], color[2]))
                else:
                    # Multiple rays per pixel (antialiasing)
                    color_sum = glm.vec3(0.0)
                    for _ in range(self.rays_per_pixel):
                        # Jittered sub-pixel
                        jitter_x = x + self._rng.uniform(0.0, 1.0)
                        jitter_y = y + self._rng.uniform(0.0, 1.0)
                        u = jitter_x / film.width
                        v = (film.height - jitter_y) / film.height
                        ray = camera.generate_ray(u, v)
                        color_sum += self.trace_ray(ray)
                    color_avg = color_sum / self.rays_per_pixel
                    film.accumulate(x, y, (color_avg[0], color_avg[1], color_avg[2]))

        # Post-processing
        film.average()
        film.clamp()

        return film
