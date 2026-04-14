# CLI Contract: Progressive Pinhole Ray Tracer

**Feature**: 001-raytracer-pinole
**Date**: 2026-04-09

## Command Interface

```
python -m src.cli.main [OPTIONS]
```

## Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `--step` | int (1–5) | No | 5 | Rendering step to execute. 1 = point light only, 5 = full features. |
| `--rays-per-pixel` | int (≥1) | No | auto | Number of primary rays per pixel. Auto: 1 for steps 1–2, 4 for steps 3–5. |
| `--light-samples` | int (≥1) | No | auto | Number of shadow rays per area light. Auto: 1 for point light, 16 for area light. |
| `--output` | str (path) | No | `output/` | Directory to save PNG files. |
| `--seed` | int | No | 42 | Random seed for reproducible rendering. |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success — image(s) rendered |
| 1 | Invalid arguments (e.g., step < 1 or > 5, negative ray count) |
| 2 | Runtime error (e.g., file write failure) |

## Output

For each executed step, a PNG file is created at `{output}/step_{N}.png` where N is the step number (1–5).

When `--step 5` is used, all 5 PNG files are generated sequentially (step_1.png through step_5.png).
When `--step 3` is used, only step_3.png is generated (the user can compare with previous steps by running with different --step values).

## Error Messages

All error messages are written to stderr in the format:
```
Error: {description}
```

Examples:
- `Error: --step must be an integer between 1 and 5`
- `Error: --rays-per-pixel must be >= 1`
- `Error: --light-samples must be >= 1`

## Example Invocations

```bash
# Run all 5 steps with defaults
python -m src.cli.main

# Run step 1 only (point light, flat red)
python -m src.cli.main --step 1

# Run step 3 with 16 rays per pixel
python -m src.cli.main --step 3 --rays-per-pixel 16

# Run step 5 with custom light samples and output directory
python -m src.cli.main --step 5 --light-samples 64 --output renders/

# Reproducible run with explicit seed
python -m src.cli.main --seed 12345
```
