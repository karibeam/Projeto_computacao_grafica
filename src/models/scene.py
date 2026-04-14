"""Scene composition — objects, lights, and camera."""

from __future__ import annotations

from typing import Union  # noqa: F401

from pyglm import glm

from src.models.camera import PinholeCamera
from src.models.geometry import Ellipsoid, Plane, Sphere
from src.models.light import AreaLight, PointLight

SceneObject = Sphere | Ellipsoid | Plane
SceneLight = PointLight | AreaLight


class Scene:
    """Composition of all geometric objects, lights, and a camera.

    Attributes:
        objects: Ordered list of scene geometry.
        lights: Ordered list of light sources.
        camera: View camera.
        ambient_light: Global ambient light color.
    """

    __slots__ = ("objects", "lights", "camera", "ambient_light")

    def __init__(
        self,
        objects: list[SceneObject] | None = None,
        lights: list[SceneLight] | None = None,
        camera: PinholeCamera | None = None,
        ambient_light: glm.vec3 = glm.vec3(0.05, 0.05, 0.05),
    ) -> None:
        """Initialize a Scene.

        Args:
            objects: List of geometric objects.
            lights: List of light sources.
            camera: View camera.
            ambient_light: Global ambient light intensity.
        """
        self.objects: list[SceneObject] = objects if objects is not None else []
        self.lights: list[SceneLight] = lights if lights is not None else []
        self.camera: PinholeCamera = camera if camera is not None else PinholeCamera()
        self.ambient_light = ambient_light

    @classmethod
    def default_step1(cls) -> Scene:
        """Create the default scene for step 1 (point light, flat red sphere, no shadows)."""
        camera = PinholeCamera(
            eye=glm.vec3(0.0, 2.0, 5.0),
            look_at=glm.vec3(0.0, 1.0, 0.0),
        )
        sphere = Sphere(
            center=glm.vec3(0.0, 1.0, 0.0),
            radius=1.0,
            object_id=0,
        )
        plane = Plane(
            point=glm.vec3(0.0, 0.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            object_id=2,
        )
        light = PointLight(
            position=glm.vec3(0.0, 2.0, 3.0),
            intensity=glm.vec3(1.0, 1.0, 1.0),
        )
        return cls(
            objects=[sphere, plane],
            lights=[light],
            camera=camera,
        )

    @classmethod
    def default_steps(cls) -> dict[int, Scene]:
        """Create scenes for all 5 steps.

        Returns:
            Dictionary mapping step number (1-5) to Scene.
        """
        # Camera: positioned at (0, 2, 5), pointing at sphere center (0, 1, 0)
        camera = PinholeCamera(
            eye=glm.vec3(0.0, 2.0, 5.0),
            look_at=glm.vec3(0.0, 1.0, 0.0),
        )

        # Step 1-3: sphere; Step 5: ellipsoid (standing upright: taller on Y)
        sphere = Sphere(
            center=glm.vec3(0.0, 1.0, 0.0),
            radius=1.0,
            object_id=0,
        )
        ellipsoid = Ellipsoid(
            center=glm.vec3(0.0, 1.8, 0.0),
            radii=glm.vec3(0.7, 1.8, 0.6),
            object_id=0,
        )
        plane = Plane(
            point=glm.vec3(0.0, 0.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            object_id=2,
        )

        # Point light: centered above the sphere
        point_light = PointLight(
            position=glm.vec3(0.0, 2.0, 3.0),
            intensity=glm.vec3(2.0, 2.0, 2.0),
        )
        # Brighter point light for steps 2-4 so specular highlights are visible
        point_light_bright = PointLight(
            position=glm.vec3(0.0, 2.0, 3.0),
            intensity=glm.vec3(4.0, 4.0, 4.0),
        )
        # Point lights for step 4: two lights, one on LEFT and one on RIGHT
        # Both positioned closer to the sphere for stronger illumination
        point_light_left = PointLight(
            position=glm.vec3(-3.0, 3.0, 0.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )

        point_light_right = PointLight(
            position=glm.vec3(3.0, 3.0, 0.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )

        # Area light for step 4.1: positioned on the LEFT side, centered
        area_light_41 = AreaLight(
            corner=glm.vec3(-3.5, 3.0, 0.0),
            edge_u=glm.vec3(0.0, 0.0, 2.0),
            edge_v=glm.vec3(0.0, -2.0, 0.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )

        # Point light for step 4.1: positioned on the RIGHT side, centered
        # Opposite side from the area light
        point_light_41 = PointLight(
            position=glm.vec3(3.0, 3.0, 0.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )

        scenes: dict[int, Scene] = {}

        # Ambient per step: step 1 = 0.1, steps 2-5 = 0.2
        ambient_1 = glm.vec3(0.1, 0.1, 0.1)
        ambient_2to5 = glm.vec3(0.2, 0.2, 0.2)

        # Step 1: point light, flat red, no shadows
        scenes[1] = cls(
            objects=[sphere, plane],
            lights=[point_light],
            camera=camera,
            ambient_light=ambient_1,
        )

        # Step 2: point light (bright), Phong, shadows
        scenes[2] = cls(
            objects=[sphere, plane],
            lights=[point_light_bright],
            camera=camera,
            ambient_light=ambient_2to5,
        )

        # Step 3: point light (bright), Phong, shadows, antialiasing
        scenes[3] = cls(
            objects=[sphere, plane],
            lights=[point_light_bright],
            camera=camera,
            ambient_light=ambient_2to5,
        )

        # Step 4: two point lights (left + right), Phong, shadows, antialiasing
        scenes[4] = cls(
            objects=[sphere, plane],
            lights=[point_light_left, point_light_right],
            camera=camera,
            ambient_light=ambient_2to5,
        )

        # Step 4.1: same as step 3 (point light + Phong + AA) but with
        # area light instead of point light — test for shadow + penumbra
        # Now includes both area light (soft shadows) and point light (hard shadows)
        scenes[4.1] = cls(
            objects=[sphere, plane],
            lights=[area_light_41, point_light_41],
            camera=camera,
            ambient_light=ambient_2to5,
        )

        # Step 5: area light (left), Phong, ellipsoid
        # Camera: moved back to see full ellipsoid (center at y=1.8, height ~3.6)
        camera_step5 = PinholeCamera(
            eye=glm.vec3(0.0, 3.0, 7.0),
            look_at=glm.vec3(0.0, 1.8, 0.0),
        )
        scenes[5] = cls(
            objects=[ellipsoid, plane],
            lights=[area_light_41],
            camera=camera_step5,
            ambient_light=ambient_2to5,
        )

        return scenes
