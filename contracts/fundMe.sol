// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    address public owner;
    address[] public funders;
    AggregatorV3Interface public priceFeed;
    mapping(address => uint256) public addressToFund;

    constructor(address _pricefeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_pricefeed);
    }

    function fund() public payable {
        uint256 minFund = 50 * 10**18; // Minumum fund of $50
        require(getConversionRate(msg.value) >= minFund, "Insufficient funds!");
        addressToFund[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        return uint256(answer * 10000000000);
    }

    function getConversionRate(uint256 ethAmt) public view returns (uint256) {
        uint256 ethRate = getPrice();
        uint256 ethAmtInUSD = (ethRate * ethAmt) / 1000000000000000000;
        return ethAmtInUSD;
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (uint256 i = 0; i < funders.length; i++) {
            addressToFund[funders[i]] = 0;
        }
        funders = new address[](0);
    }
}
