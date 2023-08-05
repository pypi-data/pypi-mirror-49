# Pokerware

An application for those that don't want to manually look up [pokerware](https://github.com/skeeto/pokerware) words.

# Usage
``` $ pokerware --help
usage: pokerware [-h] [--formal] [--slang] [--custom CUSTOM_PATH]
                 code [code ...]

Generate Pokerware password

positional arguments:
  code                  A sequence of (Value, Suit, Value, Suit, Suit) entries

optional arguments:
  -h, --help            show this help message and exit
  --formal              Lookup words in the 'formal' wordlist
  --slang               Lookup words in the 'slang' wordlist
  --custom CUSTOM_PATH  Lookup words in a custom wordlist
```

## Examples
```
$ pokerware --formal ACADD ACTCC 3C4CH 5STHS
abide anemia fake peace
$ pokerware --slang ACADD
abate
```
