import random
from src.sha256 import *

fake_disk = {
    "global_salt": "ff82a2419dff8a7f",
    "master_check": "d273174f",
    "vault": {}
}

def generate_salt(length=16):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    salt = ""
    for index in range(length):
      salt += characters[random.randint(0, 61)]
    full_hash = hash(salt)
    salt = full_hash[:16]
    
    return salt

def derive_key(password, salt):
  assert isinstance(password, str)
  assert isinstance(salt, str)
  key = password + salt
  for i in range(10):
    key = hash(key)
  return key

def xor_cipher(key, data):
    result_bytes = []
    for i in range(len(data)):
        char_val = ord(data[i])
        
        key_val = ord(key[i % len(key)])    
        xor_val = char_val ^ key_val     
        result_bytes.append(xor_val)
    return bytes(result_bytes).hex()