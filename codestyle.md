# Code Style Guide

This document follows the following mainstream official standards:

- PEP 8 – Style Guide for Python Code
  https://peps.python.org/pep-0008/
- Google Python Style Guide
  https://google.github.io/styleguide/pyguide.html

## 1. Indentation

- Use 4 spaces per indent level. Tabs are forbidden.
- Do not mix tabs and spaces.

## 2. Naming Conventions

| Type | Style | Example |
|------|-------|---------|
| Variables / functions | snake_case | `safe_calc`, `get_history` |
| Classes | PascalCase | `History` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_PORT` |
| Private functions | Leading underscore | `_parse_expression` |

## 3. Imports

- Group standard library, third-party libraries, and local modules separately, with a blank line between groups.
- Import one module per line, but multiple objects from the same module may be combined.

```python
import re
from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
```

## 4. Comments

- Add a `#` or a `"""docstring"""` above each function describing its purpose.
- Comments must be indented the same as the code they refer to.
- Inline comments should have at least two spaces before them.

```python
# Safe calculation function
def safe_calc(expr):
    ...
```

## 5. Line Length and Whitespace

- Maximum 79 characters per line (PEP 8).
- Operators should have one space on each side, e.g. `a + b`.
- One space after commas and colons, none before.

## 6. Functions and Classes

- Two blank lines between functions.
- Two blank lines between classes.
- Keep function parameters under 5 when possible.

## 7. Strings

- Prefer double quotes `"..."`.
- Use triple quotes `"""..."""` for multi-line strings.

## 8. Exception Handling

- Catch specific exception types; avoid bare `except:`.
- Return clear error messages for user errors; return generic messages for unknown errors.

```python
except ZeroDivisionError as e:
    return jsonify({"success": False, "message": str(e)}), 400
```

## 9. Database Operations

- Always call `db.session.commit()` after writing data.
- Keep database operations inside service functions; avoid complex logic in route handlers.

## 10. File Encoding

- All source files use UTF-8 encoding.
````
