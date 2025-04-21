import ctypes
import os
import shutil
import requests
import time
import sys
import webbrowser
import tempfile
import subprocess
from colorama import init, Fore, Style

# ——— Initialize ———
ctypes.windll.kernel32.SetConsoleTitleW("RLM Key System")
init(autoreset=True)

# ——— Constants ———
FREEMIUM_URL  = "https://raw.githubusercontent.com/keyholderRLM/KEY/refs/heads/main/key.txt"
PREMIUM_URL   = "https://raw.githubusercontent.com/keyholderRLM/KEY/refs/heads/main/premium.txt"
APPDATA_PATH  = os.getenv("APPDATA")
RLM_DIR       = os.path.join(APPDATA_PATH, "RLM")
KEY_FILE      = os.path.join(RLM_DIR, "registered_keys.txt")
LAUNCH_TOKEN  = "LAVA2024"    # ← must match the check in both batch files

# Ensure RLM folder exists
os.makedirs(RLM_DIR, exist_ok=True)

# ——— Key Storage Helpers ———
def load_registered_keys():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return [line.strip() for line in f]
    return []

def save_registered_key(key):
    with open(KEY_FILE, 'a') as f:
        f.write(key + "\n")

# ——— Fetch remote keys ———
def fetch_keys(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text.strip().splitlines()
    except Exception as e:
        print(Fore.RED + f"Error fetching keys from {url}: {e}")
        return []

FREEMIUM_KEYS = fetch_keys(FREEMIUM_URL)
PREMIUM_KEYS  = fetch_keys(PREMIUM_URL)

# ——— UI Helpers ———
def loading_animation():
    os.system('title RLM Key System')
    sys.stdout.write(Fore.YELLOW + "Processing")
    sys.stdout.flush()
    for _ in range(5):
        time.sleep(0.5)
        sys.stdout.write(".")
        sys.stdout.flush()
    print("\n" + Fore.GREEN + "Verification Complete!" + Style.RESET_ALL)

def launch_batch(file_name):
    rlm_path   = os.path.join(RLM_DIR, file_name)
    local_path = os.path.abspath(file_name)

    if os.path.exists(rlm_path):
        path_to_run = rlm_path
    elif os.path.exists(local_path):
        try:
            shutil.copy(local_path, RLM_DIR)
            path_to_run = rlm_path
        except Exception as e:
            print(Fore.YELLOW + f"Warning: could not copy to RLM folder: {e}")
            path_to_run = local_path
    else:
        print(Fore.RED + f"Error: '{file_name}' not found in AppData or current folder.")
        return

    # Launch the batch (it will check %TEMP%\run.token internally)
    subprocess.call(f'cmd /c start "" "{path_to_run}"', shell=True)

def open_linkvertise():
    webbrowser.open("https://link-hub.net/1314021/key-system")
    print(Fore.GREEN + "Opening LinkVertise page..." + Style.RESET_ALL)

def display_features():
    print(Fore.CYAN + "\nFeatures:")
    print(Fore.YELLOW + "  📁  Paid & Free Tools")
    print(Fore.YELLOW + "  👥  Can easily Dm the owner via tiktok")
    print(Fore.YELLOW + "  ⚙   Automated Licenses")
    print(Fore.YELLOW + "  ★★★★★ 5 Star Ratings")
    print(Fore.YELLOW + "  💡  Tool Suggestions" + Style.RESET_ALL)
    print()

# ——— Core: Verify & Launch ———
def verify_key(user_key):
    if user_key in FREEMIUM_KEYS:
        loading_animation()
        print(Fore.GREEN + "Freemium Key Accepted!" + Style.RESET_ALL)
        batch_file = "RLMmain.bat"
    elif user_key in PREMIUM_KEYS:
        loading_animation()
        print(Fore.BLUE + "Premium Key Accepted!" + Style.RESET_ALL)
        batch_file = "RLMpremium.bat"
    else:
        print(Fore.RED + "Incorrect key! Please try again." + Style.RESET_ALL)
        return

    # Write secure token to TEMP
    token_path = os.path.join(tempfile.gettempdir(), "run.token")
    with open(token_path, "w") as tf:
        tf.write(LAUNCH_TOKEN)

    # Launch the authorized batch
    launch_batch(batch_file)

# ——— Registration & Login ———
def register_key():
    regs = load_registered_keys()
    new = input("Enter a new key to register: ").strip()
    if new in FREEMIUM_KEYS or new in PREMIUM_KEYS:
        if new in regs:
            print(Fore.RED + "This key is already registered!")
        else:
            save_registered_key(new)
            print(Fore.GREEN + "Registration successful!")
    else:
        print(Fore.RED + "Invalid key! Not found in authorized lists.")

def login():
    regs = load_registered_keys()
    while True:
        user_key = input("Enter your registered key to login: ").strip()
        if user_key in regs:
            print(Fore.GREEN + "Login successful!")
            verify_key(user_key)
            break
        else:
            print(Fore.RED + "Incorrect key! Please try again.")

# ——— Main Menu ———
def main():
    print(Fore.MAGENTA + "----------------------------------------")
    print(Fore.MAGENTA + "         RLM Key System                ")
    print(Fore.MAGENTA + "----------------------------------------" + Style.RESET_ALL)
    display_features()
    print(Fore.CYAN + "1. Register a new key")
    print("2. Login with existing key")
    print("3. Open LinkVertise")
    print("4. Exit" + Style.RESET_ALL)

    choice = input("Choose an option: ").strip()
    if choice == "1":
        register_key()
    elif choice == "2":
        login()
    elif choice == "3":
        open_linkvertise()
    elif choice == "4":
        print(Fore.GREEN + "Goodbye!")
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid choice!")
        main()

if __name__ == "__main__":
    main()
