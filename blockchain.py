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
        self.chain.append({
            "hash": block.hash(), "previous": block.previous_hash, "data": block.data, "nonce": block.nonce,
        })

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].get("hash")
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                print(block)
                self.add(block)
                break
            else:
                block.nonce+=1

# @snoop
@logger.catch
def main():
    blockchain = BlockChain()
    database = ["Hello World!", "GM", "Hiya!", "sweet Dreams!"]
    num = 0

    for data in database:
        num+=1
        blockchain.mine(Block(data, num))

    for block in blockchain.chain:
        print(block)


if __name__ == '__main__':
    main()
