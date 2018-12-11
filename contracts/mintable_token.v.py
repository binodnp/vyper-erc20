# Detailed ERC20 token with Ownable, Cap, and Mintable features.
# Author: Binod Nirvan
# This file is released under Apache 2.0 license.
# Burnable tokens are such tokens that can be irreversibly burned (destroyed).
# Ported from Open Zeppelin
# https://github.com/OpenZeppelin
# https://github.com/ethereum/EIPs/issues/20
# Based on code by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
# The decimals are only for visualization purposes.
# All the operations are done using the smallest and indivisible token unit,
# just as on Ethereum all the operations are done in wei.
# 
# See https://github.com/OpenZeppelin
# Open Zeppelin tests ported: MintableToken.behaviour.js, MintableToken.test.js, CappedToken.behaviour.js, CappedToken.test.js

#OWNABLE
OwnershipRenounced: event({_previousOwner: indexed(address)})
OwnershipTransferred: event({_previousOwner: indexed(address), _newOwner: indexed(address)})

#ERC20
Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})

#MINTABLE
Mint: event({_to: indexed(address), _amount: uint256})
MintFinished: event()

#OWNABLE
owner: public(address)

#ERC20
name: public(bytes32)
symbol: public(bytes32)
totalSupply: public(uint256)
decimals: public(int128)
balances: map(address, uint256)
allowed: map(address, map(address, uint256))

#MINTABLE
maximumSupply: public(uint256)
mintingFinished: public(bool)


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

#ERC 20
@public
def __init__(_name: bytes32, _symbol: bytes32, _totalSupply: uint256, _maximumSupply: uint256, _decimals: int128):
    """
    @dev Initializes this contract.
    """

    assert _totalSupply <= _maximumSupply, "Sorry but the total supply cannot be more than maximum supply."

    self.name = _name
    self.symbol = _symbol
    self.totalSupply = _totalSupply
    self.maximumSupply = _maximumSupply
    self.decimals = _decimals

    self.balances[msg.sender] = self.totalSupply
    self.owner = msg.sender


@public
@constant
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@public
def transfer(_to: address, _amount: uint256) -> bool:
    """
    @notice Transfers the specified value of the tokens to the destination address. 
    @param _to The destination wallet address to transfer funds to.
    @param _value The amount of tokens to send to the destination address.
    """

    if self.balances[msg.sender] >= _amount and \
       self.balances[_to] + _amount >= self.balances[_to]:
        self.balances[msg.sender] -= _amount
        self.balances[_to] += _amount

        log.Transfer(msg.sender, _to, _amount)
        return True
    else:
        return False


@public
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    """
    @notice Transfers tokens from a specified wallet address.
    @param _from The address to transfer funds from.
    @param _to The address to transfer funds to.
    @param _value The amount of tokens to transfer.
    """

    if _value <= self.allowed[_from][msg.sender] and \
       _value <= self.balances[_from]:
        self.balances[_from] -= _value
        self.allowed[_from][msg.sender] -= _value
        self.balances[_to] += _value

        log.Transfer(_from, _to, _value)
        return True
    else:
        return False

@public
def approve(_spender: address, _amount: uint256) -> bool:
    """
    @notice Approves a wallet address to spend on behalf of the sender.
    @param _spender The address which is approved to spend on behalf of the sender.
    @param _value The amount of tokens approve to spend. 
    """

    self.allowed[msg.sender][_spender] = _amount
    log.Approval(msg.sender, _spender, _amount)
    return True

@public
def increaseApproval(_spender: address, _addedValue: uint256) -> bool:
    """
    @notice Increases the approval of the spender.
    @param _spender The address which is approved to spend on behalf of the sender.
    @param _addedValue The added amount of tokens approved to spend.
    """

    self.allowed[msg.sender][_spender] += _addedValue
    log.Approval(msg.sender, _spender, self.allowed[msg.sender][_spender])
    return True

@public
def decreaseApproval(_spender: address, _subtractedValue: uint256) -> bool:
    """
    @notice Decreases the approval of the spender.
    @param _spender The address of the spender to decrease the allocation from.
    @param _subtractedValue The amount of tokens to subtract from the approved allocation.
    """

    if(_subtractedValue >= self.allowed[msg.sender][_spender]):
        self.allowed[msg.sender][_spender] = 0
    else:
        self.allowed[msg.sender][_spender] -= _subtractedValue

    log.Approval(msg.sender, _spender, self.allowed[msg.sender][_spender])
    return True


@public
@constant
def allowance(_owner: address, _spender: address) -> uint256:
    """
    @notice Function to check the amount of tokens that an owner allowed to a spender.
    @param _owner address The address which owns the funds.
    @param _spender address The address which will spend the funds.
    @return A uint256 specifying the amount of tokens still available for the spender.
    """
    return self.allowed[_owner][_spender]

@public
def finishMinting() -> bool:
    """
    @notice Function to stop minting new tokens.
    @return True if the operation was successful.
    """

    assert msg.sender == self.owner, "Access is denied."
    assert not self.mintingFinished, "The minting was already finished."

    self.mintingFinished = True
    log.MintFinished()
    return True

#MINTABLE
@public
@constant
def cap() -> uint256:
    return self.maximumSupply

@public
def mint(_to: address, _amount: uint256) -> bool:
    """
    @notice Function to mint tokens
    @param _to The address that will receive the minted tokens.
    @param _amount The amount of tokens to mint.
    @return A boolean that indicates if the operation was successful.
    """

    assert msg.sender == self.owner, "Access is denied."
    assert self.totalSupply + _amount <= self.maximumSupply, "You cannot print those many tokens."
    assert not self.mintingFinished, "Minting cannot be performed anymore."

    self.totalSupply += _amount
    self.balances[_to] += _amount

    log.Mint(_to, _amount)
    log.Transfer(ZERO_ADDRESS, _to, _amount)

    return True
