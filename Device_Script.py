import json
from brownie import (
    accounts,
    network,
    Contract,
)
from eth_account import Account

import psutil
import time

from web3 import Web3, HTTPProvider

# Configuration
http_provider_url = "http://127.0.0.1:8545"  # Replace with your HTTP provider URL
private_key = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"  # Replace with your private key
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Replace with your contract address

function_name = "setDeviceVariables"  # Replace with the function you want to call

abi_json_string ="""
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "deviceAddress",
				"type": "address"
			}
		],
		"name": "addDevice",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			}
		],
		"name": "addUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "deviceAddress",
				"type": "address"
			}
		],
		"name": "removeDevice",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			}
		],
		"name": "removeUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "variable1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable3",
				"type": "uint256"
			}
		],
		"name": "setDeviceVariables",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "data",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable3",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "dataByDevices",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "devices",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "deviceAddress",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "variable1",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable2",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "variable3",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "devicesByUser",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "deviceAddress",
				"type": "address"
			}
		],
		"name": "getData",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "timestamp",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "variable1",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "variable2",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "variable3",
						"type": "uint256"
					}
				],
				"internalType": "struct DeviceRegistry.Data[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "deviceAddress",
				"type": "address"
			}
		],
		"name": "getDeviceVariables",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getUserDevices",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "id",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "deviceAddress",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "variable1",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "variable2",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "variable3",
						"type": "uint256"
					}
				],
				"internalType": "struct DeviceRegistry.Device[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getUsers",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "userAddress",
						"type": "address"
					}
				],
				"internalType": "struct DeviceRegistry.User[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "users",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]"""

def get_cpu_usage():
    return int(psutil.cpu_percent())

def get_cpu_temperature():
    temps = psutil.sensors_temperatures()
    for name, entries in temps.items():
        if "core" in name.lower():
            return int(entries[0].current)
    return 0

def get_ram_usage():
    ram_info = psutil.virtual_memory()
    return int(ram_info.percent)
while True:
	variable1 = get_cpu_usage()
	variable2 = get_cpu_temperature()
	variable3 = get_ram_usage()
	variables = (variable1, variable2, variable3)  # Replace with your function's arguments

	w3 = Web3(HTTPProvider(http_provider_url))

	# Load the contract using the ABI and address
	abi = json.loads(abi_json_string)


	contract = w3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=abi)

	# Import the private key and create an account with it
	eth_account = Account.from_key(private_key)

	transaction_data = {
		"from": eth_account.address,
		"gas": 1000000,
		"gasPrice": w3.toWei("50", "gwei"),
		"nonce": w3.eth.getTransactionCount(eth_account.address),
	}

	transaction = contract.functions.setDeviceVariables(variable1, variable2, variable3).buildTransaction(transaction_data)
	signed_transaction = eth_account.signTransaction(transaction)
	transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
	
	print(f"CPU Usage: {variable1}%, CPU Temperature: {variable2}°C, RAM Usage: {variable3}%")
	print(f"Transaction sent with hash: {transaction_hash.hex()}")
	time.sleep(10)