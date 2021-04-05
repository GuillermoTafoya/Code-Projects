import Traductor 
import csv
import time
import pyperclip
from Traductor import random
import pickle

def loadData(filename):

    openedfile = open(filename, "rb")
    dictionary = pickle.load(openedfile)
    openedfile.close()
    return dictionary



def validateMasterPassword(masterPassword, passwords):
    cifer = passwords["MasterPassword"]

    while not Traductor.validateMaster(masterPassword, cifer[0], cifer[1], 1): 
        print("Access denied. Enter correct password. ")
        masterPassword=input(">>")

    print("Valid password".center(50,"."))
    print("\nWelcome back, master.")
    return masterPassword

def getKey():
    try:
        firstNum=int(input("Insert your first key: ")) 
    except:
        firstNum=10000
    try:
        secondNum=int(input("Insert your second key: ")) 
    except:
        secondNum=10000
    key=firstNum * secondNum 
    return key

def getPasswordFromAccounts(master, account,key1,key2,passwords):
        key=key1*key2
        master = master
        if account in passwords:
            cifer = passwords[account]

            if account=="MasterPassword":
                
                #Traductor.copyDesciferedToClipboard(master, cifer[0], cifer[1],key)
                pyperclip.copy(str(master))
                print("MasterPassword [{}] successfully copied to clipboard.".format(master))
                
            else:
                Traductor.copyDesciferedToClipboard(master, cifer[0], cifer[1],key)
                s = pyperclip.paste()
                print("Password [{}] from [{}] successfully copied to clipboard.".format(s, account))
        else:
            print("Account not found.")        

def getNewCypheredPassword(master, changePasswordKey1, changePasswordKey2, newPassword):
    key=changePasswordKey1*changePasswordKey2
    return Traductor.toCypher(master, newPassword, key)

def addAccount(master, addAccount, key1, key2, pw, newPassword,filename):
        account=addAccount
        if account not in pw.keys():
            
            PWlist, iv =getNewCypheredPassword(master, key1, key2, newPassword)
            pw.setdefault(account,[PWlist,iv])
            save(filename, pw)
            print(f'[{addAccount}] was successfuly added with password [{newPassword}] and keys [{key1}] and [{key2}]')
        else:
            print("That account already exists.")


def save(filename, passwords):
    filesave = open(filename, 'wb')
    pickle.dump(passwords,filesave) 

def deleteAccount(account,passwords,filename):
    if account in passwords.keys() and account != "MasterPassword":
        del passwords[account]
        save(filename,passwords)
        print("Account successfully obliterated.")
    else:
        if account =="MasterPassword":
            print("You cannot delete the MasterPassword.")
        else:
            print("There is not account named [%s] stored." %account)
            

def changePassword(MASTER, changePasswordAccount, changePasswordKey1, changePasswordKey2, passwords, newPassword,filename):
    account=changePasswordAccount
    if account in passwords.keys():
        key = 1
        if account == "MasterPassword":
            print("All keys for stored accounts will be needed.")
            cmd = input("If any key is wrong or an error occurs, the password will be lost. Continue? Y/N ")
            if cmd != "Y":
                return
            #print("DONT close the window")
            previousMaster = MASTER
            PW, IV = Traductor.toCypher(newPassword,"00000000000000000000",key)
            passwords["MasterPassword"] = [PW,IV]
            for newACCOUNT, newCIFER in passwords.items():
                
                if newACCOUNT != "MasterPassword":
                    PasswordKey1 = int(input("Key1 for [{}]: ".format(newACCOUNT)))
                    PasswordKey2 = int(input("Key2 for [{}]: ".format(newACCOUNT)))
                    passFromAccount = Traductor.fromCypher(PasswordKey1*PasswordKey2,newCIFER[0],Traductor.makeKey(previousMaster,newCIFER[1]),newCIFER[1])
                    PW, IV = getNewCypheredPassword(newPassword, PasswordKey1, PasswordKey2, passFromAccount)
                    passwords[newACCOUNT]=[PW,IV]
                    print("Account [{}] Successfully Recifered.".format(newACCOUNT))
                    print("Password registered as [{}] with keys [{}] and [{}]".format(passFromAccount,PasswordKey1,PasswordKey2))
            
            print(f"The MasterPassword was successfully changed to [{newPassword}].\n")
            MASTER = newPassword
            save(filename,passwords)

        else:

            PW, IV = getNewCypheredPassword(MASTER, changePasswordKey1, changePasswordKey2, newPassword)

            passwords[account]=[PW,IV]
            save(filename,passwords)
            print("\nProcess successfully terminated.\nNew password for [{}] is [{}]".format(account, newPassword))
            print("Keys registered as [{}] and [{}]".format(changePasswordKey1,changePasswordKey2))
    else:
        print("\nThere is not account named [%s] stored." %account)
    return MASTER


def generateNewPassword(length):
    newPass = []
    for i in range(length):
        newPass.append(chr(random.randrange(33, 126)))
    generatedPassword = "".join(newPass)
    return generatedPassword



