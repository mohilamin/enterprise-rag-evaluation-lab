from __future__ import annotations

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger."""
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    return logging.getLogger(name)
