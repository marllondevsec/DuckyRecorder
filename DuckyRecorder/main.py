from DuckyRecorder.cli.menu import main_menu
from DuckyRecorder.config import ensure_directories

def main():
    ensure_directories()
    main_menu()

if __name__ == "__main__":
    main()
