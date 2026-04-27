"""Material definition for surface shading."""

from __future__ import annotations

from pyglm import glm


class Material:
    """Surface properties for Phong-based shading.

    Attributes:
        color: Base surface color (RGB, each component in [0, 1]).
        ambient: Ambient reflection coefficient k_a (default: 0.1).
        diffuse: Diffuse reflection coefficient k_d (default: 0.7).
        specular: Specular reflection coefficient k_s (default: 0.3).
        shininess: Specular exponent n (default: 32.0).
        reflectivity: Reflection factor [0, 1] for recursive rays (default: 0.0).
        is_emissive: Whether the material emits light (bypasses shading) (default: False).
    """

    __slots__ = ("color", "ambient", "diffuse", "specular", "shininess", "reflectivity", "is_emissive")

    def __init__(
        self,
        color: glm.vec3 = glm.vec3(1.0, 1.0, 1.0),
        ambient: float = 0.1,
        diffuse: float = 0.7,
        specular: float = 0.3,
        shininess: float = 32.0,
        reflectivity: float = 0.0,
        is_emissive: bool = False,
    ) -> None:
        """Initialize a Material.

        Args:
            color: RGB base color.
            ambient: Ambient reflection coefficient.
            diffuse: Diffuse reflection coefficient.
            specular: Specular reflection coefficient.
            shininess: Specular highlight sharpness exponent.
            reflectivity: Reflection fraction [0, 1].
            is_emissive: If True, object is self-illuminated.
        """
        self.color = color
        self.ambient = max(0.0, min(1.0, ambient))
        self.diffuse = max(0.0, min(1.0, diffuse))
        self.specular = max(0.0, min(1.0, specular))
        self.shininess = max(1.0, shininess)
        self.reflectivity = max(0.0, min(1.0, reflectivity))
        self.is_emissive = is_emissive

    @classmethod
    def flat_red(cls) -> Material:
        """Create a flat red material (step 1 — no Phong, color only)."""
        return cls(color=glm.vec3(1.0, 0.0, 0.0))

    @classmethod
    def phong_default(cls) -> Material:
        """Create a default Phong material with white color."""
        return cls(color=glm.vec3(1.0, 1.0, 1.0))
