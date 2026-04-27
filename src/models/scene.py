"""Scene composition — objects, lights, and camera."""

from __future__ import annotations

from typing import Union  # noqa: F401

from pyglm import glm

from src.models.camera import PinholeCamera
from src.models.geometry import Box, Ellipsoid, Plane, Sphere, Tetrahedron
from src.models.light import AreaLight, PointLight
from src.models.material import Material

SceneObject = Sphere | Ellipsoid | Plane | Box | Tetrahedron
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
            eye=glm.vec3(0.0, 0.5, 5.0),
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
            position=glm.vec3(0.0, 3.0, 3.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )
        # Point lights for step 3 dual-light variant
        point_light_left = PointLight(
            position=glm.vec3(-3.0, 3.0, 0.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )

        point_light_right = PointLight(
            position=glm.vec3(3.0, 3.0, 0.0),
            intensity=glm.vec3(3.0, 3.0, 3.0),
        )

        import math
        
        # Box for step 7: positioned at same location as sphere, but rotated to be visible in 3D
        box = Box(
            center=glm.vec3(0.0, 1.0, 0.0),
            size=glm.vec3(1.2, 1.2, 1.2),
            rotation=glm.vec3(math.radians(30), math.radians(45), 0.0),
            object_id=3,
        )

        # Area light for step 5: positioned above the ellipsoid
        # Using uniform sampling with 32 samples per pixel
        area_light_step5 = AreaLight(
            corner=glm.vec3(-2.0, 5.0, -2.0),
            edge_u=glm.vec3(4.0, 0.0, 0.0),
            edge_v=glm.vec3(0.0, 0.0, 4.0),
            intensity=glm.vec3(5.0, 5.0, 5.0),
        )

        # Area light for step 6: rectangular light above the sphere
        # Using uniform sampling with 16 samples per pixel
        area_light_step6 = AreaLight(
            corner=glm.vec3(-2.0, 5.0, -2.0),
            edge_u=glm.vec3(4.0, 0.0, 0.0),
            edge_v=glm.vec3(0.0, 0.0, 4.0),
            intensity=glm.vec3(5.0, 5.0, 5.0),
        )

        scenes: dict[int, Scene] = {}

        # Ambient per step: step 1 = 0.1, steps 1.5-6 = 0.2
        ambient_1 = glm.vec3(0.1, 0.1, 0.1)
        ambient_15to6 = glm.vec3(0.2, 0.2, 0.2)

        # Step 1: point light, flat red, no shadows
        scenes[1] = cls(
            objects=[sphere, plane],
            lights=[point_light],
            camera=camera,
            ambient_light=ambient_1,
        )

        # Step 1.5: point light, flat color with shadows (no Phong)
        scenes[15] = cls(
            objects=[sphere, plane],
            lights=[point_light_bright],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 2: point light (bright), Phong, shadows
        scenes[2] = cls(
            objects=[sphere, plane],
            lights=[point_light_bright],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 3: point light (bright), Phong, shadows, antialiasing
        # Single light variant (rendered separately)
        scenes[3] = cls(
            objects=[sphere, plane],
            lights=[point_light_bright],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 3 dual light variant (rendered separately)
        scenes[31] = cls(
            objects=[sphere, plane],
            lights=[point_light_left, point_light_right],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 4: area light (rectangular) with uniform sampling (16 samples), sphere
        # Replaced point light with area light for soft shadows
        scenes[4] = cls(
            objects=[sphere, plane],
            lights=[area_light_step6],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 5: area light (rectangular) with uniform sampling (24 samples), ellipsoid
        # Camera: moved back to see full ellipsoid (center at y=1.8, height ~3.6)
        # Using same area light configuration as step 6
        camera_step5 = PinholeCamera(
            eye=glm.vec3(0.0, 3.0, 7.0),
            look_at=glm.vec3(0.0, 1.8, 0.0),
        )
        scenes[5] = cls(
            objects=[ellipsoid, plane],
            lights=[area_light_step6],
            camera=camera_step5,
            ambient_light=ambient_15to6,
        )

        # Step 6: area light (rectangular) with uniform sampling (16 samples), sphere
        # Same camera as step 4 for direct comparison
        scenes[6] = cls(
            objects=[sphere, plane],
            lights=[area_light_step6],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 7: box with point light (bright), Phong, shadows
        # Same illumination as steps 2-4 (single point light)
        scenes[7] = cls(
            objects=[box, plane],
            lights=[point_light_bright],
            camera=camera,
            ambient_light=ambient_15to6,
        )

        # Step 8: box and tetrahedron side by side
        tetra_size = 1.8
        tetra_center = glm.vec3(1.2, tetra_size * 0.5 / math.sqrt(3), -0.5)
        tetrahedron = Tetrahedron(
            center=tetra_center,
            size=glm.vec3(tetra_size, tetra_size, tetra_size),
            rotation=glm.vec3(math.atan(-math.sqrt(2)), -math.radians(45), 0.0),
            material=Material(color=glm.vec3(0.1, 0.4, 1.0)),
            object_id=4,
        )
        
        # Spin the tetrahedron around its vertical axis to show the lateral face
        spin_mat = glm.rotate(glm.mat4(1.0), math.radians(30), glm.vec3(0.0, 1.0, 0.0))
        spin_transform = glm.translate(glm.mat4(1.0), tetra_center) * spin_mat * glm.translate(glm.mat4(1.0), -tetra_center)
        tetrahedron.local_to_world = spin_transform * tetrahedron.local_to_world
        tetrahedron.world_to_local = glm.inverse(tetrahedron.local_to_world)
        box_size = 1.2
        box_step8 = Box(
            center=glm.vec3(-1.2, box_size / 2.0, 1.5),
            size=glm.vec3(box_size, box_size, box_size),
            rotation=glm.vec3(0.0, math.radians(45), 0.0),
            object_id=3,
        )
        camera_step8 = PinholeCamera(
            eye=glm.vec3(0.0, 1.5, 7.5),
            look_at=glm.vec3(0.0, 1.0, 0.0),
        )
        scenes[8] = cls(
            objects=[box_step8, tetrahedron, plane],
            lights=[point_light_left, point_light_right],
            camera=camera_step8,
            ambient_light=ambient_15to6,
        )

        # Step 9: Cornell Box with Area Light
        floor = Plane(point=glm.vec3(0.0, 0.0, 0.0), normal=glm.vec3(0.0, 1.0, 0.0), material=Material(color=glm.vec3(0.8, 0.8, 0.8)), object_id=10)
        ceiling = Plane(point=glm.vec3(0.0, 6.0, 0.0), normal=glm.vec3(0.0, -1.0, 0.0), material=Material(color=glm.vec3(0.8, 0.8, 0.8)), object_id=11)
        back_wall = Plane(point=glm.vec3(0.0, 0.0, -3.0), normal=glm.vec3(0.0, 0.0, 1.0), material=Material(color=glm.vec3(0.8, 0.8, 0.8)), object_id=12)
        left_wall = Plane(point=glm.vec3(-3.0, 0.0, 0.0), normal=glm.vec3(1.0, 0.0, 0.0), material=Material(color=glm.vec3(0.8, 0.1, 0.1)), object_id=13)
        right_wall = Plane(point=glm.vec3(3.0, 0.0, 0.0), normal=glm.vec3(-1.0, 0.0, 0.0), material=Material(color=glm.vec3(0.1, 0.8, 0.1)), object_id=14)

        area_light_step9 = AreaLight(
            corner=glm.vec3(-1.5, 5.9, -1.5),
            edge_u=glm.vec3(3.0, 0.0, 0.0),
            edge_v=glm.vec3(0.0, 0.0, 3.0),
            intensity=glm.vec3(1.5, 1.5, 1.5),
        )

        scenes[9] = cls(
            objects=[box_step8, tetrahedron, floor, ceiling, back_wall, left_wall, right_wall],
            lights=[area_light_step9],
            camera=camera_step8,
            ambient_light=ambient_15to6,
        )

        # Step 10: Reflective sphere and visual area light in Cornell Box
        ceiling_10 = Plane(point=glm.vec3(0.0, 6.0, 0.0), normal=glm.vec3(0.0, -1.0, 0.0), material=Material(color=glm.vec3(0.8, 0.8, 0.8)), object_id=11)
        
        area_light_step10 = AreaLight(
            corner=glm.vec3(-0.2, 5.9, 2.8),
            edge_u=glm.vec3(0.4, 0.0, 0.0),
            edge_v=glm.vec3(0.0, 0.0, 0.4),
            intensity=glm.vec3(1.5, 1.5, 1.5),
        )
        
        light_box = Box(
            center=glm.vec3(0.0, 5.95, 3.0),
            size=glm.vec3(0.4, 0.05, 0.4),
            rotation=glm.vec3(0.0, 0.0, 0.0),
            material=Material(color=glm.vec3(1.0, 1.0, 1.0), is_emissive=True),
            object_id=15,
        )
        
        mirror_sphere = Sphere(
            center=glm.vec3(-1.2, 1.7, 1.5),
            radius=0.5,
            material=Material(color=glm.vec3(0.1, 0.1, 0.1), specular=0.9, shininess=100.0, reflectivity=0.85),
            object_id=16,
        )

        camera_step10 = PinholeCamera(
            eye=glm.vec3(0.0, 2.0, 8.5),
            look_at=glm.vec3(0.0, 3.0, 1.0),
        )

        scenes[10] = cls(
            objects=[box_step8, tetrahedron, mirror_sphere, light_box, floor, ceiling_10, back_wall, left_wall, right_wall],
            lights=[area_light_step10],
            camera=camera_step10)

        return scenes
