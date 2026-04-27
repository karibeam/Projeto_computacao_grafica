import sys
from pyglm import glm
from src.models.ray import Ray
from src.models.scene import Scene
from src.models.geometry import Tetrahedron, Plane
import math
from src.services.shading import _is_in_shadow_point

# Build the scene just for shadow testing
scenes = Scene.default_steps()
scene11 = scenes[11]

# Let's test floor points along the X axis under the tetrahedron
print("Shadow on floor at z=-0.5 for different X:")
for ix in range(50):
    x = 1.2 + (ix - 25) * 0.1
    pos = glm.vec3(x, 0.0, -0.5)
    light = scene11.lights[0]
    light_dir = light.position - pos
    light_dist = glm.length(light_dir)
    L = glm.normalize(light_dir)
    
    in_shadow = _is_in_shadow_point(pos, glm.vec3(0,1,0), L, light_dist, scene11)
    print("X" if in_shadow else ".", end="")
print("")

