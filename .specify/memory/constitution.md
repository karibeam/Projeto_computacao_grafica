<!--
SYNC IMPACT REPORT
==================
Version change: N/A → 1.0.0 (initial constitution)
Modified principles: N/A (first version)
Added sections:
  - Core Principles (5 principles)
  - Code Quality Standards
  - Project Structure & Architecture
  - Development Workflow & Testing
  - Governance
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ no changes needed (generic Constitution Check section)
  - .specify/templates/spec-template.md ✅ no changes needed (technology-agnostic)
  - .specify/templates/tasks-template.md ✅ no changes needed (generic structure)
Follow-up TODOs: None
-->

# Projeto Computação Gráfica Constitution

## Core Principles

### I. Readable Python First (NON-NEGOTIABLE)

All code MUST be written in Python following PEP 8 style guidelines. Readability is the primary
design criterion — code is read far more often than it is written. Every module, class, and public
function MUST include docstrings conforming to Google or NumPy style. Variable and function names
MUST be descriptive and self-explanatory. Avoid clever one-liners when a clearer multi-line
alternative exists.

**Rationale**: Computer graphics algorithms are mathematically dense; clear code prevents subtle
bugs and makes review feasible.

### II. Modular Architecture — MVC / Pipeline Separation

The application MUST follow a clear separation of concerns: rendering/pipeline logic, user
interaction (GUI/CLI), and data models MUST live in separate modules. Recommended architecture:

- **Models** — geometric primitives, scene graphs, transformation matrices
- **Services/Pipeline** — rendering passes, shaders, rasterization, ray tracing logic
- **Views/Interface** — window management, input handling, display output

No module may import from a layer above it. Dependency direction MUST always flow:
View → Service → Model. Circular imports are prohibited.

**Rationale**: Graphics applications naturally intertwle computation and presentation; enforcing
layers keeps each testable and swappable.

### III. Test-Driven Verification (NON-NEGOTIABLE)

Every algorithm with numerical output MUST have unit tests verifying correctness against known
results. Test categories:

- **Unit tests** — individual functions (e.g., matrix multiplication, vector normalization)
- **Integration tests** — full pipeline runs (e.g., render a known scene, compare output image)
- **Regression tests** — pixel-level or near-equality comparisons for rendering output

Tests MUST use `pytest`. Numerical comparisons MUST use `pytest.approx` with explicit tolerance.
A test suite that cannot assert correctness is not a test suite.

**Rationale**: Floating-point arithmetic introduces subtle differences; explicit tolerances prevent
flaky tests and catch real regressions.

### IV. Performance Awareness & Profiling

Graphics code MUST be measurable. Any function processing pixels, vertices, or rays MUST include
timing instrumentation or be covered by profiling benchmarks. Performance budgets:

- Interactive frame rate target: ≥ 30 fps for real-time rendering
- Batch rendering: document total time and memory per scene

Use `time.perf_counter` for benchmarking. Do NOT optimize without profiling first. Premature
optimization is prohibited — clarity before speed, then measure and optimize hotspots.

**Rationale**: Unprofiled optimization degrades readability without guaranteed benefit.

### V. Determinism & Reproducibility

Given identical inputs and seed values, every rendering MUST produce identical output. Random
number generation (e.g., for Monte Carlo ray tracing) MUST accept an explicit seed parameter.
All external resources (file paths, shader files, textures) MUST be resolved relative to the
project root, not absolute paths. Build and run commands MUST work on macOS, Linux, and Windows
without modification.

**Rationale**: Reproducible rendering is essential for testing, debugging, and scientific validity.

## Code Quality Standards

All Python code MUST target version 3.11 or later. The following tools and standards are
mandatory:

- **Linting**: `ruff` — zero warnings allowed in CI
- **Formatting**: `ruff format` — consistent style across all files
- **Type hints**: Required on all function signatures (parameters and return types). Use `typing`
  module for complex types. `mypy` strict mode for static type checking.
- **Imports**: Absolute imports only. Organized with standard library first, third-party second,
  local modules third (one blank line between groups).
- **Error handling**: Use specific exceptions (`ValueError`, `RuntimeError`, custom subclasses).
  Never bare `except:`. All exceptions MUST include a clear message.
- **Constants**: Magic numbers in rendering (e.g., PI, EPSILON, MAX_DEPTH) MUST be named constants
  at module level with a comment explaining the choice.

## Project Structure & Architecture

The project follows a standard Python package layout with clear separation between library code,
CLI entry points, and tests:

```
src/
├── __init__.py          # Package metadata and version
├── models/              # Geometric primitives, scenes, cameras
├── services/            # Rendering pipeline, algorithms, transformations
├── cli/                 # Command-line entry points (thin layer)
└── utils/               # Shared helpers (math, I/O, logging)

tests/
├── unit/                # Fast, isolated function tests
├── integration/          # Full pipeline / scene render tests
└── regression/           # Output image comparison tests

examples/                # Sample scenes, demo scripts
assets/                  # Textures, meshes, config files
```

The `src/` directory MUST be importable as a package. The `cli/` module MUST contain only argument
parsing and delegation — all business logic stays in `services/` or `models/`.

## Development Workflow & Testing

- **Virtual environments**: All development uses an isolated `venv/`. Dependencies pinned in
  `requirements.txt`. No global installs for project code.
- **Commits**: Atomic and descriptive. One logical change per commit. Reference issue or task ID.
- **Pull requests**: MUST include a description of the rendering or algorithm change, test results,
  and a sample output image when applicable.
- **Test gate**: ALL tests MUST pass before merging. No exceptions. Run `pytest tests/` locally
  before pushing.
- **Documentation**: Every new algorithm or rendering technique added MUST include a reference
  (paper, textbook, URL) in the docstring.

## Governance

This constitution supersedes all other development practices in the project. Any deviation
requires explicit approval and MUST be documented as an exception in the relevant PR or commit
message.

**Amendment process**: Propose changes via a PR modifying this file. The PR MUST include a
rationale for each change and assess impact on existing code and tests.

**Versioning policy**: Semantic versioning (`MAJOR.MINOR.PATCH`):
- MAJOR — removal or backward-incompatible redefinition of a principle
- MINOR — addition of a new principle or section
- PATCH — clarifications, wording fixes, non-semantic refinements

**Compliance review**: Every PR and code review MUST verify adherence to the principles above.
If a principle cannot be followed, document the violation reason inline and reference this file.

**Version**: 1.0.0 | **Ratified**: 2026-04-09 | **Last Amended**: 2026-04-09
