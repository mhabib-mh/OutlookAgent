@echo off
echo.================================================
echo. Starting Outlook MCP Server with Poetry...      
echo.================================================

:: Navigate to the mcp_server directory
cd ..\mcp_server || (
    echo.
    echo. Error: mcp_server directory not found.
    echo. Ensure you are running this script from the 'scripts' directory.
    echo.
    exit /b
)

:: Check Global Environment
echo.-------------------------------------------------
echo. Check Global Environment...
echo.-------------------------------------------------

:: Check if Python is installed
echo.
echo. Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo. Python is not installed.
    echo. Please install Python from https://www.python.org/downloads/
    exit /b
) else (
    echo. Python is installed.
    echo.
)

:: Setting up the virtual environment (.venv) using Poetry
echo.
echo. Setting up the virtual environment (.venv)...
if not exist ".venv" (
    echo. Creating virtual environment using Poetry...
    python -m venv .venv
)

:: Activate the Virtual Environment
echo.-------------------------------------------------
echo. Activating Virtual Environment for MCP_Server...
echo.-------------------------------------------------

call .venv\Scripts\activate

:: Ensure Poetry is available in the venv
echo.
echo. Checking if Poetry is installed...
.venv\Scripts\python -m pip show poetry >nul 2>&1
if errorlevel 1 (
    echo. Poetry is not installed. Installing Poetry...
    .venv\Scripts\python -m pip install poetry
) else (
    echo. Poetry is already installed.
)

:: Install Dependencies using Poetry
echo.
echo. Installing Dependencies with Poetry...
.venv\Scripts\poetry install

:: Load environment variables from the .env file if it exists
echo.
if exist ".env" (
    echo. Loading environment variables from .env...
    for /f "tokens=1,* delims==" %%A in (.env) do (
        set "%%A=%%B"
        echo. Loaded %%A=%%B
    )
) else (
    echo.
    echo. Warning: .env file not found. Skipping environment variable loading.
    echo.
)

:: Set PYTHONPATH dynamically for local usage (avoids mcp_server import issues)
set PYTHONPATH=.
echo.
echo. PYTHONPATH set to: %PYTHONPATH%


:: Start the Uvicorn server using Poetry
echo.
echo.================================================
echo. Starting Uvicorn server on http://127.0.0.1:8000...
echo.================================================
echo.
.venv\Scripts\poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
