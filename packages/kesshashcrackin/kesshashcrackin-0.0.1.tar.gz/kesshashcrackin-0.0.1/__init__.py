import hashlib


class HashCrack:
    def __init__(self, hash_string: str, wordlist):
        self.hash = hash_string
        self.wordlist = wordlist

    def md5(self) -> str:
        for line in open(self.wordlist).readlines():
            password = line.strip()
            password = password.encode('utf-8')

            hashed_wl = hashlib.md5(password).hexdigest()
            if hashed_wl == self.hash:
                return line.strip()

    def sha1(self) -> str:
        for line in open(self.wordlist).readlines():
            password = line.strip()
            password = password.encode('utf-8')

            hashed_wl = hashlib.sha1(password).hexdigest()
            if hashed_wl == self.hash:
                return line.strip()

    def sha256(self) -> str:
        for line in open(self.wordlist).readlines():
            password = line.strip()
            password = password.encode('utf-8')

            hashed_wl = hashlib.sha256(password).hexdigest()
            if hashed_wl == self.hash:
                return line.strip()

    def get_all(self) -> str: . . .