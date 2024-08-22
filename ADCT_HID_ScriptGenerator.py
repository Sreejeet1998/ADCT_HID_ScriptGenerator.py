import json
from tkinter import *
from tkinter import filedialog, messagebox
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

vrs = 2.1

def checkversionnumber():
    # Correct raw URL to access the file content directly
    url = "https://raw.githubusercontent.com/Sreejeet1998/ADCT_HID_ScriptGenerator.py/master/version"

    # Send a GET request to fetch the file content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        file_content = response.text
        if float(file_content)>float(vrs):
            messagebox.showinfo('App Info', 'Info: Update to newer version!')
        else:pass
    else:
        print(f"Failed to retrieve file: {response.status_code}")

# Call the function to check the version number
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
    # Load the last directory from the config file
    initial_dir = load_last_dir()

    # Open the file dialog with the initial directory set
    template.filename = filedialog.askopenfilename(
        title=titletext,
        initialdir=initial_dir,
        filetypes=(
            ("HID Template files", "*.xlsx"),
            ("all files", "*.*")
        )
    )

    if template.filename:  # If a file was selected
        # Update the last_dir in the config file
        save_last_dir(os.path.dirname(template.filename))
        # Update the label with the selected file's path
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

    if filename:  # If a file was selected
        # Update the last_dir in the config file
        save_last_dir(os.path.dirname(filename))
        # Update the label with the selected file's path
        myLabel.configure(text=filename)
        # Call the custom function with the selected filename
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