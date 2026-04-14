# Quickstart: Progressive Pinhole Ray Tracer

**Feature**: 001-raytracer-pinole
**Date**: 2026-04-09

## Prerequisites

- Python 3.11 or later
- pip (Python package manager)

## Setup

```bash
# Create and activate virtual environment (if not already done)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install numpy PyGLM pillow pytest ruff mypy
```

Or if a `requirements.txt` exists:

```bash
pip install -r requirements.txt
```

## Run

```bash
# Render all 5 steps with default settings
python -m src.cli.main

# Render a specific step
python -m src.cli.main --step 1

# Render with custom ray counts
python -m src.cli.main --step 3 --rays-per-pixel 16
python -m src.cli.main --step 5 --light-samples 64

# Reproducible run with seed
python -m src.cli.main --seed 42
```

## Output

PNG files are saved to the `output/` directory:
- `output/step_1.png` — Point light, flat red sphere, no shadows
- `output/step_2.png` — Shadows + Phong shading
- `output/step_3.png` — Antialiasing applied
- `output/step_4.png` — Area light with soft shadows
- `output/step_5.png` — Uniform sampling + ellipsoid

## Verify

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run only unit tests
pytest tests/unit/

# Run with coverage (if pytest-cov installed)
pytest tests/ --cov=src
```

## Lint and Type Check

```bash
# Lint with ruff
ruff check src/ tests/

# Format check
ruff format --check src/ tests/

# Type check with mypy
mypy src/
```

## Project Structure Overview

```
src/
├── models/       — Geometric primitives, camera, lights, materials
├── services/     — Rendering algorithms, coordinate transforms, pipeline
├── cli/          — Command-line entry point
└── utils/        — Image I/O helpers

tests/
├── unit/         — Fast isolated function tests
├── integration/  — Full pipeline tests
└── regression/   — Output image comparison tests
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'glm'` | Run `pip install PyGLM` |
| `ModuleNotFoundError: No module named 'numpy'` | Run `pip install numpy` |
| `ModuleNotFoundError: No module named 'PIL'` | Run `pip install pillow` |
| Output directory not found | The directory is created automatically; check write permissions |
| Rendering is very slow | Reduce `--rays-per-pixel` and `--light-samples` values |
| Black output image | Check that objects are positioned within the camera's view |
