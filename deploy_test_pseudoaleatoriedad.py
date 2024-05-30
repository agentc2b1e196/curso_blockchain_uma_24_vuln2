import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from eth_tester import EthereumTester, PyEVMBackend
from solcx import compile_source, install_solc, set_solc_version
from eth_account import Account

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   install_solc("0.8.13");
   set_solc_version('0.8.13');
   return compile_source(source,output_values=['abi','bin'])


def deploy_test_contract(w3, contract_interface):
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    constr = contract.constructor('Hello World')
    tx_hash = constr.transact()

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address

def test_transaction(address):
    contract = w3.eth.contract(address=address, abi=contract_interface["abi"])
    print("Sending transaction to update 2\n")
    tx_hash = contract.functions.update("Hello World 2").transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    pprint.pprint(dict(receipt))

def read_msg_transaction(address):
    contract = w3.eth.contract(address=address, abi=contract_interface["abi"])
    print("Sending transaction to read message\n")
    tx_hash = contract.functions.read_message().transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    pprint.pprint(dict(receipt))

def send_eth(sender_sk, sender_addr, destination):
    #accounts = w3.eth.accounts
    #sender = accounts[0]

    #web3.providers.eth_tester
    #eth_tester = w3.providers[0].ethereum_tester
    #eth_tester_account_private_keys = eth_tester.backend.account_keys
    #private_key = eth_tester_account_private_keys[0]
    #print(f"Private key of account[0]: {private_key.to_hex()}")

    #account_from_private_key = Account.from_key(private_key)
    #sender = account_from_private_key.address

    initial_balance_sender = w3.eth.get_balance(sender_addr)
    initial_balance_recipient = w3.eth.get_balance(destination)
    #print(f"Initial balance of sender: {w3.from_wei(initial_balance_sender, 'ether')} ETH")
    #print(f"Initial balance of recipient: {w3.from_wei(initial_balance_recipient, 'ether')} ETH")

    amount = w3.to_wei(100, 'ether')

    # Create a transaction
    tx = {
        'from': sender_addr,
        'to': destination,
        'value': amount,
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(sender_addr),
    }

    # Sign the transaction with the sender's private key
    signed_tx = w3.eth.account.sign_transaction(tx, sender_sk)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(f"Transaction hash: {tx_receipt.transactionHash.hex()}")

    final_balance_sender = w3.eth.get_balance(sender_addr)
    final_balance_recipient = w3.eth.get_balance(destination)
    #print(f"Final balance of sender: {w3.from_wei(final_balance_sender, 'ether')} ETH")
    #print(f"Final balance of recipient: {w3.from_wei(final_balance_recipient, 'ether')} ETH")

#w3 = Web3(EthereumTesterProvider(PyEVMBackend()))

eth_tester = EthereumTester(backend=PyEVMBackend())
provider = EthereumTesterProvider(eth_tester)
w3 = Web3(provider)
backend = eth_tester.backend

if not w3.is_connected():
    raise Exception("Failed to connect")

contract_source_path = 'Pseudoaleatoriedad.sol'
compiled_sol = compile_source_file('Pseudoaleatoriedad.sol')

contract_id, contract_interface = compiled_sol.popitem()

address = deploy_test_contract(w3, contract_interface)
print(f'Deployed test contract {contract_id} to: {address}\n')

test_transaction(address)
#read_msg_transaction(address)
contract = w3.eth.contract(address=address, abi=contract_interface["abi"])
print(contract.functions.read_message().call())
print(contract.functions.read_number().call())

new_account = Account.create()
private_key = new_account._private_key.hex()
public_address = new_account.address


sender_sk = backend.account_keys[0]
sender_account = Account.from_key(sender_sk)
sender_addr = sender_account.address

send_eth(sender_sk, sender_addr, public_address)


#address = w3.personal.newAccount('the-passphrase')
contract.functions.test_pseudorandomness(public_address).call()
print(contract.functions.read_message().call())
print(contract.functions.read_number().call())


for i in range(100):
    #new_account = Account.create()
    #private_key = new_account._private_key.hex()
    #public_address = new_account.address
    #print(public_address)
    #address = w3.personal.newAccount('the-passphrase')
    #contract.functions.test_pseudorandomness(public_address).call()
    new_account = Account.create()
    private_key = new_account._private_key.hex()
    public_address = new_account.address
    send_eth(sender_sk, sender_addr, public_address)
    tx = contract.functions.test_pseudorandomness(public_address).build_transaction({
        'from': public_address,
        'nonce': w3.eth.get_transaction_count(public_address),
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    #tx_hash = contract.functions.test_pseudorandomness(public_address).transact({'from': public_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(contract.functions.read_message().call())
    print(contract.functions.read_number().call())



#gas_estimate = store_var_contract.functions.setVar(255).estimate_gas()
#print(f'Gas estimate to transact with setVar: {gas_estimate}')

#if gas_estimate < 100000:
#     print("Sending transaction to setVar(255)\n")
#     tx_hash = store_var_contract.functions.setVar(255).transact()
#     receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
#     print("Transaction receipt mined:")
#     pprint.pprint(dict(receipt))
#     print("\nWas transaction successful?")
#     pprint.pprint(receipt["status"])
#else:
#     print("Gas cost exceeds 100000")
