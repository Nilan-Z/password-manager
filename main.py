from src.sha256 import *
from src.derivation import *

fake_disk = {
  "users": {}
}

if __name__ == "__main__":
  while True:
    print("\n[1] Register\n[2] Login\n[3] Exit")
    start_choice = input("Choose an option: ")
    
    if start_choice == "1":
      username = input("Choose a username: ")
      if username in fake_disk["users"]:
        print("Username already exists")
      else:
        password = input("Choose a master password: ")
        salt = generate_salt()
        master_key = derive_key(password, salt)
        fake_disk["users"][username] = {
          "salt": salt,
          "check": hash(master_key)[:8],
          "vault": {}
        }
        
    elif start_choice == "2":
      users_list = list(fake_disk["users"].keys())
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
            user_data = fake_disk["users"][username]
            master_key = derive_key(input("Enter your password: "), user_data["salt"])
            
            if hash(master_key)[:8] == user_data["check"]:
              login = True
              while login == True:
                print("\nSelect an option:\n\n[1] Add a password\n[2] Remove a password\n[3] View passwords\n[4] Logout")
                option = input("Choose an option: ")
                
                if option == "1":
                  service = input("Service name: ")
                  password = input(f"Password for {service}: ")
                  user_data["vault"][service] = xor_cipher(master_key, password)
                  
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
                      
                elif option == "3":
                  print("\n--- DECRYPTED PASSWORDS ---")
                  if not user_data["vault"]:
                    print("Vault is empty")
                  for s, h in user_data["vault"].items():
                    raw_data = bytes.fromhex(h).decode('latin1')
                    decrypted_hex = xor_cipher(master_key, raw_data)
                    print(f"{s}: {bytes.fromhex(decrypted_hex).decode('latin1')}")
                    
                elif option == "4":
                  login = False
            else:
              print("Wrong password")
          
    elif start_choice == "3":
      break