// Specifies the version of Solidity, using semantic versioning.
// Learn more: https://solidity.readthedocs.io/en/v0.5.10/layout-of-source-files.html#pragma

// Simplificado (una consulta) de https://docs.chain.link/vrf/v2/direct-funding/examples/get-a-random-number
pragma solidity ^0.8.13;

import {VRFV2WrapperConsumerBase} from "./node_modules/@chainlink/contracts/src/v0.8/vrf/VRFV2WrapperConsumerBase.sol";
import {LinkTokenInterface} from "./node_modules/@chainlink/contracts/src/v0.8/shared/interfaces/LinkTokenInterface.sol";

abstract contract PseudoaleatoriedadSol is VRFV2WrapperConsumerBase{

    uint256 public constant THRESHOLD = 10; // different tests depending on threshold
    uint256 public r = 0; // for debugging/testing purpose
    string public message; // for debugging/testing purpose
    uint32 callbackGasLimit = 100000;

    struct RequestStatus {
        uint256 paid; // amount paid in link
        bool fulfilled; // whether the request has been successfully fulfilled
        uint256[] randomWords;
    }

    event RequestSent(uint32 numWords);

    // Address LINK - hardcoded for Sepolia
    address linkAddress = 0x779877A7B0D9E8603169DdbD7836e478b4624789;
    // address WRAPPER - hardcoded for Sepolia
    address wrapperAddress = 0xab18414CD93297B0d12ac29E63Ca20f515b3DB46;

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

    function test_randomness_oracle(address user) public {
        uint256[] memory randomWords;
        RequestStatus({
            paid: VRF_V2_WRAPPER.calculateRequestPrice(callbackGasLimit),
            randomWords: new uint256[](0),
            fulfilled: false
        });
        emit RequestSent(1);
        // Confirma transacción manualmente...
        // y espera un momento a que el oráculo haga su magia
        uint256 randomNumber = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(randomWords[0],user)
                )
            )
        );

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
