# Implementation Plan: Progressive Pinhole Ray Tracer

**Branch**: `001-raytracer-pinole` | **Date**: 2026-04-09 | **Spec**: [spec.md](../spec.md)
**Input**: Feature specification from `/specs/001-raytracer-pinole/spec.md`

## Summary

Build a Python-based progressive pinhole ray tracer that renders a scene (plane + sphere/ellipsoid) through 5 incremental steps: (1) point light with flat color, (2) shadows + Phong, (3) antialiasing, (4) area light, (5) uniform sampling + ellipsoid. All calculations in local coordinates transformed to global. Output: 512x512 PNG images per step. Technology stack: NumPy (numerical ops), PyGLM (math/transformations), Pillow (PNG output).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: NumPy (array operations, vectorization), PyGLM (matrix math, transformations, vector types), Pillow (PNG image output)
**Storage**: N/A (file output only — PNG images)
**Testing**: pytest with pytest.approx for numerical tolerance
**Target Platform**: macOS, Linux, Windows (cross-platform Python)
**Project Type**: CLI application / offline renderer
**Performance Goals**: Each 512x512 step completes in seconds to minutes (offline rendering); no real-time requirement
**Constraints**: All intersection/shading math in local coordinates → transform to global; progressive steps must be incremental (each step adds to previous); configurable rays-per-pixel and light-sample CLI arguments
**Scale/Scope**: Single scene, 512x512 film, 5 rendering steps, configurable ray counts (typical range: 1–64 rays/pixel, 1–128 light samples)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| **Readable Python First** — PEP 8, docstrings (Google/NumPy style), descriptive names | ✅ Pass | All modules will include full docstrings; naming follows descriptive conventions |
| **Modular Architecture — MVC/Pipeline** — models/, services/, cli/ separation; dependency flow View → Service → Model | ✅ Pass | Structure follows constitution: models (primitives, camera, light), services (renderer, pipeline), cli (argparse thin layer) |
| **Test-Driven Verification** — pytest, pytest.approx, unit + integration + regression tests | ✅ Pass | Unit tests for math functions, integration for full pipeline, regression for pixel comparison |
| **Performance Awareness** — time.perf_counter for benchmarking, no premature optimization | ✅ Pass | Timing instrumentation on rendering steps; profiling documented |
| **Determinism & Reproducibility** — identical output for identical inputs/seeds, relative paths, cross-platform | ✅ Pass | Explicit seed parameters for random sampling; all paths relative to project root |
| **Type hints** on all signatures, mypy strict, ruff lint/format, absolute imports | ✅ Pass | Enforced in all source files |
| **No circular imports**, dependency direction View → Service → Model | ✅ Pass | Module graph verified during implementation |

**All gates passed.**

## Project Structure

### Documentation (this feature)

```text
specs/001-raytracer-pinole/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── ray.py           # Ray data class (origin, direction)
│   ├── camera.py        # PinholeCamera class
│   ├── geometry.py      # Sphere, Ellipsoid, Plane primitives
│   ├── light.py         # PointLight, AreaLight
│   ├── material.py      # Material (Phong parameters, flat color)
│   ├── scene.py         # Scene composition (objects, lights)
│   └── film.py          # Film buffer (512x512 pixel accumulation)
├── services/
│   ├── __init__.py
│   ├── coordinate.py    # Local ↔ global coordinate transforms
│   ├── intersection.py  # Ray-object intersection routines
│   ├── shading.py       # Illumination models (flat, Phong)
│   ├── sampling.py      # Antialiasing (jittered), uniform area light sampling
│   ├── renderer.py      # Core ray tracer (primary rays, shadow rays)
│   └── pipeline.py      # Progressive rendering orchestration (steps 1-5)
├── cli/
│   ├── __init__.py
│   └── main.py          # CLI entry point (argparse, delegation)
└── utils/
    ├── __init__.py
    └── image_io.py      # PNG output via Pillow

tests/
├── unit/
│   ├── test_ray.py
│   ├── test_camera.py
│   ├── test_geometry.py
│   ├── test_intersection.py
│   ├── test_shading.py
│   ├── test_sampling.py
│   ├── test_coordinate.py
│   └── test_film.py
├── integration/
│   └── test_pipeline.py    # Full step render verification
└── regression/
    └── test_output.py      # Pixel comparison against reference images

examples/
└── render_all_steps.py     # Demo script: run all 5 steps

requirements.txt            # Dependencies: numpy, PyGLM, pillow, pytest, ruff, mypy
```

**Structure Decision**: Single project Python package layout per constitution. The `models/` module owns geometric primitives and scene data. `services/` owns all rendering computation. `cli/` is a thin argument-parsing layer. `utils/` handles I/O. No circular imports; dependency flow: cli → services → models.

## Complexity Tracking

> No constitution violations. All gates passed without justification needed.
