# Data Model: Progressive Pinhole Ray Tracer

**Feature**: 001-raytracer-pinole
**Date**: 2026-04-09

## Entities

### Ray

A directed line segment used for ray-object intersection.

| Field | Type | Description |
|-------|------|-------------|
| `origin` | `glm.vec3` | Starting point of the ray in 3D space |
| `direction` | `glm.vec3` | Normalized direction vector |

**Validation**: `direction` must be normalized (length ≈ 1.0).

**Relationships**: Created by `PinholeCamera` (primary rays) and by `Renderer` at hit points (shadow rays). Passed to intersection routines.

---

### HitRecord

Information about a ray-object intersection.

| Field | Type | Description |
|-------|------|-------------|
| `t` | `float` | Distance along ray from origin to hit point (t > 0 for valid hits) |
| `point` | `glm.vec3` | World-space intersection point |
| `normal` | `glm.vec3` | World-space surface normal at hit point (normalized) |
| `material` | `Material` | Material of the hit object |
| `object_id` | `int` | Identifier of the hit object (for debugging) |

**Validation**: `t > 0.001` (epsilon to avoid self-intersection). `normal` must be normalized.

**State transitions**: N/A (immutable data container).

---

### PinholeCamera

Defines the viewing model with a single viewpoint and a rectangular film plane.

| Field | Type | Description |
|-------|------|-------------|
| `eye` | `glm.vec3` | Camera position in world space |
| `look_at` | `glm.vec3` | Point the camera is looking at |
| `up` | `glm.vec3` | Up direction vector (default: `(0, 1, 0)`) |
| `fov` | `float` | Vertical field of view in degrees |
| `film_width` | `int` | Number of horizontal pixels (default: 512) |
| `film_height` | `int` | Number of vertical pixels (default: 512) |

**Validation**: `fov` in (0, 180). `film_width`, `film_height` > 0. `eye` must not equal `look_at`.

**Derived properties**:
- `view_matrix`: `glm.lookAt(eye, look_at, up)` — world-to-camera transform
- `inverse_view_matrix`: inverse of `view_matrix` — camera-to-world transform
- `aspect_ratio`: `film_width / film_height`

---

### Material

Surface properties for shading.

| Field | Type | Description |
|-------|------|-------------|
| `color` | `glm.vec3` | Base surface color (RGB, each component in [0, 1]) |
| `ambient` | `float` | Ambient reflection coefficient (k_a, default: 0.1) |
| `diffuse` | `float` | Diffuse reflection coefficient (k_d, default: 0.7) |
| `specular` | `float` | Specular reflection coefficient (k_s, default: 0.3) |
| `shininess` | `float` | Specular exponent (n, default: 32.0) |

**Validation**: All color components in [0, 1]. Coefficients in [0, 1]. `shininess` > 0.

**Specialization**: For step 1 (flat color), only `color` is used; all other coefficients are ignored.

---

### PointLight

A zero-dimensional light source emitting equally in all directions.

| Field | Type | Description |
|-------|------|-------------|
| `position` | `glm.vec3` | Light position in world space |
| `intensity` | `glm.vec3` | Light color/intensity (RGB, each component in [0, ∞)) |

**Validation**: `intensity` components ≥ 0.

---

### AreaLight

A two-dimensional rectangular light source producing soft shadows.

| Field | Type | Description |
|-------|------|-------------|
| `corner` | `glm.vec3` | One corner of the rectangular light in world space |
| `edge_u` | `glm.vec3` | First edge vector defining the light's extent |
| `edge_v` | `glm.vec3` | Second edge vector defining the light's extent |
| `intensity` | `glm.vec3` | Light color/intensity (RGB) |

**Validation**: `edge_u` and `edge_v` must not be parallel (cross product ≠ 0). `intensity` components ≥ 0.

**Derived properties**:
- `area`: `glm.length(glm.cross(edge_u, edge_v))`
- `center`: `corner + 0.5 * edge_u + 0.5 * edge_v`
- `normal`: `normalize(glm.cross(edge_u, edge_v))`

**Sampling**: A random point on the light is computed as: `corner + u * edge_u + v * edge_v` where `u, v ~ Uniform(0, 1)`.

---

### Sphere

A geometric primitive defined as a unit sphere in local space.

| Field | Type | Description |
|-------|------|-------------|
| `local_to_world` | `glm.mat4` | Transformation matrix from local to world space |
| `world_to_local` | `glm.mat4` | Inverse of `local_to_world` |
| `material` | `Material` | Surface material properties |
| `object_id` | `int` | Unique identifier |

**Validation**: `local_to_world` must be invertible.

**Local-space definition**: Unit sphere centered at origin `(0, 0, 0)` with radius `1.0`.

---

### Ellipsoid

A geometric primitive defined as a scaled unit sphere in local space.

| Field | Type | Description |
|-------|------|-------------|
| `local_to_world` | `glm.mat4` | Transformation matrix (includes scale for semi-axes) |
| `world_to_local` | `glm.mat4` | Inverse of `local_to_world` |
| `material` | `Material` | Surface material properties |
| `object_id` | `int` | Unique identifier |

**Validation**: Same as Sphere. Scale factors (semi-axes rx, ry, rz) must be > 0.

**Local-space definition**: Unit sphere at origin. Semi-axes are encoded as scale factors in `local_to_world`. Normal transformation requires inverse-transpose of upper-left 3×3 of `world_to_local`.

---

### Plane

An infinite flat surface serving as the ground plane.

| Field | Type | Description |
|-------|------|-------------|
| `point` | `glm.vec3` | A point on the plane in world space |
| `normal` | `glm.vec3` | Plane normal in world space (normalized) |
| `material` | `Material` | Surface material properties (typically a checkerboard or solid color) |
| `object_id` | `int` | Unique identifier |

**Validation**: `normal` must be normalized.

---

### Scene

Composition of all geometric objects and lights.

| Field | Type | Description |
|-------|------|-------------|
| `objects` | `list[Sphere | Ellipsoid | Plane]` | Ordered list of scene geometry |
| `lights` | `list[PointLight | AreaLight]` | Ordered list of light sources |
| `camera` | `PinholeCamera` | View camera |
| `ambient_light` | `glm.vec3` | Global ambient light color (default: `(0.05, 0.05, 0.05)`) |

**Validation**: At least one object and one light. Camera must be valid.

---

### Film

The 512×512 pixel buffer where radiance values are accumulated.

| Field | Type | Description |
|-------|------|-------------|
| `width` | `int` | Horizontal pixel count (512) |
| `height` | `int` | Vertical pixel count (512) |
| `pixels` | `numpy.ndarray` | Float buffer of shape `(height, width, 3)` for RGB accumulation |

**Validation**: `width` == 512, `height` == 512. Pixel values in [0, ∞) before tone mapping, clamped to [0, 1] for output.

**Lifecycle**:
1. **Created** — initialized to zeros
2. **Accumulated** — each ray's color added to corresponding pixel
3. **Averaged** — divided by samples per pixel
4. **Tone mapped** — clamped to [0, 1]
5. **Converted** — to uint8 and written as PNG

---

## Validation Rules Summary

| Rule | Description |
|------|-------------|
| V-001 | All vectors used as directions (ray directions, normals) must be normalized |
| V-002 | All color values must be in [0, 1] before output, [0, ∞) during computation |
| V-003 | Ray-object intersection distance `t` must be > epsilon (0.001) to avoid self-intersection |
| V-004 | Transformation matrices must be invertible |
| V-005 | Ray counts (rays-per-pixel, light-samples) must be ≥ 1 |

---

## Data Flow

```
CLI arguments (step, rays-per-pixel, light-samples)
    ↓
Scene configuration (camera, objects, lights)
    ↓
Pipeline.select(step) → configures which features are active
    ↓
For each pixel (y, x):
    For each sub-ray sample:
        Camera.generate_ray(x, y, jitter) → Ray
        Renderer.trace_ray(ray, depth=0) → Color
            For each light:
                If PointLight: single shadow ray
                If AreaLight: N shadow rays (uniform sampling)
                Compute visibility → shadow factor
            Compute shading (flat or Phong) → Color
        Film.accumulate(x, y, color)
Film.average() → tone mapping → clamp
Film.to_image() → Pillow Image → save PNG
```
