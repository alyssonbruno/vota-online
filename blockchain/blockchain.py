from random import randint
from ..database import database

MIN = 0
MAX = 999999

__CHAIN_DATABASE__ = '.blockchain.db'


class BlockchainDB:
    def __init__(self):
        self.__conn = database.get_conection(__CHAIN_DATABASE__)
        database.create_if_not_existe_table('blockchain', '''
            CREATE TABLE blockchain(
                id number primary key,
                chain text,
                last number,
                first number 
            )
        ''', self.__conn)

    def close(self):
        self.__conn.close()

    def get(self, id: int):
        self.__conn.execute('SELECT chain, last, first FROM blockchain WHERE id = ?', id)
        return self.__conn.fetchone()

    def insert(self, id, chain, last, first):
        self.__conn.execute('INSERT INTO blockchain(chain, last, first) VALUES (?,?,?,?)', (id, chain, last, first))
        return self.__conn.commit()

    def update(self, id, chain, last, first):
        self.__conn.execute('UPDATE blockchain SET chain=?, last=?, first=? where id = ?', (chain, last, first, id))
        return self.__conn.commit()


class Blockchain:
    def __init__(self, id: int = None):
        self.closed = False
        self.__db = BlockchainDB()

        if id is None:
            self.__database_number = randint(MIN, MAX)
            self.__chain = {}
            self.__last = -1
            self.__first = -1
            self.__db.insert(self.__database_number, self.__chain, self.__last, self.__first)
        else:
            self.__database_number = id
            (self.__chain, self.__last, self.__first) = self.__db.get(self.__database_number)
        self.__actual = self.__first

    def close(self):
        if self.closed:
            raise Exception('You are face to the door')
        self.__db.update(self.__database_number, self.__chain, self.__last, self.__first)
        self.__db.close()
        self.closed = True

    def send(self, value):
        if self.closed:
            raise Exception('the blockchain is closed')
        key = self.__last + 1
        self.__chain[key] = {
            'value': value,
            'hash': hash(frozenset(self.__chain)),
            'prior': self.__last,
        }
        if self.__first == -1:
            self.__first = key
        self.__last = key
        return key

    def get(self, key: int = None):
        if self.closed:
            raise Exception('Not here man')
        if key is None:
            self.__actual += 1
            if self.__actual in self.__chain.keys():
                return self.__chain[self.__actual]
            else:
                self.__actual = self.__last
                raise Exception('No more for you!')
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
