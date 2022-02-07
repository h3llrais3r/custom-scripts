rem Launch bat with administrative rights!
call kodi_settings.bat

echo Creating kodi movies library symlinks
set INPUT_DIR=library\movies
set DEST_DIR=%KODI_USERDATA_DIR%\%INPUT_DIR%
mkdir -p %DEST_DIR%
for /f "tokens=*" %%f in ('dir /s /b /a-d "%~dp0%INPUT_DIR%"') do mklink "%DEST_DIR%\%%~nxf" "%%~dpnxf"

echo Creating kodi tvshows library symlinks
set INPUT_DIR=library\tvshows
set DEST_DIR=%KODI_USERDATA_DIR%\%INPUT_DIR%
mkdir -p %DEST_DIR%
for /f "tokens=*" %%f in ('dir /s /b /a-d "%~dp0%INPUT_DIR%"') do mklink "%DEST_DIR%\%%~nxf" "%%~dpnxf"
