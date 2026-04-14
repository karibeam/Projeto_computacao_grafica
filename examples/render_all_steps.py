"""Demo script — render all 5 steps with default settings.

Usage:
    python examples/render_all_steps.py
    python examples/render_all_steps.py --rays-per-pixel 16 --light-samples 64
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.models.scene import Scene
from src.services.pipeline import Pipeline


def main() -> None:
    """Render all 5 progressive steps."""
    print("=" * 60)
    print("Progressive Pinhole Ray Tracer — All Steps")
    print("=" * 60)

    pipeline = Pipeline(output_dir="output", seed=42)
    scenes = Scene.default_steps()

    paths = pipeline.render_all(scenes=scenes)

    print("\nOutput files:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
