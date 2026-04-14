"""Image I/O — saving film buffers as PNG files using Pillow."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

from src.models.film import Film


def save_film_as_png(film: Film, path: str | Path) -> Path:
    """Save a Film buffer as a PNG image.

    Args:
        film: The rendered film buffer.
        path: Output file path (will be created if directory doesn't exist).

    Returns:
        The resolved output path.

    Raises:
        RuntimeError: If the image cannot be saved.
    """
    output_path = Path(path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        image_array = film.to_image_array()
        image = Image.fromarray(image_array, mode="RGB")
        image.save(str(output_path), "PNG")
    except Exception as exc:
        raise RuntimeError(f"Failed to save image to {output_path}: {exc}") from exc

    return output_path
