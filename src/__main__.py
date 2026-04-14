"""Allow running the application as `python -m src`."""

import sys

from src.cli.main import main

sys.exit(main())
