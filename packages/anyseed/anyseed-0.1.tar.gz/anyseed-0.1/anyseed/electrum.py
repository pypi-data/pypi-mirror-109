import unicodedata, hashlib, string, hmac
from typing import AnyStr
from .old_mnemonic import mn_decode

# The hash of the mnemonic seed must begin with this
SEED_PREFIX        = '01'      # Standard wallet
SEED_PREFIX_SW     = '100'     # Segwit wallet
SEED_PREFIX_2FA    = '101'     # Two-factor authentication
SEED_PREFIX_2FA_SW = '102'     # Two-factor auth, using segwit

# http://www.asahi-net.or.jp/~ax2s-kmtn/ref/unicode/e_asia.html
CJK_INTERVALS = [
    (0x4E00, 0x9FFF, 'CJK Unified Ideographs'),
    (0x3400, 0x4DBF, 'CJK Unified Ideographs Extension A'),
    (0x20000, 0x2A6DF, 'CJK Unified Ideographs Extension B'),
    (0x2A700, 0x2B73F, 'CJK Unified Ideographs Extension C'),
    (0x2B740, 0x2B81F, 'CJK Unified Ideographs Extension D'),
    (0xF900, 0xFAFF, 'CJK Compatibility Ideographs'),
    (0x2F800, 0x2FA1D, 'CJK Compatibility Ideographs Supplement'),
    (0x3190, 0x319F , 'Kanbun'),
    (0x2E80, 0x2EFF, 'CJK Radicals Supplement'),
    (0x2F00, 0x2FDF, 'CJK Radicals'),
    (0x31C0, 0x31EF, 'CJK Strokes'),
    (0x2FF0, 0x2FFF, 'Ideographic Description Characters'),
    (0xE0100, 0xE01EF, 'Variation Selectors Supplement'),
    (0x3100, 0x312F, 'Bopomofo'),
    (0x31A0, 0x31BF, 'Bopomofo Extended'),
    (0xFF00, 0xFFEF, 'Halfwidth and Fullwidth Forms'),
    (0x3040, 0x309F, 'Hiragana'),
    (0x30A0, 0x30FF, 'Katakana'),
    (0x31F0, 0x31FF, 'Katakana Phonetic Extensions'),
    (0x1B000, 0x1B0FF, 'Kana Supplement'),
    (0xAC00, 0xD7AF, 'Hangul Syllables'),
    (0x1100, 0x11FF, 'Hangul Jamo'),
    (0xA960, 0xA97F, 'Hangul Jamo Extended A'),
    (0xD7B0, 0xD7FF, 'Hangul Jamo Extended B'),
    (0x3130, 0x318F, 'Hangul Compatibility Jamo'),
    (0xA4D0, 0xA4FF, 'Lisu'),
    (0x16F00, 0x16F9F, 'Miao'),
    (0xA000, 0xA48F, 'Yi Syllables'),
    (0xA490, 0xA4CF, 'Yi Radicals'),
]

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

def is_CJK(c):
    n = ord(c)
    for imin,imax,name in CJK_INTERVALS:
        if n>=imin and n<=imax: return True
    return False

def normalize_string(txt: AnyStr):
    if isinstance(txt, bytes):
        utxt = txt.decode("utf8")
    elif isinstance(txt, str):
        utxt = txt
    else:
        return False
    return unicodedata.normalize("NFKD", utxt)

def normalize_text(seed: str) -> str:
    # normalize
    seed = unicodedata.normalize('NFKD', seed)
    # lower
    seed = seed.lower()
    # remove accents
    seed = u''.join([c for c in seed if not unicodedata.combining(c)])
    # normalize whitespaces
    seed = u' '.join(seed.split())
    # remove whitespaces between CJK
    seed = u''.join([seed[i] for i in range(len(seed)) if not (seed[i] in string.whitespace and is_CJK(seed[i-1]) and is_CJK(seed[i+1]))])
    return seed

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