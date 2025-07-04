"""
template_utils.py

Simple template rendering utilities for placeholder-based string substitution.

Currently supports lightweight string rendering with {{ key }} syntax.
If the logic becomes more complex (e.g., advanced conditions, loops, filters),
or if we begin managing many template files, we can move to a more structured
templating system (like Jinja2) and organize this into a `templates/` package.
"""

def render_template(template: str, context: dict) -> str:
    """
    Simple placeholder replacement using double curly braces.

    Example:
        template = "Hello {{ name }}, your code is {{ code }}"
        context = {"name": "Ola", "code": "12345"}
        ➜ "Hello Ola, your code is 12345"

    Args:
        template (str): The template string containing {{ placeholders }}.
        context (dict): Key-value pairs to replace in the template.

    Returns:
        str: The rendered string with all placeholders replaced.
    """
    for key, value in context.items():
        template = template.replace(f"{{{{ {key} }}}}", str(value))
    return template
