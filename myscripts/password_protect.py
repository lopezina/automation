from getpass import getpass
from cryptography.fernet import Fernet
 
key_file_path = "vault\enc.key"
p_file_path = "vault\p.txt"
 
# use for generate a symmetric key.
# then store the key as a file.
def generate_key_file():
    key = Fernet.generate_key()
    with open(key_file_path, 'wb') as file:
        file.write(key)
 
# Use the key for encryption and decryption.
def use_key():
    with open(key_file_path, 'rb') as file:
        return file.read()
 
# Get the password from user.
# the password is a string, before passing to Fernet for encryption
# the plaintext has to be converted to bytes, which is why encode('utf-8').
def store_mgmt_password():
    password = getpass('Enter your password, as password is not found: ')
    key = use_key()
    fernet = Fernet(key)
    # convert the plaintext password into bytes
    # and store the encrypted byte to enc_password.
    enc_password = fernet.encrypt(password.encode('utf-8'))
    # save the encrypted password to p.txt.
    with open(p_file_path, 'wb') as file:
        file.write(enc_password)
 
# Decrypt the p.txt and get the plaintext password.
def get_mgmt_password():
    key = use_key()
    fernet = Fernet(key)
    with open(p_file_path, 'rb') as file:
        password_in_bytes = file.read()
    # The content in the p.txt is byte, which is why decode('utf-8') to convert to string.
    return fernet.decrypt(password_in_bytes).decode('utf-8')

