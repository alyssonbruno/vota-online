from .blockchain import Blockchain
from ..database import database


class Manager:

    def __get_blockchain(self, id_election):
        c = database.get_conection()
        c.create_if_not_existe_table('blockchain', '''
        CREATE TABLE blockchain(
            id_election      NUMBER,
            id_blockchain   NUMBER 
        ) 
        ''')
        c.execute('SELECT id_blockchain FROM blockchain WHERE id_election=?', id_election)
        return c.fetchone()

    def __save_blockchain(self, id_blockchain, id_election):
        c = database.get_conection()
        c.execute('INSERT INTO blockchain(id_blockchain, id_election) VALUES (?,?)', id_blockchain, id_election)
        return c.fetchone()

    def __init__(self, election: str):
        if not election:
            raise Exception('Invalide value to election')

        __id = self.__get_blockchain(election)
        if __id:
            self.__id_blockchain = __id
            self.blockchain = Blockchain(self.__id_blockchain)
        else:
            self.blockchain = Blockchain()
            self.__id_blockchain = self.blockchain.get_database_id()
            self.__save_blockchain(self.__id_blockchain, election)


if __name__ == 'main':
    print("It's rock!")
