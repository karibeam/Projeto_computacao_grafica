"""Ray and HitRecord data classes."""

from __future__ import annotations

from pyglm import glm


class Ray:
    """A directed line segment used for ray-object intersection.

    Attributes:
        origin: Starting point of the ray in 3D space.
        direction: Normalized direction vector.
    """

    __slots__ = ("origin", "direction")

    def __init__(self, origin: glm.vec3, direction: glm.vec3) -> None:
        """Initialize a Ray.

        Args:
            origin: Ray origin point.
            direction: Ray direction (will be normalized).
        """
        self.origin = origin
        self.direction = glm.normalize(direction)

    def point_at(self, t: float) -> glm.vec3:
        """Compute the point along the ray at parameter t.

        Args:
            t: Distance parameter along the ray.

        Returns:
            The 3D point at origin + t * direction.
        """
        return self.origin + t * self.direction


class HitRecord:
    """Information about a ray-object intersection.

    Attributes:
        t: Distance along ray from origin to hit point.
        point: World-space intersection point.
        normal: World-space surface normal (normalized).
        material: Material of the hit object.
        object_id: Identifier of the hit object.
    """

    __slots__ = ("t", "point", "normal", "material", "object_id")

    def __init__(
        self,
        t: float,
        point: glm.vec3,
        normal: glm.vec3,
        material: Material,  # type: ignore[name-defined]  # noqa: F821
        object_id: int,
    ) -> None:
        """Initialize a HitRecord.

        Args:
            t: Intersection distance (must be > 0).
            point: World-space hit position.
            normal: World-space surface normal.
            material: Object material.
            object_id: Unique object identifier.
        """
        self.t = t
        self.point = point
        self.normal = glm.normalize(normal)
        self.material = material
        self.object_id = object_id
