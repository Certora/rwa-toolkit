pragma solidity ^0.8.0;


interface IERC20 {
  function balanceOf(address user) external view returns (uint256);
}


contract Voting {

  mapping(address => bool) internal _hasVoted;

  uint256 public votesInFavor;
  uint256 public votesAgainst;
  uint256 public totalVotes;
  
  address public immutable tokenA;
  address public immutable tokenB;

  constructor (
    address _tokenA,
    address _tokenB
  ) {
    tokenA = _tokenA;
    tokenB = _tokenB;
  }

  function balances(address user) internal view returns (uint256, uint256) {
    return (
      IERC20(tokenA).balanceOf(user),
      IERC20(tokenB).balanceOf(user)
    );
  }

  function votingPower(address user) public view returns (uint256) {
    uint256 balanceA;
    uint256 balanceB;
    (balanceA, balanceB) = balances(user);
    return balanceA + balanceB;
  }

  function vote(bool isInFavor) public {
    require(!_hasVoted[msg.sender]);
    _hasVoted[msg.sender] = true;
    
    uint256 power = votingPower(msg.sender);
    require(power > 0);

    totalVotes += 1;
    if (isInFavor) {
      votesInFavor += power;
    } else {
      votesAgainst += power;
    }
  }
}
