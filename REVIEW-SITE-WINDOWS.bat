@echo off
setlocal EnableExtensions
cd /d "%~dp0"
echo.
echo    NCNS DIGITAL - PRIVATE LOCAL SITE PREVIEW
echo    This starts only on your PC at http://127.0.0.1:8765/
echo    Nothing is published to the internet.
echo.
where py >nul 2>nul
if not errorlevel 1 (
  set "PYEXE=py -3"
  goto run
)
where python >nul 2>nul
if not errorlevel 1 (
  set "PYEXE=python"
  goto run
)
echo ERROR: Python 3 is not installed or unavailable in PATH.
echo Install Python 3, then double-click this file again.
pause
exit /b 1
:run
start "NCNS local preview server - close to stop" cmd /k "%PYEXE% -m http.server 8765 --bind 127.0.0.1"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8765/"
echo.
echo If the site did not open, copy this into your browser:
echo http://127.0.0.1:8765/
echo.
echo Close the "NCNS local preview server" window to stop the preview.
pause
