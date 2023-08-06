from setuptools import setup

setup(name='anyseed',
      version='1.1',
      description='Generating Seed from any mnemonic phrase',
      packages=['anyseed'],
      package_data={
        "anyseed": [
            "bip39_wordlist/english.txt",
            "bip39_wordlist/italian.txt",
            "bip39_wordlist/french.txt",
            "bip39_wordlist/spanish.txt",
            "bip39_wordlist/portuguese.txt",
            "bip39_wordlist/czech.txt",
            "bip39_wordlist/chinese_simplified.txt",
            "bip39_wordlist/chinese_traditional.txt",
            "bip39_wordlist/korean.txt",
            "bip39_wordlist/japanese.txt",
            "electrum_wordlist/chinese_simplified.txt",
            "electrum_wordlist/english.txt",
            "electrum_wordlist/japanese.txt",
            "electrum_wordlist/portuguese.txt",
            "electrum_wordlist/spanish.txt",
        ]
    },
      author_email='phoenixburton@yandex.ru',
      zip_safe=False)