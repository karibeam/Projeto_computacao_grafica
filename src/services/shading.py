"""Illumination models: flat color and Phong.

Implements:
- Flat color (step 1): simple light intensity attenuation with no material model.
- Phong (steps 2+): ambient + diffuse + specular using the Blinn-Phong variant.
"""

from __future__ import annotations

import random
from collections.abc import Callable

from pyglm import glm

from src.models.light import AreaLight, PointLight
from src.models.ray import HitRecord
from src.models.scene import Scene
from src.services.sampling import generate_uniform_area_samples


def compute_flat_color(
    hit: HitRecord,
    scene: Scene,
    use_shadows: bool = False,
) -> glm.vec3:
    """Compute flat color shading — only the base color modulated by light.

    In step 1, the sphere is rendered as pure red with no material model.
    The light simply determines if a surface point is illuminated or not.

    Args:
        hit: Intersection record.
        scene: The scene containing lights.
        use_shadows: Whether to cast shadow rays.

    Returns:
        RGB color vector.
    """
    color = glm.vec3(0.0)

    for light in scene.lights:
        if isinstance(light, PointLight):
            light_dir = light.position - hit.point
            light_dist = glm.length(light_dir)
            light_dir_norm = glm.normalize(light_dir)

            if use_shadows:
                # Simple shadow check — binary (in shadow or not)
                shadow = _is_in_shadow_point(
                    hit.point, hit.normal, light_dir_norm, light_dist, scene
                )
                if shadow:
                    continue

            # Simple attenuation (inverse square)
            attenuation = 1.0 / (
                1.0 + 0.1 * light_dist + 0.01 * light_dist * light_dist
            )
            color += light.intensity * attenuation * hit.material.color

        elif isinstance(light, AreaLight):
            # For flat color with area light, use center point
            light_dir = light.center - hit.point
            light_dist = glm.length(light_dir)
            light_dir_norm = glm.normalize(light_dir)

            if use_shadows:
                shadow = _is_in_shadow_point(
                    hit.point, hit.normal, light_dir_norm, light_dist, scene
                )
                if shadow:
                    continue

            attenuation = 1.0 / (
                1.0 + 0.05 * light_dist + 0.01 * light_dist * light_dist
            )
            color += light.intensity * attenuation * hit.material.color

    # Add ambient
    color += scene.ambient_light * hit.material.color

    return glm.clamp(color, 0.0, 1.0)  # type: ignore[no-any-return]


def compute_phong(
    hit: HitRecord,
    scene: Scene,
    view_dir: glm.vec3,
    use_shadows: bool = True,
    light_samples: int = 1,
    rng: Callable[[], tuple[float, float]] | random.Random | None = None,
) -> glm.vec3:
    """Compute Phong illumination using the Blinn-Phong variant.

    Components:
    - Ambient: k_a * ambient_light
    - Diffuse: k_d * I_l * max(0, N · L)
    - Specular: k_s * I_l * max(0, N · H)^n  (H = normalize(L + V))

    Args:
        hit: Intersection record.
        scene: The scene containing lights.
        view_dir: Normalized vector from hit point toward the camera.
        use_shadows: Whether to cast shadow rays.
        light_samples: Number of samples for area lights.
        rng: Random number generator callable returning (u, v) in [0, 1).

    Returns:
        RGB color vector.
    """
    color = glm.vec3(0.0)
    mat = hit.material
    
    if getattr(mat, "is_emissive", False):
        return mat.color * 3.0
        
    N = hit.normal
    V = view_dir

    # Ambient component
    color += mat.ambient * scene.ambient_light * mat.color

    for light in scene.lights:
        if isinstance(light, PointLight):
            light_dir = light.position - hit.point
            light_dist = glm.length(light_dir)
            L = glm.normalize(light_dir)

            # Shadow check
            if use_shadows and _is_in_shadow_point(
                hit.point, N, L, light_dist, scene
            ):
                continue

            # Diffuse
            NdotL = max(0.0, glm.dot(N, L))
            diffuse = mat.diffuse * light.intensity * NdotL * mat.color

            # Specular (Blinn-Phong)
            specular = glm.vec3(0.0)
            if NdotL > 0:
                H = glm.normalize(L + V)
                NdotH = max(0.0, glm.dot(N, H))
                specular = mat.specular * light.intensity * (NdotH**mat.shininess)

            # Attenuation
            attenuation = 1.0 / (
                1.0 + 0.1 * light_dist + 0.01 * light_dist * light_dist
            )
            color += (diffuse + specular) * attenuation

        elif isinstance(light, AreaLight):
            # Area light: sample multiple points (Monte Carlo)
            samples = generate_uniform_area_samples(light, light_samples, rng)
            for sample_point in samples:
                light_dir = sample_point - hit.point
                light_dist = glm.length(light_dir)
                L = glm.normalize(light_dir)

                # Shadow check
                if use_shadows and _is_in_shadow_area(
                    hit.point, N, L, light_dist, light, scene
                ):
                    continue

                # Diffuse
                NdotL = max(0.0, glm.dot(N, L))
                diffuse = mat.diffuse * light.intensity * NdotL * mat.color

                # Specular (Blinn-Phong)
                specular = glm.vec3(0.0)
                if NdotL > 0:
                    H = glm.normalize(L + V)
                    NdotH = max(0.0, glm.dot(N, H))
                    specular = mat.specular * light.intensity * (NdotH**mat.shininess)

                # Distance attenuation (reduced for area lights)
                attenuation = 1.0 / (
                    1.0 + 0.01 * light_dist + 0.001 * light_dist * light_dist
                )
                color += (diffuse + specular) * attenuation

            # Average over samples
            if light_samples > 1:
                color /= light_samples

    return glm.clamp(color, 0.0, 1.0)  # type: ignore[no-any-return]


def _is_in_shadow_point(
    point: glm.vec3,
    normal: glm.vec3,
    light_dir: glm.vec3,
    light_dist: float,
    scene: Scene,
) -> bool:
    """Check if a point is in shadow from a point light.

    Args:
        point: Surface point.
        normal: Surface normal at the hit point.
        light_dir: Normalized direction toward the light.
        light_dist: Distance to the light.
        scene: The scene.

    Returns:
        True if the point is in shadow.
    """
    from src.models.ray import Ray
    from src.services.intersection import find_closest_hit

    # Offset along normal to prevent self-intersection (shadow acne)
    offset = max(0.01, 0.01 * glm.length(light_dir))
    shadow_origin = point + normal * offset
    shadow_ray = Ray(shadow_origin, light_dir)
    shadow_hit = find_closest_hit(shadow_ray, scene)
    return shadow_hit is not None and shadow_hit.t < light_dist


def _is_in_shadow_area(
    point: glm.vec3,
    normal: glm.vec3,
    light_dir: glm.vec3,
    light_dist: float,
    area_light: AreaLight,
    scene: Scene,
) -> bool:
    """Check if a point is in shadow from a specific point on an area light.

    Args:
        point: Surface point.
        normal: Surface normal at the hit point.
        light_dir: Normalized direction toward the sampled light point.
        light_dist: Distance to the sampled light point.
        area_light: The area light.
        scene: The scene.

    Returns:
        True if the point is in shadow for this sample.
    """
    from src.models.ray import Ray
    from src.services.intersection import find_closest_hit

    # Offset along normal to prevent self-intersection (shadow acne)
    offset = max(0.01, 0.01 * glm.length(light_dir))
    shadow_origin = point + normal * offset
    shadow_ray = Ray(shadow_origin, light_dir)
    shadow_hit = find_closest_hit(shadow_ray, scene)
    return shadow_hit is not None and shadow_hit.t < light_dist
