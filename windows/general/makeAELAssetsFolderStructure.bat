REM RUN AS ADMINISTRATOR AT THE LOCATION WHERE YOU WANT TO CREATE THE FOLDER STRUCTURE!

REM Make Nintendo_NES AEL assets
rmdir /S Nintendo_NES
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

cd..

REM Make Nintendo_SNES AEL assets
rmdir /S Nintendo_SNES
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

cd..

REM Make Sega_Genesis AEL assets
rmdir /S Sega_Genesis
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

cd..

REM Make Sega_Master_System AEL assets
rmdir /S Sega_Master_System
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

cd..