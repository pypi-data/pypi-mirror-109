# anyseed
Generating seed from any mnemonic phrase

## Installing
```
  pip3 install anyseed
```

## Using
```python
  from anyseed import get_seed
  words = "pelican orphan cherry mouse lucky never ketchup cross million cross blue bring parade shadow steak"
  password = ""
  seed_data = get_seed(words, password)
  print("Type: {}\nSeed: {}".format(seed_data["type"], seed_data["seed"].hex()))
  # Type: bip39
  # Seed: 96d48cc015cecbf01b5d06da2ec59fd2849e768147a06e29053b45d800517f4374107d846175ac760535f176d1b7f771461c871c7bb3247f0c63c92727a98829
```
Works with electrum and bip39 mnemonics words and languages.
Possible types: ["electrum", "bip39", "unknown"]