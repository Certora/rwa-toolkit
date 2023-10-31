/**
 * # Simple voting spec - examples of view summaries
 *
 */

methods
{
    function votesInFavor() external returns (uint256) envfree;
    function votesAgainst() external returns (uint256) envfree;
    function totalVotes() external returns (uint256) envfree;

    // Always summary.
    // We want to summarize the internal function.
    function votingPower(address user) internal returns (uint256) => ALWAYS(2);
}


/// @title Integrity of `vote` method
rule voteIntergrity(bool isInFavor) {

    uint256 preInFavor = votesInFavor();
    uint256 preAgainst = votesAgainst();
    uint256 preTotal = totalVotes();

    env e;
    vote(e, isInFavor);

    assert (
        (isInFavor => votesInFavor() > preInFavor) &&
        (!isInFavor => votesAgainst() > preAgainst)
    );
    assert totalVotes() > preTotal, "Total votes must increase";
    assert votingPower(e, e.msg.sender) > 0;
}


/// @title Example of vote
rule voteExample(bool isInFavor) {

    env e;
    vote(e, isInFavor);

    satisfy votingPower(e, e.msg.sender) > 0;
}
