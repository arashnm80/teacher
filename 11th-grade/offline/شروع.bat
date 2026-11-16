@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

if not exist "playground\vendor\pyodide\pyodide.js" goto :missing
if not exist "playground\vendor\pyodide\pyodide.asm.js" goto :missing
if not exist "playground\vendor\pyodide\pyodide.asm.wasm" goto :missing
if not exist "playground\vendor\pyodide\python_stdlib.zip" goto :missing
if not exist "playground\vendor\pyodide-legacy\pyodide.js" goto :missing
if not exist "playground\vendor\pyodide-legacy\pyodide.asm.wasm" goto :missing
if not exist "playground\vendor\pyodide-legacy\python_stdlib.zip" goto :missing
if not exist "playground\vendor\codemirror\codemirror.min.js" goto :missing
if not exist "playground\vendor\codemirror\mode\python\python.min.js" goto :missing
goto :run

:missing
echo.
echo ERROR: playground\vendor is incomplete. Unzip the whole file again.
echo.
pause
exit /b 1

:run
REM Empty title "" on purpose: a title can make START mis-parse.
where pythonw >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /B pythonw "%~dp0playground\launcher.py"
  exit /b 0
)
where python >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /B python "%~dp0playground\launcher.py"
  exit /b 0
)
where py >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /B py -3 "%~dp0playground\launcher.py"
  exit /b 0
)
echo.
echo Python 3 was not found. Install Python 3 (with tkinter), then run this file again.
echo.
pause
exit /b 1
