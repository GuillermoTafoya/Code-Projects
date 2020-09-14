import Traductor 
import csv
import time
import pyperclip


def loadData():
    with open('Passwords.csv', mode='r') as csv_file:
        dataFrame = csv.DictReader(csv_file)
        dictionary=dict()
        for row in dataFrame:
            pW=getList(row["Passwords"])
            dictionary.setdefault(row["Accounts"],pW)
        return dictionary

def getList(houdiny):
    s=houdiny
    newList=[]
    try:
        s=s[s.index('[')+1:s.index(']')]
    except:
        return s
    while True:
        try:
            x=int(s[0:s.index(',')])
        except:
            x=int(s[0:])
        newList.append(x)
        try:
            s=(s[s.index(',')+1:])
        except:
            break
    return newList

def validateMasterPassword(masterPassword, masterInput):
    while masterPassword != masterInput: 
        masterPassword=input()
    print("Valid password".center(50,"."))
    print("\nWelcome back, master.")

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

def getPasswordFromAccounts(account,key1,key2,passwords):
        key=key1*key2
        if account in passwords:
            if account=="MasterPassword" and key==0:
                pyperclip.copy(passwords[account])
                print("Password successfully copied to clipboard.")
            else:
                Traductor.copyDesciferedToClipboard(passwords[account],key)
                print("Password successfully copied to clipboard.")
        else:
            print("\nAccount not found.")        

def getNewCypheredPassword(changePasswordKey1, changePasswordKey2, newPassword):
    key=changePasswordKey1*changePasswordKey2
    setNew=newPassword
    Traductor.toCypher(setNew,key)

def addAccount(addAccount, key1, key2, pw, newPassword):
        account=addAccount
        if account not in pw.keys():
            getNewCypheredPassword(key1, key2, newPassword)
            x=pyperclip.paste()
            list=getList(x)
            key=key1*key2
            Traductor.copyDesciferedToClipboard(list, key)
            pw.setdefault(account,list)
            save(pw)
            print("\nAccount successfuly added.")
        else:
            print("\nThat account already exists.")


def save(passwords):
    with open('Passwords.csv', mode='w') as dataBase:
        writer = csv.writer(dataBase, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Accounts","Passwords"])
        for k,v in passwords.items():
            writer.writerow([k,v])

def deleteAccount(account,passwords):
    if account in passwords.keys() and account != "MasterPassword":
        del passwords[account]
        save(passwords)
        print("\nAccount successfully obliterated.\n")
    else:
        if account =="MasterPassword":
            print("You cannot delete the MasterPassword.")
        else:
            print("\nThere is not account named %s stored." %account)
            

def changePassword(changePasswordAccount, changePasswordKey1, changePasswordKey2, passwords, newPassword):
    account=changePasswordAccount
    if account in passwords.keys():
        if account == "MasterPassword":
            passwords["MasterPassword"] = newPassword
            save(passwords)
            print(f"The MasterPassword was successfully changed to {newPassword}.\n")
        else:

            getNewCypheredPassword(changePasswordKey1, changePasswordKey2, newPassword)
            x=pyperclip.paste()
            list=getList(x)
            key=changePasswordKey1*changePasswordKey2
            passwords[account]=list
            save(passwords)
            print("\nProcess successfully terminated.")
    else:
        print("\nThere is not account named %s stored." %account)






