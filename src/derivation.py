import random
from src.sha256 import SHA256

class Derivation:
    """
    The Derivation class provides methods for generating salts, deriving keys from passwords, and performing XOR cipher operations for encrypting and decrypting passwords in the vault. It uses the SHA256 class to perform hashing operations, which are essential for both key derivation and generating salts.
    """
    def __init__(self):
        """
        Derivation class is responsible for generating salts, deriving keys from passwords, and performing XOR cipher operations for encrypting and decrypting passwords in the vault.
        It uses the SHA256 class to perform hashing operations, which are essential for both key derivation and generating salts."""
        fake_disk = {
            "global_salt": "ff82a2419dff8a7f",
            "master_check": "d273174f",
            "vault": {}
        }

        self.sha256 = SHA256()

    def generate_salt(self, length=16):
        """
        Generates a random salt string of the specified length.
        Args:
            length (int, optional): The length of the salt to be generated. Defaults to 16.
        Returns:
            str: A randomly generated salt string of the specified length.
        """
        assert isinstance(length, int)
        assert length > 0

        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        salt = ""
        for index in range(length):
            salt += characters[random.randint(0, 61)]
        full_hash = self.sha256.hash(salt)
        salt = full_hash[:16]
        
        return salt

    def derive_key(self, password, salt):
        """
        Derives a key from the given password and salt using a simple iterative hashing process.
        Args:
            password (str): The password from which to derive the key.
            salt (str): The salt to be used in the key derivation process.
        Returns:
            str: The derived key obtained by hashing the combination of the password and salt iteratively.
        """
        assert isinstance(password, str)
        assert isinstance(salt, str)
        
        key = password + salt
        for i in range(10):
            key = self.sha256.hash(key)
        return key

    def xor_cipher(self, key, data):
        """
        Performs an XOR cipher operation on the given data using the provided key. The key is repeated as necessary to match the length of the data.
        Args:
            key (str): The key to be used for the XOR cipher operation.
            data (str): The data to be encrypted or decrypted using the XOR cipher.
        Returns:
            str: The result of the XOR cipher operation, returned as a hexadecimal string.
        """
        assert isinstance(key, str) and isinstance(data, str)
        assert isinstance(data, str)
        assert len(key) > 0
        assert len(data) > 0

        result_bytes = []
        for i in range(len(data)):
            char_val = ord(data[i])
            
            key_val = ord(key[i % len(key)])    
            xor_val = char_val ^ key_val     
            result_bytes.append(xor_val)
        return bytes(result_bytes).hex()