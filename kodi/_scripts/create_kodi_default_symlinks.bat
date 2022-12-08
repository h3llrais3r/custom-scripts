rem Launch bat with administrative rights!
call kodi_settings.bat

echo Creating kodi default symlinks
mklink %KODI_USERDATA_DIR%\sources.xml %~dp0..\userdata\sources.xml
mklink %KODI_USERDATA_DIR%\passwords.xml %~dp0..\userdata\passwords.xml
mklink %KODI_USERDATA_DIR%\advancedsettings.xml %~dp0..\userdata\advancedsettings.xml
