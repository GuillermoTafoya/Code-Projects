import pyperclip
import random

def toCypher(password, key):
    cyphertext=[]
    for c in password:
        cyphertext.append(ord(c)*key)
    pyperclip.copy(str(cyphertext))   

def fromCypher(cyphertext, key):
    text=[]
    for c in cyphertext:
        try:
            char=int((c/key))
            if char>31:
                text.append(chr(char))
            else:
                text.append(chr(random.randrange(33, 126)))
        except:
            text.append(chr(random.randrange(33, 126)))
    return text

def copyDesciferedToClipboard(cyphertext, key):
    text=fromCypher(cyphertext,key)
    descyfered="".join(text)
    pyperclip.copy(descyfered)