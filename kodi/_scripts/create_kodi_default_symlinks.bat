rem Launch bat with administrative rights!
call kodi_settings.bat

echo Creating kodi default symlinks
mklink %KODI_USERDATA_DIR%\sources.xml %~dp0..\sources.xml
mklink %KODI_USERDATA_DIR%\passwords.xml %~dp0..\passwords.xml
mklink %KODI_USERDATA_DIR%\advancedsettings.xml %~dp0..\advancedsettings.xml
