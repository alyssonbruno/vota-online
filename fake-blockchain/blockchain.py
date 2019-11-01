from random import randint
from hashlib import sha512 as sha

MIN = 0
MAX = 999999

__CHAIN_DATABASE__ = {}


class Blockchain:
    def __init__(self, id: int = None):
        self.closed = False

        if id is None:
            self.__database_number = randint(MIN, MAX)
            self.__chain = {}
            self.__last = -1
            self.__first = -1

        else:
            self.__database_number = id
            self.__chain = __CHAIN_DATABASE__[id]['banco']
            self.__last = __CHAIN_DATABASE__[id]['last']
            self.__first = __CHAIN_DATABASE__[id]['first']
        self.__actual = self.__first

    def close(self):
        if self.closed:
            raise Exception('Já está fechado')
        if self.__database_number in __CHAIN_DATABASE__.keys():
            __CHAIN_DATABASE__[self.__database_number] = {
                'banco': self.__chain,
                'first': self.__first,
                'last': self.__last
            }
        else:
            __CHAIN_DATABASE__[self.__database_number] = {
                'banco':  self.__chain,
                'first': self.__first,
                'last': self.__last
            }
        self.closed = True

    def send(self, value):
        if self.closed:
            raise Exception('Fechado')
        key = self.__last+1
        self.__chain[key] = {
            'valor': value,
            'hash': hash(frozenset(self.__chain)),
            'prior': self.__last,
        }
        if self.__first == -1:
            self.__first = key
        self.__last = key
        return key

    def get(self, key: int = None):
        if self.closed:
            raise Exception('Fechado')
        if key is None:
            self.__actual += 1
            if self.__actual in self.__chain.keys():
                return self.__chain[self.__actual]
            else:
                self.__actual = self.__last
                raise Exception('Final do arquivo baby!')
        else:
            return self.__chain[key]

    def get_database_id(self):
        return self.__database_number


if __name__ == '__main__':

    print(__CHAIN_DATABASE__)
    b = Blockchain()
    id = b.get_database_id()
    key1 = b.send('teste')
    key2 = b.send('outro teste')
    b.close()
    del b
    print(__CHAIN_DATABASE__)
    b1 = Blockchain(id)
    key3 = b1.send('alysson')
    assert key1 != key3
    key4 = b1.send('bruno')
    assert (key4 != key1) and (key4 != key3)
    print(b1.get())
    print(b1.get(key2))
    b1.close()
    print(__CHAIN_DATABASE__)
