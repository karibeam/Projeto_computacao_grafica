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
        rotation: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        material: Material | None = None,
        object_id: int = 3,
    ) -> None:
        """Initialize a Box.

        Args:
            center: World-space center position.
            size: Dimensions (width, height, depth).
            rotation: Rotation in radians around x, y, z axes.
            material: Surface material (default: flat red).
            object_id: Unique object identifier.
        """
        self.min_corner = glm.vec3(-0.5, -0.5, -0.5)
        self.max_corner = glm.vec3(0.5, 0.5, 0.5)
        
        model = glm.translate(glm.mat4(1.0), center)
        if rotation.x != 0.0:
            model = glm.rotate(model, rotation.x, glm.vec3(1.0, 0.0, 0.0))
        if rotation.y != 0.0:
            model = glm.rotate(model, rotation.y, glm.vec3(0.0, 1.0, 0.0))
        if rotation.z != 0.0:
            model = glm.rotate(model, rotation.z, glm.vec3(0.0, 0.0, 1.0))
            
        self.local_to_world = model * glm.scale(glm.mat4(1.0), size)
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

        t_min_vec = glm.vec3(0.0)
        t_max_vec = glm.vec3(0.0)
        
        for i in range(3):
            if abs(dir_local[i]) < 1e-8:
                inv_dir = 1e8 if dir_local[i] >= 0 else -1e8
            else:
                inv_dir = 1.0 / dir_local[i]
                
            t0 = (self.min_corner[i] - origin_local[i]) * inv_dir
            t1 = (self.max_corner[i] - origin_local[i]) * inv_dir
            
            t_min_vec[i] = min(t0, t1)
            t_max_vec[i] = max(t0, t1)

        t_enter = max(max(t_min_vec.x, t_min_vec.y), t_min_vec.z)
        t_exit = min(min(t_max_vec.x, t_max_vec.y), t_max_vec.z)

        if t_enter > t_exit or t_exit < 0:
            return None

        t_hit = t_enter if t_enter > EPSILON else t_exit
        if t_hit < EPSILON:
            return None

        # Hit point in local space
        hit_local = origin_local + t_hit * dir_local

        # Transform to world space
        hit_world = glm.vec3(self.local_to_world * glm.vec4(hit_local, 1.0))

        # Compute normal in local space based on which face was hit
        tol = 1e-4
        normal_local = glm.vec3(0.0)
        if abs(hit_local.x - self.max_corner.x) < tol:
            normal_local.x = 1.0
        elif abs(hit_local.x - self.min_corner.x) < tol:
            normal_local.x = -1.0
        elif abs(hit_local.y - self.max_corner.y) < tol:
            normal_local.y = 1.0
        elif abs(hit_local.y - self.min_corner.y) < tol:
            normal_local.y = -1.0
        elif abs(hit_local.z - self.max_corner.z) < tol:
            normal_local.z = 1.0
        elif abs(hit_local.z - self.min_corner.z) < tol:
            normal_local.z = -1.0
        
        # Fallback normal
        if glm.length(normal_local) < 0.1:
            normal_local = glm.vec3(0.0, 1.0, 0.0)

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


class Tetrahedron:
    """A regular tetrahedron defined in local space.

    The local-to-world matrix encodes position (translation), rotation, and size (scale).

    Attributes:
        local_to_world: Transformation matrix from local to world space.
        world_to_local: Inverse of local_to_world.
        material: Surface material.
        object_id: Unique identifier.
    """

    __slots__ = ("local_to_world", "world_to_local", "material", "object_id", "vertices", "faces")

    def __init__(
        self,
        center: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        size: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        rotation: glm.vec3 = glm.vec3(0.0, 0.0, 0.0),
        material: Material | None = None,
        object_id: int = 4,
    ) -> None:
        """Initialize a Tetrahedron.

        Args:
            center: World-space center position.
            size: Dimensions (scale).
            rotation: Rotation in radians around x, y, z axes.
            material: Surface material (default: flat red).
            object_id: Unique object identifier.
        """
        # Standard tetrahedron vertices inscribed in a unit cube
        self.vertices = [
            glm.vec3(0.5, 0.5, 0.5),
            glm.vec3(0.5, -0.5, -0.5),
            glm.vec3(-0.5, 0.5, -0.5),
            glm.vec3(-0.5, -0.5, 0.5)
        ]
        
        # Faces with counter-clockwise winding
        self.faces = [
            (0, 2, 1),
            (0, 1, 3),
            (0, 3, 2),
            (1, 2, 3)
        ]

        model = glm.translate(glm.mat4(1.0), center)
        if rotation.x != 0.0:
            model = glm.rotate(model, rotation.x, glm.vec3(1.0, 0.0, 0.0))
        if rotation.y != 0.0:
            model = glm.rotate(model, rotation.y, glm.vec3(0.0, 1.0, 0.0))
        if rotation.z != 0.0:
            model = glm.rotate(model, rotation.z, glm.vec3(0.0, 0.0, 1.0))

        self.local_to_world = model * glm.scale(glm.mat4(1.0), size)
        self.world_to_local = glm.inverse(self.local_to_world)
        self.material = material if material is not None else Material.flat_red()
        self.object_id = object_id

    def _intersect_triangle(
        self, ray_origin: glm.vec3, ray_dir: glm.vec3, v0: glm.vec3, v1: glm.vec3, v2: glm.vec3
    ) -> tuple[float, glm.vec3] | None:
        """Möller-Trumbore ray-triangle intersection."""
        e1 = v1 - v0
        e2 = v2 - v0
        h = glm.cross(ray_dir, e2)
        a = glm.dot(e1, h)

        if -1e-6 < a < 1e-6:
            return None  # Ray is parallel to triangle

        f = 1.0 / a
        s = ray_origin - v0
        u = f * glm.dot(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = glm.cross(s, e1)
        v = f * glm.dot(ray_dir, q)

        if v < 0.0 or u + v > 1.0:
            return None

        t = f * glm.dot(e2, q)

        if t > EPSILON:
            # Calculate geometric normal
            n = glm.normalize(glm.cross(e1, e2))
            
            # Ensure the normal points OUTWARD relative to the origin (0,0,0) of the tetrahedron.
            # v0 is a point on the surface. For an outward normal from origin, dot(n, v0) should be > 0.
            if glm.dot(n, v0) < 0:
                n = -n
            return t, n

        return None

    def intersect(self, ray: Ray) -> HitRecord | None:
        """Test ray-tetrahedron intersection in local space.

        Args:
            ray: World-space ray to test.

        Returns:
            HitRecord if intersection found, None otherwise.
        """
        # Transform ray to local space
        origin_local = glm.vec3(self.world_to_local * glm.vec4(ray.origin, 1.0))
        dir_local_raw = glm.vec3(self.world_to_local * glm.vec4(ray.direction, 0.0))
        dir_local = glm.normalize(dir_local_raw)

        closest_t = float('inf')
        closest_n = None

        # Check intersection with all 4 triangular faces
        for face in self.faces:
            res = self._intersect_triangle(
                origin_local, dir_local,
                self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[2]]
            )
            if res is not None:
                t, n = res
                if t < closest_t:
                    closest_t = t
                    closest_n = n

        if closest_t == float('inf') or closest_t < EPSILON:
            return None

        # Hit point in local space
        hit_local = origin_local + closest_t * dir_local

        # Transform hit point to world space
        hit_world = glm.vec3(self.local_to_world * glm.vec4(hit_local, 1.0))

        # Transform normal to world space using inverse-transpose
        inv_transpose = glm.transpose(glm.mat3(self.world_to_local))
        normal_world = glm.normalize(inv_transpose * closest_n)

        # Compute world-space t
        t_world = glm.length(hit_world - ray.origin)
        if glm.dot(ray.direction, hit_world - ray.origin) < 0:
            t_world = -t_world

        return HitRecord(
            t_world, hit_world, normal_world, self.material, self.object_id
        )
