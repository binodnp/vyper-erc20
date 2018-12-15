# TokenVesting
# Contributors: Binod Nirvan
# This file is released under Apache 2.0 license.
# @dev A token holder contract that can release its token balance gradually like a
# typical vesting scheme, with a cliff and vesting period. Optionally revocable by the
# owner.
# Ported from Open Zeppelin
# https://github.com/OpenZeppelin
# 
# See https://github.com/OpenZeppelin
# Open Zeppelin tests ported: TokenVesting.test.js, Ownable.test.js, Ownable.behaviour.js


#@dev Features referenced by this contract
contract TokenContract:
    def balanceOf(_owner: address) -> uint256: constant
    def transfer(_to: address, _value: uint256) -> bool: modifying

#OWNABLE
OwnershipRenounced: event({_previousOwner: indexed(address)})
OwnershipTransferred: event({_previousOwner: indexed(address), _newOwner: indexed(address)})

Released: event({_amount: uint256})
Revoked: event()

#OWNABLE
owner: public(address)

#beneficiary of tokens after they are released
beneficiary: public(address)
cliff: public(timedelta)
start: public(timestamp)
duration: public(timedelta)

revocable: public(bool)

released: public(map(address, uint256))
revoked: public(map(address, bool))


#OWNABLE
# This feature is ported from Open Zeppelin. 
# The ownable feature provides basic authorization control functions 
# and simplifies the implementation of "user permissions".

@public
def renounceOwnership():
    """
    @dev Allows the current owner to relinquish control of the contract.
    @notice Renouncing to ownership will leave the contract without an owner.
    It will not be possible to call the functions with the `onlyOwner`
    modifier anymore.
    """

    assert msg.sender == self.owner, "Access is denied."

    log.OwnershipRenounced(msg.sender)
    self.owner = ZERO_ADDRESS

@public 
def transferOwnership(_newOwner: address):
    """
    @dev Allows the current owner to transfer control of the contract to a newOwner.
    @param _newOwner The address to transfer ownership to.
    """
    assert msg.sender == self.owner, "Access is denied."
    assert _newOwner != ZERO_ADDRESS, "Invalid owner supplied."

    log.OwnershipTransferred(msg.sender, _newOwner)
    self.owner = _newOwner


@public
def __init__(_beneficiary: address, _start: timestamp, _cliff: timedelta, _duration: timedelta, _revocable: bool):
    """
    @dev Creates a vesting contract that vests its balance of any ERC20 token to the
    _beneficiary, gradually in a linear fashion until _start + _duration. By then all
    of the balance will have vested.
    @param _beneficiary address of the beneficiary to whom vested tokens are transferred
    @param _cliff duration in seconds of the cliff in which tokens will begin to vest
    @param _start the time (as Unix time) at which point vesting starts
    @param _duration duration in seconds of the period in which the tokens will vest
    @param _revocable whether the vesting is revocable or not
    """
    assert _beneficiary != ZERO_ADDRESS, "Invalid address."
    assert _cliff <= _duration, "Invalid value supplied for the parameter _duration."

    self.beneficiary = _beneficiary
    self.start = _start
    self.cliff = _cliff
    self.duration = _duration
    self.revocable = _revocable

    #OWNABLE
    self.owner = msg.sender


@public
@constant
def getVestedAmount(_token: address) -> uint256:
    currentBalance: uint256 = TokenContract(_token).balanceOf(self)
    totalBalance: uint256 = currentBalance + self.released[_token]

    if block.timestamp < (self.start + self.cliff):
        return 0
    elif (block.timestamp >= self.start + self.duration) or self.revoked[_token]:
        return totalBalance
    else:
        return totalBalance * (block.timestamp - self.start) / self.duration

@public
@constant
def getReleasableAmount(_token: address) -> uint256:
    return self.getVestedAmount(_token) - self.released[_token]

@public
def release(_token: address):
    unreleased: uint256 = self.getReleasableAmount(_token)
    assert unreleased > 0, "Nothing to release."

    self.released[_token] += unreleased

    assert TokenContract(_token).transfer(self.beneficiary, unreleased)
    log.Released(unreleased)

@public
def revoke(_token: address):
    assert msg.sender == self.owner, "Access is denied."
    assert self.revocable, "Sorry but this vesting schedule is not revocable."
    assert not self.revoked[_token], "Sorry but this vesting was already revoked."

    closingBalance: uint256 = TokenContract(_token).balanceOf(self)
    unreleased: uint256 = self.getReleasableAmount(_token)
    refund: uint256 = closingBalance - unreleased

    self.revoked[_token] = True

    assert TokenContract(_token).transfer(self.owner, refund), "We could not revoke this vesting due to an unknown error."

    log.Revoked()
