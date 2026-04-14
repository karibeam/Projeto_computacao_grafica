"""Unit tests for geometric primitives (Sphere, Ellipsoid, Plane)."""

import pytest
from pyglm import glm

from src.models.geometry import Ellipsoid, Plane, Sphere
from src.models.ray import Ray


class TestSphere:
    """Tests for the Sphere primitive."""

    def test_sphere_hit_front(self) -> None:
        """Test ray hitting the front of a sphere."""
        sphere = Sphere(center=glm.vec3(0.0, 0.0, -5.0), radius=1.0)
        ray = Ray(origin=glm.vec3(0.0, 0.0, 0.0), direction=glm.vec3(0.0, 0.0, -1.0))

        hit = sphere.intersect(ray)
        assert hit is not None
        assert hit.t == pytest.approx(4.0, abs=0.01)

    def test_sphere_miss(self) -> None:
        """Test ray missing the sphere."""
        sphere = Sphere(center=glm.vec3(0.0, 0.0, -5.0), radius=1.0)
        ray = Ray(origin=glm.vec3(5.0, 0.0, 0.0), direction=glm.vec3(0.0, 0.0, -1.0))

        hit = sphere.intersect(ray)
        assert hit is None

    def test_sphere_normal_at_hit(self) -> None:
        """Test that sphere normal points outward from center."""
        sphere = Sphere(center=glm.vec3(0.0, 0.0, -5.0), radius=1.0)
        ray = Ray(origin=glm.vec3(0.0, 0.0, 0.0), direction=glm.vec3(0.0, 0.0, -1.0))

        hit = sphere.intersect(ray)
        assert hit is not None
        # Normal should point away from center (toward the ray origin)
        assert hit.normal.z > 0

    def test_sphere_local_coordinates(self) -> None:
        """Test that intersection math works in local space."""
        # Sphere translated to (0, 3, -5)
        sphere = Sphere(center=glm.vec3(0.0, 3.0, -5.0), radius=2.0)
        ray = Ray(origin=glm.vec3(0.0, 3.0, 0.0), direction=glm.vec3(0.0, 0.0, -1.0))

        hit = sphere.intersect(ray)
        assert hit is not None
        assert hit.t == pytest.approx(3.0, abs=0.01)


class TestEllipsoid:
    """Tests for the Ellipsoid primitive."""

    def test_ellipsoid_hit(self) -> None:
        """Test ray hitting an ellipsoid."""
        ellipsoid = Ellipsoid(
            center=glm.vec3(0.0, 0.0, -5.0),
            radii=glm.vec3(2.0, 1.0, 1.5),
        )
        ray = Ray(origin=glm.vec3(0.0, 0.0, 0.0), direction=glm.vec3(0.0, 0.0, -1.0))

        hit = ellipsoid.intersect(ray)
        assert hit is not None

    def test_ellipsoid_normal_transform(self) -> None:
        """Test that ellipsoid normals are correctly transformed."""
        ellipsoid = Ellipsoid(
            center=glm.vec3(0.0, 0.0, -5.0),
            radii=glm.vec3(2.0, 1.0, 1.0),
        )
        # Hit at center along Z
        ray = Ray(origin=glm.vec3(0.0, 0.0, 0.0), direction=glm.vec3(0.0, 0.0, -1.0))
        hit = ellipsoid.intersect(ray)

        assert hit is not None
        # Normal should point toward the ray origin (along +Z)
        assert hit.normal.z > 0


class TestPlane:
    """Tests for the Plane primitive."""

    def test_plane_hit_above(self) -> None:
        """Test ray hitting a horizontal plane from above."""
        plane = Plane(point=glm.vec3(0.0, 0.0, 0.0), normal=glm.vec3(0.0, 1.0, 0.0))
        ray = Ray(origin=glm.vec3(0.0, 5.0, 0.0), direction=glm.vec3(0.0, -1.0, 0.0))

        hit = plane.intersect(ray)
        assert hit is not None
        assert hit.t == pytest.approx(5.0)

    def test_plane_miss_parallel(self) -> None:
        """Test ray parallel to plane (no hit)."""
        plane = Plane(point=glm.vec3(0.0, 0.0, 0.0), normal=glm.vec3(0.0, 1.0, 0.0))
        ray = Ray(origin=glm.vec3(0.0, 5.0, 0.0), direction=glm.vec3(1.0, 0.0, 0.0))

        hit = plane.intersect(ray)
        assert hit is None

    def test_plane_normal(self) -> None:
        """Test that plane normal is correct."""
        plane = Plane(point=glm.vec3(0.0, 0.0, 0.0), normal=glm.vec3(0.0, 1.0, 0.0))
        ray = Ray(origin=glm.vec3(0.0, 5.0, 0.0), direction=glm.vec3(0.0, -1.0, 0.0))

        hit = plane.intersect(ray)
        assert hit is not None
        assert hit.normal.y == pytest.approx(1.0)
