import hashlib


class Keypair:
    def __init__(self, key1, key2) -> None:
        self.key1 = key1
        self.key2 = key2

    def join_keypair(self):
        # print(self.key1 + self.key2)
        return self.key1.strip() + self.key2.strip()

    def generate_hash(self):
        self.join_keypair()
        self.hash_result = hashlib.sha256(self.key1.encode())
        return self.hash_result.hexdigest()
