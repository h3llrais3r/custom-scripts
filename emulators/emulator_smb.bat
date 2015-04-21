@echo off
@rem Launch an emulator with a game rom from a smb share
@rem Remove the 'smb:' prefix from the %ROM% parameter
@rem This is needed because the emulators cannot open a file like "smb://<path_to_rom>"
@rem %1 = %EMULATOR% parameter
@rem %2 = %ROM% parameter
set OLDDIR=%CD%
set EMULATOR_PATH=C:\Tools\Emulators
if %1=="NES" goto :NES
if %1=="SNES" goto :SNES
if %1=="N64" goto :N64
if %1=="SEGA" goto :SEGA
if %1=="SMS" goto :SMS
if %1=="GEN" goto :GEN
if %1=="MAME" goto :MAME
:NES
set EMULATOR_PATH=%EMULATOR_PATH%\Nestopia 
set EMULATOR=nestopia.exe
goto :ROM
:SNES
set EMULATOR_PATH=%EMULATOR_PATH%\Snes9x
set EMULATOR=snes9x-x64.exe -fullscreen
goto :ROM
:N64
set EMULATOR_PATH=%EMULATOR_PATH%\Project64
set EMULATOR=project64.exe
goto :ROM
:SEGA
set EMULATOR_PATH=%EMULATOR_PATH%\Fusion
set EMULATOR=fusion.exe -auto -fullscreen
goto :ROM
:SMS
set EMULATOR_PATH=%EMULATOR_PATH%\Fusion
set EMULATOR=fusion.exe -sms -auto -fullscreen
goto :ROM
:GEN
set EMULATOR_PATH=%EMULATOR_PATH%\Fusion
set EMULATOR=fusion.exe -gen -auto -fullscreen
goto :ROM
:MAME
set EMULATOR_PATH=%EMULATOR_PATH%\Mame
set EMULATOR=mame64.exe -skip_gameinfo
goto :ROM
:ROM
if %2=="SMB" goto :SMB
set ROM=%2
@rem remove " before and after rom for N64
if %1=="N64" set ROM=%ROM:~1,-1%
goto :START_EMULATOR
:SMB
set ROM=%3
@rem remove "smb: at the front and " at the end
set ROM=%ROM:~5,-1%
@rem add " before and after rom for non N64
if not %1=="N64" set ROM="%ROM%"
goto :START_EMULATOR
:START_EMULATOR
cd %EMULATOR_PATH%
echo call %EMULATOR% %ROM%
call %EMULATOR% %ROM%
cd %OLDDIR%