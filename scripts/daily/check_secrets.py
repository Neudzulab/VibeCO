"""Check that required production secrets are available.

The daily stability workflow depends on PROD_BASE_URL and PROD_API_TOKEN.
This helper exits with status code 2 when any required secret is missing
and prints a marker for each absent variable so the CI job can react.
"""

from __future__ import annotations

import os
import sys


REQUIRED_SECRETS = ("PROD_BASE_URL", "PROD_API_TOKEN")


def main() -> int:
    missing = []
    for name in REQUIRED_SECRETS:
        value = os.getenv(name)
        if not value:
            print(f"MISSING:{name}")
            missing.append(name)
    if missing:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
