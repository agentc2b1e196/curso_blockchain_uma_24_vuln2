// Specifies the version of Solidity, using semantic versioning.
// Learn more: https://solidity.readthedocs.io/en/v0.5.10/layout-of-source-files.html#pragma
pragma solidity ^0.8.13;

contract Pseudoaleatoriedad {

    uint256 public constant THRESHOLD = 10; // different tests depending on threshold
    uint256 public r = 0; // for debugging/testing purpose
    string public message; // for debugging/testing purpose

    constructor(string memory initMessage) {
        // Accepts a string argument `initMessage` and sets the value into the contract's `message` storage variable).
        message = initMessage;
    }

    function update(string memory newMessage) public {
        string memory oldMsg = message;
        message = newMessage;
    }

    // function update threshold?

    // changed visibility to public to simulate attack vector
    // analogy to PoW. THRESHOLD similar to Difficulty parameter.
    // Difference: direct effect on the logic of the contract instead of consensus mechanism
    // Since block.number and block.timestamp can be known in advance, there is no difference in security
    function test_pseudorandomness_addr(address user) public {
        uint256 randomNumber = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        user
        ))));

        if (randomNumber < THRESHOLD) {
            string memory newMessage = "BROKEN";
            message = newMessage;
        } else {
            string memory newMessage = "Hello World";
            message = newMessage;
        }
        r = randomNumber;
    }

    function test_pseudorandomness(address user) public {
        uint256 randomNumber = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp,
                        user
        ))));

        if (randomNumber < THRESHOLD) {
            string memory newMessage = "BROKEN";
            message = newMessage;
        } else {
            string memory newMessage = "Hello World";
            message = newMessage;
        }
        r = randomNumber;
    }

    function read_message() public returns (string memory) {
        return message;
    }

    function read_number() public returns (uint256) {
        return r;
    }

}
