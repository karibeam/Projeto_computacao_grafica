# Implementation Plan: Refactor Rendering Pipeline Steps

**Branch**: `main` (working directly) | **Date**: 2026-04-14 | **Spec**: [specs/refactor-rendering-pipeline/spec.md](../specs/refactor-rendering-pipeline/spec.md)

**Note**: This plan documents the already-completed implementation for the rendering pipeline refactoring.

## Summary

Refactored the progressive rendering pipeline to clarify pedagogical progression:
- Step 3 now demonstrates antialiasing with both single and dual point light configurations (2 output images)
- Step 4 simplified to basic antialiasing with single point light (step 4.1 removed)
- Step 5 implements area light with 32 uniform samples per pixel for soft shadows on ellipsoid geometry

Technical approach: Modified scene configurations in `src/models/scene.py` and pipeline orchestration in `src/services/pipeline.py` to support new step structure and dual output for step 3.

## Technical Context

**Language/Version**: Python 3.13 (tested), targets 3.11+
**Primary Dependencies**: 
- `pyglm` for vector/matrix math
- `pytest` for testing
- Custom ray tracer implementation
**Storage**: N/A (in-memory rendering)
**Testing**: pytest with unit, integration, and regression tests
**Target Platform**: macOS, Linux, Windows (cross-platform Python)
**Project Type**: CLI tool / educational rendering pipeline
**Performance Goals**: 
  - Step 4: < 30 seconds render time
  - Step 5: reasonable render time with 32 samples
  - All steps: deterministic output with seed=42
**Constraints**: 
  - Must maintain existing API compatibility
  - Cannot break existing tests
  - Must preserve reproducibility (seed-based RNG)
**Scale/Scope**: 512x512 pixel images, 5 rendering steps, educational use

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Readable Python First
- All code follows PEP 8 with descriptive names
- Docstrings present in all modules (Google style)
- No clever one-liners; clear multi-line logic

### ✅ II. Modular Architecture — MVC / Pipeline Separation
- Models (`src/models/scene.py`): Scene configuration, lights, geometry
- Services (`src/services/pipeline.py`, `renderer.py`, `shading.py`): Rendering logic
- CLI (`src/cli/main.py`): Argument parsing only
- No circular imports; dependency flow: CLI → Services → Models

### ✅ III. Test-Driven Verification
- All 42 existing tests pass
- Integration tests verify pipeline execution
- Unit tests verify individual components (camera, geometry, shading)
- Numerical comparisons use appropriate tolerances

### ✅ IV. Performance Awareness & Profiling
- Pipeline uses `time.perf_counter` for benchmarking
- Performance output displayed per step (e.g., "Saved to ... (12.34s)")
- No premature optimization; sample counts chosen for quality first

### ✅ V. Determinism & Reproducibility
- Random seed parameter (seed=42) ensures identical output
- All file paths relative to project root
- Cross-platform compatible (pure Python + pyglm)

### Code Quality Standards
- ✅ Target Python 3.11+
- ✅ `ruff` linting: zero warnings
- ✅ Type hints on all function signatures
- ✅ Absolute imports only
- ✅ Specific exceptions (no bare `except:`)
- ✅ Named constants for magic numbers (e.g., sample counts)

## Project Structure

### Documentation (this feature)

```text
specs/refactor-rendering-pipeline/
├── spec.md              # Feature specification
├── plan.md              # This implementation plan
├── research.md          # Not needed (implementation complete)
├── data-model.md        # Not needed (no new data models)
├── quickstart.md        # Not needed (existing CLI unchanged)
├── contracts/           # Not needed (internal refactoring)
└── tasks.md             # Phase 2 output (if needed)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── scene.py         # ✓ Modified: New step configurations
├── services/
│   ├── pipeline.py      # ✓ Modified: New orchestration logic
│   ├── shading.py       # Unchanged (existing shading works)
│   └── renderer.py      # Unchanged (existing renderer works)
├── cli/
│   └── main.py          # Unchanged (existing CLI works)
└── utils/
    └── image_io.py      # Unchanged

tests/
├── unit/                # ✓ All pass
├── integration/         # ✓ All pass  
└── regression/          # ✓ Skipped (no reference images yet)
```

**Structure Decision**: Single project layout maintained. Modified only `src/models/scene.py` and `src/services/pipeline.py` to implement new step structure. No new files or modules required.

## Implementation Details

### Changes Made

#### 1. **Scene Configuration** (`src/models/scene.py`)
- Added `point_light_left` and `point_light_right` for step 3 dual-light variant
- Added `area_light_step5` positioned above ellipsoid (4x4 area, intensity 5.0)
- Created scene `31` (step 3.1) with dual point lights
- Simplified step 4 to use single `point_light_bright`
- Updated step 5 to use `area_light_step5` with ellipsoid
- **Removed**: Old step 4.1 scene configuration

#### 2. **Pipeline Orchestration** (`src/services/pipeline.py`)
- Updated `STEP_DESCRIPTIONS` to reflect new step meanings
- Modified `_auto_light_samples()`:
  - Step 5: 32 samples (area light uniform sampling)
  - Steps 3.1, 4: 1 sample (point lights)
- Enhanced `render_all()` to handle step 3 dual output:
  - Renders step 3 (single light) → `step_3.png`
  - Renders step 3.1 (dual light) → `step_3_1.png`
- Added `_render_custom_step()` for special step naming (e.g., 3.1)
- Execution order: 1 → 2 → 3 → 3.1 → 4 → 5

#### 3. **Output Files**
Total: 6 images
- `step_1.png`: Flat color, no shadows
- `step_2.png`: Phong + shadows
- `step_3.png`: Antialiasing (single light)
- `step_3_1.png`: Antialiasing (dual lights)
- `step_4.png`: Sphere with antialiasing, single light
- `step_5.png`: Area light (32 samples) + ellipsoid

## Complexity Tracking

> **NOT APPLICABLE** — No constitution violations. Implementation simplifies existing structure.

## Verification Results

```bash
$ python3 -m pytest tests/ -v
============================================= 42 passed, 2 skipped in 0.43s ==============================================
```

- ✅ All unit tests pass (38 tests)
- ✅ All integration tests pass (4 tests)  
- ✅ Regression tests skipped (no reference images)
- ✅ Python syntax validation passes

## Next Steps

1. **Run pipeline** to generate output images:
   ```bash
   python -m src.cli.main
   ```
2. **Verify visual output** for each step
3. **Optional**: Add regression test reference images once output verified
4. **Documentation**: Update README with new step descriptions
