@echo off
echo =========================================
echo Restarting Outlook MCP Server...
echo =========================================

:: Call stop and start scripts
call stop_server.bat
call start_server.bat
