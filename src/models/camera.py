"""Pinhole camera model."""

from __future__ import annotations

from pyglm import glm

from src.models.ray import Ray


class PinholeCamera:
    """A pinhole camera with a rectangular film plane.

    The camera is defined by an eye position, a look-at point, an up vector,
    and a vertical field of view. Rays are cast from the eye through each
    pixel on the film plane.

    Attributes:
        eye: Camera position in world space.
        look_at: Point the camera is looking at.
        up: Up direction vector.
        fov: Vertical field of view in degrees.
        film_width: Number of horizontal pixels.
        film_height: Number of vertical pixels.
    """

    __slots__ = (
        "eye",
        "look_at",
        "up",
        "fov",
        "film_width",
        "film_height",
        "_aspect_ratio",
        "_view_matrix",
        "_inverse_view_matrix",
    )

    def __init__(
        self,
        eye: glm.vec3 = glm.vec3(0.0, 2.0, 5.0),
        look_at: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        up: glm.vec3 = glm.vec3(0.0, 1.0, 0.0),
        fov: float = 60.0,
        film_width: int = 512,
        film_height: int = 512,
    ) -> None:
        """Initialize the pinhole camera.

        Args:
            eye: Camera position.
            look_at: Target point.
            up: Up vector.
            fov: Vertical field of view in degrees.
            film_width: Film width in pixels.
            film_height: Film height in pixels.
        """
        self.eye = eye
        self.look_at = look_at
        self.up = glm.normalize(up)
        self.fov = fov
        self.film_width = film_width
        self.film_height = film_height

        self._aspect_ratio = film_width / film_height
        self._view_matrix = glm.lookAt(self.eye, self.look_at, self.up)
        self._inverse_view_matrix = glm.inverse(self._view_matrix)

    def generate_ray(self, u: float, v: float, jitter: glm.vec2 = glm.vec2(0.0)) -> Ray:
        """Generate a primary ray through the film plane at (u, v).

        Args:
            u: Horizontal coordinate in [0, 1] (0 = left, 1 = right).
            v: Vertical coordinate in [0, 1] (0 = bottom, 1 = top).
            jitter: Sub-pixel jitter offset in normalized [-0.5, 0.5] range.

        Returns:
            A Ray from the eye through the film plane at the given coordinates.
        """
        # Apply jitter in pixel-normalized space
        pixel_u = u + jitter.x / self.film_width
        pixel_v = v + jitter.y / self.film_height

        # Convert to NDC [-1, 1]
        ndc_x = (2.0 * pixel_u - 1.0) * self._aspect_ratio
        ndc_y = 2.0 * pixel_v - 1.0

        # Compute direction in camera space using half-angle
        fov_rad = glm.radians(self.fov)
        half_height = glm.tan(fov_rad / 2.0)
        half_width = half_height * self._aspect_ratio

        camera_dir = glm.vec3(
            ndc_x * half_width,
            ndc_y * half_height,
            -1.0,  # Camera looks along -Z
        )
        camera_dir = glm.normalize(camera_dir)

        # Transform to world space
        world_dir = glm.vec3(self._inverse_view_matrix * glm.vec4(camera_dir, 0.0))
        world_dir = glm.normalize(world_dir)

        return Ray(self.eye, world_dir)
