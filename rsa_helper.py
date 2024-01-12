import rsa

def generate_keys(file_name, key_len = 1024):
    (publicKey, privateKey) = rsa.newkeys(key_len)
    with open(file_name + '/publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open(file_name + 'privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))

def load_keys(file_name):
    with open(file_name + 'publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open(file_name + 'privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return publicKey, privateKey

def encrypt(message, key):
    return rsa.encrypt(message.encode('utf-8'), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('utf-8')
    except:
        return None
def encrypt_file(file_name, publicKey):
    with open(file_name, 'r') as file:
        content = file.read()
    encrypted_content = rsa.encrypt(content.encode('utf-8'), publicKey)
    return encrypted_content
def main():
    generate_keys("keys/test/")
    publicKey, privateKey = load_keys("keys/test/")

    message = input('Enter a message:')
    ciphertext = encrypt(message, publicKey)

    print(f'Cipher text: {ciphertext}')
    plaintext = decrypt(ciphertext, privateKey)
    print(f'Plain text: {plaintext}')

if __name__ == '__main__':
    main()