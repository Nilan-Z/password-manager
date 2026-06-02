import json
import os
from colorama import Fore, Back, Style, init

from src.sha256 import SHA256
from src.derivation import Derivation

init(autoreset=True)

DATA_FILE = "data/data.json"

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

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
	clear_screen()
	ascii_art = f"""{Fore.CYAN}
	 ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
	 ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
	 ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
	 ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
	 ██║     ██║  ██║███████║███████║╚███╝███╔╝╚██████╔╝██║  ██║██████╔╝
	 ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
	
	 ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
	 ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
	 ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
	 ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
	 ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
	 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
	{Style.RESET_ALL}
	"""
	print(ascii_art)
	
	while True:
		clear_screen()
		print(f"\n{Fore.CYAN}{'='*40}")
		print(f"{Fore.CYAN}[1] Register\n[2] Login\n[3] Exit")
		print(f"{Fore.CYAN}{'='*40}")
		start_choice = input(f"{Fore.YELLOW}Choose an option: {Style.RESET_ALL}")
		
		if start_choice == "1":
			username = input(f"{Fore.YELLOW}Choose a username: {Style.RESET_ALL}")
			if username in data["users"]:
				print(f"{Fore.RED}Username already exists")
				input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
			else:
				password = input(f"{Fore.YELLOW}Choose a master password: {Style.RESET_ALL}")
				salt = derivation.generate_salt()
				master_key = derivation.derive_key(password, salt)
				data["users"][username] = {
					"salt": salt,
					"check": sha256.hash(master_key)[:8],
					"vault": {}
				}
				save_data(data)
				print(f"{Fore.GREEN}Account registered successfully")
				input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
				
		elif start_choice == "2":
			users_list = list(data["users"].keys())
			if not users_list:
				print(f"{Fore.RED}No accounts found")
			else:
				clear_screen()
				print(f"{Fore.CYAN}Select your profile:")
				for i in range(len(users_list)):
					print(f"{Fore.CYAN}[{i}] {users_list[i]}")
					
				user_idx_str = input(f"{Fore.YELLOW}Select profile number: {Style.RESET_ALL}")
				if user_idx_str.isdigit():
					idx = int(user_idx_str)
					if 0 <= idx < len(users_list):
						username = users_list[idx]
						user_data = data["users"][username]
						master_key = derivation.derive_key(input(f"{Fore.YELLOW}Enter your password: {Style.RESET_ALL}"), user_data["salt"])
						
						if sha256.hash(master_key)[:8] == user_data["check"]:
							clear_screen()
							print(f"{Fore.GREEN}Login successful")
							login = True
							while login == True:
								clear_screen()
								print(f"\n{Fore.CYAN}{'='*40}")
								print(f"{Fore.CYAN}[1] Add a password\n[2] Remove a password\n[3] View passwords\n[4] Logout")
								print(f"{Fore.CYAN}{'='*40}")
								option = input(f"{Fore.YELLOW}Choose an option: {Style.RESET_ALL}")
								
								if option == "1":
									clear_screen()
									service = input(f"{Fore.YELLOW}Service name: {Style.RESET_ALL}")
									password = input(f"{Fore.YELLOW}Password for {service}: {Style.RESET_ALL}")
									user_data["vault"][service] = derivation.xor_cipher(master_key, password)
									save_data(data)
									print(f"{Fore.GREEN}Password added successfully")
									input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
									
								elif option == "2":
									clear_screen()
									accounts = list(user_data["vault"].keys())
									if not accounts:
										print(f"{Fore.YELLOW}No passwords to remove")
									else:
										print(f"{Fore.CYAN}Select password to remove:")
										for i in range(len(accounts)):
											print(f"{Fore.CYAN}[{i}] {accounts[i]}")
										num_str = input(f"{Fore.YELLOW}Select the number to remove: {Style.RESET_ALL}")
										if num_str.isdigit():
											num = int(num_str)
											if 0 <= num < len(accounts):
												del user_data["vault"][accounts[num]]
												save_data(data)
												print(f"{Fore.GREEN}Password removed successfully")
										input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
										
								elif option == "3":
									clear_screen()
									print(f"\n{Fore.CYAN}{'='*40}")
									print(f"{Fore.CYAN}DECRYPTED PASSWORDS")
									print(f"{Fore.CYAN}{'='*40}")
									if not user_data["vault"]:
										print(f"{Fore.YELLOW}Vault is empty")
									else:
										for s, h in user_data["vault"].items():
											raw_data = bytes.fromhex(h).decode('latin1')
											decrypted_hex = derivation.xor_cipher(master_key, raw_data)
											pwd = bytes.fromhex(decrypted_hex).decode('latin1')
											print(f"{Fore.GREEN}{s}{Style.RESET_ALL}: {pwd}")
									input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
										
								elif option == "4":
									login = False
									clear_screen()
									print(f"{Fore.GREEN}Logged out successfully")
									input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
						else:
							print(f"{Fore.RED}Wrong password")
				
		elif start_choice == "3":
			break