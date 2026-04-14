"""Unit tests for the Ray data class."""

import pytest
from pyglm import glm

from src.models.material import Material
from src.models.ray import HitRecord, Ray


class TestRay:
    """Tests for the Ray class."""

    def test_ray_creation(self) -> None:
        """Test basic ray creation."""
        origin = glm.vec3(0.0, 0.0, 0.0)
        direction = glm.vec3(0.0, 0.0, -1.0)
        ray = Ray(origin, direction)

        assert ray.origin == origin
        assert glm.length(ray.direction) == pytest.approx(1.0)

    def test_ray_direction_normalization(self) -> None:
        """Test that ray direction is automatically normalized."""
        origin = glm.vec3(0.0, 0.0, 0.0)
        direction = glm.vec3(1.0, 2.0, 3.0)
        ray = Ray(origin, direction)

        expected = glm.normalize(direction)
        assert ray.direction.x == pytest.approx(expected.x)
        assert ray.direction.y == pytest.approx(expected.y)
        assert ray.direction.z == pytest.approx(expected.z)

    def test_point_at(self) -> None:
        """Test point computation along the ray."""
        origin = glm.vec3(1.0, 2.0, 3.0)
        direction = glm.vec3(1.0, 0.0, 0.0)
        ray = Ray(origin, direction)

        point = ray.point_at(5.0)
        assert point.x == pytest.approx(6.0)
        assert point.y == pytest.approx(2.0)
        assert point.z == pytest.approx(3.0)


class TestHitRecord:
    """Tests for the HitRecord class."""

    def test_hit_record_creation(self) -> None:
        """Test basic hit record creation."""
        point = glm.vec3(1.0, 2.0, 3.0)
        normal = glm.vec3(0.0, 1.0, 0.0)
        mat = Material.flat_red()
        hit = HitRecord(t=5.0, point=point, normal=normal, material=mat, object_id=0)

        assert hit.t == pytest.approx(5.0)
        assert hit.point == point
        assert hit.object_id == 0

    def test_hit_record_normal_normalization(self) -> None:
        """Test that normal is automatically normalized."""
        point = glm.vec3(0.0, 0.0, 0.0)
        normal = glm.vec3(0.0, 3.0, 0.0)
        mat = Material.flat_red()
        hit = HitRecord(t=1.0, point=point, normal=normal, material=mat, object_id=0)

        assert glm.length(hit.normal) == pytest.approx(1.0)
        assert hit.normal.y == pytest.approx(1.0)
