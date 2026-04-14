"""Geometric primitives: Sphere, Ellipsoid, and Plane.

All intersection math is performed in local coordinates. Objects store a
local-to-world transformation matrix. When a ray is tested against an
object, the ray is transformed into local space, the intersection is
computed, and the result is transformed back to world space.
"""

from __future__ import annotations

from pyglm import glm

from src.models.material import Material
from src.models.ray import HitRecord, Ray

# Epsilon to avoid self-intersection
EPSILON = 0.001


class Sphere:
    """A sphere defined as a unit sphere in local space.

    The local-to-world matrix encodes position (translation) and radius (scale).

    Attributes:
        local_to_world: Transformation matrix from local to world space.
        world_to_local: Inverse of local_to_world.
        material: Surface material.
        object_id: Unique identifier.
    """

    __slots__ = ("local_to_world", "world_to_local", "material", "object_id")

    def __init__(
        self,
        center: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        radius: float = 1.0,
        material: Material | None = None,
        object_id: int = 0,
    ) -> None:
        """Initialize a Sphere.

        Args:
            center: World-space center position.
            radius: Sphere radius.
            material: Surface material (default: flat red).
            object_id: Unique object identifier.
        """
        self.local_to_world = glm.translate(glm.mat4(1.0), center) * glm.scale(
            glm.mat4(1.0), glm.vec3(radius)
        )
        self.world_to_local = glm.inverse(self.local_to_world)
        self.material = material if material is not None else Material.flat_red()
        self.object_id = object_id

    def intersect(self, ray: Ray) -> HitRecord | None:
        """Test ray-sphere intersection in local space.

        Args:
            ray: World-space ray to test.

        Returns:
            HitRecord if intersection found, None otherwise.
        """
        # Transform ray to local space
        origin_local = glm.vec3(self.world_to_local * glm.vec4(ray.origin, 1.0))
        dir_local = glm.vec3(self.world_to_local * glm.vec4(ray.direction, 0.0))
        dir_local = glm.normalize(dir_local)

        # Ray-sphere intersection in local space (unit sphere at origin)
        oc = origin_local
        a = glm.dot(dir_local, dir_local)
        b = 2.0 * glm.dot(oc, dir_local)
        c = glm.dot(oc, oc) - 1.0
        discriminant = b * b - 4.0 * a * c

        if discriminant < 0:
            return None

        sqrt_disc = glm.sqrt(discriminant)
        t_local = (-b - sqrt_disc) / (2.0 * a)

        if t_local < EPSILON:
            t_local = (-b + sqrt_disc) / (2.0 * a)
            if t_local < EPSILON:
                return None

        # Compute hit point in local space
        hit_local = origin_local + t_local * dir_local

        # Transform hit point to world space
        hit_world = glm.vec3(self.local_to_world * glm.vec4(hit_local, 1.0))

        # Normal in local space (for unit sphere: just the point itself)
        normal_local = hit_local
        # Transform normal to world space using inverse-transpose
        # For uniform scale, we can use the upper 3x3 of local_to_world
        normal_world = glm.vec3(
            glm.transpose(glm.mat3(self.local_to_world)) * normal_local
        )
        normal_world = glm.normalize(normal_world)

        # Compute world-space t
        t_world = glm.length(hit_world - ray.origin)
        if glm.dot(ray.direction, hit_world - ray.origin) < 0:
            t_world = -t_world

        return HitRecord(
            t_world, hit_world, normal_world, self.material, self.object_id
        )


class Ellipsoid:
    """An ellipsoid defined as a scaled unit sphere in local space.

    The local-to-world matrix encodes position (translation) and semi-axis
    lengths (scale factors rx, ry, rz).

    Attributes:
        local_to_world: Transformation matrix from local to world space.
        world_to_local: Inverse of local_to_world.
        material: Surface material.
        object_id: Unique identifier.
    """

    __slots__ = ("local_to_world", "world_to_local", "material", "object_id")

    def __init__(
        self,
        center: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        radii: glm.vec3 = glm.vec3(1.5, 1.0, 0.8),
        material: Material | None = None,
        object_id: int = 1,
    ) -> None:
        """Initialize an Ellipsoid.

        Args:
            center: World-space center position.
            radii: Semi-axis lengths (rx, ry, rz).
            material: Surface material (default: flat red).
            object_id: Unique object identifier.
        """
        self.local_to_world = glm.translate(glm.mat4(1.0), center) * glm.scale(
            glm.mat4(1.0), radii
        )
        self.world_to_local = glm.inverse(self.local_to_world)
        self.material = material if material is not None else Material.flat_red()
        self.object_id = object_id

    def intersect(self, ray: Ray) -> HitRecord | None:
        """Test ray-ellipsoid intersection in local space.

        Args:
            ray: World-space ray to test.

        Returns:
            HitRecord if intersection found, None otherwise.
        """
        # Transform ray to local space
        origin_local = glm.vec3(self.world_to_local * glm.vec4(ray.origin, 1.0))
        dir_local = glm.vec3(self.world_to_local * glm.vec4(ray.direction, 0.0))
        dir_local = glm.normalize(dir_local)

        # Intersection with unit sphere in local space
        oc = origin_local
        a = glm.dot(dir_local, dir_local)
        b = 2.0 * glm.dot(oc, dir_local)
        c = glm.dot(oc, oc) - 1.0
        discriminant = b * b - 4.0 * a * c

        if discriminant < 0:
            return None

        sqrt_disc = glm.sqrt(discriminant)
        t_local = (-b - sqrt_disc) / (2.0 * a)

        if t_local < EPSILON:
            t_local = (-b + sqrt_disc) / (2.0 * a)
            if t_local < EPSILON:
                return None

        # Hit point in local space
        hit_local = origin_local + t_local * dir_local

        # Transform to world space
        hit_world = glm.vec3(self.local_to_world * glm.vec4(hit_local, 1.0))

        # Normal: for non-uniform scale, use inverse-transpose of upper 3x3
        inv_transpose = glm.transpose(glm.mat3(self.world_to_local))
        normal_world = glm.normalize(inv_transpose * hit_local)

        # World-space t
        t_world = glm.length(hit_world - ray.origin)
        if glm.dot(ray.direction, hit_world - ray.origin) < 0:
            t_world = -t_world

        return HitRecord(
            t_world, hit_world, normal_world, self.material, self.object_id
        )


class Plane:
    """An infinite flat surface serving as the ground plane.

    Attributes:
        point: A point on the plane in world space.
        normal: Plane normal in world space (normalized).
        material: Surface material.
        object_id: Unique identifier.
    """

    __slots__ = ("point", "normal", "material", "object_id")

    def __init__(
        self,
        point: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        normal: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        material: Material | None = None,
        object_id: int = 2,
    ) -> None:
        """Initialize a Plane.

        Args:
            point: A point on the plane.
            normal: Plane normal (will be normalized).
            material: Surface material (default: gray).
            object_id: Unique object identifier.
        """
        self.point = point
        self.normal = glm.normalize(normal)
        self.material = (
            material
            if material is not None
            else Material(color=glm.vec3(0.6, 0.6, 0.6))
        )
        self.object_id = object_id

    def intersect(self, ray: Ray) -> HitRecord | None:
        """Test ray-plane intersection.

        Args:
            ray: World-space ray to test.

        Returns:
            HitRecord if intersection found, None otherwise.
        """
        denom = glm.dot(self.normal, ray.direction)

        if abs(denom) < 1e-6:
            return None  # Ray parallel to plane

        t = glm.dot(self.point - ray.origin, self.normal) / denom

        if t < EPSILON:
            return None

        hit_point = ray.point_at(t)

        return HitRecord(t, hit_point, self.normal, self.material, self.object_id)


class Box:
    """An axis-aligned box defined by min and max corners in local space.

    The local-to-world matrix encodes position (translation) and size (scale).

    Attributes:
        local_to_world: Transformation matrix from local to world space.
        world_to_local: Inverse of local_to_world.
        material: Surface material.
        object_id: Unique identifier.
    """

    __slots__ = ("local_to_world", "world_to_local", "material", "object_id", "min_corner", "max_corner")

    def __init__(
        self,
        center: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        size: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        material: Material | None = None,
        object_id: int = 3,
    ) -> None:
        """Initialize a Box.

        Args:
            center: World-space center position.
            size: Dimensions (width, height, depth).
            material: Surface material (default: flat red).
            object_id: Unique object identifier.
        """
        self.min_corner = glm.vec3(-0.5, -0.5, -0.5)
        self.max_corner = glm.vec3(0.5, 0.5, 0.5)
        
        self.local_to_world = glm.translate(glm.mat4(1.0), center) * glm.scale(
            glm.mat4(1.0), size
        )
        self.world_to_local = glm.inverse(self.local_to_world)
        self.material = material if material is not None else Material.flat_red()
        self.object_id = object_id

    def intersect(self, ray: Ray) -> HitRecord | None:
        """Test ray-box intersection using slab method in local space.

        Args:
            ray: World-space ray to test.

        Returns:
            HitRecord if intersection found, None otherwise.
        """
        # Transform ray to local space
        origin_local = glm.vec3(self.world_to_local * glm.vec4(ray.origin, 1.0))
        dir_local = glm.vec3(self.world_to_local * glm.vec4(ray.direction, 0.0))
        dir_local = glm.normalize(dir_local)

        t_min = (self.min_corner[0] - origin_local[0]) / dir_local[0]
        t_max = (self.max_corner[0] - origin_local[0]) / dir_local[0]

        if t_min > t_max:
            t_min, t_max = t_max, t_min

        ty_min = (self.min_corner[1] - origin_local[1]) / dir_local[1]
        ty_max = (self.max_corner[1] - origin_local[1]) / dir_local[1]

        if ty_min > ty_max:
            ty_min, ty_max = ty_max, ty_min

        if (t_min > ty_max) or (ty_min > t_max):
            return None

        if ty_min > t_min:
            t_min = ty_min

        if ty_max < t_max:
            t_max = ty_max

        tz_min = (self.min_corner[2] - origin_local[2]) / dir_local[2]
        tz_max = (self.max_corner[2] - origin_local[2]) / dir_local[2]

        if tz_min > tz_max:
            tz_min, tz_max = tz_max, tz_min

        if (t_min > tz_max) or (tz_min > t_max):
            return None

        if tz_min > t_min:
            t_min = tz_min

        if tz_max < t_max:
            t_max = tz_max

        if t_min < EPSILON:
            if t_max < EPSILON:
                return None
            t_min = t_max

        # Hit point in local space
        hit_local = origin_local + t_min * dir_local

        # Transform to world space
        hit_world = glm.vec3(self.local_to_world * glm.vec4(hit_local, 1.0))

        # Compute normal in local space based on which face was hit
        normal_local = glm.vec3(0.0)
        for i in range(3):
            if abs(hit_local[i] - self.min_corner[i]) < EPSILON:
                normal_local[i] = -1.0
            elif abs(hit_local[i] - self.max_corner[i]) < EPSILON:
                normal_local[i] = 1.0

        # Transform normal to world space using inverse-transpose
        inv_transpose = glm.transpose(glm.mat3(self.world_to_local))
        normal_world = glm.normalize(inv_transpose * normal_local)

        # World-space t
        t_world = glm.length(hit_world - ray.origin)
        if glm.dot(ray.direction, hit_world - ray.origin) < 0:
            t_world = -t_world

        return HitRecord(
            t_world, hit_world, normal_world, self.material, self.object_id
        )
