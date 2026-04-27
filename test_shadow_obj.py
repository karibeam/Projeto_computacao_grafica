import sys
from pyglm import glm
from src.models.ray import Ray
from src.models.scene import Scene
from src.services.intersection import find_closest_hit

scenes = Scene.default_steps()
scene11 = scenes[11]

for ix in range(25):
    x = 0.0 + ix * 0.1
    pos = glm.vec3(x, 0.0, -0.5)
    light = scene11.lights[0]
    light_dir = glm.normalize(light.position - pos)
    ray = Ray(pos + glm.vec3(0,1,0)*0.01, light_dir)
    hit = find_closest_hit(ray, scene11)
    
    obj_id = hit.object_id if hit else -1
    print(f"x={x:.1f} hit_obj={obj_id} (11=ceiling, 3=box, 4=tetrahedron)")
