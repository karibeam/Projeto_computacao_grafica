"""Unit tests for the Film buffer."""

import numpy as np
import pytest

from src.models.film import Film


class TestFilm:
    """Tests for the Film class."""

    def test_film_creation(self) -> None:
        """Test basic film creation."""
        film = Film(width=512, height=512)
        assert film.width == 512
        assert film.height == 512
        assert film.pixels.shape == (512, 512, 3)
        assert film.samples.shape == (512, 512)

    def test_film_accumulate(self) -> None:
        """Test accumulating a color sample."""
        film = Film(width=4, height=4)
        film.accumulate(2, 1, (0.5, 0.3, 0.2))

        assert film.pixels[1, 2, 0] == pytest.approx(0.5)
        assert film.pixels[1, 2, 1] == pytest.approx(0.3)
        assert film.pixels[1, 2, 2] == pytest.approx(0.2)
        assert film.samples[1, 2] == 1

    def test_film_accumulate_multiple(self) -> None:
        """Test accumulating multiple samples averages correctly."""
        film = Film(width=4, height=4)
        film.accumulate(0, 0, (1.0, 0.0, 0.0))
        film.accumulate(0, 0, (0.0, 1.0, 0.0))
        film.accumulate(0, 0, (0.0, 0.0, 1.0))

        film.average()

        assert film.pixels[0, 0, 0] == pytest.approx(1.0 / 3.0)
        assert film.pixels[0, 0, 1] == pytest.approx(1.0 / 3.0)
        assert film.pixels[0, 0, 2] == pytest.approx(1.0 / 3.0)

    def test_film_clamp(self) -> None:
        """Test clamping pixel values."""
        film = Film(width=4, height=4)
        film.pixels[0, 0] = (2.0, -0.5, 0.5)
        film.clamp()

        assert film.pixels[0, 0, 0] == pytest.approx(1.0)
        assert film.pixels[0, 0, 1] == pytest.approx(0.0)
        assert film.pixels[0, 0, 2] == pytest.approx(0.5)

    def test_film_to_image_array(self) -> None:
        """Test conversion to uint8 array."""
        film = Film(width=2, height=2)
        film.pixels[0, 0] = (1.0, 0.5, 0.0)
        film.pixels[0, 1] = (0.0, 0.0, 1.0)

        arr = film.to_image_array()

        assert arr.dtype == np.uint8
        assert arr[0, 0, 0] == 255
        assert arr[0, 0, 1] == 127  # 0.5 * 255 = 127.5 → 127
        assert arr[0, 1, 2] == 255

    def test_film_clear(self) -> None:
        """Test clearing the film buffer."""
        film = Film(width=4, height=4)
        film.accumulate(0, 0, (1.0, 1.0, 1.0))
        film.clear()

        assert film.pixels[0, 0, 0] == pytest.approx(0.0)
        assert film.samples[0, 0] == 0

    def test_film_accumulate_out_of_bounds(self) -> None:
        """Test that out-of-bounds accumulation is safely ignored."""
        film = Film(width=4, height=4)
        film.accumulate(-1, 0, (1.0, 0.0, 0.0))
        film.accumulate(4, 0, (1.0, 0.0, 0.0))
        film.accumulate(0, -1, (1.0, 0.0, 0.0))
        film.accumulate(0, 4, (1.0, 0.0, 0.0))

        assert film.samples.sum() == 0
