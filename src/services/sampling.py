"""Sampling strategies for antialiasing and area lights.

- Jittered supersampling for antialiasing (stratified random samples within each pixel).
- Uniform random sampling for area lights (Monte Carlo).
"""

from __future__ import annotations

import random
from collections.abc import Callable

from pyglm import glm

from src.models.light import AreaLight


def generate_jittered_samples(
    rays_per_pixel: int,
    pixel_x: int,
    pixel_y: int,
    film_width: int,
    film_height: int,
    rng: random.Random,
) -> list[tuple[float, float, glm.vec2]]:
    """Generate jittered sub-pixel samples for antialiasing.

    Divides the pixel into an NxN grid (where N = ceil(sqrt(rays_per_pixel)))
    and casts one ray per cell with a random jitter within the cell.

    Args:
        rays_per_pixel: Number of samples (N×N grid).
        pixel_x: Pixel x-coordinate.
        pixel_y: Pixel y-coordinate.
        film_width: Film width.
        film_height: Film height.
        rng: Random number generator.

    Returns:
        List of (u, v, jitter) tuples where u, v are normalized pixel
        coordinates and jitter is the sub-pixel offset.
    """
    n = max(1, int(rays_per_pixel**0.5))
    if n * n < rays_per_pixel:
        n += 1

    samples: list[tuple[float, float, glm.vec2]] = []
    pixel_width = 1.0 / film_width
    pixel_height = 1.0 / film_height

    for i in range(n):
        for j in range(n):
            if len(samples) >= rays_per_pixel:
                break

            # Jitter within the sub-pixel cell
            jitter_x = (i + rng.uniform(0.0, 1.0)) / n
            jitter_y = (j + rng.uniform(0.0, 1.0)) / n

            # Normalized coordinates
            u = (pixel_x + jitter_x) / film_width
            v = (pixel_y + jitter_y) / film_height

            # Jitter offset for the camera
            jitter_offset = glm.vec2(
                (jitter_x - 0.5) * pixel_width,
                (jitter_y - 0.5) * pixel_height,
            )
            samples.append((u, v, jitter_offset))

        if len(samples) >= rays_per_pixel:
            break

    return samples


def generate_uniform_area_samples(
    light: AreaLight,
    num_samples: int,
    rng: Callable[[], tuple[float, float]] | random.Random | None = None,
) -> list[glm.vec3]:
    """Generate uniformly distributed sample points on an area light.

    Args:
        light: The area light to sample.
        num_samples: Number of sample points.
        rng: A callable returning (u, v) where u, v ~ Uniform(0, 1).
            If rng is a random.Random instance, it is wrapped automatically.

    Returns:
        List of world-space points on the light surface.
    """
    if rng is None:
        rng_instance = random.Random(42)
        rng = lambda: (rng_instance.random(), rng_instance.random())  # noqa: E731
    elif isinstance(rng, random.Random):
        rng_instance = rng
        rng = lambda: (rng_instance.random(), rng_instance.random())  # noqa: E731

    points = []
    for _ in range(num_samples):
        points.append(light.sample_point(rng))
    return points
