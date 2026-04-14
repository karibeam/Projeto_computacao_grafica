"""CLI entry point — argument parsing and pipeline delegation."""

from __future__ import annotations

import argparse
import sys

from src.models.scene import Scene
from src.services.pipeline import Pipeline


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point.

    Parses command-line arguments and delegates to the rendering pipeline.

    Args:
        argv: Command-line arguments (defaults to sys.argv).

    Returns:
        Exit code (0 = success, 1 = invalid args, 2 = runtime error).
    """
    parser = argparse.ArgumentParser(description="Progressive Pinhole Ray Tracer.")
    parser.add_argument(
        "--step",
        type=float,
        default=None,
        help="Rendering step (1-6, 1.5, or 3.1). Default: run all steps.",
    )
    parser.add_argument(
        "--rays-per-pixel",
        type=int,
        default=None,
        help="Primary rays per pixel for antialiasing. Auto: 1 for steps 1-2, 4 for 3-3.1, 8 for 4-6.",
    )
    parser.add_argument(
        "--light-samples",
        type=int,
        default=None,
        help="Shadow rays per area light sample. Auto: 1 for point light, 16 for step 4, 24 for step 6, 32 for step 5.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory for PNG files. Default: output/",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible rendering. Default: 42.",
    )

    args = parser.parse_args(argv)

    VALID_STEPS = {1, 1.5, 2, 3, 3.1, 4, 5, 6}

    # Validate arguments
    if args.step is not None and args.step not in VALID_STEPS:
        print("Error: --step must be 1, 1.5, 2, 3, 3.1, 4, 5, or 6", file=sys.stderr)
        return 1

    if args.rays_per_pixel is not None and args.rays_per_pixel < 1:
        print("Error: --rays-per-pixel must be >= 1", file=sys.stderr)
        return 1

    if args.light_samples is not None and args.light_samples < 1:
        print("Error: --light-samples must be >= 1", file=sys.stderr)
        return 1

    try:
        pipeline = Pipeline(output_dir=args.output, seed=args.seed)

        if args.step is not None:
            # Render a single step
            scenes = Scene.default_steps()

            # Handle step 1.5 and 3.1 (keys are 15 and 31 in the dictionary)
            if args.step == 1.5:
                scene_key = 15
            elif args.step == 3.1:
                scene_key = 31
            else:
                scene_key = args.step

            pipeline.render_step(
                step=args.step,
                scene=scenes[scene_key],
                rays_per_pixel=args.rays_per_pixel,
                light_samples=args.light_samples,
            )
        else:
            # Render all steps
            pipeline.render_all(
                rays_per_pixel=args.rays_per_pixel,
                light_samples=args.light_samples,
            )

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
