# Tasks: Progressive Pinhole Ray Tracer

**Input**: Design documents from `/specs/001-raytracer-pinole/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli-contract.md, research.md, quickstart.md

**Tests**: Included — spec explicitly requests pytest with pytest.approx for numerical tolerance.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and tooling

- [x] T001 Verify project structure matches plan.md layout (`src/models/`, `src/services/`, `src/cli/`, `src/utils/`, `tests/`)
- [x] T002 [P] Ensure `requirements.txt` contains numpy, PyGLM, pillow, pytest, ruff, mypy
- [x] T003 [P] Create `src/__init__.py` with package docstring and version
- [x] T004 [P] Create `src/cli/__init__.py` with package docstring
- [x] T005 [P] Create `src/models/__init__.py` with package docstring
- [x] T006 [P] Create `src/services/__init__.py` with package docstring
- [x] T007 [P] Create `src/utils/__init__.py` with package docstring
- [x] T008 Configure `ruff` in `pyproject.toml` or `ruff.toml` (line-length 88, target Python 3.11)
- [x] T009 Configure `mypy` in `mypy.ini` or `pyproject.toml` (strict mode, Python 3.11 target)
- [x] T010 Create `pytest.ini` or `pyproject.toml` with pytest configuration (testpaths = tests/)

**Checkpoint**: Project structure and tooling ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 [P] Implement `Ray` data class in `src/models/ray.py` with `origin: glm.vec3`, `direction: glm.vec3`, normalization validation
- [x] T012 [P] Implement `Material` data class in `src/models/material.py` with `color`, `ambient`, `diffuse`, `specular`, `shininess` fields and validation
- [x] T013 Implement `Film` class in `src/models/film.py` with 512x512 numpy buffer, `accumulate()`, `average()`, `to_image()` methods
- [x] T014 Implement `PinholeCamera` class in `src/models/camera.py` with `eye`, `look_at`, `up`, `fov`, `film_width`, `film_height`, `view_matrix`, `inverse_view_matrix`, and `generate_ray(x, y, jitter)` method
- [x] T015 Implement `coordinate.py` in `src/services/coordinate.py` with `local_to_world()`, `world_to_local()`, `transform_normal()` functions using inverse-transpose for normals
- [x] T016 Implement base `Scene` class in `src/models/scene.py` with `objects`, `lights`, `camera`, `ambient_light` fields
- [x] T017 Implement `image_io.py` in `src/utils/image_io.py` with `save_image(film, filepath)` using Pillow `Image.fromarray()`
- [x] T018 Implement `HitRecord` data class in `src/services/intersection.py` with `t`, `point`, `normal`, `material`, `object_id` fields
- [x] T019 Create default scene configuration function in `src/models/scene.py` — `create_default_scene()` with predefined camera, plane, sphere, and point light positions

**Checkpoint**: Foundation ready — core models, camera, film, coordinate transforms, and scene composition are functional

---

## Phase 3: User Story 1 — Render Basic Scene with Point Light (Priority: P1) 🎯 MVP

**Goal**: Render a 512x512 image with a red sphere on a plane, illuminated by a point light, no shadows, flat color

**Independent Test**: Run `python -m src.cli.main --step 1` and verify `output/step_1.png` shows a red sphere on a plane with point light illumination and no shadows

### Tests for User Story 1 ⚠️

- [x] T020 [P] [US1] Unit test for `Ray` creation and normalization in `tests/unit/test_ray.py`
- [x] T021 [P] [US1] Unit test for `PinholeCamera.generate_ray()` in `tests/unit/test_camera.py`
- [x] T022 [P] [US1] Unit test for `Film` accumulation and `to_image()` in `tests/unit/test_film.py`
- [x] T023 [US1] Unit test for point light rendering pipeline in `tests/integration/test_pipeline.py` — verify step 1 produces valid PNG

### Implementation for User Story 1

- [x] T024 [P] [US1] Implement `PointLight` class in `src/models/light.py` with `position`, `intensity` fields
- [x] T025 [P] [US1] Implement `Plane` class in `src/models/geometry.py` with `point`, `normal`, `material`, `object_id`, and `intersect(ray)` method returning `HitRecord`
- [x] T026 [P] [US1] Implement `Sphere` class in `src/models/geometry.py` with `local_to_world`, `world_to_local`, `material`, `object_id`, and `intersect(ray)` method (ray transformed to local space, unit sphere intersection, hit transformed back)
- [x] T027 [US1] Implement ray-sphere intersection math in `src/services/intersection.py` — `intersect_sphere(ray_local)` returning `HitRecord` with local→global transform
- [x] T028 [US1] Implement ray-plane intersection math in `src/services/intersection.py` — `intersect_plane(ray)` returning `HitRecord`
- [x] T029 [US1] Implement `closest_hit(ray, scene)` in `src/services/intersection.py` — iterates all objects, returns nearest valid `HitRecord`
- [x] T030 [US1] Implement flat color shading in `src/services/shading.py` — `shade_flat(hit, light, scene)` returning `glm.vec3` color (no shadow ray, just `light.intensity * material.color`)
- [x] T031 [US1] Implement `Renderer` class in `src/services/renderer.py` with `trace_primary_ray(ray, scene, step=1)` method: calls `closest_hit()`, then `shade_flat()` for step 1
- [x] T032 [US1] Implement `Pipeline` class in `src/services/pipeline.py` with `render_step(step=1, film, scene, rays_per_pixel=1, light_samples=1)` — iterates all pixels, casts primary rays, accumulates colors
- [x] T033 [US1] Implement CLI entry point in `src/cli/main.py` with `--step`, `--rays-per-pixel`, `--light-samples`, `--output`, `--seed` arguments per cli-contract.md
- [x] T034 [US1] Wire CLI `--step 1` to `Pipeline.render_step(step=1)` and save `output/step_1.png` via `image_io.save_image()`

**Checkpoint**: `python -m src.cli.main --step 1` produces a valid 512x512 PNG with a red sphere on a plane, point light, no shadows

---

## Phase 4: User Story 2 — Render with Shadows and Phong Model (Priority: P2)

**Goal**: Render with shadow calculations and the Phong illumination model (ambient + diffuse + specular)

**Independent Test**: Run `python -m src.cli.main --step 2` and verify `output/step_2.png` shows Phong-shaded sphere with visible shadows cast by objects

### Tests for User Story 2 ⚠️

- [x] T035 [P] [US2] Unit test for shadow ray visibility check in `tests/unit/test_intersection.py`
- [x] T036 [P] [US2] Unit test for Phong shading components (ambient, diffuse, specular) in `tests/unit/test_shading.py`
- [x] T037 [US2] Integration test for step 2 pipeline in `tests/integration/test_pipeline.py` — verify shadow boundaries in output

### Implementation for User Story 2

- [x] T038 [P] [US2] Implement `is_in_shadow(ray_to_light, scene)` in `src/services/intersection.py` — casts shadow ray, returns True if any object blocks light
- [x] T039 [P] [US2] Implement `Material` with Phong coefficients (ambient=0.1, diffuse=0.7, specular=0.3, shininess=32.0) defaults in `src/models/material.py`
- [x] T040 [US2] Implement Phong shading in `src/services/shading.py` — `shade_phong(hit, light, scene, view_dir)` with ambient, diffuse (`max(0, N·L)`), specular (`max(0, N·H)^shininess` using Blinn-Phong half-vector)
- [x] T041 [US2] Update `Renderer.trace_primary_ray()` in `src/services/renderer.py` for step 2: cast shadow ray toward point light, call `is_in_shadow()`, apply `shade_phong()` if visible or ambient-only if shadowed
- [x] T042 [US2] Update `Pipeline` to handle step 2 — pass Phong material to shading, ensure shadow rays are cast
- [x] T043 [US2] Update CLI default scene to include Phong material for sphere (red color with Phong coefficients)

**Checkpoint**: `python -m src.cli.main --step 2` produces Phong-shaded image with shadows; step 1 still works independently

---

## Phase 5: User Story 3 — Render with Antialiasing (Priority: P3)

**Goal**: Render with supersampling antialiasing using jittered sub-pixel rays, configurable via `--rays-per-pixel`

**Independent Test**: Run `python -m src.cli.main --step 3 --rays-per-pixel 4` and verify `output/step_3.png` shows smoother edges compared to step 2

### Tests for User Story 3 ⚠️

- [x] T044 [P] [US3] Unit test for jittered sampling in `tests/unit/test_sampling.py`
- [x] T045 [US3] Integration test for step 3 — compare edge smoothness vs step 2 in `tests/regression/test_output.py`

### Implementation for User Story 3

- [x] T046 [P] [US3] Implement `generate_jittered_rays(camera, x, y, rays_per_pixel)` in `src/services/sampling.py` — divides pixel into sub-cells, casts one jittered ray per cell
- [x] T047 [US3] Update `Pipeline.render_step()` for step 3: for each pixel, call `generate_jittered_rays()`, trace each ray, average colors
- [x] T048 [US3] Update `Renderer.trace_primary_ray()` to support multiple samples per pixel (average result)
- [x] T049 [US3] Wire `--rays-per-pixel` CLI argument to `Pipeline` for step 3 (default: 4 if not specified)

**Checkpoint**: `python -m src.cli.main --step 3 --rays-per-pixel 4` produces antialiased image; steps 1-2 still work independently

---

## Phase 6: User Story 4 — Render with Area Light (Priority: P4)

**Goal**: Render with a rectangular area light source producing soft shadows, configurable via `--light-samples`

**Independent Test**: Run `python -m src.cli.main --step 4 --light-samples 16` and verify `output/step_4.png` shows soft shadows with gradual falloff

### Tests for User Story 4 ⚠️

- [x] T050 [P] [US4] Unit test for `AreaLight` random point sampling in `tests/unit/test_light.py`
- [x] T051 [P] [US4] Unit test for area light shadow averaging in `tests/unit/test_shading.py`
- [x] T052 [US4] Integration test for step 4 — verify soft shadow quality in `tests/integration/test_pipeline.py`

### Implementation for User Story 4

- [x] T053 [P] [US4] Implement `AreaLight` class in `src/models/light.py` with `corner`, `edge_u`, `edge_v`, `intensity`, `random_point()` method, `area`, `center`, `normal` properties
- [x] T054 [P] [US4] Implement `sample_area_light_shadow(area_light, hit_point, num_samples)` in `src/services/sampling.py` — generates `num_samples` random points on light, returns shadow factor (fraction of unblocked rays)
- [x] T055 [US4] Implement `shade_phong_with_area_light(hit, area_light, scene, view_dir, light_samples)` in `src/services/shading.py` — averages Phong shading over multiple shadow ray samples
- [x] T056 [US4] Update `Renderer.trace_primary_ray()` for step 4: detect `AreaLight` in scene, call `sample_area_light_shadow()`, apply `shade_phong_with_area_light()`
- [x] T057 [US4] Update default scene to use `AreaLight` instead of `PointLight` for step 4
- [x] T058 [US4] Wire `--light-samples` CLI argument to `Pipeline` for step 4 (default: 16 if not specified)

**Checkpoint**: `python -m src.cli.main --step 4 --light-samples 16` produces soft shadow image; steps 1-3 still work independently

---

## Phase 7: User Story 5 — Render with Uniform Sampling and Ellipsoid (Priority: P5)

**Goal**: Render with uniform Monte Carlo sampling for area light and ellipsoid geometry replacing the sphere

**Independent Test**: Run `python -m src.cli.main --step 5 --rays-per-pixel 4 --light-samples 32` and verify `output/step_5.png` shows ellipsoid with uniform soft shadows

### Tests for User Story 5 ⚠️

- [x] T059 [P] [US5] Unit test for `Ellipsoid` intersection in local coordinates in `tests/unit/test_geometry.py`
- [x] T060 [P] [US5] Unit test for normal transformation with inverse-transpose in `tests/unit/test_coordinate.py`
- [x] T061 [US5] Integration test for step 5 — verify ellipsoid rendering and uniform sampling quality in `tests/integration/test_pipeline.py`
- [x] T062 [US5] Regression test comparing all 5 steps output in `tests/regression/test_output.py`

### Implementation for User Story 5

- [x] T063 [P] [US5] Implement `Ellipsoid` class in `src/models/geometry.py` with `local_to_world` (encoding rx, ry, rz scale factors), `world_to_local`, `material`, `object_id`, `intersect(ray)` method
- [x] T064 [US5] Implement uniform area light sampling in `src/services/sampling.py` — `uniform_sample_area_light(area_light, num_samples)` using stratified or pure Monte Carlo with `--seed` reproducibility
- [x] T065 [US5] Implement ellipsoid intersection in `src/services/intersection.py` — transform ray to local space (unit sphere), compute hit, transform back, apply inverse-transpose to normal
- [x] T066 [US5] Update `Renderer.trace_primary_ray()` for step 5: use `uniform_sample_area_light()`, handle `Ellipsoid` in scene
- [x] T067 [US5] Update default scene to replace `Sphere` with `Ellipsoid` (e.g., rx=1.5, ry=1.0, rz=0.8) for step 5
- [x] T068 [US5] Update `Pipeline.render_step(step=5)` to orchestrate uniform sampling + ellipsoid rendering
- [x] T069 [US5] Add input validation for `--rays-per-pixel >= 1` and `--light-samples >= 1` in CLI, with proper error messages per cli-contract.md
- [x] T070 [US5] Implement `--step 5` to render all 5 steps sequentially (step_1.png through step_5.png) per cli-contract.md contract

**Checkpoint**: `python -m src.cli.main --step 5` produces all 5 PNG files with progressive quality improvement; each step works independently when called with `--step N`

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T071 [P] Create `examples/render_all_steps.py` demo script — runs all 5 steps with default settings and prints timing info
- [x] T072 [P] Add `time.perf_counter()` benchmarking to `Pipeline.render_step()` — print render time per step
- [x] T073 [P] Add Google/NumPy-style docstrings to all public classes and functions across `src/`
- [x] T074 [P] Add type hints to all function signatures and verify with `mypy src/ --strict`
- [x] T075 Run `ruff check src/ tests/` and fix all linting issues
- [x] T076 Run `ruff format src/ tests/` to ensure consistent code style
- [x] T077 [P] Create `quickstart.md` validation — run all examples from quickstart.md and verify outputs
- [x] T078 [P] Add edge case handling: zero/negative ray counts, ray misses, objects behind camera, extreme ellipsoid ratios
- [x] T079 Verify no circular imports with `python -c "import src"` and module graph analysis
- [x] T080 Run full test suite `pytest tests/ -v` and ensure all tests pass
- [x] T081 Run `mypy src/` and ensure zero type errors

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — **BLOCKS** all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3 → P4 → P5)
  - Each story is independently testable
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

```
Phase 1: Setup ──→ Phase 2: Foundational ──→ Phase 3: US1 (P1) ──→ Phase 4: US2 (P2)
                                                      │
                                                      ├──→ Phase 5: US3 (P3)
                                                      │
                                                      ├──→ Phase 6: US4 (P4)
                                                      │
                                                      └──→ Phase 7: US5 (P5)
```

- **US1 (P1)**: Core pipeline — no dependencies on other stories. Foundation for all subsequent steps.
- **US2 (P2)**: Depends on US1 pipeline — adds shadow rays + Phong shading.
- **US3 (P3)**: Depends on US2 shading — adds supersampling antialiasing.
- **US4 (P4)**: Depends on US3 sampling — replaces PointLight with AreaLight.
- **US5 (P5)**: Depends on US4 area light — adds uniform sampling + ellipsoid geometry.

**Note**: While stories build on each other technically, each is independently testable via `--step N` CLI argument.

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models (geometry, light, material) before services (intersection, shading)
- Services before pipeline integration
- Pipeline integration before CLI wiring
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] (T002–T007) can run in parallel
- All Foundational tasks marked [P] (T011–T012, T017) can run in parallel (within Phase 2)
- Once Foundational phase completes, US1 can begin
- Within US1: T020, T021, T022 (tests) can run in parallel; T024, T025, T026 (models) can run in parallel
- Within US2: T035, T036 (tests) can run in parallel
- Within US3: T044, T045 (tests) can run in parallel
- Within US4: T050, T051 (tests) can run in parallel
- Within US5: T059, T060 (tests) can run in parallel
- Polish tasks T071–T074, T077–T079 can all run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T020: "Unit test for Ray creation and normalization in tests/unit/test_ray.py"
Task T021: "Unit test for PinholeCamera.generate_ray() in tests/unit/test_camera.py"
Task T022: "Unit test for Film accumulation and to_image() in tests/unit/test_film.py"

# Launch all models for User Story 1 together:
Task T024: "Implement PointLight class in src/models/light.py"
Task T025: "Implement Plane class in src/models/geometry.py"
Task T026: "Implement Sphere class in src/models/geometry.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run `python -m src.cli.main --step 1` and verify `output/step_1.png`
5. Commit and demo

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Test with `--step 1` → Commit → Demo (MVP!)
3. Add US2 → Test with `--step 2` → Commit → Demo
4. Add US3 → Test with `--step 3` → Commit → Demo
5. Add US4 → Test with `--step 4` → Commit → Demo
6. Add US5 → Test with `--step 5` → Commit → Demo
7. Each step produces a valid PNG and doesn't break previous steps

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (core pipeline)
   - Developer B: US2 (shadows + Phong) — can start once US1 pipeline is wired
   - Developer C: US3 (antialiasing) — can start once US2 shading is complete
3. US4 and US5 follow sequentially as they depend on area light and ellipsoid

---

## Task Summary

| Phase | Description | Task Count |
|-------|-------------|------------|
| Phase 1: Setup | Project structure, tooling | 10 |
| Phase 2: Foundational | Core models, camera, film, transforms | 9 |
| Phase 3: US1 (P1) | Point light, flat color, basic pipeline | 15 |
| Phase 4: US2 (P2) | Shadows + Phong shading | 9 |
| Phase 5: US3 (P3) | Antialiasing (jittered supersampling) | 6 |
| Phase 6: US4 (P4) | Area light with soft shadows | 9 |
| Phase 7: US5 (P5) | Uniform sampling + ellipsoid | 12 |
| Phase 8: Polish | Docstrings, linting, benchmarks, edge cases | 11 |
| **Total** | | **81** |

### Independent Test Criteria per Story

| Story | Test Command | Expected Output |
|-------|-------------|-----------------|
| US1 | `python -m src.cli.main --step 1` | `output/step_1.png` — red sphere, plane, point light, no shadows |
| US2 | `python -m src.cli.main --step 2` | `output/step_2.png` — Phong-shaded sphere with shadows |
| US3 | `python -m src.cli.main --step 3 --rays-per-pixel 4` | `output/step_3.png` — smoother edges than step 2 |
| US4 | `python -m src.cli.main --step 4 --light-samples 16` | `output/step_4.png` — soft shadows from area light |
| US5 | `python -m src.cli.main --step 5` | `output/step_1.png` through `output/step_5.png` — all 5 progressive renders |

### Suggested MVP Scope

**User Story 1 (Phase 3)** delivers the minimum viable product:
- Core ray tracing pipeline (camera → rays → intersection → shading → film → PNG)
- Point light illumination
- Red sphere on a plane
- Configurable CLI entry point
- Single valid output image (`output/step_1.png`)
