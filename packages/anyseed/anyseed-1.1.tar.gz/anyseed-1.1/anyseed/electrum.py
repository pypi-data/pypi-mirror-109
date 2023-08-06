import hashlib, hmac
from .old_mnemonic import mn_decode
from .tools import normalize_text

# The hash of the mnemonic seed must begin with this
SEED_PREFIX        = '01'      # Standard wallet
SEED_PREFIX_SW     = '100'     # Segwit wallet
SEED_PREFIX_2FA    = '101'     # Two-factor authentication
SEED_PREFIX_2FA_SW = '102'     # Two-factor auth, using segwit

def bh2u(x: bytes) -> str:
    """
    str with hex representation of a bytes-like object

    >>> x = bytes((1, 2, 10))
    >>> bh2u(x)
    '01020A'
    """
    return x.hex()

def hmac_oneshot(key: bytes, msg: bytes, digest) -> bytes:
    if hasattr(hmac, 'digest'):
        # requires python 3.7+; faster
        return hmac.digest(key, msg, digest)
    else:
        return hmac.new(key, msg, digest).digest()

def is_new_seed(x: str, prefix=SEED_PREFIX) -> bool:
    x = normalize_text(x)
    s = bh2u(hmac_oneshot(b"Seed version", x.encode('utf8'), hashlib.sha512))
    return s.startswith(prefix)

def is_old_seed(seed: str) -> bool:
    seed = normalize_text(seed)
    words = seed.split()
    try:
        # checks here are deliberately left weak for legacy reasons, see #3149
        mn_decode(words)
        uses_electrum_words = True
    except Exception:
        uses_electrum_words = False
    try:
        seed = bytes.fromhex(seed)
        is_hex = (len(seed) == 16 or len(seed) == 32)
    except Exception:
        is_hex = False
    return is_hex or (uses_electrum_words and (len(words) == 12 or len(words) == 24))

def seed_type(x: str) -> str:
    num_words = len(x.split())
    if is_old_seed(x):
        return 'old'
    elif is_new_seed(x, SEED_PREFIX):
        return 'standard'
    elif is_new_seed(x, SEED_PREFIX_SW):
        return 'segwit'
    elif is_new_seed(x, SEED_PREFIX_2FA) and (num_words == 12 or num_words >= 20):
        # Note: in Electrum 2.7, there was a breaking change in key derivation
        #       for this seed type. Unfortunately the seed version/prefix was reused,
        #       and now we can only distinguish them based on number of words. :(
        return '2fa'
    elif is_new_seed(x, SEED_PREFIX_2FA_SW):
        return '2fa_segwit'
    return ''

def is_electrum_seed(x: str) -> bool:
    return bool(seed_type(x))