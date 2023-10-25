/**
 * # Setup for RwaUrn2 using dispatch and harness
 */
using Vat as _Vat;
using GemJoin as _GemJoin;
using DaiJoin as _DaiJoin;
using Dai as _Dai;

// Tokens
using AAVE as _AAVE;
using BAL as _BAL;
using BAT as _BAT;


methods {
    function gemJoin() external returns (address) envfree;
    function gemBalanceOf(address) external returns (uint256) envfree;

    function GemJoin.gem() external returns (address) envfree;

    function _.transferFrom(
        address, address, uint256
    ) external => DISPATCHER(true);
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
}


rule reachability(method f) {
    env e;
    calldataarg args;
    f(e, args);
    satisfy true;
}


/**
 * @title Proves `lock` followed by `free` returns relevant balances to original state
 * This uses the method `gemBalanceOf` defined in the harness `RwaUrn2Harness`.
 * @dev Using dispatch means that the `gem` token can also be `Dai`.
 */
rule freeInvertsLockWithHarness(uint256 wad, address thirdParty) {
    // NOTE: Using dispatch means that the `gem` token can also be `Dai`.
    require _GemJoin.gem() != _Dai;

    storage initial = lastStorage;
    env e;

    uint256 preBalance = gemBalanceOf(currentContract);
    uint256 preJoinBalance = gemBalanceOf(_GemJoin);
    uint256 preSenderBalance = gemBalanceOf(e.msg.sender);
    uint256 preThirdPartyBalance = gemBalanceOf(thirdParty);

    lock(e, wad);
    free(e, wad);
    
    storage final = lastStorage;

    assert initial[currentContract] == final[currentContract];
    assert initial[_Vat] == final[_Vat];
    assert initial[_GemJoin] == final[_GemJoin];
    assert initial[_DaiJoin] == final[_DaiJoin];

    // Balances comparison
    assert gemBalanceOf(currentContract) == preBalance;
    assert gemBalanceOf(_GemJoin) == preJoinBalance;
    assert gemBalanceOf(e.msg.sender) == preSenderBalance;

    // Third party balance comparison
    assert gemBalanceOf(thirdParty) == preThirdPartyBalance;
}
