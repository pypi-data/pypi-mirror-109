import hashlib
from .tools import normalize_string
from .electrum import is_electrum_seed
from .bip39 import Bip39

def pbkdf2_hmac(mnemonic, password):
    mnemonic_bytes = mnemonic.encode("utf-8")
    password_bytes = password.encode("utf-8")
    seed = hashlib.pbkdf2_hmac(
        "sha512", mnemonic_bytes, password_bytes, 2048
    )
    return seed[:64]

def get_seed(mnemonic, password=""):
    mnemonic = normalize_string(mnemonic)
    password = normalize_string(password)
    # Check strings 
    if mnemonic == False or password == False:
        return False
    password_word = "mnemonic"
    mnemonic_type = "unknown"
    # Check for electrum seed
    if is_electrum_seed(mnemonic):
        password_word = "electrum"
        mnemonic_type = "electrum"
    else:
        bip39 = Bip39(mnemonic)
        if bip39.is_valid():
            mnemonic_type = "bip39"
    return {"type": mnemonic_type, "seed": pbkdf2_hmac(mnemonic, password_word + password)}