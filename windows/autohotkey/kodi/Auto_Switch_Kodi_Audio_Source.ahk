; This script detects the headset and handles kodi audio settings accordingly
; By default the 5.1 receiver is enabled
; When the headset is connected, it switches to the settings for the headset
; When the headset is disconnected, it switches back to the settings for the receiver
; REMARK: I assume that the headset becomes the default audio devices in windows when it connects; if not, we'll also need to add a switch of audio device in the kodi settings (not included in this script)
; To hunt down the GUID, use Detect_Hardware_Changes.ahk
; ALTERNATIVE: You could also check with a tool like regshot (https://sourceforge.net/projects/regshot/) the registry changes when the headset connects (keys added) or disconnects (keys removed)
; When you know the keys that are added/removed you could also easily check these keys with autohotkey and do the switch based on that (see https://autohotkey.com/board/topic/70836-any-way-to-detect-bluetooth-device-status/)

; GUID of device from which you want to detect the hardware changes
; You need to get the GUID from the instance id value to get the unique device id
DEVICE_INSTANCE_ID := "{4C319AE9-878C-464C-A243-D3D41119EECF}" ; bluetooth headset Philips SHB7000

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
    MsgBox, Unable to RegisterDeviceNotification!
    ExitApp
}
Return

MsgMonitor(wParam, lParam, msg)
{
    global DEVICE_INSTANCE_ID, DBT_DEVTYP_DEVICEINTERFACE, DBT_DEVICEARRIVAL, DBT_DEVICEREMOVECOMPLETE
    
    if (wParam == DBT_DEVICEARRIVAL)
    {
        ; lParam points to a DEV_BROADCAST_HDR structure
        dbch_size := NumGet(lParam+0, 0, "UInt")
        dbch_devicetype := NumGet(lParam+0, 4, "UInt")
        if (dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE)
        {
            ; lParam points to a DEV_BROADCAST_DEVICEINTERFACE structure
            dbcc_name := GetString(lParam+28)
            dbcc_classguid := GetGuid(lParam+12)
            devices := ListDevices(lParam+12, dbcc_name) ; list devices impacted by hardware change
            for index, device in devices
            {
                if (InStr(device.instanceId, DEVICE_INSTANCE_ID)) ; check if our device is in the list of devices
                {
                    if (device.physicalDeviceObjectName) ; check if physicalDeviceObjectName is available (available means physically connected or enabled)
                    {
                        ;MsgBox, Device %DEVICE_INSTANCE_ID% physically connected (or enabled)
                        ; Load headset settings
                        Run load_headset_settings.py
                    }
                }
            }
        }
    } 
    else if (wParam == DBT_DEVICEREMOVECOMPLETE)
    {
        ; lParam points to a DEV_BROADCAST_HDR structure
        dbch_size := NumGet(lParam+0, 0, "UInt")
        dbch_devicetype := NumGet(lParam+0, 4, "UInt")
        if (dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE)
        {
            ; lParam points to a DEV_BROADCAST_DEVICEINTERFACE structure
            dbcc_name := GetString(lParam+28)
            dbcc_classguid := GetGuid(lParam+12)
            devices := ListDevices(lParam+12, dbcc_name) ; list devices impacted by hardware change
            for index, device in devices
            {
                if (InStr(device.instanceId, DEVICE_INSTANCE_ID)) ; check if our device is in the list of devices
                {
                    if (!device.physicalDeviceObjectName) ; check if physicalDeviceObjectName is blank (blank means physically disconnected or disabled)
                    {
                        ;MsgBox, Device %DEVICE_INSTANCE_ID% physically disconnected (or disabled)
                        ; Load receiver settings
                        Run load_receiver_settings.py
                    }
                }
            }
        }
    }  
}

ListDevices(GUIDAddr = 0, FindDevicePath = "")
{
    global DIGCF_DEVICEINTERFACE, DIGCF_ALLCLASSES, SPDRP_FRIENDLYNAME, SPDRP_DEVICEDESC, SPDRP_MFG, SPDRP_CLASS, SPDRP_SERVICE, SPDRP_ENUMERATOR_NAME, SPDRP_PHYSICAL_DEVICE_OBJECT_NAME, SPDRP_LOCATION_INFORMATION
   
    hMod := DllCall("LoadLibrary", "str", "setupapi.dll")
    hDev := DllCall("setupapi\SetupDiGetClassDevs", "UInt", GuidAddr, "UInt", 0, "UInt", 0, "UInt", DIGCF_DEVICEINTERFACE)
    
    Res := []
    Loop
    {
        sRes :=
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
        
        Device := {}
        Device.index := A_Index
        Device.classGuid := GetGuid(&DevInfoData+4)
        Device.id := NumGet(DevInfoData, 20, "UInt")
        Device.name := Name
        Device.instanceId := DevName
        Device.friendlyName := GetRegistryProperty(hDev, DevInfoData, SPDRP_FRIENDLYNAME)
        Device.deviceDescription := GetRegistryProperty(hDev, DevInfoData, SPDRP_DEVICEDESC)
        Device.mfg := GetRegistryProperty(hDev, DevInfoData, SPDRP_MFG)
        Device.class := GetRegistryProperty(hDev, DevInfoData, SPDRP_CLASS)
        Device.service := GetRegistryProperty(hDev, DevInfoData, SPDRP_SERVICE)
        Device.enumeratorName := GetRegistryProperty(hDev, DevInfoData, SPDRP_ENUMERATOR_NAME)
        Device.physicalDeviceObjectName := GetRegistryProperty(hDev, DevInfoData, SPDRP_PHYSICAL_DEVICE_OBJECT_NAME)
        Device.locationInformation := GetRegistryProperty(hDev, DevInfoData, SPDRP_LOCATION_INFORMATION)
        Device.string := sRes
        
        Res.Push(Device)
    }

    DllCall("setupapi\SetupDiDestroyDeviceInfoList", "UInt", hDev)
    DllCall("FreeLibrary", "UInt", hMod)
    
    Return Res
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

GetRegistryProperty(hDev, ByRef DevInfoData, Prop)
{
    VarSetCapacity(NameType, 4, 0)
    VarSetCapacity(Name, 1024, 0)
    Ret:= DllCall("setupapi\SetupDiGetDeviceRegistryProperty", "UInt", hDev, "UInt", &DevInfoData, "UInt", Prop, "UInt", &NameType, "Str", Name, "UInt", 1024, "UInt", 0, "UInt")
    if (Ret <> 1)
    {
        ErrMsg := FormatMessageFromSystem(A_LastError)
        ;Res := "Not Found, Ret " Ret " ErrorLevel " ErrorLevel " " A_LastError " " ErrMsg
        Res :=
    }
    else
    {
        Res := Name
    }
    Return Res
}