@echo off
@rem RUN AS ADMINISTRATOR!
@rem This script creates the assets folders for games for usage with AEL (Advanced Emulator Launcher)
@rem It makes use of assets scraped from emumovies to \\192.168.0.100\Games\Assets\<console>\<artwork>

set PATH=
set /P PATH=Specify the path to your AEL-assets folder (empty = current directory): 
if "%PATH%"=="" goto N64
cd /D %PATH%
goto N64

:N64
echo.
set N64=
set CLEANUP=
set /P N64=Create Nintendo_N64 AEL assets folder? (Y/n): 
if not "%N64%"=="" if not "%N64%"=="y" goto NES
if exist %cd%\Nintendo_N64 set /P CLEANUP=Nintendo_N64 already exists, remove it? (Y/n): 
if "%CLEANUP%"=="" rmdir /S /Q Nintendo_N64
if "%CLEANUP%"=="y" rmdir /S /Q Nintendo_N64
echo Creating Nintendo_N64 AEL assets
mkdir Nintendo_N64
cd Nintendo_N64
mklink /D titles \\192.168.0.100\Games\Assets\Nintendo_N64\Title
mklink /D snaps \\192.168.0.100\Games\Assets\Nintendo_N64\Snap
mklink /D boxfronts \\192.168.0.100\Games\Assets\Nintendo_N64\Box
mklink /D boxbacks \\192.168.0.100\Games\Assets\Nintendo_N64\BoxBack
mklink /D cartridges \\192.168.0.100\Games\Assets\Nintendo_N64\Cart
mklink /D fanarts \\192.168.0.100\Games\Assets\Nintendo_N64\Background
mkdir banners
mklink /D clearlogos \\192.168.0.100\Games\Assets\Nintendo_N64\Logos
mkdir flyers
mkdir maps
mkdir manuals
mkdir trailers

cd ..

:NES
echo.
set NES=
set CLEANUP=
set /P NES=Create Nintendo_NES AEL assets folder (Y/n): 
if not "%NES%"=="" if not "%NES%"=="y" goto SNES
if exist %cd%\Nintendo_NES set /P CLEANUP=Nintendo_NES already exists, remove it? (Y/n): 
if "%CLEANUP%"=="" rmdir /S /Q Nintendo_NES
if "%CLEANUP%"=="y" rmdir /S /Q Nintendo_NES
echo Creating Nintendo_NES AEL assets
mkdir Nintendo_NES
cd Nintendo_NES
mklink /D titles \\192.168.0.100\Games\Assets\Nintendo_NES\Title
mklink /D snaps \\192.168.0.100\Games\Assets\Nintendo_NES\Snap
mklink /D boxfronts \\192.168.0.100\Games\Assets\Nintendo_NES\Box
mklink /D boxbacks \\192.168.0.100\Games\Assets\Nintendo_NES\BoxBack
mklink /D cartridges \\192.168.0.100\Games\Assets\Nintendo_NES\Cart
mkdir fanarts
mkdir banners
mklink /D clearlogos \\192.168.0.100\Games\Assets\Nintendo_NES\Logos
mkdir flyers
mkdir maps
mkdir manuals
mkdir trailers

cd ..

:SNES
echo.
set SNES=
set CLEANUP=
set /P SNES=Create Nintendo_SNES AEL assets folder (Y/n): 
if not "%SNES%"=="" if not "%SNES%"=="y" goto GEN
if exist %cd%\Nintendo_SNES set /P CLEANUP=Nintendo_SNES already exists, remove it? (Y/n): 
if "%CLEANUP%"=="" rmdir /S /Q Nintendo_SNES
if "%CLEANUP%"=="y" rmdir /S /Q Nintendo_SNES
echo Creating Nintendo_SNES AEL assets
mkdir Nintendo_SNES
cd Nintendo_SNES
mklink /D titles \\192.168.0.100\Games\Assets\Nintendo_SNES\Title
mklink /D snaps \\192.168.0.100\Games\Assets\Nintendo_SNES\Snap
mklink /D boxfronts \\192.168.0.100\Games\Assets\Nintendo_SNES\Box
mkdir boxbacks
mklink /D cartridges \\192.168.0.100\Games\Assets\Nintendo_SNES\Cart
mklink /D fanarts \\192.168.0.100\Games\Assets\Nintendo_SNES\Background
mkdir banners
mklink /D clearlogos \\192.168.0.100\Games\Assets\Nintendo_SNES\Logos
mkdir flyers
mkdir maps
mkdir manuals
mkdir trailers

cd ..

:GEN
echo.
set GEN=
set CLEANUP=
set /P GEN=Create Sega_Genesis AEL assets folder (Y/n): 
if not "%GEN%"=="" if not "%GEN%"=="y" goto SMS
if exist %cd%\Sega_Genesis set /P CLEANUP=Sega_Genesis already exists, remove it? (Y/n): 
if "%CLEANUP%"=="" rmdir /S /Q Sega_Genesis
if "%CLEANUP%"=="y" rmdir /S /Q Sega_Genesis
echo Creating Sega_Genesis AEL assets
mkdir Sega_Genesis
cd Sega_Genesis
mklink /D titles \\192.168.0.100\Games\Assets\Sega_Genesis\Title
mklink /D snaps \\192.168.0.100\Games\Assets\Sega_Genesis\Snap
mklink /D boxfronts \\192.168.0.100\Games\Assets\Sega_Genesis\Box
mkdir boxbacks
mklink /D cartridges \\192.168.0.100\Games\Assets\Sega_Genesis\Cart
mklink /D fanarts \\192.168.0.100\Games\Assets\Sega_Genesis\Background
mkdir banners
mklink /D clearlogos \\192.168.0.100\Games\Assets\Sega_Genesis\Logos
mkdir flyers
mkdir maps
mkdir manuals
mkdir trailers

cd ..

:SMS
echo.
set SMS=
set CLEANUP=
set /P SMS=Create Sega_Master_System AEL assets folder (Y/n): 
if not "%SMS%"=="" if not "%SMS%"=="y" goto END
if exist %cd%\Sega_Master_System set /P CLEANUP=Sega_Master_System already exists, remove it? (Y/n): 
if "%CLEANUP%"=="" rmdir /S /Q Sega_Master_System
if "%CLEANUP%"=="y" rmdir /S /Q Sega_Master_System
echo Creating Sega_Master_System AEL assets
mkdir Sega_Master_System
cd Sega_Master_System
mklink /D titles \\192.168.0.100\Games\Assets\Sega_Master_System\Title
mklink /D snaps \\192.168.0.100\Games\Assets\Sega_Master_System\Snap
mklink /D boxfronts \\192.168.0.100\Games\Assets\Sega_Master_System\Box
mklink /D boxbacks \\192.168.0.100\Games\Assets\Sega_Master_System\BoxBack
mklink /D cartridges \\192.168.0.100\Games\Assets\Sega_Master_System\Cart
mklink /D fanarts \\192.168.0.100\Games\Assets\Sega_Master_System\Background
mkdir banners
mklink /D clearlogos \\192.168.0.100\Games\Assets\Sega_Master_System\Logos
mkdir flyers
mkdir maps
mkdir manuals
mkdir trailers

cd ..

:END