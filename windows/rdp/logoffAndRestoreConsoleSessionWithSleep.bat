@rem Logoff from remote desktop and restore the console (sessinID = 1) session and put computer to sleep
@rem In case you have hibernate enabled on your pc, you'll also need to disable it (see https://winaero.com/blog/how-to-sleep-a-windows-computer-from-the-command-line/)
@rem A small timeout is added in between to be sure the remote desktop connection is properly ended and console is restored
@rem Run with administrative rights
@rem Program location: %windir%\system32
tscon.exe 1 /dest:console
timeout 2 /nobreak
powercfg -hibernate off
rundll32.exe powrprof.dll,SetSuspendState 0,1,0
powercfg -hibernate on
