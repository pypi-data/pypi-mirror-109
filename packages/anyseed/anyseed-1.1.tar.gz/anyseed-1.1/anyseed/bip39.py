import os, hashlib
from .tools import normalize_string, int_to_binstr, binstr_to_bytes, bytes_to_binstr, encode
from .wordlist import Wordlist

class Bip39:

    WORD_BITS: int = 11

    def __init__(self, phrase):
        self.phrase = normalize_string(phrase)
        self.words = self.phrase.split(" ")
        self.wordlists = self.get_wordlists()
        self.lang = self.get_lang()
        self.wordlist = self.wordlists[self.lang] if self.lang != False else False
        self.binary_words = self.get_binary() if self.wordlist != False else False

    def get_words_files(self):
        words_dir = os.path.split(os.path.realpath(__file__))[0] + "/bip39_wordlist/"
        files = []
        for file in os.listdir(words_dir):
            lang = file.replace(".txt", "")
            files.append({
                "lang": lang,
                "filename": words_dir + file
            })
        return files

    def get_wordlists(self):
        files = self.get_words_files()
        wordlists = {}
        for wordlist in files:
            fh = open(wordlist["filename"], "r", encoding="utf-8")
            lines = fh.readlines()
            words = []
            for word in lines:
                word = normalize_string(word.strip())
                words.append(word)
            wordlists[wordlist["lang"]] = Wordlist(words)
            fh.close()
        return wordlists

    def get_lang(self):
        for lang, wordlist in self.wordlists.items():
            next_lang = False
            for word in self.words:
                if wordlist.__contains__(word):
                    continue
                else:
                    next_lang = True
                    break
            if not next_lang:
                return lang
        return False

    def get_binary(self):
        binary_words = []
        for word in self.words:
            binary_words.append(int_to_binstr(self.wordlist.index(word), Bip39.WORD_BITS))
        return binary_words

    def get_binary_str(self):
        return "".join(self.binary_words) if self.binary_words != False else ""

    def get_checksum_len(self, binary_str):
        return len(binary_str) // 33

    def get_checksum(self):
        binary_str = self.get_binary_str()
        return binary_str[-self.get_checksum_len(binary_str):]

    def get_entropy_bytes(self):
        binary_str = self.get_binary_str()
        checksum_len = self.get_checksum_len(binary_str)
        entropy_bin = binary_str[:-checksum_len]
        return binstr_to_bytes(entropy_bin, checksum_len * 8)

    def compute_checksum(self):
        binary_str = self.get_binary_str()
        entropy_bytes = self.get_entropy_bytes()
        entropy_hash_bin = bytes_to_binstr(hashlib.sha256(encode(entropy_bytes)).digest(), hashlib.sha256().digest_size * 8)
        checksum_bin = entropy_hash_bin[:self.get_checksum_len(binary_str)]
        return checksum_bin

    def is_valid(self):
        if self.lang == False:
            return False
        checksum = self.get_checksum()
        comp_checksum = self.compute_checksum()
        return checksum == comp_checksum