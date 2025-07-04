"""
input_utils.py

General-purpose utilities for normalizing and transforming flexible user or API input.

This module is useful when inputs may vary in type (e.g., a string or a list),
and you want to safely standardize them to a consistent structure.

Currently includes:
- normalize_email_list: converts comma- or semicolon-separated strings or lists
  to a clean list of email addresses.

If input processing becomes more complex (e.g., boolean flags, enums, nested dict parsing),
this file can be split into more focused modules (e.g., `parsers/`, `normalizers/`, etc.).
"""

from typing import Union, List
import re


def normalize_email_list(value: Union[str, List[str]]) -> List[str]:
    """
    Normalize email input into a list of email addresses.

    Supports:
    - Comma-separated string: "a@example.com, b@example.com"
    - Semicolon-separated string: "a@example.com; b@example.com"
    - List of strings

    Args:
        value (str | List[str]): Email input.

    Returns:
        List[str]: Cleaned list of email addresses.
    """
    if isinstance(value, str):
        # Split on commas or semicolons, ignoring empty entries
        return [email.strip() for email in re.split(r"[;,]", value) if email.strip()]
    if isinstance(value, list):
        return value
    return []
