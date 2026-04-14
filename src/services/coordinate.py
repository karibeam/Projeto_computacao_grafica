"""Coordinate transformation helpers.

All intersection math is done in local coordinates. These helpers provide
convenience functions for converting between local and world spaces.
"""

from __future__ import annotations

from pyglm import glm


def local_to_world_transform(local_point: glm.vec3, matrix: glm.mat4) -> glm.vec3:
    """Transform a point from local to world space.

    Args:
        local_point: Point in local/object space.
        matrix: Local-to-world transformation matrix.

    Returns:
        Point in world space.
    """
    return glm.vec3(matrix * glm.vec4(local_point, 1.0))


def world_to_local_transform(
    world_point: glm.vec3, inverse_matrix: glm.mat4
) -> glm.vec3:
    """Transform a point from world to local space.

    Args:
        world_point: Point in world space.
        inverse_matrix: World-to-local transformation matrix (inverse of local-to-world).

    Returns:
        Point in local/object space.
    """
    return glm.vec3(inverse_matrix * glm.vec4(world_point, 1.0))
