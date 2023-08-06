from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)

cipher = Fernet(key)

# ----------------------------------------------------

with open('../../my_key.txt', 'wb') as f:
    f.write(key)

text_to_secure = open('../../stih.txt', 'rb').read()
print(text_to_secure)

with open('../../my_secured_text.txt', 'wb') as f:
    f.write(cipher.encrypt(text_to_secure))

text_to_unsecure = open('../../my_secured_text.txt', 'rb').read()
print(text_to_unsecure)

with open('../../my_unsecured_text.txt', 'wb') as f:
    f.write(cipher.decrypt(text_to_unsecure))