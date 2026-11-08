@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

if not exist "app\vendor\pyodide\pyodide.js" goto :missing
if not exist "app\vendor\pyodide\pyodide.asm.js" goto :missing
if not exist "app\vendor\pyodide\pyodide.asm.wasm" goto :missing
if not exist "app\vendor\pyodide\python_stdlib.zip" goto :missing
if not exist "app\vendor\pyodide-legacy\pyodide.js" goto :missing
if not exist "app\vendor\pyodide-legacy\pyodide.asm.wasm" goto :missing
if not exist "app\vendor\pyodide-legacy\python_stdlib.zip" goto :missing
goto :run

:missing
echo.
echo ERROR: app\vendor\pyodide is incomplete.
echo Copy the whole playground folder, or ask the teacher to restore the offline engine.
echo.
pause
exit /b 1

:run
REM Important: first quoted arg to START is the window TITLE.
REM Always use empty title "" — a Persian title can make START mis-parse and
REM launch a second odd process that looks like the launcher reopening.
where pythonw >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /B pythonw "%~dp0app\launcher.py"
  exit /b 0
)

where python >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /B python "%~dp0app\launcher.py"
  exit /b 0
)

where py >nul 2>&1
if %ERRORLEVEL%==0 (
  start "" /B py -3 "%~dp0app\launcher.py"
  exit /b 0
)

echo Python was not found. Trying tools\start-cli.bat ...
call "%~dp0tools\start-cli.bat"
exit /b %ERRORLEVEL%
