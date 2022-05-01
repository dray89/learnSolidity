// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";


contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public usdEntryFee;
    uint256 public randomness; 
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN, 
        CLOSED, 
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(bytes32 requestId);

    constructor(address _priceFeedAddress, 
                address _vrfCoordinator, 
                address _link,
                uint256 _fee,
                bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link){
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }
        

    function enter() public payable {
        //$50 minimum
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), 'Not enough Ether');
        players.push(msg.sender);
    }  

    function getEntranceFee() public view returns(uint256) {
        (, int price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        // $50, $2000/Eth
        // 50 /2000
        // 50 * 10000/2000
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice; //additional 18 decimals
        return costToEnter; 

    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, 'CANNOT START A NEW LOTTERY YET');
        lottery_state = LOTTERY_STATE.OPEN;
    }
    function endLottery() public onlyOwner {
            lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
            bytes32 requestId = requestRandomness(keyhash, fee); //returns bytes32 request id
            emit RequestedRandomness(requestId)
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "YOU ARE NOT THERE YET");
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        //reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}