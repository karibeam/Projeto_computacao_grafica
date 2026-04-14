"""Unit tests for coordinate transformations."""

import pytest
from pyglm import glm

from src.services.coordinate import local_to_world_transform, world_to_local_transform


class TestCoordinateTransforms:
    """Tests for local ↔ world coordinate transformations."""

    def test_local_to_world_translation(self) -> None:
        """Test translating a point from local to world space."""
        matrix = glm.translate(glm.mat4(1.0), glm.vec3(5.0, 3.0, 1.0))
        local_point = glm.vec3(0.0, 0.0, 0.0)

        world_point = local_to_world_transform(local_point, matrix)

        assert world_point.x == pytest.approx(5.0)
        assert world_point.y == pytest.approx(3.0)
        assert world_point.z == pytest.approx(1.0)

    def test_world_to_local_translation(self) -> None:
        """Test translating a point from world to local space."""
        matrix = glm.translate(glm.mat4(1.0), glm.vec3(5.0, 3.0, 1.0))
        inv_matrix = glm.inverse(matrix)
        world_point = glm.vec3(5.0, 3.0, 1.0)

        local_point = world_to_local_transform(world_point, inv_matrix)

        assert local_point.x == pytest.approx(0.0)
        assert local_point.y == pytest.approx(0.0)
        assert local_point.z == pytest.approx(0.0)

    def test_roundtrip(self) -> None:
        """Test that local→world→local returns the original point."""
        matrix = glm.translate(glm.mat4(1.0), glm.vec3(1.0, 2.0, 3.0)) * glm.scale(
            glm.mat4(1.0), glm.vec3(2.0)
        )
        inv_matrix = glm.inverse(matrix)
        original = glm.vec3(1.0, 1.0, 1.0)

        world = local_to_world_transform(original, matrix)
        back = world_to_local_transform(world, inv_matrix)

        assert back.x == pytest.approx(original.x, abs=1e-5)
        assert back.y == pytest.approx(original.y, abs=1e-5)
        assert back.z == pytest.approx(original.z, abs=1e-5)

    def test_scale_transform(self) -> None:
        """Test scaling a point from local to world space."""
        matrix = glm.scale(glm.mat4(1.0), glm.vec3(3.0, 2.0, 1.0))
        local_point = glm.vec3(1.0, 1.0, 1.0)

        world_point = local_to_world_transform(local_point, matrix)

        assert world_point.x == pytest.approx(3.0)
        assert world_point.y == pytest.approx(2.0)
        assert world_point.z == pytest.approx(1.0)
