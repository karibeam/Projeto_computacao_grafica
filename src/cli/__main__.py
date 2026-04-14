"""Allow running the CLI as `python -m src.cli.main`."""

import sys

from src.cli.main import main

sys.exit(main())
