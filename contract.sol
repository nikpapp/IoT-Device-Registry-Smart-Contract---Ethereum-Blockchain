pragma solidity ^0.8.0;

contract DeviceRegistry {
    address public owner;

    // Define the User and Device structs
    struct User {
        string name;
        address userAddress;
    }

    struct Device {
        uint256 id;
        string name;
        address deviceAddress;
        uint256 variable1;
        uint256 variable2;
        uint256 variable3;
    }

    struct Data {
        uint256 timestamp;
        uint256 variable1;
        uint256 variable2;
        uint256 variable3;
    }

    // Define the users and devices arrays and the devicesByUser mapping
    User[] public users;
    Device[] public devices;
    Data[] public data;
    mapping (address => uint256[]) public devicesByUser;
    mapping (address => uint256[]) public dataByDevices;

    // Define the onlyOwner modifier
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can call this function.");
        _;
    }

    // Define the onlyUser modifier
    modifier onlyUser() {
        bool isUser = false;
        for (uint256 i = 0; i < users.length; i++) {
            if (users[i].userAddress == msg.sender) {
                isUser = true;
                break;
            }
        }
        require(isUser, "Only registered users can call this function.");
        _;
    }

    // Define the constructor to set the contract owner
    constructor() {
        owner = msg.sender;
    }

    // Define the addUser function to allow the owner to add a user
    function addUser(address userAddress, string memory name) public onlyOwner {
        // Create a new User struct and add it to the users array
        User memory newUser = User(name, userAddress);
        users.push(newUser);
    }

    // Define the removeUser function to allow the owner to remove a user
    function removeUser(address userAddress) public onlyOwner {
        // Find the user with the specified address
        for (uint256 i = 0; i < users.length; i++) {
            if (users[i].userAddress == userAddress) {
                // Remove the user from the users array by swapping with the last element and then reducing the array length
                uint256 lastIndex = users.length - 1;
                users[i] = users[lastIndex];
                users.pop();
                break;
            }
        }

        // Remove all devices associated with the user from the devicesByUser mapping and devices array
        uint256[] storage deviceIds = devicesByUser[userAddress];
        for (uint256 i = 0; i < deviceIds.length; i++) {
            uint256 deviceId = deviceIds[i];
            for (uint256 j = 0; j < devices.length; j++) {
                if (devices[j].id == deviceId) {
                    // Remove the device from the devices array by swapping with the last element and then reducing the array length
                    uint256 lastIndex = devices.length - 1;
                    devices[j] = devices[lastIndex];
                    devices.pop();
                    break;
                }
            }
        }
        delete devicesByUser[userAddress];
    }

// Define the addDevice function to allow users to add a device
    function addDevice(address deviceAddress) public onlyUser {
        uint256 deviceId;
        // Check if the device has already been added by the user
        for (uint256 i = 0; i < devicesByUser[msg.sender].length; i++) {
            deviceId = devicesByUser[msg.sender][i];
            if (devices[deviceId - 1].deviceAddress == deviceAddress) {
                revert("Device has already been added by the user.");
            }
        }

        // Create a new Device struct and add it to the devices array
        Device memory newDevice = Device(devices.length + 1, "", deviceAddress, 0, 0, 0);
        devices.push(newDevice);

        // Associate the device with the user by adding the device ID to the devicesByUser mapping
        deviceId = devices.length;
        devicesByUser[msg.sender].push(deviceId);
    }

// Define the removeDevice function to allow users to remove a device
    function removeDevice(address deviceAddress) public onlyUser {
        uint256 deviceIndex = 0;
        bool deviceFound = false;

        // Find the device with the specified address
        for (uint256 i = 0; i < devicesByUser[msg.sender].length; i++) {
            uint256 deviceId = devicesByUser[msg.sender][i];
            if (devices[deviceId - 1].deviceAddress == deviceAddress) {
                deviceIndex = i;
                deviceFound = true;
                break;
            }
        }

        // Remove the device from the devicesByUser mapping and devices array if found
        if (deviceFound) {
            uint256 deviceId = devicesByUser[msg.sender][deviceIndex];

            // Remove the device ID from the devicesByUser mapping
            uint256 lastIndex = devicesByUser[msg.sender].length - 1;
            devicesByUser[msg.sender][deviceIndex] = devicesByUser[msg.sender][lastIndex];
            devicesByUser[msg.sender].pop();

            // Remove the device from the devices array by swapping with the last element and then reducing the array length
            lastIndex = devices.length - 1;
            devices[deviceId - 1] = devices[lastIndex];
            devices.pop();
        }
    }
    // Define the setDeviceVariables function to allow a device to change its three variables
    function setDeviceVariables(uint256 variable1, uint256 variable2, uint256 variable3) public {
        uint256 deviceId = getDeviceId(msg.sender);

        // Check if the calling address is a device
        bool isDevice = false;
        for (uint256 i = 0; i < devices.length; i++) {
            if (devices[i].deviceAddress == msg.sender) {
                isDevice = true;
                break;
            }
        }
        require(isDevice, "Only devices can call this function.");

        // Update the device's variables if it matches the calling device
        if (devices[deviceId - 1].deviceAddress == msg.sender) {
            devices[deviceId - 1].variable1 = variable1;
            devices[deviceId - 1].variable2 = variable2;
            devices[deviceId - 1].variable3 = variable3;

            // Add the new data to the device's history if it matches the calling device
            uint256 timestamp = block.timestamp;
            Data memory newData = Data(timestamp, variable1, variable2, variable3);
            data.push(newData);
            dataByDevices[msg.sender].push(data.length);
        }
    }

    // Internal function to get the ID of the device calling the function
    function getDeviceId(address deviceAddress) internal view returns (uint256) {
        uint256 deviceId = 0;

        for (uint256 i = 0; i < devices.length; i++) {
            if (devices[i].deviceAddress == deviceAddress) {
                deviceId = devices[i].id;
                break;
            }
        }

        require(deviceId > 0, "Only devices can call this function.");
        return deviceId;
    }

    // Define the getDeviceVariables function to allow a user to read the variables of a device associated with their account
    function getDeviceVariables(address deviceAddress) public view onlyUser returns (uint256, uint256, uint256) {
        uint256 deviceId = getDeviceId(deviceAddress);

        // Get the device's variables if it matches a device associated with the calling user
        if (devicesByUser[msg.sender].length > 0) {
            for (uint256 i = 0; i < devicesByUser[msg.sender].length; i++) {
                if (devices[devicesByUser[msg.sender][i] - 1].id == deviceId) {
                    return (devices[deviceId - 1].variable1, devices[deviceId - 1].variable2, devices[deviceId - 1].variable3);
                }
            }
        }

        // Return zeros if the device is not associated with the calling user
        return (0, 0, 0);
    }

    //Define the getData function to allow a user to retrieve the history of a device's variables
    function getData(address deviceAddress) public view onlyUser returns (Data[] memory) {
        uint256 deviceId = getDeviceId(deviceAddress);
        uint256[] storage dataIds = dataByDevices[deviceAddress];
        Data[] memory deviceData = new Data[](dataIds.length);

        for (uint256 i = 0; i < dataIds.length; i++) {
            uint256 dataIndex = dataIds[i] - 1;
            deviceData[i] = data[dataIndex];
        }

        return deviceData;
    }

    // Define the getUserDevices function to allow a user to retrieve all the devices associated with their account
    function getUserDevices() public view onlyUser returns (Device[] memory) {
        uint256[] storage deviceIds = devicesByUser[msg.sender];
        Device[] memory userDevices = new Device[](deviceIds.length);

        for (uint256 i = 0; i < deviceIds.length; i++) {
            uint256 deviceId = deviceIds[i];
            userDevices[i] = devices[deviceId - 1];
        }

        return userDevices;
    }

    // Define the getUsers function to allow the contract owner to retrieve all the available users
    function getUsers() public view onlyOwner returns (User[] memory) {
        return users;
    }


}

