def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for ch in plaintext:
        if ch.isalpha():
            code = ord(ch) + shift
            if ch in "XYZxyz":
                code -= 26
            finalLetter = chr(code)
            ciphertext += finalLetter
        else:
            ciphertext += ch

    return ciphertext
