# Research: Progressive Pinhole Ray Tracer

**Feature**: 001-raytracer-pinole
**Date**: 2026-04-09

## Decision 1: Math Library Selection — PyGLM vs Alternatives

**Decision**: Use PyGLM (`pyglm`) for matrix math, vector types, and coordinate transformations.

**Rationale**: PyGLM provides GLM-style (OpenGL Mathematics) vector and matrix operations in Python. It offers `glm.vec3`, `glm.mat4`, and transformation functions (`glm.translate`, `glm.scale`, `glm.rotate`, `glm.inverse`) that map directly to the local→global coordinate transformation workflow required by the spec. It is lighter than PyOpenGL and does not require an OpenGL context.

**Alternatives considered**:
- **Pure NumPy**: Can do all matrix math but requires manual wrapping into transformation matrices; more verbose for 3D graphics conventions.
- **NumPy + custom helpers**: Would work but duplicates what GLM already provides.
- **PyGLM**: Chosen — provides standard graphics math conventions (vec3, vec4, mat4) with clean API.

**Reference**: GLM documentation (https://glm.g-truc.net/), PyGLM on PyPI.

---

## Decision 2: Numerical Operations — NumPy for Vectorization

**Decision**: Use NumPy for array operations, pixel buffer management, and vectorized computations.

**Rationale**: NumPy excels at bulk array operations. The film buffer (512×512×3 RGB values) is naturally a NumPy array. Vectorized operations (e.g., normalizing many ray directions at once, computing Phong shading across pixels) can be significantly faster than Python loops. NumPy and PyGLM complement each other: PyGLM for individual ray/transform math, NumPy for bulk pixel processing.

**Alternatives considered**:
- **Pure Python lists**: Too slow for 512×512 pixel processing with multiple rays.
- **CuPy / GPU**: Overkill for this educational project; adds CUDA dependency.
- **NumPy**: Chosen — standard, well-supported, works cross-platform.

---

## Decision 3: Image Output — Pillow (PIL)

**Decision**: Use Pillow for PNG image generation.

**Rationale**: Pillow's `Image.fromarray()` accepts NumPy arrays directly, making it trivial to convert the film buffer (numpy uint8 array of shape 512×512×3) to a PNG file. It is the standard Python image library, well-maintained, and cross-platform.

**Alternatives considered**:
- **PPM (raw text/binary)**: Simplest format but not widely viewable; requires external conversion.
- **imageio**: Another option but Pillow is more established and has simpler API for this use case.
- **Pillow**: Chosen — `Image.fromarray(pixels).save("output.png")` is a one-liner.

**Reference**: Pillow documentation (https://pillow.readthedocs.io/).

---

## Decision 4: Ray-Object Intersection in Local Coordinates

**Decision**: All intersection tests are performed in object-local space. Objects store a local-to-world transformation matrix. When a ray is tested against an object, the ray is first transformed into the object's local space (using the inverse of the object's world matrix), intersection is computed in local space, then the hit point and normal are transformed back to world space.

**Rationale**: This approach simplifies intersection math — a sphere is always centered at origin with radius 1 in local space, an ellipsoid is always a unit sphere scaled by axis factors. The transformation handles arbitrary position, rotation, and scale in the scene. This matches the spec requirement: "faca todos os calculos nas coordenadas locais para depois transformar para coordenadas globais."

**Reference**: "Physically Based Rendering" (PBRT), Chapter 4 — Geometry and Transformations.

---

## Decision 5: Phong Illumination Model Implementation

**Decision**: Implement the classic Phong reflection model with three components:
- **Ambient**: `I_a * k_a` (constant ambient light)
- **Diffuse**: `I_l * k_d * max(0, N · L)` (Lambertian reflection)
- **Specular**: `I_l * k_s * max(0, R · V)^n` (Blinn-Phong or classic Phong with reflection vector)

Using the **Blinn-Phong** variant (half-vector `H = normalize(L + V)`, specular = `max(0, N · H)^n`) for computational efficiency and common usage in computer graphics education.

**Rationale**: Blinn-Phong is the standard taught in graphics courses and produces visually equivalent results to classic Phong at lower computational cost. The specular exponent `n` (shininess) controls highlight sharpness.

**Reference**: "Computer Graphics: Principles and Practice" (Hughes et al.), Phong/Blinn-Phong illumination models.

---

## Decision 6: Antialiasing Strategy — Supersampling with Jittered Samples

**Decision**: Implement supersampling antialiasing by casting multiple rays per pixel with jittered (stratified random) sub-pixel positions. Each pixel is divided into an N×N grid; one ray is cast per sub-pixel cell with random offset within the cell. The final pixel color is the average of all samples.

**Rationale**: Jittered supersampling reduces aliasing artifacts (jagged edges, Moiré patterns) more effectively than uniform grid sampling at the same sample count. The number of rays per pixel is configurable via CLI (e.g., `--rays-per-pixel 4` for 2×2, `--rays-per-pixel 16` for 4×4).

**Reference**: "Ray Tracing from the Ground Up" (Kerr), antialiasing chapter.

---

## Decision 7: Area Light Sampling — Uniform Monte Carlo

**Decision**: For area lights, sample points uniformly distributed across the rectangular light surface. For each shadow test, randomly select a point on the area light and cast a shadow ray. Average results over N samples (configurable via `--light-samples` CLI flag).

**Rationale**: Uniform random sampling is the simplest area light strategy and produces soft shadows. While stratified or low-discrepancy sampling (e.g., Halton, Sobol) produces less noise at the same sample count, uniform sampling is sufficient for the educational scope and matches the spec requirement for "luz espacial com amostra uniforme."

**Reference**: "Physically Based Rendering" (PBRT), Chapter 12 — Light Transport and Sampling.

---

## Decision 8: Ellipsoid Representation

**Decision**: Represent the ellipsoid as a scaled unit sphere in local coordinates. The transformation matrix encodes the three semi-axis lengths (rx, ry, rz) as scale factors. Intersection test is identical to sphere intersection in local space; normals are transformed using the inverse-transpose of the local-to-world matrix to account for non-uniform scaling.

**Rationale**: This approach reuses the sphere intersection code exactly. The inverse-transpose normal transformation is necessary because non-uniform scaling distorts normals. This is a standard technique in ray tracing.

**Reference**: "Ray Tracing: The Rest of Your Life" (Shirley), ellipsoid handling via transformation.

---

## Decision 9: CLI Argument Design

**Decision**: The CLI accepts the following arguments:
- `--step` (int, 1–5): Which rendering step to execute. Default: 5 (all features).
- `--rays-per-pixel` (int, ≥1): Number of primary rays per pixel for antialiasing. Default: 1 (step 1-2), 4 (step 3+).
- `--light-samples` (int, ≥1): Number of shadow rays per area light sample. Default: 1 (point light), 16 (area light).
- `--output` (str): Output directory for PNG files. Default: `output/`.
- `--seed` (int, optional): Random seed for reproducibility. Default: 42.

**Rationale**: Minimal but complete. Covers all configurable parameters from the spec. Sensible defaults allow running without any arguments (`python -m src.cli.main` runs step 5 with defaults).

---

## All NEEDS CLARIFICATION Resolved

No remaining unknowns. All technology choices are documented with rationale and alternatives.
