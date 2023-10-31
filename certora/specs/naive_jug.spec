/**
 * # Jug spec - a naive example
 *
 * Notes
 * - It is better to expose `ONE()` using harness than using the `RAY_CVL()` definition
 *   below, as exposing it will be more stable under code changes.
 */
using Vat as _vat;


methods {
    function ilks(bytes32) external returns (uint256, uint256) envfree;

    function Vat.ilks(bytes32) external returns (
        uint256, uint256, uint256, uint256, uint256
    ) envfree;
}


definition RAY_CVL() returns uint256 = 10^27; // Better to expose `ONE` using harness


/// @title Rate is monotonically increasing
rule rateCheck(env e, bytes32 ilk) {
    uint256 duty;
    duty, _ = ilks(ilk);
    require duty >= RAY_CVL();
    
    uint256 rateBefore;
    _, rateBefore, _, _, _ = _vat.ilks(ilk);

    drip(e, ilk);

    uint256 rateAfter;
    _, rateAfter, _, _, _ = _vat.ilks(ilk);

    assert rateBefore <= rateAfter, "Rate monotonically increases";
}


/** @title To see an actual example of the rate calculation
 *  Mainly to see that the summary works well.
 */
rule rateExample(env e, bytes32 ilk) {
    uint256 duty;
    duty, _ = ilks(ilk);
    require duty >= RAY_CVL();
    
    uint256 rateBefore;
    _, rateBefore, _, _, _ = _vat.ilks(ilk);

    drip(e, ilk);

    uint256 rateAfter;
    _, rateAfter, _, _, _ = _vat.ilks(ilk);

    satisfy rateBefore <= rateAfter;
}
