"""
validators.py

Generic validation utilities for the MCP server.

Currently includes basic validators like email format validation.
If this module grows more complex in the future (e.g., separate validators
for usernames, passwords, URLs, etc.), we can split it into multiple
files under a `validators/` subpackage for better organization.
"""

import re

def validate_email_format(email: str) -> bool:
    """
    Validates an email address using a basic regex pattern.

    Args:
        email (str): Email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email))
