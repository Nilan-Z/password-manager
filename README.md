# 🔐 Password Manager

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A simple command-line password manager that stores encrypted credentials in a JSON vault.
This project uses a master password, SHA256-based key derivation, and XOR-based vault encryption.

---

## 📚 Table of Contents

- Features
- Note
- Installation
- Usage
- Storage
- Security
- Example
- License

---

## 🚀 Features

## ⚠️ Note

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/Nilan-Z/password-manager.git
cd password-manager
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt`, the project only depends on the Python standard library.

---

## ▶️ Usage

Run the command-line app:

```bash
python main.py
```

Then choose one of the options:

    [1] Register
    [2] Login
    [3] Exit

After login, choose:

    [1] Add a password
    [2] Remove a password
    [3] View passwords
    [4] Logout

Notes:

- Each account is stored under a username.
- Vault entries are encrypted and saved automatically on add/remove operations.
- The master password is required to decrypt stored passwords.

---

## ⚙️ Storage

User data is stored in `data.json` in the repository root.
The file structure looks like this:

```json
{
  "users": {
    "username": {
      "salt": "...",
      "check": "...",
      "vault": {
        "service": "..."
      }
    }
  }
}
```

If `data.json` does not exist or is invalid, the app starts with an empty vault.

---

## 🧠 Security

## 🧾 Example

## 📄 License

This project is licensed under the [MIT License](LICENSE).
