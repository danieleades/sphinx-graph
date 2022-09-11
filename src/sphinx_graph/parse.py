from typing import List, Optional


def list(input: Optional[str]) -> List[str]:
    """Parse a comma-separated list of strings."""
    if input is None:
        return []
    return [link.strip() for link in input.split(",")]
