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
    // `RwaUrn2`
    function gemJoin() external returns (address) envfree;
    function outputConduit() external returns (address) envfree;
    function gemBalanceOf(address) external returns (uint256) envfree;

    // `GemJoin`
    function GemJoin.gem() external returns (address) envfree;

    // `DaiJoin`
    function DaiJoin.mul(uint x, uint y) internal returns (uint) => mulSummary(x, y);

    // `Vat`
    function Vat._mul(uint x, uint y) internal returns (uint) => mulSummary(x, y);

    // `Jug`
    function Jug._rpow(
        uint x, uint n, uint b
    ) internal returns (uint) => rpowSummary(x, n, b);

    // `Dai`
    function Dai.balanceOf(address) external returns (uint) envfree;

    // Wild-card (for dispatching to different tokens)
    function _.transferFrom(
        address, address, uint256
    ) external => DISPATCHER(true);
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
}

// Summaries -------------------------------------------------------------------

/** @title Multiplication summary
 *  This is needed to avoid time-outs in `wipeInvertsDraw`.
 */
function mulSummary(uint x, uint y) returns uint {
    mathint result = x * y;
    uint z = require_uint256(result);
    return z;
}   


/** @title Summary of power calculation in fixed point
 *  Summarizes ((x / b) ^ n) * b), needed for `wipeInvertsDraw` below.
 */
function rpowSummary(uint x, uint n, uint b) returns uint {
    if (x == 0 && n > 0) {
        // 0^n = 0 for n != 0
        return 0;
    }

    // In all other cases the result must be at least b
    uint result;
    require result >= b;
    return result;
}


// Rules -----------------------------------------------------------------------

/// @title Check setup reachbility (sanity)
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


/**
 * @title Proves `draw` followed by `wipe` keeps some things unchanged
 * @dev Using dispatch means that the `gem` token can also be `Dai`.
 * @dev Some balances in `Dai` will be changed, as will `Vat.debt` and `Vat.ilks[-]`
 */
rule wipeInvertsDraw(uint256 wad, address thirdParty) {
    // Ensure `thirdParty` is not one of the main actors
    require (
        (thirdParty != currentContract) &&
        (thirdParty != _GemJoin.gem()) &&
        (thirdParty != outputConduit())
    );

    uint preBalance = _Dai.balanceOf(thirdParty);
    storage initial = lastStorage;
    env e;

    draw(e, wad);
    wipe(e, wad);
    
    storage final = lastStorage;
    assert initial[currentContract] == final[currentContract];
    assert initial[_GemJoin] == final[_GemJoin];
    assert initial[_DaiJoin] == final[_DaiJoin];

    // Third party Dai balance unchanged
    assert _Dai.balanceOf(thirdParty) == preBalance;
}
