@rem Logoff from remote desktop and restore the console (sessinID = 1) session
@rem Run with administrative rights
@rem Program location: %windir%\system32
tscon.exe 1 /dest:console
