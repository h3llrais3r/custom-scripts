rem Launch bat with administrative rights!
call kodi_settings.bat

echo Creating kodi video playlists symlinks
set INPUT_DIR=playlists\video
set DEST_DIR=%KODI_USERDATA_DIR%\%INPUT_DIR%
mkdir %DEST_DIR%
for /f "tokens=*" %%f in ('dir /s /b /a-d "%~dp0..\userdata\%INPUT_DIR%"') do mklink "%DEST_DIR%\%%~nxf" "%%~dpnxf"