"""Light source definitions: point light and area light."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from pyglm import glm

if TYPE_CHECKING:
    pass


class PointLight:
    """A zero-dimensional light source emitting equally in all directions.

    Attributes:
        position: Light position in world space.
        intensity: Light color/intensity (RGB).
    """

    __slots__ = ("position", "intensity")

    def __init__(
        self,
        position: glm.vec3 = glm.vec3(5.0, 8.0, 5.0),
        intensity: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
    ) -> None:
        """Initialize a PointLight.

        Args:
            position: World-space position.
            intensity: RGB light intensity.
        """
        self.position = position
        self.intensity = intensity


class AreaLight:
    """A two-dimensional rectangular light source producing soft shadows.

    A random point on the light surface is computed as:
        corner + u * edge_u + v * edge_v,  where u, v ~ Uniform(0, 1).

    Attributes:
        corner: One corner of the rectangular light in world space.
        edge_u: First edge vector defining the light's extent.
        edge_v: Second edge vector defining the light's extent.
        intensity: Light color/intensity (RGB).
    """

    __slots__ = (
        "corner",
        "edge_u",
        "edge_v",
        "intensity",
        "_area",
        "_center",
        "_normal",
    )

    def __init__(
        self,
        corner: glm.vec3 = glm.vec3(3.0, 6.0, 3.0),
        edge_u: glm.vec3 = glm.vec3(4.0, 0.0, 0.0),
        edge_v: glm.vec3 = glm.vec3(0.0, 0.0, 4.0),
        intensity: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
    ) -> None:
        """Initialize an AreaLight.

        Args:
            corner: World-space corner point.
            edge_u: First edge vector.
            edge_v: Second edge vector.
            intensity: RGB light intensity.
        """
        self.corner = corner
        self.edge_u = edge_u
        self.edge_v = edge_v
        self.intensity = intensity

        cross = glm.cross(edge_u, edge_v)
        self._area = glm.length(cross)
        self._center = corner + 0.5 * edge_u + 0.5 * edge_v
        self._normal = (
            glm.normalize(cross) if self._area > 0 else glm.vec3(0.0, 1.0, 0.0)
        )

    @property
    def area(self) -> float:
        """Return the surface area of the light."""
        return self._area

    @property
    def center(self) -> glm.vec3:
        """Return the center point of the light."""
        return self._center

    @property
    def normal(self) -> glm.vec3:
        """Return the surface normal of the light."""
        return self._normal

    def sample_point(self, rng: Callable[[], tuple[float, float]]) -> glm.vec3:
        """Sample a random point on the light surface.

        Args:
            rng: A callable returning (u, v) where u, v ~ Uniform(0, 1).

        Returns:
            A random point on the rectangular light surface.
        """
        u, v = rng()
        return self.corner + u * self.edge_u + v * self.edge_v
