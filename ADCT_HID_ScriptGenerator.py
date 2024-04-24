from tkinter import *
from tkinter import filedialog
import generateConfig_copyData
import generateConfig_useMap
import generateConfig_add
import generateConfig_fieldremove
import warnings

warnings.filterwarnings('ignore')

root = Tk()
var = IntVar()
root.title("HID Script Generator V-2.0")


class templateFile():
    filename = ""

def browseFiles(titletext, myLabel, template):
    template.filename = filedialog.askopenfilename(title=titletext,
                                                   filetypes=(("HID Template files",
                                                               "*.xlsx"),
                                                              ("all files",
                                                               "*.*")))
    myLabel.configure(text=template.filename)
    var.set(1)

def saveFile(myLabel):
    myLabel.configure(text="")
    filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=(("HID Script file",
                                                               "*.csv"),
                                                              ("all files",
                                                               "*.*")))
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
        generateConfig_fieldremove.generate_script(deleteField.filename, outfile)
    outfile.close()
    print("Done...")

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