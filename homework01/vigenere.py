def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword = keyword.lower()
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            key = ord(keyword[i % len(keyword)]) - 97
            c = ord(plaintext[i])
            if plaintext[i].isupper() and c >= 91 - key:
                ciphertext += chr(c - 26 + key)
            elif plaintext[i].islower() and c >= 123 - key:
                ciphertext += chr(c - 26 + key)
            else:
                ciphertext += chr(c + key)
        else:
            ciphertext += plaintext[i]

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword = keyword.lower()
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            key = ord(keyword[i % len(keyword)]) - 97
            c = ord(ciphertext[i])
            if ciphertext[i].isupper() and c <= 64 + key:
                plaintext += chr(c + 26 - key)
            elif ciphertext[i].islower() and c <= 96 + key:
                plaintext += chr(c + 26 - key)
            else:
                plaintext += chr(c - key)
        else:
            plaintext += ciphertext[i]

    return plaintext
