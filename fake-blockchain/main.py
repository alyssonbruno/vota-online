from .blockchain import Blockchain

class Manager:
    def __init__(self, blockchain):
        if blockchain is None:
            self.blockchain = Blockchain()
        else:
            self.blockchain = blockchain

if __name__ == 'main':
    print("It's rock!")
