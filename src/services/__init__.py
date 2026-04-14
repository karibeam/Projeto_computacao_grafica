"""Rendering pipeline, algorithms, coordinate transforms, and sampling."""

from src.services.coordinate import local_to_world_transform, world_to_local_transform
from src.services.intersection import find_closest_hit
from src.services.pipeline import Pipeline
from src.services.renderer import Renderer
from src.services.sampling import (
    generate_jittered_samples,
    generate_uniform_area_samples,
)
from src.services.shading import compute_flat_color, compute_phong

__all__ = [
    "local_to_world_transform",
    "world_to_local_transform",
    "find_closest_hit",
    "compute_flat_color",
    "compute_phong",
    "generate_jittered_samples",
    "generate_uniform_area_samples",
    "Renderer",
    "Pipeline",
]
