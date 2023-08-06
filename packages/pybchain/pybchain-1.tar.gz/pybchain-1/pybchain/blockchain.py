from time import time
import hashlib


class Block:
    def __init__(self, data="", last_hash=0):
        self.__time = time()
        self.__data = data
        self.__last_hash = last_hash
        self.__hash_string = str(self.__time)+self.__data+str(self.__last_hash)

    def hash(self):
        return hashlib.sha256(self.__hash_string.encode()).hexdigest()

    def data(self):
        return self.__data


if __name__ == "__main__":
    blockchain = []
    example_string = "Hello my name is Python"
    for i in example_string.split(" "):
        try:
            last_hash = blockchain[len(blockchain)-1].hash()
        except:
            last_hash = 0
        blockchain.append(Block(i, last_hash))

    for i in blockchain:
        print(f"{i.data()} -> {i.hash()}")
