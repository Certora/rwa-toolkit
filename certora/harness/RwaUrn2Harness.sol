// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity 0.6.12;

import {RwaUrn2} from "../../src/urns/RwaUrn2.sol";
import {DSTokenAbstract} from "dss-interfaces/dapp/DSTokenAbstract.sol";

/**
 * @dev Harness to expose gem.allowance and gem.approve
 */
contract RwaUrn2Harness is RwaUrn2 {

  constructor(
    address vat_,
    address jug_,
    address gemJoin_,
    address daiJoin_,
    address outputConduit_
  ) RwaUrn2(vat_, jug_, gemJoin_, daiJoin_, outputConduit_) public {
  }
  
  function gemBalanceOf(address src) public view returns (uint256) {
    return DSTokenAbstract(gemJoin.gem()).balanceOf(src);
  }
}
