genesis_block = {
        "previous_hash": "",
        "index": 0,
        "transactions": []
    }

blockchain = [genesis_block]
open_transactions = []
owner = "Johny"
participants = {"Johny"}


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def get_transaction_value():
    tx_recipient = input("Enter recipient: ")
    tx_amount = float(input("Enter amount to sent"))
    return tx_recipient, tx_amount


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block["transactions"] if tx['sender'] == participant] for block in blockchain]
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    tx_recipient = [[tx['amount'] for tx in block["transactions"] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions
    }
    blockchain.append(block)
    return True


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def menu():
    global open_transactions
    waiting_for_input = True
    while waiting_for_input:
        print('Please choose')
        print('1: Add a new transaction value')
        print('2: Mine a new block')
        print('3: Output the blockchain blocks')
        print('4: Output participants')
        print('h: Manipulate the chain')
        print('q: Quit')
        user_choice = get_user_choice()
        if user_choice == '1':
            recipient, amount = get_transaction_value()
            add_transaction(recipient, amount=amount)
            print(open_transactions)
        elif user_choice == '2':
            if mine_block():
                open_transactions = []
        elif user_choice == '3':
            print_blockchain_elements()
        elif user_choice == '4':
            print(participants)
        elif user_choice == 'h':
            # Make sure that you don't try to "hack" the blockchain if it's empty
            if len(blockchain) >= 1:
                blockchain[0] = {
                    'previous_hash': '',
                    'index': 0,
                    'transactions': [{'sender': 'Chris', 'recipient': 'Max', 'amount': 100.0}]
                }
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
        print(get_balance('Johny'))
    else:
        print('User left!')


if __name__ == '__main__':
    menu()
