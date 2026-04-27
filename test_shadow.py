import sys
from pyglm import glm
from src.models.ray import Ray
from src.models.scene import Scene
from src.models.geometry import Tetrahedron
import math

tetra_size = 1.8
tetra_center = glm.vec3(1.2, tetra_size * 0.5 / math.sqrt(3), -0.5)
from src.models.material import Material
tetrahedron = Tetrahedron(
    center=tetra_center,
    size=glm.vec3(tetra_size, tetra_size, tetra_size),
    rotation=glm.vec3(math.atan(-math.sqrt(2)), -math.radians(45), 0.0),
    material=Material(color=glm.vec3(0.1, 0.4, 1.0)),
    object_id=4,
)

spin_mat = glm.rotate(glm.mat4(1.0), math.radians(30), glm.vec3(0.0, 1.0, 0.0))
spin_transform = glm.translate(glm.mat4(1.0), tetra_center) * spin_mat * glm.translate(glm.mat4(1.0), -tetra_center)
tetrahedron.local_to_world = spin_transform * tetrahedron.local_to_world
tetrahedron.world_to_local = glm.inverse(tetrahedron.local_to_world)

# Ray from floor right under tetrahedron:
floor_pos = glm.vec3(1.2, 0.01, -0.5)
light_pos = glm.vec3(0.0, 5.9, 0.0)

ray_dir = glm.normalize(light_pos - floor_pos)
ray = Ray(floor_pos, ray_dir)

hit = tetrahedron.intersect(ray)
print(f"Shadow ray hit: {hit is not None}")
if hit:
    print(f"Hit t: {hit.t}")
