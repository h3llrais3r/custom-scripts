# Custom script to check for your current ip.
# It checks for your current ip and stores it in a file.
# It compares your current ip with your previous ip from the file.
# If the ip is different, it shows a popup to indicate it.


import os
import re
import urllib2
import Tkinter
import tkMessageBox


LOG_FILE = "checkIP.log"
URL = "http://checkip.dyndns.org/index.html"
REGEX = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


def run():
    previous_ip = _read_previous_ip()
    print "previous ip: " + previous_ip
    current_ip = _check_current_ip()
    print "current ip: " + current_ip
    if current_ip != previous_ip:
        _write_current_ip(current_ip)
        _show_popup(previous_ip, current_ip)


def _check_current_ip():
    ip = ""
    try:
        response = urllib2.urlopen(URL)
        content = response.read()
        response.close()
        result = REGEX.search(content)
        if result:
            ip = result.group()
    except:
        print "Could not check current ip!"
    return ip


def _read_previous_ip():
    ip = ""
    filename = LOG_FILE
    try:
        if os.path.exists(filename):
            file = open(filename, "r")
            ip = file.readline()
            file.close()
    except:
        print "Could not read previous ip!"
    return ip


def _write_current_ip(ip):
    filename = LOG_FILE
    file = open(filename, "w")
    file.write(ip)
    file.close()


def _show_popup(previous, current):
    window = Tkinter.Tk()
    window.wm_withdraw()
    message = "IP changed from '" + previous + "' to '" + current + "'"
    message += "\n"
    message += "Update the Hurricane Tunnel Broker configuration for IPV6 usage."
    message += "\n"
    message += "Location: 'http://tunnelbroker.net'"
    message += "\n"
    message += "Field to change: client IPV4 address to '" + current + "'"
    tkMessageBox.showinfo("IP Change", message)


# Run the script
run()