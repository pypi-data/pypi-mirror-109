import hashlib
from .electrum import normalize_string, is_electrum_seed

def get_seed(mnemonic, password=""):
    mnemonic = normalize_string(mnemonic)
    password = normalize_string(password)
    if mnemonic == False or password == False:
        return False
    password = ("electrum" if is_electrum_seed(mnemonic) else "mnemonic") + password
    mnemonic_bytes = mnemonic.encode("utf-8")
    password_bytes = password.encode("utf-8")
    seed = hashlib.pbkdf2_hmac(
        "sha512", mnemonic_bytes, password_bytes, 2048
    )
    return seed[:64]