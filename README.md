# Calculator Backend

## Project Introduction

A calculator backend built with Flask + SQLite that provides a secure mathematical expression evaluation service, together with calculation history storage, query, and deletion features for the frontend.

Main responsibilities:
- Receive mathematical expressions sent from the frontend
- Safely parse and evaluate expressions (supporting operator precedence, parentheses, unary plus/minus, decimals)
- Handle errors (invalid expressions, division by zero)
- Persist successful calculation records into a SQLite database
- Provide APIs for querying, deleting, and clearing history records

## Technology Stack

- Python 3.8+
- Flask 3.x
- Flask-SQLAlchemy 3.x
- Flask-CORS 5.x
- SQLite 3

## Runtime Environment

- Python 3.8 or above
- OS: Windows 10 / 11
- No separate database installation is required; SQLite is created automatically

## Local Paths

| Item | Path |
|------|------|
| Python interpreter | `D:\软件\python\python.exe` |
| Backend project | `D:\FZU\calculator_backend` |

## Installation

Run the following command in CMD:

```bash
"D:\软件\python\python.exe" -m pip install flask flask-sqlalchemy flask-cors
```

If the download is slow, use a mirror:

```bash
"D:\软件\python\python.exe" -m pip install flask flask-sqlalchemy flask-cors -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Startup

### Step 1: Open CMD and enter the backend directory

```bash
cd /d "D:\FZU\calculator_backend"
```

### Step 2: Start the backend

```bash
"D:\软件\python\python.exe" app.py
```

Note: Python on this machine is not added to the system PATH, so the full path `"D:\软件\python\python.exe"` is used instead of just `python`.

### Step 3: Success indicator

The terminal will display:

```text
* Serving Flask app 'app'
* Debug mode: on
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://192.168.3.53:5000
Press CTRL+C to quit
```

Seeing `Running on http://127.0.0.1:5000` means startup succeeded.

Note: This CMD window must stay open while the service is running. Closing it stops the backend.

## Database Initialization

No manual initialization is required. On first run, the program automatically creates a `calculator.db` file in `D:\FZU\calculator_backend` and creates the `history` table.

Table structure:

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| expression | VARCHAR(200) | Calculation expression |
| result | VARCHAR(50) | Calculation result |
| created_at | DATETIME | Calculation time |

## Frontend / Backend Connection

The frontend specifies the backend address through the following constant in `index.html`:

```javascript
const API = 'http://127.0.0.1:5000';
```

If the backend is deployed elsewhere, change this to the actual service address.

## API Reference

### 1. Calculate

Request: POST /api/calculate

Body:

```json
{ "expression": "1+2*3" }
```

Success response (HTTP 200):

```json
{
  "success": true,
  "expression": "1+2*3",
  "result": 7
}
```

Error response (HTTP 400):

```json
{
  "success": false,
  "message": "Division by zero is not allowed"
}
```

### 2. Get History

Request: GET /api/history

Response (HTTP 200):

```json
{
  "success": true,
  "history": [
    {
      "id": 1,
      "expression": "1+2*3",
      "result": "7",
      "created_at": "2026-10-04 15:20:00"
    }
  ]
}
```

### 3. Delete a History Record

Request: DELETE /api/history/{id}

Response (HTTP 200):

```json
{ "success": true }
```

Returns HTTP 404 if the record does not exist.

### 4. Clear All History

Request: DELETE /api/history

Response (HTTP 200):

```json
{ "success": true, "message": "All history cleared" }
```

## Sample Runtime Log

After startup, the terminal prints incoming requests in real time, for example:

```text
127.0.0.1 - - [04/Oct/2026 22:33:01] "OPTIONS /api/calculate HTTP/1.1" 200 -
127.0.0.1 - - [04/Oct/2026 22:33:01] "POST /api/calculate HTTP/1.1" 200 -
127.0.0.1 - - [04/Oct/2026 22:33:01] "GET /api/history HTTP/1.1" 200 -
127.0.0.1 - - [04/Oct/2026 22:34:13] "DELETE /api/history HTTP/1.1" 200 -
```

All status codes are 200, indicating the frontend and backend communicate correctly.

## Security Notes

The backend strictly forbids executing arbitrary user input as code. The evaluation flow is:

1. A regex whitelist `^[\d\s+\-*/().]+$` is applied first, allowing only digits, spaces, operators `+ - * /`, parentheses, and decimal points.
2. Because letters, underscores, and brackets are rejected, users cannot construct calls to system functions or dangerous expressions.
3. The evaluation uses `eval(expr, {"__builtins__": None}, {})`, restricting `__builtins__` to empty to further prevent code injection.
4. All exceptions are converted into standardized error responses.

## Project Structure

```text
calculator_backend/
├── app.py            # Main backend program
├── calculator.db     # SQLite database (auto-generated on first run)
├── README.md         # Project documentation
└── codestyle.md      # Code style guide
```

## FAQ

Q1: "Address already in use" on startup?

A: Port 5000 is occupied, possibly by a previous Python process. End all python.exe processes in Task Manager and restart.

Q2: The frontend shows "Cannot connect to backend"?

A: Confirm the backend is running and that the browser can access http://127.0.0.1:5000/api/history.

Q3: What if the database file is lost?

A: Just restart the backend; calculator.db will be recreated automatically.

Q4: Why is the full path used instead of just `python`?

A: Python is installed at D:\软件\python and is not added to the system PATH. Typing just `python` will not be recognized, so the full path is used.
```
