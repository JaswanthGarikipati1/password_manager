from cryptography.fernet import Fernet
from flask import current_app

def create_cipher_suite(secret_key):
    return Fernet(secret_key)

def encrypt_text(cipher_suite, text):
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt_text(cipher_suite, encrypted_text):
    return cipher_suite.decrypt(encrypted_text.encode()).decode()
