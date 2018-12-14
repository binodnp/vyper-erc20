# Token Timelock
# Contributors: Binod Nirvan
# This file is released under Apache 2.0 license.
# @dev TokenTimelock is a token holder contract that will allow a
# beneficiary to extract the tokens after a given release time
# Ported from Open Zeppelin
# https://github.com/OpenZeppelin
# 
# See https://github.com/OpenZeppelin
# Open Zeppelin tests ported: TokenTimelock.test.js


#@dev Features referenced by this contract
contract TokenContract:
    def balanceOf(_owner: address) -> uint256: constant
    def transfer(_to: address, _value: uint256) -> bool: modifying

# ERC20 basic token contract being held
token: address

#beneficiary of tokens after they are released
beneficiary: public(address)

#timestamp when token release is enabled
releaseTime: public(timestamp)

@public
def __init__(_token: address, _beneficiary: address, _releaseTime: timestamp):
    """
    @notice Initializes this contract.
    @param _token The address of the ERC20 token to create a timelock.
    @param _beneficiary The wallet address of the beneficiary who will receive the token after the release time.
    @param _releaseTime The timestamp on which the token timelock will end.
    """

    assert _releaseTime > block.timestamp, "Invalid value for release time."
    self.token = _token
    self.beneficiary = _beneficiary
    self.releaseTime = _releaseTime

@public
def release():
    """
    @notice Transfers tokens held by timelock to beneficiary.
    """

    assert msg.sender == self.beneficiary, "Access is denied."
    assert block.timestamp >= self.releaseTime, "Access is denied. It's too early to withdraw your tokens."

    amount : uint256 = TokenContract(self.token).balanceOf(self)
    assert amount > 0, "Nothing to withdraw."

    assert TokenContract(self.token).transfer(self.beneficiary, amount), "Sorry but the transaction was reverted due to an unknown error."
