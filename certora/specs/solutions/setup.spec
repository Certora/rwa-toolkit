/**
 * # Setup for RwaUrn2 using linking
 */
using AAVE as _AAVE;


methods {
    function gemJoin() external returns (address) envfree;
    function AAVE.allowance(address, address) external returns (uint256) envfree;
}


rule reachability(method f) {
    env e;
    calldataarg args;
    f(e, args);
    satisfy true;
}


/**
 * @title Proves `lock` followed by `free` returns to original state almost
 * The only exception being the allowances that were modified.
 */
rule freeInvertsLock(uint256 wad) {
    storage initial = lastStorage;
    env e;

    uint256 senderAllowance = _AAVE.allowance(e.msg.sender, currentContract);
    uint256 thisAllowance = _AAVE.allowance(currentContract, gemJoin());
    
    lock(e, wad);
    free(e, wad);
    
    // Restore allowances to initial state
    _AAVE.approve(e, currentContract, senderAllowance);

    env eCur;  // An `env` where the sender is the current contract
    require eCur.msg.sender == currentContract;
    _AAVE.approve(eCur, gemJoin(), thisAllowance);

    storage final = lastStorage;
    assert initial == final;
}
