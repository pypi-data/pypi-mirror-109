import os, unicodedata
from typing import Sequence, Dict
from types import MappingProxyType

_WORDLIST_CACHE = {}  # type: Dict[str, Wordlist]

filenames = {
    'en':'english.txt',
    'es':'spanish.txt',
    'ja':'japanese.txt',
    'pt':'portuguese.txt',
    'zh':'chinese_simplified.txt'
}

def resource_path(*parts):
    pkg_dir = os.path.split(os.path.realpath(__file__))[0]
    return os.path.join(pkg_dir, *parts)

class Wordlist(tuple):

    def __init__(self, words: Sequence[str]):
        super().__init__()
        index_from_word = {w: i for i, w in enumerate(words)}
        self._index_from_word = MappingProxyType(index_from_word)  # no mutation

    def index(self, word, start=None, stop=None) -> int:
        try:
            return self._index_from_word[word]
        except KeyError as e:
            raise ValueError from e

    def __contains__(self, word) -> bool:
        try:
            self.index(word)
        except ValueError:
            return False
        else:
            return True

    @classmethod
    def from_file(cls, filename) -> 'Wordlist':
        path = resource_path('electrum_wordlist', filename)
        if path not in _WORDLIST_CACHE:
            with open(path, 'r', encoding='utf-8') as f:
                s = f.read().strip()
            s = unicodedata.normalize('NFKD', s)
            lines = s.split('\n')
            words = []
            for line in lines:
                line = line.split('#')[0]
                line = line.strip(' \r')
                assert ' ' not in line
                if line:
                    words.append(line)

            _WORDLIST_CACHE[path] = Wordlist(words)
        return _WORDLIST_CACHE[path]