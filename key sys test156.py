import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("RLM Key sys")
import os
import requests
import time
import sys
import webbrowser
from colorama import init, Fore, Style

# Initialize colorama for colorful terminal output
init(autoreset=True)

# --- GitHub Key URLs ---
FREEMIUM_URL = "https://raw.githubusercontent.com/keyholderRLM/KEY/refs/heads/main/key.txt"
PREMIUM_URL = "https://raw.githubusercontent.com/keyholderRLM/KEY/refs/heads/main/premium.txt"

# --- Determine AppData Path and Create RLM Folder ---
APPDATA_PATH = os.getenv("APPDATA")
RLM_DIR = os.path.join(APPDATA_PATH, "RLM")
if not os.path.exists(RLM_DIR):
    os.makedirs(RLM_DIR)

# Path to the registered_keys.txt file
KEY_FILE = os.path.join(RLM_DIR, "registered_keys.txt")

# --- Load/Save Keys from File ---
def load_registered_keys():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return [line.strip() for line in f.readlines()]
    return []

def save_registered_key(key):
    with open(KEY_FILE, 'a') as f:
        f.write(key + "\n")

# --- Fetch Keys from GitHub ---
def fetch_keys(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            keys = response.text.strip().splitlines()
            return keys
        else:
            print(Fore.RED + "Error: Failed to fetch keys from " + url)
            return []
    except Exception as e:
        print(Fore.RED + "Error fetching keys: " + str(e))
        return []

FREEMIUM_KEYS = fetch_keys(FREEMIUM_URL)
PREMIUM_KEYS = fetch_keys(PREMIUM_URL)

# --- Loading Animation (CMD-style) ---
def loading_animation():
    # Set CMD window title (Windows only)
    os.system('title RLM Key System')
    # Print loading text in yellow
    sys.stdout.write(Fore.YELLOW + "Processing")
    sys.stdout.flush()
    for _ in range(5):
        time.sleep(0.5)
        sys.stdout.write(".")
        sys.stdout.flush()
    print("\n" + Fore.GREEN + "Verification Complete!" + Style.RESET_ALL)

# --- Launch Batch File ---
def launch_batch(file_name):
    full_path = os.path.abspath(file_name)
    if os.path.exists(full_path):
        # Launch the batch file in a new CMD window
        os.system(f'cmd /c start "" "{full_path}"')
    else:
        print(Fore.RED + f"Error: Batch file '{file_name}' not found!" + Style.RESET_ALL)

# --- Open LinkVertise in Browser (Optional) ---
def open_linkvertise():
    webbrowser.open("https://link-hub.net/1314021/key-system")
    print(Fore.GREEN + "Opening LinkVertise page..." + Style.RESET_ALL)

# --- Display Features ---
def display_features():
    print(Fore.CYAN + "\nFeatures:")
    print(Fore.YELLOW + "  📁  Paid & Free Tools")
    print(Fore.YELLOW + "  👥  Can easily Dm the owner via tiktok")
    print(Fore.YELLOW + "  ⚙   Automated Licenses")
    print(Fore.YELLOW + "  ★★★★★ 5 Star Ratings")
    print(Fore.YELLOW + "  💡  Tool Suggestions" + Style.RESET_ALL)
    print()

# --- Key Verification ---
def verify_key(user_key):
    if user_key in FREEMIUM_KEYS:
        loading_animation()
        print(Fore.GREEN + "Freemium Key Accepted!" + Style.RESET_ALL)
        launch_batch("RLMmain.bat")
    elif user_key in PREMIUM_KEYS:
        loading_animation()
        print(Fore.BLUE + "Premium Key Accepted!" + Style.RESET_ALL)
        launch_batch("RLMpremium 0.9.bat")
    else:
        print(Fore.RED + "Incorrect key! Please check your key and try again." + Style.RESET_ALL)

# --- Registration and Login --- 

def register_key():
    registered_keys = load_registered_keys()
    new_key = input("Enter a new key to register: ").strip()
    # Check if the key is valid (exists in either Freemium or Premium keys list)
    if new_key in FREEMIUM_KEYS or new_key in PREMIUM_KEYS:
        if new_key in registered_keys:
            print(Fore.RED + "This key is already registered!" + Style.RESET_ALL)
        else:
            save_registered_key(new_key)
            print(Fore.GREEN + "Registration successful!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid key! This key does not exist in the freemium or premium lists." + Style.RESET_ALL)

def login():
    registered_keys = load_registered_keys()
    while True:
        user_key = input("Enter your registered key to login: ").strip()
        if user_key in registered_keys:
            print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
            verify_key(user_key)
            break  # Exit the loop once the login is successful
        else:
            print(Fore.RED + "Incorrect key! Please check your key and try again." + Style.RESET_ALL)

# --- Main Function ---
def main():
    # Display a header with color
    print(Fore.MAGENTA + "----------------------------------------")
    print(Fore.MAGENTA + "         RLM Key System                ")
    print(Fore.MAGENTA + "----------------------------------------" + Style.RESET_ALL)
    
    # Show the features list
    display_features()
    
    # Prompt user for action
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
        print(Fore.GREEN + "Exiting... Goodbye!" + Style.RESET_ALL)
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid choice! Please try again." + Style.RESET_ALL)
        main()

# Run the main function
if __name__ == "__main__":
    main()
