import random
from src.sha256 import SHA256

class Derivation:
    def __init__(self):
        fake_disk = {
            "global_salt": "ff82a2419dff8a7f",
            "master_check": "d273174f",
            "vault": {}
        }

        self.sha256 = SHA256()

    def generate_salt(self, length=16):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        salt = ""
        for index in range(length):
            salt += characters[random.randint(0, 61)]
        full_hash = self.sha256.hash(salt)
        salt = full_hash[:16]
        
        return salt

    def derive_key(self, password, salt):
        assert isinstance(password, str)
        assert isinstance(salt, str)
        key = password + salt
        for i in range(10):
            key = self.sha256.hash(key)
        return key

    def xor_cipher(self, key, data):
        result_bytes = []
        for i in range(len(data)):
            char_val = ord(data[i])
            
            key_val = ord(key[i % len(key)])    
            xor_val = char_val ^ key_val     
            result_bytes.append(xor_val)
        return bytes(result_bytes).hex()