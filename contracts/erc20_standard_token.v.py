# Standard ERC20 token
# Contributors: Binod Nirvan
# This file is released under Apache 2.0 license.
# http://www.apache.org/licenses/
# Ported from Open Zeppelin 
# https://github.com/OpenZeppelin
# ERC20 token implementation with some additional features.
# https://github.com/ethereum/EIPs/issues/20
# Based on code by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol
# The decimals are only for visualization purposes.
# All the operations are done using the smallest and indivisible token unit,
# just as on Ethereum all the operations are done in wei.
# 
# See https://github.com/OpenZeppelin
# Open Zeppelin tests ported: BasicToken.test.js, DetailedERC20.test.js, MintableToken.behaviour.js, MintableToken.test.js, StandardToken.test.js
Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})

name: public(bytes32)
symbol: public(bytes32)
totalSupply: public(uint256)
decimals: public(int128)
balances: map(address, uint256)
allowed: map(address, map(address, uint256))

@public
def __init__(_name: bytes32, _symbol: bytes32, _totalSupply: uint256, _decimals: int128):
    """
    @dev Initializes this contract.
    """

    self.name = _name
    self.symbol = _symbol
    self.totalSupply = _totalSupply
    self.decimals = _decimals

    self.balances[msg.sender] = self.totalSupply


@public
@constant
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@public
def transfer(_to: address, _value: uint256) -> bool:
    """
    @notice Transfers the specified value of the tokens to the destination address. 
    @param _to The destination wallet address to transfer funds to.
    @param _value The amount of tokens to send to the destination address.
    """

    assert _value <= self.balances[msg.sender], "You do not have sufficient balance to transfer these many tokens."
    assert _to != ZERO_ADDRESS, "Invalid address"

    self.balances[msg.sender] -= _value
    self.balances[_to] += _value

    log.Transfer(msg.sender, _to, _value)
    return True


@public
def transferFrom(_from: address, _to: address, _value: uint256) -> bool:
    """
    @notice Transfers tokens from a specified wallet address.
    @param _from The address to transfer funds from.
    @param _to The address to transfer funds to.
    @param _value The amount of tokens to transfer.
    """

    assert _value <= self.balances[_from], "The specified account does not have sufficient balance to transfer these many tokens."
    assert _value <= self.allowed[_from][msg.sender], "You don't have approval to transfer these many tokens."
    assert _to != ZERO_ADDRESS, "Invalid address"

    self.balances[_from] -= _value
    self.allowed[_from][msg.sender] -= _value
    self.balances[_to] += _value

    log.Transfer(_from, _to, _value)
    return True

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
