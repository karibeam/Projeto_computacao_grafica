"""Unit tests for sampling functions."""

import random

import pytest
from pyglm import glm

from src.models.light import AreaLight
from src.services.sampling import (
    generate_jittered_samples,
    generate_uniform_area_samples,
)


class TestJitteredSamples:
    """Tests for jittered supersampling."""

    def test_generates_correct_count(self) -> None:
        """Test that the correct number of samples is generated."""
        rng = random.Random(42)
        samples = generate_jittered_samples(
            rays_per_pixel=4,
            pixel_x=0,
            pixel_y=0,
            film_width=512,
            film_height=512,
            rng=rng,
        )
        assert len(samples) == 4

    def test_samples_in_valid_range(self) -> None:
        """Test that sample coordinates are in valid range."""
        rng = random.Random(42)
        samples = generate_jittered_samples(
            rays_per_pixel=4,
            pixel_x=256,
            pixel_y=256,
            film_width=512,
            film_height=512,
            rng=rng,
        )

        for u, v, _jitter in samples:
            assert 0.0 <= u <= 1.0
            assert 0.0 <= v <= 1.0


class TestUniformAreaSamples:
    """Tests for uniform area light sampling."""

    def test_generates_correct_count(self) -> None:
        """Test that the correct number of samples is generated."""
        light = AreaLight()
        rng = random.Random(42)
        samples = generate_uniform_area_samples(light, 16, rng)
        assert len(samples) == 16

    def test_samples_on_light_surface(self) -> None:
        """Test that samples lie on the light surface."""
        light = AreaLight(
            corner=glm.vec3(0.0, 5.0, 0.0),
            edge_u=glm.vec3(2.0, 0.0, 0.0),
            edge_v=glm.vec3(0.0, 0.0, 2.0),
        )
        rng = random.Random(42)
        samples = generate_uniform_area_samples(light, 8, rng)

        for point in samples:
            # Y should be 5.0 (light is horizontal at y=5)
            assert point.y == pytest.approx(5.0)
            # X should be in [0, 2]
            assert 0.0 <= point.x <= 2.0
            # Z should be in [0, 2]
            assert 0.0 <= point.z <= 2.0
