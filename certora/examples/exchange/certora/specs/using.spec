// Verification of Transferer contract
using ERC20DummyA as _ERC20DummyA;
using ERC20DummyB as _ERC20DummyB;


methods {
    function ERC20DummyA.balanceOf(address) external returns (uint256) envfree;
    function ERC20DummyB.balanceOf(address) external returns (uint256) envfree;
}


/// @title Integrity of `transferAtoB` (w.r.t. current contract)
rule transferIntegrity(uint256 amount) {

    mathint preA = _ERC20DummyA.balanceOf(currentContract);
    mathint preB = _ERC20DummyB.balanceOf(currentContract);

    require preA + amount <= max_uint256;

    env e;
    require e.msg.sender != currentContract;
    transferAtoB(e, amount);
    
    mathint postA = _ERC20DummyA.balanceOf(currentContract);
    mathint postB = _ERC20DummyB.balanceOf(currentContract);

    assert postA - preA == to_mathint(amount);
    assert preB - postB == to_mathint(amount);
}
