# Setup on Windows

- Run the `create_kodi_xxx.bat` files for the desired userdata you want to symlink to you kodi installation


# Setup on Chromecast

- Location userdata on chromecast: `/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/userdata/`
- Location logs on chromecast: `/storage/emulated/0/Android/data/org.xbmc.kodi/files/.kodi/temp/kodi.log`

- Adapt kodi app rights: access to files -> always
- Enable developer tools on chromecast
- Enabled adb (android debugging) in developer tools
- Connect to chromecast via adb: `adb connect <ip>`
- Allow adb connection on chromecast
- Add new source in kodi file browser to: `/storage/emulated/0/Download`
- Push userdata to download folder on device with adb: `adb push C:\Tools\GitHub\custom-scripts\kodi\userdata /storage/emulated/0/Download`
- Use the kodi file browser to copy required userdata from this source to your kodi installation profile

# Jellyfin for kodi installation

- Download `repository.jellyfin.kodi.zip` from https://jellyfin.org/docs/general/clients/kodi/
- Push zip to download folder on device with adb: `adb push C:\Temp\repository.jellyfin.kodi.zip /storage/emulated/0/Download`
- Enable unknown sources in Kodi settings: System - Addons
- Install addon repository in kodi from zip
- Install Jellyfin for kodi addon from repository in kodi
