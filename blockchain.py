from hashlib import sha256

import snoop
from loguru import logger

from heartrate import trace

trace(browser=True)


class Block():
    data, hash, nonce = None, None, 0
    previous_hash = "0" * 64

    def __init__(self, data, number=0):
        self.data, self.number = data, number

    def hash(self):
        data2hash, h = "", sha256()
        for arg in [self.previous_hash, self.number, self.data, self.nonce]:
            data2hash += str(arg)
        h.update(data2hash.encode("utf-8"))
        return h.hexdigest()

    def __str__(self):
        return f"Block: \t{self.number}\nHash: \t{self.hash()}\nPrevious: {self.previous_hash}\nNonce: \t{self.nonce}"


class BlockChain():
    difficulty = 4

    def __init__(self, chain=[]):
        self.chain = chain

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block);
                break
            else:
                block.nonce += 1

    def is_valid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i - 1].hash()
            if _previous != _current or _current[:self.difficulty] != "0" * self.difficulty:
                return False
        return True


# @snoop
@logger.catch
def main():
    blockchain = BlockChain()
    database = ["Hello World!", "GM", "Hiya!", "sweet Dreams!"]
    num = 0

    for data in database:
        num += 1
        blockchain.mine(Block(data, num))

    for block in blockchain.chain:
        print(block)
        print("^"*128)

    blockchain.chain[2].data = "Corrupted"
    blockchain.mine(blockchain.chain[2])

    print(blockchain.is_valid())


if __name__ == '__main__':
    main()
