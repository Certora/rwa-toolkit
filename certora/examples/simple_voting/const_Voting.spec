/**
 * # Simple voting spec - examples of view summaries
 *
 */

methods
{
    function votesInFavor() external returns (uint256) envfree;
    function votesAgainst() external returns (uint256) envfree;
    function totalVotes() external returns (uint256) envfree;

    function votingPower(address user) external returns (uint256) envfree;

    // Constant summary.
    function balances(address) internal returns (uint256, uint256) => CONSTANT;
}


/// @title Integrity of `vote` method
rule voteIntergrity(bool isInFavor) {

    uint256 preInFavor = votesInFavor();
    uint256 preAgainst = votesAgainst();
    uint256 preTotal = totalVotes();

    env e;
    uint256 vp = votingPower(e.msg.sender);
    vote(e, isInFavor);

    assert (
        (isInFavor => votesInFavor() > preInFavor) &&
        (!isInFavor => votesAgainst() > preAgainst)
    );
    assert totalVotes() > preTotal, "Total votes must increase";
    assert votingPower(e.msg.sender) > 0;
}


/// @title Example of vote
rule voteExample(bool isInFavor) {

    env e;
    vote(e, isInFavor);

    satisfy votingPower(e.msg.sender) > 0;
}