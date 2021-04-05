import pyperclip
import random
import hashlib
import pyaes
import os

def makeKey(masterkey,iv):
    key = hashlib.pbkdf2_hmac("sha256", bytes(str(masterkey).encode()), iv,200000)
    return key

def toCypher(masterkey,password, UserKey):
    cyphertext=[]
    for c in password:
        cyphertext.append(ord(c)*UserKey)
    iv = os.urandom(16)
    key = makeKey(masterkey, iv)
    encrypter = pyaes.Encrypter(pyaes.AESModeOfOperationCBC(key, iv))
    securePW = encrypter.feed(",".join(map(str,cyphertext)).encode('utf8'))
    securePW += encrypter.feed()

    return securePW, iv

def fromCypher(masterkey, cyphertext, key, iv):
    decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(key, iv))
    decryptedData = decrypter.feed(cyphertext)
    decryptedData += decrypter.feed()

    decrypted = list(map(int,decryptedData.decode('utf8').split(",")))
    text=[]
    for c in decrypted:
        try:
            char=int((c/masterkey))
            if char>31:
                text.append(chr(char))
            else:
                text.append(chr(random.randrange(33, 126)))
        except:
            text.append(chr(random.randrange(33, 126)))
    return "".join(text)

def copyDesciferedToClipboard(masterKey, cyphertext, iv, key):
    text=fromCypher(key, cyphertext, makeKey(masterKey,iv), iv)
    pyperclip.copy(text)

def validateMaster(masterKey, cyphertext, iv, key=1):
    try:
        text=fromCypher(key, cyphertext, makeKey(masterKey,iv), iv)
    except:
        text="denied"

    return text == "00000000000000000000"

