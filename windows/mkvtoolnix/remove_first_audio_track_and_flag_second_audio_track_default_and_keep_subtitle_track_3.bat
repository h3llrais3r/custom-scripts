REM Remove the first audio track from the mkv and flag the second one as default
FOR /F "delims=*" %%A IN ('dir /b *.mkv') DO "C:\\Tools\\mkvtoolnix\\mkvmerge.exe" -o "fixed_%%A" -a !1 --default-track 2 --subtitle-tracks 3 --compression -1:none "%%A"
PAUSE