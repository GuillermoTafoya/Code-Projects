import Password_Locker
import Traductor 
from GUI import save, generateNewPassword
import os
import pickle
import re
import cl

def new(filename="Passwords", masterPassword="Default", mode="GUI"):
    try:
        passwords = dict()
        PW, IV = Traductor.toCypher(masterPassword,"00000000000000000000",1)
        passwords.setdefault("MasterPassword", [PW,IV])
        save(filename,passwords)

        print("Created new file [{}] with Key [{}] and MasterPassword [{}]".format(filename,1,masterPassword))
        if mode=="GUI":
            openGUI(filename, masterPassword)
    except:
        print("An exception occured.")
        print("Intended use is:\n» 'new filename masterPassword key1 key2'")

def openGUI(filename, masterPassword="Default"):
    try:
        Password_Locker.runGUI(filename, masterPassword)
    except:
        print("An exception occured on 'openGUI'")

def validatefile(filename):

    try:
        openedfile = open(filename, "rb")
        dictionary = pickle.load(openedfile)
        openedfile.close()
        dictionary["MasterPassword"]
        #print(filename,"valid")
        return True
    except:
        #print(filename,"not valid")
        return False

def openCL(filename, password="Default"):
    cl.open(filename,password)


def start():
    try:
        path=sys._MEIPASS
    except Exception:
        path=os.path.abspath(".")

    stringSearcher = re.compile(r'"(\w|\s)+"')
    placeholder = generateNewPassword(30)
    while True:
        
        textinput = input("#")
        
        filename_with_spaces = stringSearcher.search(textinput)
        
        if filename_with_spaces:
            filename = filename_with_spaces.group()
            textinput = textinput.replace(filename,placeholder)
            cmd = textinput.split()
            cmd[cmd.index(placeholder)] = filename[1:-1]
            placeholder = generateNewPassword(30)

        else:
            cmd = textinput.split()


        
        if cmd[0].lower() in {"dir", "ls", "list"} and len(cmd)==1:
            for filename in os.listdir(path):
                if validatefile(filename):
                    print(f'-{filename}')
        elif cmd[0].lower() in {"del", "delete", "remove"}:
            if len(cmd)!=2:
                print("Unrecognized sintax.\nIntended use is:\n» 'delete filename'")
            elif os.path.exists(cmd[1]):
                if validatefile(cmd[1]):
                    os.remove(cmd[1])
                else:
                    print("Not a valid file to remove.")
            else:
                print("The file does not exist")
        elif cmd[0].lower()== "gui" and len(cmd)>1: #GUI calls
            if cmd[1] == "open":
                if len(cmd)<3:
                    print("Unrecognized sintax.\nIntended use is:\n» 'gui open filename password'")
                    continue
                if not validatefile(cmd[2]):
                    print("Not a valid file")
                    continue

                if len(cmd)==3:
                    openGUI(cmd[2])

                elif len(cmd)==4:
                    openGUI(cmd[2],cmd[3])
                    
                else:
                    print("Unrecognized sintax.\nIntended use is:\n» 'GUI open filename password'")
            elif cmd[1]== "new": #create new and open its gui
                if len(cmd)>2 and cmd[2] in os.listdir(path):
                    print("FILENAME [{}] already exists.".format(cmd[2]))
                    continue
                if len(cmd) == 3:
                    new(filename=cmd[2], masterPassword="Default", mode="GUI")
                    
                elif len(cmd) == 4:
                    new(filename=cmd[2], masterPassword=cmd[3], mode="GUI")

                else:
                    print("Unrecognized sintax.\nIntended use is:\n» 'GUI new filename masterPassword'")
        elif cmd[0].lower()== "new": #NEW file using CL
            if len(cmd)>1 and cmd[1] in os.listdir(path):
                print("FILENAME [{}] already exists.".format(cmd[1]))
                continue
            if len(cmd) == 2:
                new(filename=cmd[1], mode="CL")

            elif len(cmd) == 3:
                new(filename=cmd[1], masterPassword=cmd[2], mode="CL")

            else:
                print("Unrecognized sintax.\nIntended use is:\n» 'new filename masterPassword'")
        elif cmd[0].lower()=="open": #open file with CL
            if len(cmd)<2:
                print("Unrecognized sintax.\nIntended use is:\n» 'open filename password'")
                continue
            if not validatefile(cmd[1]):
                    print("Not a valid file")
                    continue

            if len(cmd)==2:
                openCL(cmd[1])

            elif len(cmd)==3:
                openCL(cmd[1],cmd[2])
                
            else:
                print("Unrecognized sintax.\nIntended use is:\n» 'open filename password'")
        elif cmd[0].lower() == "help":
            print(
                """
                CL
                    » Show valid directory:     'dir'
                    » Delete a file:            'delete filename'
                    » Create a new file:        'new filename masterPassword'
                    » Open file with terminal:  'open filename password'
                    » New random password:      'pass length'
                    » Clean terminal:           'cls'
                    » Exit terminal:            'end'
                GUI
                    » Open a file with GUI:     'GUI open filename password'
                    » Open a new file with GUI: 'GUI new filename masterPassword'
                """

            )
        elif cmd[0].lower() == "pass":
            try:
                cl.makeNewPassword(int(cmd[1]))
            except:
                print("Exception occured.\nIntended use is\n» 'pass int(length)'")
        elif cmd in (["clc"],["clear"],["cls"],["clean"]):
            os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd in (["close"],["exit"],["end"]):
            #print(cmd)
            #input("Press ENTER to finish...")
            break
        else:
            print(f'Command [{" ".join(cmd)}] not recognized.')



if __name__ == "__main__":
    start()