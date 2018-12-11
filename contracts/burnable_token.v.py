# Detailed ERC20 token with Burnable feature.
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
# Open Zeppelin tests ported: BurnableToken.behaviour.js, BurnableToken.test.js

#ERC20
Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})

#BURNABLE
Burn: event({_burner: indexed(address), _value: uint256})

#ERC20
name: public(bytes32)
symbol: public(bytes32)
totalSupply: public(uint256)
decimals: public(int128)
balances: map(address, uint256)
allowed: map(address, map(address, uint256))

#ERC 20
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


#BURNABLE
@public
def burn(_value: uint256):
    """
    @notice Burns the supplied amount of tokens from the sender wallet.
    @param _value The amount of token to be burned.
    """
    assert _value <= self.balances[msg.sender], "You don't have that many tokens to burn."

    self.balances[msg.sender] -= _value
    self.totalSupply -= _value

    log.Burn(msg.sender, _value)
    log.Transfer(msg.sender, ZERO_ADDRESS, _value)
