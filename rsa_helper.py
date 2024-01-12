import rsa

def generate_keys():
    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))

def load_keys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return publicKey, privateKey

def encrypt(message, key):
    return rsa.encrypt(message.encode('utf-8'), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('utf-8')
    except:
        return False

def main():
    generate_keys()
    publicKey, privateKey = load_keys()

    message = input('Enter a message:')
    ciphertext = encrypt(message, publicKey)

    print(f'Cipher text: {ciphertext}')
    plaintext = decrypt(ciphertext, privateKey)
    print(f'Plain text: {plaintext}')

if __name__ == '__main__':
    main()