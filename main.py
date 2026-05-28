import json
import os

from src.sha256 import SHA256
from src.derivation import Derivation

DATA_FILE = "database.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, dict) and "users" in data:
                return data
    except (json.JSONDecodeError, OSError):
        pass

    return {"users": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


data = load_data()
sha256 = SHA256()
derivation = Derivation()

if __name__ == "__main__":
  """
  This is the main entry point of the password manager application. It provides a command-line interface for users to register, log in, and manage their passwords securely. The application uses the Derivation class to handle key generation and encryption, and the SHA256 class for hashing operations. User data is stored in a JSON file, and the application ensures that passwords are encrypted before being saved to the vault.
  """
  while True:
    print("\n[1] Register\n[2] Login\n[3] Exit")
    start_choice = input("Choose an option: ")
    
    if start_choice == "1":
      username = input("Choose a username: ")
      if username in data["users"]:
        print("Username already exists")
      else:
        password = input("Choose a master password: ")
        salt = derivation.generate_salt()
        master_key = derivation.derive_key(password, salt)
        data["users"][username] = {
          "salt": salt,
          "check": sha256.hash(master_key)[:8],
          "vault": {}
        }
        save_data(data)
        
    elif start_choice == "2":
      users_list = list(data["users"].keys())
      if not users_list:
        print("No accounts found")
      else:
        for i in range(len(users_list)):
          print(f"[{i}] {users_list[i]}")
          
        user_idx_str = input("Select profile number: ")
        if user_idx_str.isdigit():
          idx = int(user_idx_str)
          if 0 <= idx < len(users_list):
            username = users_list[idx]
            user_data = data["users"][username]
            master_key = derivation.derive_key(input("Enter your password: "), user_data["salt"])
            
            if sha256.hash(master_key)[:8] == user_data["check"]:
              login = True
              while login == True:
                print("\nSelect an option:\n\n[1] Add a password\n[2] Remove a password\n[3] View passwords\n[4] Logout")
                option = input("Choose an option: ")
                
                if option == "1":
                  service = input("Service name: ")
                  password = input(f"Password for {service}: ")
                  user_data["vault"][service] = derivation.xor_cipher(master_key, password)
                  save_data(data)
                  
                elif option == "2":
                  accounts = list(user_data["vault"].keys())
                  if not accounts:
                    print("No passwords to remove")
                  else:
                    for i in range(len(accounts)):
                      print(f"[{i}] {accounts[i]}")
                    num_str = input("Select the number to remove: ")
                    if num_str.isdigit():
                      num = int(num_str)
                      if 0 <= num < len(accounts):
                        del user_data["vault"][accounts[num]]
                        save_data(data)
                      
                elif option == "3":
                  print("\n--- DECRYPTED PASSWORDS ---")
                  if not user_data["vault"]:
                    print("Vault is empty")
                  for s, h in user_data["vault"].items():
                    raw_data = bytes.fromhex(h).decode('latin1')
                    decrypted_hex = derivation.xor_cipher(master_key, raw_data)
                    print(f"{s}: {bytes.fromhex(decrypted_hex).decode('latin1')}")
                    
                elif option == "4":
                  login = False
            else:
              print("Wrong password")
          
    elif start_choice == "3":
      break