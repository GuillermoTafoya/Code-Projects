import GUI
from tkinter import *
from tkinter import ttk 
from tkinter import scrolledtext 
from PIL import ImageTk,Image  
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import sys
import winsound

def resource_path(relative_path):
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path,relative_path)

passwords=GUI.loadData()

masterInput=passwords["MasterPassword"]
masterPassword=input()
GUI.validateMasterPassword(masterPassword, masterInput)

songs={
    0:0,
    1:229,
    2:540,
    3:706,
    4:924,
    5:1200,
    6:1510
    }

nowToPlay=random.randrange(0,7)



root = Tk()
root.title("Unlocked")
root.geometry("600x400")
root.minsize(600,400)
root.maxsize(600,400)
root.iconbitmap('unlocked.ico')


ZeldaJazz=resource_path("Zelda Jazz.mp3")


try:
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(ZeldaJazz)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_pos(songs[nowToPlay])
except:
    try:
        winsound.PlaySound("Zelda Jazz" , winsound.SND_ASYNC)
    except:
        print("The jazz band couldn't make it")


#Handy functions

def swap(frame):
    frame.tkraise()
    searchBar.tkraise()

def combineFuncs(*funcs):
    def combinedFunc(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combinedFunc

def clearSearch(event, defaultText):
    if event.widget.get() == defaultText:
        event.widget.delete(0, "end")

#Define frames

searchBar = Frame(root)
titleScreen = Frame(root, width=600, height=400)
getPasswordScreen = Frame(root, width=400, height=300)
addAccountScreen = Frame(root, width=400, height=300)
deleteAccountScreen = Frame(root, width=400, height=300)
changePassword = Frame(root, width=400, height=300)
displayAccounts = Frame(root, width=400, height=300)

for frame in (getPasswordScreen, addAccountScreen, deleteAccountScreen, changePassword, displayAccounts):
    frame.place(relx = 0, rely = 0, relheight = 0.99, relwidth = 0.99)

titleScreen.place(relx = 0, rely = 0, relheight = 0.99, relwidth = 0.99)
searchBar.place(relx = 0, rely = 0, relheight = 0.1, relwidth = 1)

barWelcome = ImageTk.PhotoImage(Image.open("BarWelcome.jpg").resize((600, 400), Image.ANTIALIAS))
barBackground = ImageTk.PhotoImage(Image.open("BarBackground.jpg").resize((600, 400), Image.ANTIALIAS))

Welcome = Label(titleScreen, image=barWelcome)
Welcome.image = barWelcome
Welcome.place(x=0, y=0)

#titleScreen: It's an anime bar?

def setTitleScreenDefaultText(actualMasterInfo):
    message=f"The current MasterPassword is \n\"{passwords['MasterPassword']}\""
    actualMasterInfo.set(message)

message=f"The current MasterPassword is \n\"{passwords['MasterPassword']}\""
actualMasterInfo= StringVar()

greetings = Label(titleScreen, text="Welcome back".center(2,"."))
currentMP = Label(titleScreen, textvariable = actualMasterInfo, fg="white", bg="#0c0c0b")
currentMP.place(relx = (0.99-(len(message)*0.01)) , rely = 0.9, relheight = 0.1, relwidth = ((len(message)*0.01)))
greetings.place(relx = 0.432 , rely = 0.245, relheight = 0.07, relwidth = 0.15)

#getPasswordScreen

getPSBG = Label(getPasswordScreen, image=barBackground)
getPSBG.image = barBackground
getPSBG.place(x=0, y=0)

def setGetPasswordsScreenDefaultText(quickPassAccessDT,quickKey1AccessDT,quickKey2AccessDT):
    quickPassAccess.delete(0,END)
    quickKey1Access.delete(0,END)
    quickKey2Access.delete(0,END)
    quickPassAccess.insert(0, quickPassAccessDT)
    quickKey1Access.insert(0, quickKey1AccessDT)
    quickKey2Access.insert(0, quickKey2AccessDT)

def getPassword():

    try:
        GUI.getPasswordFromAccounts(str(quickPassAccess.get()),int(quickKey1Access.get()),int(quickKey2Access.get()),passwords)
    except:
        print("\nEntered keys and/or password are not valid.") 

quickPassAccessDT = "Account name"
quickKey1AccessDT = "Key 1"
quickKey2AccessDT = "Key 2"

quickPassAccess = Entry(getPasswordScreen)
quickKey1Access = Entry(getPasswordScreen)
quickKey2Access = Entry(getPasswordScreen)

centered=0.35
Button(getPasswordScreen, text = "Search password" , command = lambda: getPassword()).place(relx = centered , rely = 0.6, relheight = 0.07, relwidth = 0.3)


quickPassAccess.place(relx = centered , rely = 0.2, relheight = 0.07, relwidth = 0.3)
quickKey1Access.place(relx = centered , rely = 0.3, relheight = 0.07, relwidth = 0.3)
quickKey2Access.place(relx = centered , rely = 0.4, relheight = 0.07, relwidth = 0.3)

quickPassAccess.bind("<Button-1>", lambda do: clearSearch(do,quickPassAccessDT))
quickKey1Access.bind("<Button-1>", lambda do: clearSearch(do,quickKey1AccessDT))
quickKey2Access.bind("<Button-1>", lambda do: clearSearch(do,quickKey2AccessDT))

#changePassword

getCPSBG = Label(changePassword, image=barBackground)
getCPSBG.image = barBackground
getCPSBG.place(x=0, y=0)

def setChangePasswordScreenDefaultText(quickPassAccessDT,quickKey1AccessDT,quickKey2AccessDT, newPasswordDT):
    changePasswordAccount.delete(0,END)
    changePasswordKey1.delete(0,END)
    changePasswordKey2.delete(0,END)
    newPassword.delete(0,END)

    changePasswordAccount.insert(0, quickPassAccessDT)
    changePasswordKey1.insert(0, quickKey1AccessDT)
    changePasswordKey2.insert(0, quickKey2AccessDT)
    newPassword.insert(0, newPasswordDT)

def changePasswordMethod():

    try:
        GUI.changePassword(str(changePasswordAccount.get()),int(changePasswordKey1.get()),int(changePasswordKey2.get()),passwords,str(newPassword.get()))
    except:
        print("\nEntered keys and/or password are not valid.") 

newPasswordDT= "New Password"

changePasswordAccount = Entry(changePassword)
changePasswordKey1 = Entry(changePassword)
changePasswordKey2 = Entry(changePassword)
newPassword = Entry(changePassword)

centered=0.35
Button(changePassword, text = "Change password" , command = lambda: changePasswordMethod()).place(relx = centered , rely = 0.7, relheight = 0.07, relwidth = 0.3)


changePasswordAccount.place(relx = centered , rely = 0.2, relheight = 0.07, relwidth = 0.3)
changePasswordKey1.place(relx = centered , rely = 0.3, relheight = 0.07, relwidth = 0.3)
changePasswordKey2.place(relx = centered , rely = 0.4, relheight = 0.07, relwidth = 0.3)
newPassword.place(relx = centered , rely = 0.5, relheight = 0.07, relwidth = 0.3)

changePasswordAccount.bind("<Button-1>", lambda do: clearSearch(do,quickPassAccessDT))
changePasswordKey1.bind("<Button-1>", lambda do: clearSearch(do,quickKey1AccessDT))
changePasswordKey2.bind("<Button-1>", lambda do: clearSearch(do,quickKey2AccessDT))
newPassword.bind("<Button-1>", lambda do: clearSearch(do,newPasswordDT))

#addAccountScreen

getAASBG = Label(addAccountScreen, image=barBackground)
getAASBG.image = barBackground
getAASBG.place(x=0, y=0)

def setaddAccountScreenDefaultText(quickPassAccessDT,quickKey1AccessDT,quickKey2AccessDT, newPasswordDT):
    addAccountAccount.delete(0,END)
    addAccountKey1.delete(0,END)
    addAccountKey2.delete(0,END)
    addAccountNewPassword.delete(0,END)

    addAccountAccount.insert(0, quickPassAccessDT)
    addAccountKey1.insert(0, quickKey1AccessDT)
    addAccountKey2.insert(0, quickKey2AccessDT)
    addAccountNewPassword.insert(0, newPasswordDT)

def addPasswordMethod():
    try:
        GUI.addAccount(str(addAccountAccount.get()),int(addAccountKey1.get()),int(addAccountKey2.get()),passwords,str(addAccountNewPassword.get()))
    except:
        print("\nEntered keys and/or password are not valid.") 

addAccountAccount = Entry(addAccountScreen)
addAccountKey1 = Entry(addAccountScreen)
addAccountKey2 = Entry(addAccountScreen)
addAccountNewPassword = Entry(addAccountScreen)

centered=0.35
Button(addAccountScreen, text = "Add account" , command = lambda: addPasswordMethod()).place(relx = centered , rely = 0.7, relheight = 0.07, relwidth = 0.3)

addAccountAccount.place(relx = centered , rely = 0.2, relheight = 0.07, relwidth = 0.3)
addAccountKey1.place(relx = centered , rely = 0.3, relheight = 0.07, relwidth = 0.3)
addAccountKey2.place(relx = centered , rely = 0.4, relheight = 0.07, relwidth = 0.3)
addAccountNewPassword.place(relx = centered , rely = 0.5, relheight = 0.07, relwidth = 0.3)

addAccountAccount.bind("<Button-1>", lambda do: clearSearch(do,quickPassAccessDT))
addAccountKey1.bind("<Button-1>", lambda do: clearSearch(do,quickKey1AccessDT))
addAccountKey2.bind("<Button-1>", lambda do: clearSearch(do,quickKey2AccessDT))
addAccountNewPassword.bind("<Button-1>", lambda do: clearSearch(do,newPasswordDT))

#deleteAccountScreen

getDASBG = Label(deleteAccountScreen, image=barBackground)
getDASBG.image = barBackground
getDASBG.place(x=0, y=0)

def setDeleteAccountScreenDefaultText():
    deleteA.delete(0,END)
    deleteA.insert(0, deleteADT)

def deleteAccountMethod():
    try:
        GUI.deleteAccount(str(deleteA.get()),passwords)
    except:
        print("\nSomething went wrong.\nProcess not terminated..") 

deleteADT = "Account name"

deleteA = Entry(deleteAccountScreen)

Button(deleteAccountScreen, text = "Delete account" , command = lambda: deleteAccountMethod()).place(relx = centered , rely = 0.4, relheight = 0.07, relwidth = 0.3)


deleteA.place(relx = centered , rely = 0.2, relheight = 0.07, relwidth = 0.3)

deleteA.bind("<Button-1>", lambda do: clearSearch(do,deleteADT))


#displayAccounts

getDASSBG = Label(displayAccounts, image=barBackground)
getDASSBG.image = barBackground
getDASSBG.place(x=0, y=0)

def displayAccountText():
    accountsDisplayed.configure(state ='normal')
    accountsDisplayed.delete('1.0',END)
    accountsDisplayed.insert(INSERT, "Existing accounts:\n")
    for i in passwords.keys():
        accountsDisplayed.insert(INSERT, f"»{i}\n")
    accountsDisplayed.configure(state ='disabled')
    
accountsDisplayed = scrolledtext.ScrolledText(displayAccounts,  
                                      width = 40,  
                                      height = 10) 

accountsDisplayed.place(relx = 0.3 , rely = 0.2, relheight = 0.6, relwidth = 0.4)


#Search Bar                         

Button(searchBar, text = "Title Screen" , command = lambda: combineFuncs(swap(titleScreen),setTitleScreenDefaultText(actualMasterInfo))).grid(row=0, column=0)
Button(searchBar, text = "Get Password" , command = lambda: combineFuncs(swap(getPasswordScreen),setGetPasswordsScreenDefaultText(quickPassAccessDT,quickKey1AccessDT,quickKey2AccessDT))).grid(row=0, column=1)
Button(searchBar, text = "Change Password" , command = lambda: combineFuncs(swap(changePassword),setChangePasswordScreenDefaultText(quickPassAccessDT,quickKey1AccessDT,quickKey2AccessDT, newPasswordDT))).grid(row=0, column=2)
Button(searchBar, text = "Add Account" , command = lambda: combineFuncs(swap(addAccountScreen),setaddAccountScreenDefaultText(quickPassAccessDT,quickKey1AccessDT,quickKey2AccessDT, newPasswordDT))).grid(row=0, column=3)
Button(searchBar, text = "Delete Account" , command = lambda: combineFuncs(swap(deleteAccountScreen),setDeleteAccountScreenDefaultText())).grid(row=0, column=4)
Button(searchBar, text = "Display Accounts" , command = lambda: combineFuncs(swap(displayAccounts),displayAccountText())).grid(row=0, column=5)



setTitleScreenDefaultText(actualMasterInfo)

root.wm_attributes('-transparentcolor', 'grey')
titleScreen.tkraise()
searchBar.tkraise()
root.mainloop()
    