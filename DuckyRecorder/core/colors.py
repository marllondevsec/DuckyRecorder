def green(text: str) -> str:
    return f"\033[1;92m{text}\033[0m"

def red(text: str) -> str:
    return f"\033[1;91m{text}\033[0m"

def yellow(text: str) -> str:
    return f"\033[1;93m{text}\033[0m"

def cyan(text: str) -> str:
    return f"\033[1;96m{text}\033[0m"
