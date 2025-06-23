import os
from cryptography.fernet import Fernet, InvalidToken

KEY_FILE = "secret.key"
MASTER_PASSWORD = input('mypassword')

def generate_and_store_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    entered = input("Enter master password: ")
    if entered != MASTER_PASSWORD:
        print("Wrong password.")
        quit()
    try:
        with open(KEY_FILE, "rb") as f:
            return f.read()
    except FileNotFoundError:
        generate_and_store_key()
        return load_key()

key = load_key()
fernet = Fernet(key)

def add():

    name = input("ACCOUNT:")
    pwd = input("PASSWORD:")
    with open('password.txt', 'a') as f:
        encrypted_pwd = fernet.encrypt(pwd.encode()).decode()
        f.write(f'{name}|{encrypted_pwd}\n')

def view():
    with open('password.txt', 'r') as f:
        for line in f.readlines():
            data = line.strip()
            user, passw = data.split('|')
            try:
                decrypted_pwd = fernet.decrypt(passw.encode()).decode()
                print("ACCOUNT:", user, "PASSWORD:", decrypted_pwd)
            except InvalidToken:
                print(f"ACCOUNT: {user} | PASSWORD: <INVALID MASTER PASSWORD>")


while True:
    mode = input("What would you like to do? add, view or quit(q)").lower()

    if mode == "q":
        quit()

    elif mode == "add":
        add()

    elif mode == "view":
        view()

    else:
        print("INVALID MODE.")
        continue
        
