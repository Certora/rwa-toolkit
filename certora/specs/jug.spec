/**
 * # Jug example spec
 *
 * Notes
 * - Using `optimistic_loop` here is wrong, since bounding the number of loop iterations
 *   here is an under-approximation. Instead we use a summary.
 * - Using a `NONDET` summary here is insufficient, since the result must be either zero
 *   or not less than `b` (the base). Anything else will result in a false violation.
 * - It is better to expose `ONE()` using harness than using the `RAY_CVL()` definition
 *   below, as exposing it will be more stable under code changes.
 */
using Vat as _vat;


methods {
    function ilks(bytes32) external returns (uint256, uint256) envfree;
    // In this case using `NONDET` is insufficient
    //function _rpow(uint, uint, uint) internal returns (uint) => NONDET;
    function _rpow(
        uint x, uint n, uint b
    ) internal returns (uint) => rpowSummary(x, n, b);

    function Vat.ilks(bytes32) external returns (
        uint256, uint256, uint256, uint256, uint256
    ) envfree;
}


definition RAY_CVL() returns uint256 = 10^27; // Better to expose `ONE` using harness


/** @title Summary of power calculation in fixed point
 *  Summarizes ((x / b) ^ n) * b)
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