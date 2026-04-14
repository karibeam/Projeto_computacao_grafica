"""Unit tests for the PinholeCamera."""

import pytest
from pyglm import glm

from src.models.camera import PinholeCamera


class TestPinholeCamera:
    """Tests for the PinholeCamera class."""

    def test_camera_creation(self) -> None:
        """Test basic camera creation."""
        camera = PinholeCamera()
        assert camera.film_width == 512
        assert camera.film_height == 512
        assert camera.fov == pytest.approx(60.0)

    def test_camera_generate_ray_center(self) -> None:
        """Test ray generation through center of film."""
        camera = PinholeCamera(
            eye=glm.vec3(0.0, 0.0, 0.0),
            look_at=glm.vec3(0.0, 0.0, -1.0),
        )
        ray = camera.generate_ray(0.5, 0.5)

        assert ray.origin == camera.eye
        # Center ray should point approximately along -Z
        assert ray.direction.z < 0

    def test_camera_generate_ray_corners(self) -> None:
        """Test ray generation through corners."""
        camera = PinholeCamera(
            eye=glm.vec3(0.0, 0.0, 0.0),
            look_at=glm.vec3(0.0, 0.0, -1.0),
            fov=90.0,
        )
        # Top-left corner
        ray_tl = camera.generate_ray(0.0, 1.0)
        # Bottom-right corner
        ray_br = camera.generate_ray(1.0, 0.0)

        # Both should point generally forward (-Z)
        assert ray_tl.direction.z < 0
        assert ray_br.direction.z < 0

    def test_camera_aspect_ratio(self) -> None:
        """Test camera with non-square film."""
        camera = PinholeCamera(film_width=1024, film_height=512)
        assert camera._aspect_ratio == pytest.approx(2.0)
