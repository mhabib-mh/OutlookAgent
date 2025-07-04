@echo off
echo.================================================
echo. Stopping Outlook MCP Server...
echo.================================================

:: Check if Uvicorn is running
echo.
echo. Checking for running Uvicorn server...

:: Kill any Uvicorn process (Windows)
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "uvicorn.exe"') do taskkill /F /PID %%a >nul 2>&1

:: Kill any Python process running Uvicorn
for /f "tokens=2" %%a in ('tasklist ^| findstr /i "python.exe"') do (
    tasklist /fi "PID eq %%a" | findstr /i "uvicorn" >nul && taskkill /F /PID %%a
)

call deactivate
echo.
echo.================================================
echo. Server stopped successfully.
echo.================================================
pause
