import hashlib
import json
from collections import OrderedDict
from functools import reduce

from block import Block
from hash_util import hash_block
from transaction import Transaction

MINING_REWARD = 10
owner = "Johny"
participants = {"Johny"}


def load_data():
    try:
        with open("blockchain.txt", mode="r") as f:
            file_content = f.readlines()
            global blockchain, open_transactions

            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []

            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        genesis_block = Block(index=0, previous_hash='', transactions=[], proof=100, timestamp=0)
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Cleanup!')


load_data()


def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write("\n")
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
    except IOError:
        print("Saving failed!")


def valid_proof(transactions, last_hash, proof):
    guess = f"{[tx.to_ordered_dict() for tx in transactions]}{last_hash}{proof}".encode()
    guess_hash = hashlib.sha3_256(guess).hexdigest()
    print(guess_hash)
    return guess_hash[:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

    print(tx_sender)

    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received - amount_sent


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()

    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transaction, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input("Enter recipient: ")
    tx_amount = float(input("Enter amount to sent: "))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block: ')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of work is invalid! ")
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def menu():
    global open_transactions
    waiting_for_input = True
    while waiting_for_input:
        print('\n Please choose')
        print('1: Add a new transaction value')
        print('2: Mine a new block')
        print('3: Output the blockchain blocks')
        print('4: Output participants')
        print('5: Check transactions validity')
        print('q: Quit')
        user_choice = get_user_choice()
        if user_choice == '1':
            recipient, amount = get_transaction_value()
            if add_transaction(recipient, amount=amount):
                print("Added transaction!")
            else:
                print("Transaction failed \n")
            print(open_transactions)
        elif user_choice == '2':
            if mine_block():
                open_transactions = []
                save_data()
        elif user_choice == '3':
            print_blockchain_elements()
        elif user_choice == '4':
            print(participants)
        elif user_choice == '5':
            if verify_transactions():
                print("All transactions are valid")
            else:
                print("There are invalid transactions")
        elif user_choice == 'q':
            # This will lead to the loop to exist because it's running condition becomes False
            waiting_for_input = False
        else:
            print('Input was invalid, please pick a value from the list!')
        if not verify_chain():
            print_blockchain_elements()
            print('Invalid blockchain!')
            # Break out of the loop
            break
        print(f"Balance of {owner}: {get_balance(owner)}")
        print(get_balance('Johny'))
    else:
        print('User left!')


if __name__ == '__main__':
    menu()
