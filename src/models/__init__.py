"""Geometric primitives, cameras, lights, materials, and scene composition."""

from src.models.camera import PinholeCamera
from src.models.film import Film
from src.models.geometry import Ellipsoid, Plane, Sphere
from src.models.light import AreaLight, PointLight
from src.models.material import Material
from src.models.ray import HitRecord, Ray
from src.models.scene import Scene

__all__ = [
    "Ray",
    "HitRecord",
    "PinholeCamera",
    "Sphere",
    "Ellipsoid",
    "Plane",
    "PointLight",
    "AreaLight",
    "Material",
    "Scene",
    "Film",
]
