import json
import os
from colorama import Fore, Back, Style, init

from src.sha256 import SHA256
from src.derivation import Derivation

init(autoreset=True)

DATA_FILE = "data/data.json"

def clear_screen():
	os.system('cls' if os.name == 'nt' else 'clear')

def print_box(text, color=Fore.CYAN, width=50):
	"""Print text in a nice box"""
	print(f"{color}┌{'─' * (width - 2)}┐")
	lines = str(text).split('\n')
	for line in lines:
		padding = width - len(line) - 4
		print(f"{color}│ {line}{' ' * padding}│")
	print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_menu(title, options, color=Fore.CYAN):
	"""Print a formatted menu"""
	print(f"\n{color}╔{'═' * 48}╗")
	print(f"║ {title.center(46)} ║")
	print(f"╠{'═' * 48}╣")
	for key, value in options.items():
		print(f"║ {Fore.YELLOW}[{key}]{Style.RESET_ALL} {value:<41} ║")
	print(f"╚{'═' * 48}╝{Style.RESET_ALL}")

def print_success(text):
	"""Print success message"""
	print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

def print_error(text):
	"""Print error message"""
	print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_info(text):
	"""Print info message"""
	print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

def print_warning(text):
	"""Print warning message"""
	print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

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
	print(f"{Fore.CYAN}Welcome to Password Manager - Secure password storage{Style.RESET_ALL}\n")
	
	while True:
		options = {
			"1": "Register - Create new account",
			"2": "Login - Access your vault",
			"3": "Exit - Close application"
		}
		print_menu("MAIN MENU", options)
		start_choice = input(f"{Fore.YELLOW}➜ Choose an option: {Style.RESET_ALL}").strip()
		
		if start_choice == "1":
			clear_screen()
			print_info("Create a new account\n")
			username = input(f"{Fore.YELLOW}Username: {Style.RESET_ALL}").strip()
			if not username:
				print_error("Username cannot be empty")
				input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
				continue
			if username in data["users"]:
				print_error("Username already exists")
				input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
			else:
				password = input(f"{Fore.YELLOW}Master Password: {Style.RESET_ALL}")
				if not password:
					print_error("Password cannot be empty")
					input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
					continue
				salt = derivation.generate_salt()
				master_key = derivation.derive_key(password, salt)
				data["users"][username] = {
					"salt": salt,
					"check": sha256.hash(master_key)[:8],
					"vault": {}
				}
				save_data(data)
				print_success(f"Account '{username}' registered successfully")
				input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
				
		elif start_choice == "2":
			users_list = list(data["users"].keys())
			if not users_list:
				print_error("No accounts found. Please register first.")
			else:
				clear_screen()
				print_info("Select your profile:\n")
				for i in range(len(users_list)):
					print(f"{Fore.CYAN}  [{i}] {users_list[i]}{Style.RESET_ALL}")
				
				user_idx_str = input(f"\n{Fore.YELLOW}➜ Select profile number: {Style.RESET_ALL}").strip()
				if user_idx_str.isdigit():
					idx = int(user_idx_str)
					if 0 <= idx < len(users_list):
						username = users_list[idx]
						user_data = data["users"][username]
						password_input = input(f"{Fore.YELLOW}Master Password: {Style.RESET_ALL}")
						master_key = derivation.derive_key(password_input, user_data["salt"])
						
						if sha256.hash(master_key)[:8] == user_data["check"]:
							clear_screen()
							print_success(f"Welcome back, {username}!")
							login = True
							while login == True:
								options = {
									"1": "Add password",
									"2": "Remove password",
									"3": "View passwords",
									"4": "Logout"
								}
								print_menu(f"VAULT - {username}", options)
								option = input(f"{Fore.YELLOW}➜ Choose an option: {Style.RESET_ALL}").strip()
								
								if option == "1":
									clear_screen()
									print_info("Add a new password entry\n")
									service = input(f"{Fore.YELLOW}Service name: {Style.RESET_ALL}").strip()
									if not service:
										print_error("Service name cannot be empty")
										input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
										continue
									if service in user_data["vault"]:
										print_warning(f"'{service}' already exists. It will be overwritten.")
									password = input(f"{Fore.YELLOW}Password for {Fore.CYAN}{service}{Fore.YELLOW}: {Style.RESET_ALL}")
									user_data["vault"][service] = derivation.xor_cipher(master_key, password)
									save_data(data)
									print_success(f"Password for '{service}' added successfully")
									input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
									
								elif option == "2":
									clear_screen()
									accounts = list(user_data["vault"].keys())
									if not accounts:
										print_warning("No passwords to remove")
									else:
										print_info("Select password to remove:\n")
										for i in range(len(accounts)):
											print(f"{Fore.CYAN}  [{i}] {accounts[i]}{Style.RESET_ALL}")
										num_str = input(f"\n{Fore.YELLOW}➜ Select number to remove: {Style.RESET_ALL}").strip()
										if num_str.isdigit():
											num = int(num_str)
											if 0 <= num < len(accounts):
												confirm = input(f"{Fore.YELLOW}Are you sure? (y/n): {Style.RESET_ALL}").strip().lower()
												if confirm == 'y':
													deleted = accounts[num]
													del user_data["vault"][accounts[num]]
													save_data(data)
													print_success(f"Password for '{deleted}' removed successfully")
												else:
													print_info("Deletion cancelled")
										input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
										
								elif option == "3":
									clear_screen()
									print_info("Your encrypted passwords:\n")
									if not user_data["vault"]:
										print_warning("Vault is empty")
									else:
										print(f"{Fore.CYAN}{'─' * 50}")
										for s, h in user_data["vault"].items():
											raw_data = bytes.fromhex(h).decode('latin1')
											decrypted_hex = derivation.xor_cipher(master_key, raw_data)
											pwd = bytes.fromhex(decrypted_hex).decode('latin1')
											print(f"{Fore.GREEN}• {s:<20} {Fore.YELLOW}→ {pwd}{Style.RESET_ALL}")
										print(f"{Fore.CYAN}{'─' * 50}")
									input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
										
								elif option == "4":
									login = False
									clear_screen()
									print_success(f"Logged out successfully. Goodbye {username}!")
									input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
						else:
							print_error("Wrong password. Access denied.")
				else:
					print_error("Invalid input")
			input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
				
		elif start_choice == "3":
			clear_screen()
			print_info("Thank you for using Password Manager. Goodbye!")
			break
		else:
			print_error("Invalid option. Please try again.")