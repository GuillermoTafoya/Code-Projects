from Password_Locker import master
import GUI
import re
import os
import pyperclip

def makeNewPassword(length):

    generatedPassword = GUI.generateNewPassword(length)
    pyperclip.copy(generatedPassword)

    print(f'Generated password is: {generatedPassword}')
    print("Successfully copied to clipboard.")


def open(filename,MASTER):
    masterPassword = master(MASTER)
    passwords=GUI.loadData(filename)

    print(f'[{filename}] successfuly opened.')

    masterPassword.setNew(GUI.validateMasterPassword(masterPassword.value, passwords))

    stringSearcher = re.compile(r'"(\w|\s)+"')
    placeholder = GUI.generateNewPassword(30)
    while True:

                
        textinput = input(">")
        
        filename_with_spaces = stringSearcher.search(textinput)
        
        if filename_with_spaces:
            x = filename_with_spaces.group()
            textinput = textinput.replace(x,placeholder)
            cmd = textinput.split()
            cmd[cmd.index(placeholder)] = x[1:-1]
            placeholder = GUI.generateNewPassword(30)

        else:
            cmd = textinput.split()


        if cmd[0].lower() in {"dir", "ls", "list"} and len(cmd)==1:#Print stored accounts
            #print("Stored accounts:")
            for account in passwords.keys():
                print(f'\t» {account}')
        elif cmd[0].lower() == "get":#Get password
            if len(cmd)<2:
                print("Unrecognized sintax.\nIntended use is:\n» 'get account key1 key2'")
                continue
            try:
                if len(cmd)==2:
                    GUI.getPasswordFromAccounts(masterPassword.value,cmd[1],1,1,passwords)
                elif len(cmd)==3:
                    GUI.getPasswordFromAccounts(masterPassword.value,cmd[1],int(cmd[2]),1,passwords)
                elif len(cmd)==4:
                    GUI.getPasswordFromAccounts(masterPassword.value,cmd[1],int(cmd[2]),int(cmd[3]),passwords)
                else:
                    print("Unrecognized sintax.\nIntended use is:\n» 'get account key1 key2'")
            except:
                print("Exception occured.\nIntended use is:\n» 'get account int(key1) int(key2)'")

        elif cmd[0].lower()== "new": #NEW account
            try:
                if len(cmd) == 2:
                    GUI.addAccount(master = masterPassword.value,addAccount=cmd[1],key1=1,key2=1,pw=passwords,newPassword="Default",filename=filename)
                elif len(cmd) == 3:
                    GUI.addAccount(master = masterPassword.value,addAccount=cmd[1],key1=1,key2=1,pw=passwords,newPassword=cmd[2],filename=filename)
                elif len(cmd) == 4:
                    GUI.addAccount(master = masterPassword.value,addAccount=cmd[1],key1=int(cmd[3]),key2=1,pw=passwords,newPassword=cmd[2],filename=filename)
                elif len(cmd) == 5:
                    GUI.addAccount(master = masterPassword.value,addAccount=cmd[1],key1=int(cmd[3]),key2=int(cmd[4]),pw=passwords,newPassword=cmd[2],filename=filename)
                else:
                    print("Unrecognized sintax.\nIntended use is:\n» 'new account password key1 key2'")
            except:
                print("Exception occured.\nIntended use is\n» 'new account password int(key1) int(key2)'")
        elif cmd[0].lower() in {"del", "delete", "remove"}:
            if len(cmd)!=2:
                print("Unrecognized sintax.\nIntended use is:\n» 'delete account'")
            else:
                GUI.deleteAccount(cmd[1],passwords,filename)
        elif cmd[0] == "change":
            try:
                if len(cmd) == 3:
                    masterPassword.setNew(GUI.changePassword(masterPassword.value,changePasswordAccount=cmd[1],changePasswordKey1=1,changePasswordKey2=1,passwords=passwords,newPassword=cmd[2],filename=filename))
                elif len(cmd) == 4:
                    masterPassword.setNew(GUI.changePassword(masterPassword.value,changePasswordAccount=cmd[1],changePasswordKey1=int(cmd[3]),changePasswordKey2=1,passwords=passwords,newPassword=cmd[2],filename=filename))
                elif len(cmd) == 5:
                    masterPassword.setNew(GUI.changePassword(masterPassword.value,changePasswordAccount=cmd[1],changePasswordKey1=int(cmd[3]),changePasswordKey2=int(cmd[4]),passwords=passwords,newPassword=cmd[2],filename=filename))
                else:
                    print("Unrecognized sintax.\nIntended use is:\n» 'change account new_password key1 key2'")
            except:
                print("Exception occured.\nIntended use is\n» 'change account new_password int(key1) int(key2)'")

        elif cmd in (["clc"],["clear"],["cls"],["clean"]):
            os.system('cls' if os.name == 'nt' else 'clear')

        elif cmd[0].lower() == "pass":
            try:
                makeNewPassword(int(cmd[1]))
            except:
                print("Exception occured.\nIntended use is\n» 'pass int(length)'")

        elif cmd[0].lower() == "help":
            print(
                """
                {}
                    » Show stored accounts:     'dir'
                    » Get password:             'get account key1 key2'
                    » Add an account:           'new account password key1 key2'
                    » Delete an account:        'delete account'
                    » Change password:          'change account new_password key1 key2'
                    » New random password:      'pass length'
                    » Clean terminal:           'cls'
                    » Exit file:                'end'
                """.format(filename)

            )

        elif cmd in (["end"],["close"],["exit"]):
            #print(cmd)
            #input("Press ENTER to finish...")
            break
        else:
            print(f'Command [{" ".join(cmd)}] not recognized.')
