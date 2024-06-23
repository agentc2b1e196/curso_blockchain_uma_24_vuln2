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
    constr = contract.constructor()
    tx_hash = constr.transact()

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address

def test_transaction(address):
    contract = w3.eth.contract(address=address, abi=contract_interface["abi"])
    print("Sending transaction to update 2\n")
    tx_hash = contract.functions.update(address, "Hello Lottery World").transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    pprint.pprint(dict(receipt))

def read_msg_transaction(address):
    contract = w3.eth.contract(address=address, abi=contract_interface["abi"])
    print("Sending transaction to read message\n")
    tx_hash = contract.functions.readMessage(address).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    pprint.pprint(dict(receipt))

def send_eth(w3, sender_sk, sender_addr, destination, amount_ether=100):
    amount = w3.to_wei(amount_ether, 'ether')
    tx = {
        'from': sender_addr,
        'to': destination,
        'value': amount,
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(sender_addr),
    }
    signed_tx = w3.eth.account.sign_transaction(tx, sender_sk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

def test_lottery(w3, contract, public_address, private_key):
    tx = contract.functions.lottery(public_address).build_transaction({
        'from': public_address,
        'nonce': w3.eth.get_transaction_count(public_address),
        'gas': 2000000,
        'gasPrice': w3.to_wei('50', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    #tx_hash = contract.functions.lottery(public_address).transact({'from': public_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    #print(contract.functions.readMessage(public_address).call())
    #print(contract.functions.readNumber().call())
    message = contract.functions.readMessage(public_address).call()
    number = contract.functions.readNumber().call()
    #awards_count = contract.functions.getAwardsCount(public_address).call()
    mean = contract.functions.mean().call()
    variance = contract.functions.standardDeviation().call()
    stddev = int((variance) ** 0.5)
    
    print(f"Message: {message}")
    print(f"Random number: {number}")
    #print(f"Awards count for {public_address}: {awards_count}")
    print(f"Mean: {mean}, Variance: {variance}, Standard Deviation: {stddev}")

def test_win_lottery(w3, contract, public_address, private_key, iterations):
    for i in range(iterations):
        tx = contract.functions.lottery(public_address).build_transaction({
            'from': public_address,
            'nonce': w3.eth.get_transaction_count(public_address),
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        #tx_hash = contract.functions.lottery(public_address).transact({'from': public_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        #print(contract.functions.readMessage(public_address).call())
        #print(contract.functions.readNumber().call())
        message = contract.functions.readMessage(public_address).call()
        number = contract.functions.readNumber().call()
        #awards_count = contract.functions.getAwardsCount(public_address).call()
        mean = contract.functions.mean().call()
        variance = contract.functions.standardDeviation().call()
        stddev = int((variance) ** 0.5)
        
        print(f"Message: {message}")
        print(f"Random number: {number}")
        #print(f"Awards count for {public_address}: {awards_count}")
        print(f"Mean: {mean}, Variance: {variance}, Standard Deviation: {stddev}")

#w3 = Web3(EthereumTesterProvider(PyEVMBackend()))

eth_tester = EthereumTester(backend=PyEVMBackend())
provider = EthereumTesterProvider(eth_tester)
w3 = Web3(provider)
backend = eth_tester.backend

if not w3.is_connected():
    raise Exception("Failed to connect")

contract_source_path = 'ANormalLottery.sol'
compiled_sol = compile_source_file('ANormalLottery.sol')

contract_id, contract_interface = compiled_sol.popitem()

test_address = deploy_test_contract(w3, contract_interface)
print(f'Deployed test contract {contract_id} to: {test_address}\n')

test_transaction(test_address)
#read_msg_transaction(address)
contract = w3.eth.contract(address=test_address, abi=contract_interface["abi"])
print(contract.functions.readMessage(test_address).call())
print(contract.functions.readNumber().call())

new_account = Account.create()
private_key = new_account._private_key.hex()
public_address = new_account.address


sender_sk = backend.account_keys[0]
sender_account = Account.from_key(sender_sk)
sender_addr = sender_account.address

send_eth(w3, sender_sk, sender_addr, public_address)

#address = w3.personal.newAccount('the-passphrase')
contract.functions.lottery(public_address).call()
print(contract.functions.readMessage(public_address).call())
print(contract.functions.readNumber().call())

test_lottery(w3, contract, public_address, private_key)

test_win_lottery(w3, contract, public_address, private_key, 5)