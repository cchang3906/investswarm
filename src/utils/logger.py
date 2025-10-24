"""Simple logging utility for InvestSwarm."""

import sys
from datetime import datetime


class Logger:
    """Simple logger for console output."""

    def __init__(self):
        self.verbose = True

    def info(self, message: str):
        """Log info message."""
        if self.verbose:
            print(message)

    def error(self, message: str):
        """Log error message."""
        print(f"ERROR: {message}", file=sys.stderr)

    def warning(self, message: str):
        """Log warning message."""
        print(f"WARNING: {message}", file=sys.stderr)

    def debug(self, message: str):
        """Log debug message."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] DEBUG: {message}")


# Global logger instance
logger = Logger()
