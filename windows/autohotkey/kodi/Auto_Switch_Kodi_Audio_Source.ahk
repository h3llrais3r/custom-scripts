; This script detects the headset and handles kodi audio settings accordingly
; By default the 5.1 receiver is enabled
; When the headset is connected, it switches to the settings for the headset
; When the headset is disconnected, it switches back to the settings for the receiver
; REMARK: I assume that the headset becomes the default audio devices in windows when it connects; if not, we'll also need to add a switch of audio device in the kodi settings (not included in this script)
; To hunt down the GUID, use Detect_Hardware_Changes.ahk

; GUID of device from which you want to detect the hardware changes
DEVICE_CLASS_GUID={C166523C-FE0C-4A94-A586-F1A80CFBBF3E} ; Headset

#persistent
#SingleInstance force

;Monitor for WM_DEVICECHANGE
OnMessage(0x219, "MsgMonitor")

hWnd := GetAHKWin()

DEVICE_NOTIFY_WINDOW_HANDLE := 0x0
DEVICE_NOTIFY_ALL_INTERFACE_CLASSES := 0x00000004
DBT_DEVTYP_DEVICEINTERFACE := 5
DBT_DEVICEARRIVAL := 0x8000
DBT_DEVICEREMOVECOMPLETE := 0x8004
DIGCF_ALLCLASSES := 0x00000004 ; list of installed devices for all device setup classes or all device interface classes
DIGCF_DEVICEINTERFACE := 0x00000010 ; devices that support device interfaces for the specified device interface classes.

VarSetCapacity(DevHdr, 32, 0)
NumPut(32, DevHdr, 0, "UInt") ; sizeof(_DEV_BROADCAST_DEVICEINTERFACE)
NumPut(DBT_DEVTYP_DEVICEINTERFACE, DevHdr, 4, "UInt") ; DBT_DEVTYP_DEVICEINTERFACE
Addr := &DevHdr
Flags := DEVICE_NOTIFY_WINDOW_HANDLE|DEVICE_NOTIFY_ALL_INTERFACE_CLASSES
Msg = %Msg%RegisterDeviceNotification(%hWnd%, %Addr%, %Flags%)`r`n
Ret := DllCall("RegisterDeviceNotification", "UInt", hWnd, "UInt", Addr, "UInt", Flags)
if (!Ret)
{
    MsgBox, Unable to RegisterDeviceNotification!
    ExitApp
}
Return

MsgMonitor(wParam, lParam, msg)
{
    global DEVICE_CLASS_GUID, DBT_DEVTYP_DEVICEINTERFACE, DBT_DEVICEARRIVAL, DBT_DEVICEREMOVECOMPLETE
    
    if (wParam == DBT_DEVICEARRIVAL)
    {
        ; lParam points to a DEV_BROADCAST_HDR structure
        dbch_size       := NumGet(lParam+0, 0, "UInt")
        dbch_devicetype := NumGet(lParam+0, 4, "UInt")
        if (dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE)
        {
            ; lParam points to a DEV_BROADCAST_DEVICEINTERFACE structure
            dbcc_name := GetString(lParam+28)
            dbcc_classguid := GetGuid(lParam+12)
            devices := ListDevices(lParam+12, dbcc_name) ; list devices impacted by hardware change
            if(InStr(devices, DEVICE_CLASS_GUID)) ; check if our device is impacted
            {
                ;MsgBox, added
                ; Load headset settings
                Run load_headset_settings.py
            }
        }
    } 
    else if (wParam == DBT_DEVICEREMOVECOMPLETE)
    {
        ; lParam points to a DEV_BROADCAST_HDR structure
        dbch_size       := NumGet(lParam+0, 0, "UInt")
        dbch_devicetype := NumGet(lParam+0, 4, "UInt")
        if (dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE)
        {
            ; lParam points to a DEV_BROADCAST_DEVICEINTERFACE structure
            dbcc_name := GetString(lParam+28)
            dbcc_classguid := GetGuid(lParam+12)
            devices := ListDevices(lParam+12, dbcc_name) ; list devices impacted by hardware change
            if(InStr(devices, DEVICE_CLASS_GUID)) ; check if our device is impacted
            {  
                ;MsgBox, removed
                ; Load receiver settings
                Run load_receiver_settings.py
            }
        }
    }  
}

ListDevices(GUIDAddr = 0, FindDevicePath = "")
{
    global DIGCF_DEVICEINTERFACE, DIGCF_ALLCLASSES
   
    hMod := DllCall("LoadLibrary", "str", "setupapi.dll")
    hDev := DllCall("setupapi\SetupDiGetClassDevs", "UInt", GuidAddr, "UInt", 0, "UInt", 0, "UInt", DIGCF_DEVICEINTERFACE)
    
    Loop
    {
        VarSetCapacity(DevInfoData, 32)
        NumPut(32, DevInfoData, 0, "UInt")
        if (GUIDAddr == 0)
        {
            Ret := DllCall("setupapi\SetupDiEnumDeviceInfo", "UInt", hDev, "UInt", A_Index - 1, "UInt", &DevInfoData)
            if (Ret == 0)
            {
                break
            }
            Name := "Unknown"
        }
        else
        {
            VarSetCapacity(DID, 32)
            NumPut(32, DID, 0)
            Ret := DllCall("setupapi\SetupDiEnumDeviceInterfaces", "UInt", hDev, "UInt", 0, "UInt", GUIDAddr, "UInt", A_Index-1, "UInt", &DID)
            if (Ret <> 1)
            {
                if (Ret != 0 && A_LastError <> 259)
                {
                    ErrMsg := FormatMessageFromSystem(A_LastError)
                    sRes = %sRes% Ret %Ret% ErrorLevel %ErrorLevel% %A_LastError% %ErrMsg%
                }
                break
            }
            Name := "Unknown"
         
            VarSetCapacity(RightSize, 4)
         
            Ret := DllCall("setupapi\SetupDiGetDeviceInterfaceDetail", "UInt", hDev, "UInt", &DID, "UInt", 0, "UInt", 0, "UInt", &RightSize, "UInt", 0)
            if (Ret <> 1 && A_LastError <> 122)
            {
                ErrMsg := FormatMessageFromSystem(A_LastError)
                sRes = %sRes% Ret %Ret% ErrorLevel %ErrorLevel% %A_LastError% %ErrMsg%
            }

            SetSize := NumGet(RightSize, 0, "UInt")

            VarSetCapacity(DevInfoData, 32)
            NumPut(32, DevInfoData, 0, "UInt")
            
            VarSetCapacity(DevIntDetData, SetSize)
            NumPut(8, DevIntDetData, 0, "UInt")
            Ret := DllCall("setupapi\SetupDiGetDeviceInterfaceDetail", "UInt", hDev, "UInt", &DID, "UInt", &DevIntDetData, "UInt", SetSize, "UInt", &RightSize, "UInt", &DevInfoData)
            if (Ret <> 1)
            {
                ErrMsg := FormatMessageFromSystem(A_LastError)
                sRes = %sRes% Ret %Ret% ErrorLevel %ErrorLevel% %A_LastError% %ErrMsg%
            }
            Name := GetString(&DevIntDetData+4)
        }

        if (FindDevicePath <> "" && FindDevicePath <> Name)
        {
            continue
        }
         
        sRes .= "Device " . A_Index . " - DevInfoData Size " . NumGet(DevInfoData, 0, "UInt") . " - Device Class GUID " . GetGuid(&DevInfoData+4) . " - " . NumGet(DevInfoData, 20, "UInt") . "`r`n"
    }

    DllCall("setupapi\SetupDiDestroyDeviceInfoList", "UInt", hDev)
    DllCall("FreeLibrary", "UInt", hMod)
    
    Return sRes
}

GetAHKWin()
{
    Gui + LastFound
    hwnd := WinExist()
    Return hwnd
}

GetString(Addr)
{
   OutString := ""
   VarSetCapacity(OutString, 1024, 0)
   Loop
   {
        Char := *Addr+0
        ;MsgBox, %Char%
        if (Char == 0)
        {
            break
        }
        OutString .= Chr(Char)
        Addr ++
   }
   Return OutString
}

GetGuid(FromAddr)
{
    Guid := "{" . GetPaddedHex(FromAddr+0, "UInt", 8) . "-" . GetPaddedHex(FromAddr+4, "UShort", 4) . "-" . GetPaddedHex(FromAddr+6, "UShort", 4) . "-" 
            . GetPaddedHex(FromAddr+8, "UChar", 2) . GetPaddedHex(FromAddr+9, "UChar", 2) . "-" . GetPaddedHex(FromAddr+10, "UChar", 2) . GetPaddedHex(FromAddr+11, "UChar", 2) 
            . GetPaddedHex(FromAddr+12, "UChar", 2) . GetPaddedHex(FromAddr+13, "UChar", 2) . GetPaddedHex(FromAddr+14, "UChar", 2) . GetPaddedHex(FromAddr+15, "UChar", 2) . "}"
    Return Guid
}

; Get padded hex value from an address, pad with leading 0s up to 16 
GetPaddedHex(FromAddr, Type, PadLen)
{
    Old := A_FormatInteger 
    SetFormat, IntegerFast, Hex
    Pad := "0000000000000000"
    ; Get the number in hex
    HexStr := NumGet(FromAddr+0, 0, Type) 
    ;MsgBox, %HexStr% %Type%
    ; Strip leading 0x 
    HexStr := SubStr(HexStr, 3, StrLen(HexStr) - 2)
    ; Pad 
    if (StrLen(HexStr) < PadLen)
    {
        HexStr := SubStr(Pad, 1, PadLen - StrLen(HexStr)) . HexStr
    }
    SetFormat, IntegerFast, %Old%
    Return HexStr
}

FormatMessageFromSystem(ErrorCode)
{
    VarSetCapacity(Buffer, 2000, 32 )
    DllCall("FormatMessage"
        , "UInt", 0x1000 ; FORMAT_MESSAGE_FROM_SYSTEM
        , "UInt", 0
        , "UInt", ErrorCode
        , "UInt", 0x800 ; LANG_SYSTEM_DEFAULT (LANG_USER_DEFAULT=0x400)
        , "UInt", &Buffer
        , "UInt", 500
        , "UInt", 0)
      
    ; Strip any newlines
    Buffer := RegExReplace(Buffer, "\r\n", " ")
    Return Buffer
}