; Show a list of hardware in the system then follow hardware change notifications
; 
; Demonstrates the use of RegisterDeviceNotification and WM_DEVICECHANGE messages to detect device changes as well as the setupapi functions to find information about the devices in question
; Based on https://autohotkey.com/board/topic/70334-detecting-hardware-changes-for-example-new-usb-devices/
; Modified for 64bit systems

#SingleInstance force
#NoTrayIcon

; Monitor for WM_DEVICECHANGE 
OnMessage(0x219, "MsgMonitor")

hWnd := GetAHKWin()

Gui, Add, Text,, Current Harware List:
Gui, Add, Edit, HScroll w800 h300 vInfoOut -Wrap ReadOnly HwndInfoHwnd
Gui, Add, Text,, Harware Notifications:
Gui, Add, Edit, HScroll w800 h300 vLogOut -Wrap ReadOnly HwndLogHwnd
;Gui, Add, Button, Default gCapture vCaptureButton w150, &Capture
Gui, Show, , %A_ScriptName%

DEVICE_NOTIFY_WINDOW_HANDLE := 0x0 
DEVICE_NOTIFY_ALL_INTERFACE_CLASSES := 0x00000004
DBT_DEVTYP_DEVICEINTERFACE := 5
DBT_DEVNODES_CHANGED := 0x0007
DBT_DEVICEREMOVECOMPLETE := 0x8004
DBT_DEVICEARRIVAL := 0x8000
DBT_DEVTYP_DEVICEINTERFACE := 0x00000005
DIGCF_DEFAULT := 0x00000001 ; only valid with DIGCF_DEVICEINTERFACE; only the device that is associated with the system default device interface
DIGCF_PRESENT := 0x00000002 ; only devices that are currently present in a system
DIGCF_ALLCLASSES := 0x00000004 ; list of installed devices for all device setup classes or all device interface classes
DIGCF_PROFILE := 0x00000008 ; only devices that are a part of the current hardware profile
DIGCF_DEVICEINTERFACE := 0x00000010 ; devices that support device interfaces for the specified device interface classes.
DIGCF_INTERFACEDEVICE := DIGCF_DEVICEINTERFACE ; obsolete, only for backwards compatibility
SPINT_ACTIVE := 0x00000001
SPINT_DEFAULT := 0x00000002
SPINT_REMOVED := 0x00000004
SPDRP_FRIENDLYNAME := 0x0000000C
SPDRP_DEVICEDESC := 0x00000000
SPDRP_CLASS := 0x00000007
SPDRP_MFG := 0x0000000B
SPDRP_ENUMERATOR_NAME := 0x00000016
SPDRP_SERVICE := 0x00000004
SPDRP_PHYSICAL_DEVICE_OBJECT_NAME := 0x0000000E
SPDRP_LOCATION_INFORMATION := 0x0000000D

VarSetCapacity(DevHdr, 32, 0) 
NumPut(32, DevHdr, 0, "UInt") ; sizeof(_DEV_BROADCAST_DEVICEINTERFACE)
NumPut(DBT_DEVTYP_DEVICEINTERFACE, DevHdr, 4, "UInt") ; DBT_DEVTYP_DEVICEINTERFACE
Addr := &DevHdr
Flags := DEVICE_NOTIFY_WINDOW_HANDLE|DEVICE_NOTIFY_ALL_INTERFACE_CLASSES
Msg = %Msg%RegisterDeviceNotification(%hWnd%, %Addr%, %Flags%)`r`n
Ret := DllCall("RegisterDeviceNotification", "UInt", hWnd, "UInt", Addr, "UInt", Flags)
if (!Ret)
{
    ErrMsg := FormatMessageFromSystem(A_LastError)
    Msg = %Msg% Ret %Ret% ErrorLevel %ErrorLevel% %A_LastError% %ErrMsg%
}
Msg .= "`r`n"
SetInfo(Msg)

MakeGuid(GUID_DEVINTERFACE_MOUSE, "{4D36E96F-E325-11CE-BFC1-08002BE10318}")

; List mouse device
;ListDevices(&GUID_DEVINTERFACE_MOUSE)

; List all devices 
ListDevices()

ListDevices(GUIDAddr = 0, OutputToLog = 0, FindDevicePath = "")
{
    global DIGCF_DEVICEINTERFACE, DIGCF_ALLCLASSES, SPDRP_FRIENDLYNAME, SPDRP_DEVICEDESC, SPDRP_MFG, SPDRP_CLASS, SPDRP_SERVICE, SPDRP_ENUMERATOR_NAME, SPDRP_PHYSICAL_DEVICE_OBJECT_NAME, SPDRP_LOCATION_INFORMATION
   
    hMod :=   DllCall("LoadLibrary", "str", "setupapi.dll")

    if (GUIDAddr == 0)
    {
        hDev := DllCall("setupapi\SetupDiGetClassDevs", "UInt", 0, "UInt", 0, "UInt", 0, "UInt", DIGCF_DEVICEINTERFACE|DIGCF_ALLCLASSES)
    }
    else
    {
        hDev := DllCall("setupapi\SetupDiGetClassDevs", "UInt", GuidAddr, "UInt", 0, "UInt", 0, "UInt", DIGCF_DEVICEINTERFACE)
    }
    
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
        if (Name <> "Unknown")
        {
            sRes .= "   Name: " . Name . "`r`n"
        }

        VarSetCapacity(DevName, 1024)
        Ret := DllCall("setupapi\SetupDiGetDeviceInstanceId", "UInt", hDev, "UInt", &DevInfoData, "Str", DevName, "UInt", 1024, "UInt", 0, "UInt")
        if (Ret <> 1)
        {
            ErrMsg := FormatMessageFromSystem(A_LastError)
            sRes = %sRes% Ret %Ret% ErrorLevel %ErrorLevel% %A_LastError% %ErrMsg%
        }
        sRes .= "   Device Instance Id: " . DevName . "`r`n"
      
        sRes .= "   SPDRP_FRIENDLYNAME: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_FRIENDLYNAME) . "`r`n"
        sRes .= "   SPDRP_DEVICEDESC: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_DEVICEDESC) . "`r`n"
        sRes .= "   SPDRP_MFG: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_MFG) . "`r`n"
        sRes .= "   SPDRP_CLASS: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_CLASS) . "`r`n"
        sRes .= "   SPDRP_SERVICE: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_SERVICE) . "`r`n"
        sRes .= "   SPDRP_ENUMERATOR_NAME: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_ENUMERATOR_NAME) . "`r`n"      
        sRes .= "   SPDRP_PHYSICAL_DEVICE_OBJECT_NAME: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_PHYSICAL_DEVICE_OBJECT_NAME) . "`r`n"      
        sRes .= "   SPDRP_LOCATION_INFORMATION: " . GetRegistryProperty(hDev, DevInfoData, SPDRP_LOCATION_INFORMATION) . "`r`n"
        sRes .= "`r`n"
    }

    DllCall("setupapi\SetupDiDestroyDeviceInfoList", "UInt", hDev)
    DllCall("FreeLibrary", "UInt", hMod)
    Msg .= sRes
   
    if (!OutputToLog)
    {
        AppendInfo(Msg)
    }
    else
    {
        AppendLog(Msg)
    }
}

SetInfo(Text)
{
    global InfoHwnd
    GuiControlGet, InfoOut
    NewText := InfoOut . Text
    GuiControl, , InfoOut, %NewText%
    Return
}

AppendInfo(Text)
{
    global InfoHwnd
    GuiControlGet, InfoOut
    NewText := InfoOut . Text
    GuiControl, , InfoOut, %NewText%
    ; WM_VSCROLL (0x115), SB_BOTTOM (7)
    ;MsgBox, %InfoHwnd%
    SendMessage, 0x115, 0x0000007, 0, , ahk_id %InfoHwnd%
    Return
}

SetLog(Text)
{
    global LogHwnd
    GuiControlGet, LogOut
    NewText := LogOut . Text
    GuiControl, , LogOut, %NewText%
    Return
}

AppendLog(Text)
{
    global LogHwnd
    GuiControlGet, LogOut
    NewText := LogOut . Text
    GuiControl, , LogOut, %NewText%
    ; WM_VSCROLL (0x115), SB_BOTTOM (7)
    ;MsgBox, %LogHwnd%
    SendMessage, 0x115, 0x0000007, 0, , ahk_id %LogHwnd%
    Return
}

GetRegistryProperty(hDev, ByRef DevInfoData, Prop)
{
    VarSetCapacity(NameType, 4, 0)
    VarSetCapacity(Name, 1024, 0)
    Ret:= DllCall("setupapi\SetupDiGetDeviceRegistryProperty", "UInt", hDev, "UInt", &DevInfoData, "UInt", Prop, "UInt", &NameType, "Str", Name, "UInt", 1024, "UInt", 0, "UInt")
    if (Ret <> 1)
    {
        ErrMsg := FormatMessageFromSystem(A_LastError)
        Res := "Not Found, Ret " Ret " ErrorLevel " ErrorLevel " " A_LastError " " ErrMsg
    }
    else
    {
        Res := Name
    }
    Return Res
}

Mem2Hex( pointer, len )
{
    A_FI := A_FormatInteger
    SetFormat, Integer, Hex
    Loop, %len%  {
        Hex := *Pointer+0
        StringReplace, Hex, Hex, 0x, 0x0
        StringRight Hex, Hex, 2          
        hexDump := hexDump . hex
        Pointer ++
    }
    SetFormat, Integer, %A_FI%
    StringUpper, hexDump, hexDump
    Return hexDump
}

;GUID_DEVINTERFACE_MONITOR = {E6F07B5F-EE97-4a90-B076-33F57BF4EAA7}
MakeGuid(ByRef Out, GUID)
{
   VarSetCapacity(Out, 16)
   Out := "                "
   PutGuid(&Out, GUID)
   ;Msg := "GUID " . GUID . " Dump " . HexDump(&Out, 16) 
   ;MsgBox %Msg%
   ; The return value is not reliable because a string would be trimmed 
   Return Out
}

PutGuid(ToAddr, GUID)
{
    ; Strip a start bracket 
    if (SubStr(GUID, 1, 1) = "{")
    {
        GUID := SubStr(GUID, 2, StrLen(GUID) - 1)
    }
    NumPut("0x" . SubStr(GUID, 1,  8), ToAddr+0, 0,  "UInt")   ; DWORD Data1
    NumPut("0x" . SubStr(GUID, 10, 4), ToAddr+0, 4,  "UShort") ; WORD  Data2
    NumPut("0x" . SubStr(GUID, 15, 4), ToAddr+0, 6,  "UShort") ; WORD  Data3
    NumPut("0x" . SubStr(GUID, 20, 2), ToAddr+0, 8,  "UChar")  ; BYTE  Data4[1]
    NumPut("0x" . SubStr(GUID, 22, 2), ToAddr+0, 9,  "UChar")  ; BYTE  Data4[2]
    NumPut("0x" . SubStr(GUID, 25, 2), ToAddr+0, 10, "UChar")  ; BYTE  Data4[3]
    NumPut("0x" . SubStr(GUID, 27, 2), ToAddr+0, 11, "UChar")  ; BYTE  Data4[4]
    NumPut("0x" . SubStr(GUID, 29, 2), ToAddr+0, 12, "UChar")  ; BYTE  Data4[5]
    NumPut("0x" . SubStr(GUID, 31, 2), ToAddr+0, 13, "UChar")  ; BYTE  Data4[6]
    NumPut("0x" . SubStr(GUID, 33, 2), ToAddr+0, 14, "UChar")  ; BYTE  Data4[7]
    NumPut("0x" . SubStr(GUID, 35, 2), ToAddr+0, 15, "UChar")  ; BYTE  Data4[8]
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

MsgMonitor(wParam, lParam, msg)
{
    global DBT_DEVICEARRIVAL, DBT_DEVICEREMOVECOMPLETE, DBT_DEVTYP_DEVICEINTERFACE
    AppendLog("WM_DEVICECHANGE Message " . msg . " arrived:`r`n")
    AppendLog("WPARAM: " . GetHex(wParam) . "`r`n")
    AppendLog("LPARAM: " . GetHex(lParam) . "`r`n")
    if ((wParam == DBT_DEVICEREMOVECOMPLETE) || (wParam == DBT_DEVICEARRIVAL))
    {
        ; lParam points to a DEV_BROADCAST_HDR structure
        dbch_size       := NumGet(lParam+0, 0, "UInt")
        dbch_devicetype := NumGet(lParam+0, 4, "UInt")
        AppendLog("   dbch_size = " . dbch_size . ", dbch_devicetype = " . GetHex(dbch_devicetype) . "`r`n")
        if (dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE)
        {
            ; lParam points to a DEV_BROADCAST_DEVICEINTERFACE structure
            dbcc_name := GetString(lParam+28)
            dbcc_classguid := GetGuid(lParam+12)
            AppendLog("   dbcc_classguid = " . dbcc_classguid . "`r`n")
            AppendLog("   dbcc_name = " . dbcc_name . "`r`n`r`n")
            ;AppendLog(HexDump(lParam+0, dbch_size))
            if (wParam == DBT_DEVICEREMOVECOMPLETE)
            {
                AppendLog("Hardware removal event, removing devices:`r`n`r`n")
            }
            else
            {
                AppendLog("Hardware arrival event, adding devices:`r`n`r`n")
            }
            ListDevices(lParam+12, 1, dbcc_name)
        }
    }
    AppendLog("`r`n`r`n")
   
}

HexDump( pointer, len )
{
    A_FI := A_FormatInteger
    SetFormat, Integer, Hex
    Start := 0
    Loop, %len%  {
        Count := ((Start + 16) <= Len) ? 16 : Len - Start        
        hexLine := ""
        stringLine := ""
        Loop, %Count% {
            Hex := *Pointer+0
            Char := Chr(Hex)
            StringReplace, Hex, Hex, 0x, 0x0
            StringRight Hex, Hex, 2          
            hexLine .= hex . " " 
            if (Asc(Char) >= 32 && Asc(Char) < 127)
            {
                stringLine .= Char
            }
            else
            {
                stringLine .= "."
            }
            Pointer ++        
        }
        Start += Count
        hexDump .= hexLine . stringLine . "`r`n"
        if (Start >= len)
        {
            break
        }
    }
    SetFormat, Integer, %A_FI%
    ;StringUpper, hexDump, hexDump
    Return hexDump
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

GetHex(Num)
{
    Old := A_FormatInteger 
    SetFormat, IntegerFast, Hex
    Num += 0 
    Num .= ""
    SetFormat, IntegerFast, %Old%
    Return Num
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