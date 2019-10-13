from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:

    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Johny"
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        tx_recipient = input("Enter recipient: ")
        tx_amount = float(input("Enter amount to sent: "))
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.chain:
            print('Outputting Block: ')
            print(block)
        else:
            print('-' * 20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('\n Please choose')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            print('4: Check transactions validity')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                recipient, amount = self.get_transaction_value()
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Added transaction!")
                else:
                    print("Transaction failed \n")
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                break
            print(f"Balance of {self.id}: {self.blockchain.get_balance()}")
            print(self.blockchain.get_balance())
        else:
            print('User left!')


node = Node()
node.listen_for_input()
