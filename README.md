# IoT-Device-Registry-Smart-Contract---Ethereum-Blockchain
IoT Device Registry Smart Contract - A decentralized application for securely managing devices and data on the blockchain.

The DeviceRegistry Smart Contract is a Solidity smart contract that allows users to register and manage devices, and store and retrieve data from these devices. The contract includes the following features:

1.User Registration: The contract allows the contract owner to register users, who can then add and manage their devices.

2.Device Registration: Users can register their devices by adding the device's address to the contract. Each device is associated with a unique ID and the   device's address is verified during registration.

3.Device Management: Users can manage their devices by updating the device's three variables, and viewing the history of these variables. The contract also   supports device removal.

4.Data Management: The contract stores historical data for each device, including the timestamp and values of the three variables. Users can retrieve this   data for a specified device.

5.Access Control: The contract includes access control mechanisms to ensure that only registered users can add or manage devices, and only the contract       owner can register or remove users.



+------------------+          +----------------------+            +-----------------------+
|       Owner      |          |         User         |            |        Device         |
+------------------+          +----------------------+            +-----------------------+
| - addUser        |          | - addDevice          |            | - setDeviceVariables  |
| - removeUser     |          | - removeDevice       |            |                       |
| - getUsers       |          | - getDeviceVariables |            |                       |
|                  |          | - getUserDevices     |            |                       |
+------------------+          +----------------------+            +-----------------------+
                              | - viewDeviceHistory  | 
                              +----------------------+
                              
The Python script periodically monitors a device's system resources, specifically CPU usage, CPU temperature, and RAM usage, and updates these values as variables in a smart contract on a local Ethereum Hardhat node. The script relies on the web3.py library to interact with the Ethereum blockchain and the psutil library to collect system information.

The script first establishes a connection with the local Hardhat Ethereum node and initializes the Device Registry smart contract using the ABI and contract address. It then continuously monitors the system resources every 10 seconds. For each iteration, the script gathers the CPU usage as a percentage, the CPU temperature in Celsius, and the RAM usage as a percentage, and sends a transaction to the smart contract to update the device variables with these values.

This allows the device to maintain an up-to-date record of its system resources on the Ethereum blockchain, enabling users to track the device's performance over time through the smart contract.

