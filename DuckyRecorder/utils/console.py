import os

def clear():
    os.system("clear" if os.name != "nt" else "cls")
