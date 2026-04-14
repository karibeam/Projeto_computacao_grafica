"""Ray-object intersection routines.

Finds the closest intersection between a ray and all objects in the scene.
"""

from __future__ import annotations

from src.models.ray import HitRecord, Ray
from src.models.scene import Scene


def find_closest_hit(ray: Ray, scene: Scene) -> HitRecord | None:
    """Find the closest intersection between a ray and all scene objects.

    Iterates through all objects in the scene, testing each for intersection,
    and returns the HitRecord with the smallest positive t value.

    Args:
        ray: The ray to test.
        scene: The scene containing objects.

    Returns:
        HitRecord for the closest hit, or None if no intersection.
    """
    closest: HitRecord | None = None

    for obj in scene.objects:
        hit = obj.intersect(ray)
        if hit is not None and (closest is None or hit.t < closest.t):
            closest = hit

    return closest
