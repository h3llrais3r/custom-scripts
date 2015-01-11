@rem Show all running processes
@rem Program location: %windir%\system32\wbem
wmic.exe /OUTPUT:C:\Temp\processes.txt PROCESS get Caption,Commandline,Processid