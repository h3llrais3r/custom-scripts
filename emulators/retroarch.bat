@echo off
@rem Launch RetroArch emulator
@rem REMARK: file must be a .cmd file because a .bat file will mess up the double \\ in the rom path
@rem %1 = %LAUNCHER% parameter
@rem %2 = %ROM% parameter
set OLDDIR=%CD%
set RETROARCH_PATH=C:\Tools\RetroArch-Win64
set ROM=%2
if "%1"=="N64" goto N64
if "%1"=="NES" goto NES
if "%1"=="SNES" goto SNES
if "%1"=="SMS" goto SMS
if "%1"=="GEN" goto GEN
if "%1"=="MAME" goto MAME
echo No launcher specified
goto END

:N64
set EMULATOR_CORE_PATH="%RETROARCH_PATH%\cores\parallel_n64_libretro.dll"
goto SET_COMMAND

:NES
set EMULATOR_CORE_PATH="%RETROARCH_PATH%\cores\nestopia_libretro.dll"
goto SET_COMMAND

:SNES
set EMULATOR_CORE_PATH="%RETROARCH_PATH%\cores\snes9x_libretro.dll"
goto SET_COMMAND

:SMS
set EMULATOR_CORE_PATH="%RETROARCH_PATH%\cores\genesis_plus_gx_libretro.dll"
goto SET_COMMAND

:GEN
SET EMULATOR_CORE_PATH="%RETROARCH_PATH%\cores\genesis_plus_gx_libretro.dll"
goto SET_COMMAND

:MAME
SET EMULATOR_CORE_PATH="%RETROARCH_PATH%\cores\mame2003_plus_libretro.dll"
goto SET_COMMAND

:SET_COMMAND
set RETROARCH_COMMAND=%RETROARCH_PATH%\retroarch.exe -L %EMULATOR_CORE_PATH% -f %ROM%
goto LAUNCH_RETROARCH

:LAUNCH_RETROARCH
cd %RETROARCH_PATH%
echo Launching %RETROARCH_COMMAND%
call %RETROARCH_COMMAND%
goto END

:END
cd %OLDDIR%