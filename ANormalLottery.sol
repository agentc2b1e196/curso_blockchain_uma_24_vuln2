// Specifies the version of Solidity, using semantic versioning.
pragma solidity ^0.8.13;

contract ANormalLottery {

    // Emitted when update function is called
    event UpdatedMessages(string oldStr, string newStr);

    uint256 public constant THRESHOLD = 128;
    uint256 public r = 0;

    // State variable `message` of type `string`, marked as `private`.
    mapping(address => string) public messages;

    // Mapping to keep track of the number of times each user has been awarded.
    mapping(address => uint256) public awardsCount;

    // Variables for tracking the normal distribution
    uint256 public totalAwards = 0;
    uint256 public sumOfAwards = 0;
    uint256 public sumOfSquaredDiffs = 0;

    // Logging variables for mean and standard deviation
    //uint256 public meanAwardCount = 0;
    //uint256 public standardDeviationAwardCount = 0;

    // Constructor to initialize the contract's data.
    constructor() {}

    function update(address user, string memory newMessage) public {
        string memory oldMsg = messages[user];
        messages[user] = newMessage;
        emit UpdatedMessages(oldMsg, newMessage);
    }

    // An internal function to generate a pseudo-random number, can be used by other functions within the contract.
    function generatePseudoRandom(address user) internal view returns (uint256) {
        return uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp,
                        user
                    )
                )
            )
        );
    }

    // A public function to test pseudo-randomness and update normal distribution.
    function lottery(address user) public {
        uint256 randomNumber = generatePseudoRandom(user);

        // Check if the user is above the threshold
        if (randomNumber < THRESHOLD && !isAboveThreshold(user)) {
            uint256 currentCount = awardsCount[user];
            uint256 newCount = currentCount + 1;

            // Update the message to "W"
            messages[user] = "W";
            
            // Update the awards count for the user
            awardsCount[user] = newCount;

            // Update the normal distribution parameters
            updateStatistics(user, newCount);
        } else {
            messages[user] = "Hello Lottery World";
        }
        r = randomNumber;
    }

    // Update the statistics for the normal distribution using Welford's online algorithm
    //function updateStatistics(uint256 newCount) internal {
    //    totalAwards++;
    //    uint256 delta = newCount - mean();
    //    sumOfAwards += newCount;
    //    sumOfSquaredDiffs += delta * (newCount - mean());
    //}

    // Update the statistics for the normal distribution using Welford's online algorithm
    function updateStatistics(address user, uint256 newCount) internal {
        totalAwards++;
        
        // Calculate delta for Welford's algorithm
        uint256 currentMean = sumOfAwards / totalAwards;
        uint256 delta = newCount - currentMean;

        // Update sums
        sumOfAwards += delta;
        sumOfSquaredDiffs += delta * (newCount - currentMean);
    }

    // Calculate the mean of the awards
    function mean() public view returns (uint256) {
        return totalAwards > 0 ? sumOfAwards / totalAwards : 0;
    }

    // Calculate the variance of the awards
    function variance() public view returns (uint256) {
        return totalAwards > 1 ? sumOfSquaredDiffs / (totalAwards - 1) : 0;
    }

    // Calculate the standard deviation of the awards
    function standardDeviation() public view returns (uint256) {
        return sqrt(variance());
    }

    // A public view function to read the message.
    function readMessage(address user) public view returns (string memory) {
        return messages[user];
    }

    // A public view function to read the number `r`.
    function readNumber() public view returns (uint256) {
        return r;
    }

    // A public view function to read the award count of a user.
    function getAwardsCount(address user) public view returns (uint256) {
        return awardsCount[user];
    }

    // A public function to check if a user is above the threshold
    function isAboveThreshold(address user) public view returns (bool) {
        uint256 userCount = awardsCount[user];
        return userCount > (mean() + 2 * standardDeviation());
    }

    // Function to calculate square root
    function sqrt(uint256 x) internal pure returns (uint256 y) {
        uint256 z = (x + 1) / 2;
        y = x;
        while (z < y) {
            y = z;
            z = (x / z + z) / 2;
        }
    }
}
