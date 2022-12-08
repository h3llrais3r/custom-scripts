rem Launch bat with administrative rights!
call kodi_settings.bat

echo Creating kodi keymaps symlinks
set INPUT_DIR=userdata\keymaps
set DEST_DIR=%KODI_USERDATA_DIR%\%INPUT_DIR%
mkdir %DEST_DIR%
for /f "tokens=*" %%f in ('dir /s /b /a-d "%~dp0..\%INPUT_DIR%"') do mklink "%DEST_DIR%\%%~nxf" "%%~dpnxf"
