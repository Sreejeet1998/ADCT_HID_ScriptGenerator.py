import json
import struct
from _ctypes import sizeof
from ftplib import FTP
from tkinter import *
from tkinter import filedialog, messagebox

import paramiko
from paramiko.sftp_client import SFTP
from paramiko.sftp_server import SFTPServer

import generateConfig_copyData
import generateConfig_useMap
import generateConfig_add
import generateConfig_deleteField
import warnings
import os
import requests
warnings.filterwarnings('ignore')

root = Tk()
var = IntVar()

import requests

vrs = 3.0

def checkversionnumber():
    # FTP server details
    sftp_server = "10.72.22.220"  # Replace with your SFTP server's IP address
    username = "sftpuser"  # Replace with your SFTP username
    password = "Ndi@2023"  # Replace with your SFTP password

    # Path to the version file on the SFTP server
    remote_path = "/data/ndl/upload/sftpuser/SreejeetShome/ADCT/HID_S_Generator/version_file.txt"  # Replace with the correct path and file name

    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        ssh.connect(hostname=sftp_server, username=username, password=password)

        # Open SFTP session
        sftp = ssh.open_sftp()

        # Retrieve the version file content
        with sftp.open(remote_path, 'r') as file:
            remote_version = file.read().strip()
            remote_version = remote_version.decode()

        # Compare the remote version with the local version
        if float(remote_version) > float(vrs):
            messagebox.showinfo('App Info', f'Info: Update to latest version - {remote_version}')
        else:
            pass  # No update needed

        # Close the SFTP and SSH connections
        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"Failed to retrieve file from SFTP: {e}")

checkversionnumber()

root.title("HID Script Generator_V2.0")


class templateFile():
    filename = ""

CONFIG_FILE_1 = 'config.json'
CONFIG_FILE_2 = 'config.json'


def load_last_dir():
    """Load the last directory from the config file."""
    if os.path.exists(CONFIG_FILE_1):
        with open(CONFIG_FILE_1, 'r') as f:
            data = json.load(f)
            return data.get('last_dir', os.getcwd())
    return os.getcwd()


def save_last_dir(directory):
    """Save the last directory to the config file."""
    with open(CONFIG_FILE_1, 'w') as f:
        json.dump({'last_dir': directory}, f)


def browseFiles(titletext, myLabel, template):
    initial_dir = load_last_dir()

    template.filename = filedialog.askopenfilename(
        title=titletext,
        initialdir=initial_dir,
        filetypes=(
            ("HID Template files", "*.xlsx"),
            ("all files", "*.*")
        )
    )

    if template.filename:
        save_last_dir(os.path.dirname(template.filename))
        myLabel.configure(text=template.filename)


def load_last_dir():
    """Load the last directory from the config file."""
    if os.path.exists(CONFIG_FILE_2):
        with open(CONFIG_FILE_2, 'r') as f:
            data = json.load(f)
            return data.get('last_dir', os.getcwd())
    return os.getcwd()


def save_last_dir(directory):
    """Save the last directory to the config file."""
    with open(CONFIG_FILE_2, 'w') as f:
        json.dump({'last_dir': directory}, f)


def saveFile(myLabel):
    # Load the last directory from the config file
    initial_dir = load_last_dir()

    # Open the save file dialog with the initial directory set
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialdir=initial_dir,
        filetypes=(
            ("HID Script file", "*.csv"),
            ("all files", "*.*")
        )
    )

    if filename:
        save_last_dir(os.path.dirname(filename))
        myLabel.configure(text=filename)
        myClick(filename)


def myClick(outfilePath):
    outfile = open(outfilePath, 'w', encoding='utf-8')

    if copyData.filename:
        generateConfig_copyData.generate_script(copyData.filename, outfile)

    if useMap.filename:
        generateConfig_useMap.generate_script(useMap.filename, outfile)

    if add.filename:
        generateConfig_add.generate_script(add.filename, outfile)

    if deleteField.filename:
        generateConfig_deleteField.generate_script(deleteField.filename, outfile)
    outfile.close()

root.tkraise()
# Layout for HID copyData template
copyData = templateFile()
myLabel1 = Label(root, padx=50)
myLabel1.grid(row=0, column=0)
button1text = "Select HID copyData Template"
myButton1 = Button(root, text=button1text, command=lambda : browseFiles(button1text, myLabel1, copyData))
myButton1.grid(row=0, column=1)

# Layout for HID useMap template
useMap = templateFile()
myLabel2 = Label(root, padx=50)
myLabel2.grid(row=1, column=0)
button2text = "Select HID useMap Template"
myButton2 = Button(root, text=button2text, command=lambda: browseFiles(button2text, myLabel2, useMap))
myButton2.grid(row=1, column=1)

# Layout for HID add template
add = templateFile()
myLabel3 = Label(root, padx=50)
myLabel3.grid(row=2, column=0)
button3text = "Select HID add Template"
myButton3 = Button(root, text=button3text, command=lambda: browseFiles(button3text, myLabel3, add))
myButton3.grid(row=2, column=1)

# Layout for HID deleteField template
deleteField = templateFile()
myLabel4 = Label(root, padx=50)
myLabel4.grid(row=3, column=0)
button4text = "Select HID deleteField Template"
myButton4 = Button(root, text=button4text, command=lambda: browseFiles(button4text, myLabel4, deleteField))
myButton4.grid(row=3, column=1)

# Layout for Generate Script
myLabel5 = Label(root, padx=50)
myLabel5.grid(row=4, column=0)
myButton5 = Button(root, text="Generate Script...", command=lambda : saveFile(myLabel5))
myButton5.grid(row=4, column=1)

root.mainloop()