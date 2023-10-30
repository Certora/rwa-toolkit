// Verification of Transferer contract using dispatcher
methods {
    function balanceA() external returns (uint256) envfree;
    function balanceB() external returns (uint256) envfree;

    // ERC20 summary
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.transfer(address, uint256) external => DISPATCHER(true);
    function _.transferFrom(address, address, uint256) external => DISPATCHER(true);
}


/// @title Integrity of `transferAtoB` (w.r.t. current contract)
rule transferIntegrity(uint256 amount) {
    mathint preA = balanceA();
    mathint preB = balanceB();

    require preA + amount <= max_uint256;

    env e;
    require e.msg.sender != currentContract;
    transferAtoB(e, amount);
    
    mathint postA = balanceA();
    mathint postB = balanceB();

    assert postA - preA == to_mathint(amount);
    assert preB - postB == to_mathint(amount);
}
