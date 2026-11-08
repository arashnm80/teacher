@echo off
setlocal
cd /d "%~dp0"
REM Terminal-only server (no GUI). Teachers / debugging.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve.ps1" %*
