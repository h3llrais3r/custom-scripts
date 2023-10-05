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
- Push userdata to download folder on device with adb: `adb push /path/to/userdata /storage/emulated/0/Download`
- Use the kodi file browser to copy required userdata from this source to your kodi installation profile
