@echo off
@rem make sure that python.exe is in your path!
echo.
python %~dp0\autoMoveAndCleanup.py %1 %2 %3 %4 %5 %6
@rem C:\Tools\Python36-32\python.exe %~dp0\autoMoveAndCleanup.py %1 %2 %3 %4 %5 %6