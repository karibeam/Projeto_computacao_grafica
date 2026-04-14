"""Unit tests for shading functions."""

from pyglm import glm

from src.models.light import PointLight
from src.models.material import Material
from src.models.ray import HitRecord
from src.models.scene import Scene
from src.services.shading import compute_flat_color, compute_phong


class TestFlatColor:
    """Tests for flat color shading."""

    def test_flat_color_illuminated(self) -> None:
        """Test flat color returns surface color when lit."""
        mat = Material(color=glm.vec3(1.0, 0.0, 0.0))  # Red
        hit = HitRecord(
            t=1.0,
            point=glm.vec3(0.0, 1.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            material=mat,
            object_id=0,
        )
        light = PointLight(
            position=glm.vec3(0.0, 5.0, 0.0),
            intensity=glm.vec3(1.0, 1.0, 1.0),
        )
        scene = Scene(objects=[], lights=[light])

        color = compute_flat_color(hit, scene, use_shadows=False)
        # Should be reddish (ambient + light contribution)
        assert color.r > 0.0

    def test_flat_color_no_shadows(self) -> None:
        """Test that flat color with use_shadows=False ignores shadows."""
        mat = Material(color=glm.vec3(1.0, 0.0, 0.0))
        hit = HitRecord(
            t=1.0,
            point=glm.vec3(0.0, 1.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            material=mat,
            object_id=0,
        )
        light = PointLight(
            position=glm.vec3(0.0, 5.0, 0.0),
            intensity=glm.vec3(1.0, 1.0, 1.0),
        )
        scene = Scene(objects=[], lights=[light])

        color_no_shadows = compute_flat_color(hit, scene, use_shadows=False)
        # Should return color regardless of shadow state
        assert color_no_shadows.r > 0.0


class TestPhong:
    """Tests for Phong shading."""

    def test_phong_diffuse(self) -> None:
        """Test Phong model produces diffuse component."""
        mat = Material(
            color=glm.vec3(1.0, 1.0, 1.0),
            ambient=0.1,
            diffuse=0.8,
            specular=0.0,
        )
        hit = HitRecord(
            t=1.0,
            point=glm.vec3(0.0, 0.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            material=mat,
            object_id=0,
        )
        light = PointLight(
            position=glm.vec3(0.0, 5.0, 0.0),
            intensity=glm.vec3(1.0, 1.0, 1.0),
        )
        scene = Scene(objects=[], lights=[light])
        view_dir = glm.vec3(0.0, 1.0, 0.0)  # Looking from above

        color = compute_phong(hit, scene, view_dir, use_shadows=False)
        # Should have significant contribution from diffuse + ambient
        assert color.r > 0.1
        assert color.g > 0.1
        assert color.b > 0.1

    def test_phong_specular(self) -> None:
        """Test Phong model produces specular highlight."""
        mat = Material(
            color=glm.vec3(1.0, 1.0, 1.0),
            ambient=0.0,
            diffuse=0.5,
            specular=1.0,
            shininess=64.0,
        )
        hit = HitRecord(
            t=1.0,
            point=glm.vec3(0.0, 0.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            material=mat,
            object_id=0,
        )
        # Light and view both along normal → max specular
        light = PointLight(
            position=glm.vec3(0.0, 5.0, 0.0),
            intensity=glm.vec3(1.0, 1.0, 1.0),
        )
        scene = Scene(objects=[], lights=[light])
        view_dir = glm.vec3(0.0, 1.0, 0.0)

        color = compute_phong(hit, scene, view_dir, use_shadows=False)
        # Specular should be significant
        assert color.r > 0.5

    def test_phong_clamped(self) -> None:
        """Test that Phong output is clamped to [0, 1]."""
        mat = Material(
            color=glm.vec3(1.0, 1.0, 1.0),
            ambient=1.0,
            diffuse=1.0,
            specular=1.0,
            shininess=1.0,
        )
        hit = HitRecord(
            t=1.0,
            point=glm.vec3(0.0, 0.0, 0.0),
            normal=glm.vec3(0.0, 1.0, 0.0),
            material=mat,
            object_id=0,
        )
        light = PointLight(
            position=glm.vec3(0.0, 5.0, 0.0),
            intensity=glm.vec3(10.0, 10.0, 10.0),  # Very bright
        )
        scene = Scene(objects=[], lights=[light])
        view_dir = glm.vec3(0.0, 1.0, 0.0)

        color = compute_phong(hit, scene, view_dir, use_shadows=False)
        assert color.r <= 1.0
        assert color.g <= 1.0
        assert color.b <= 1.0
