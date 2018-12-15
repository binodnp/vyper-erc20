# ERC20 token with Ownable, Burnable, Mintable, and Transfer Lock features.
# Contributors: Binod Nirvan
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

#OWNABLE
OwnershipRenounced: event({_previousOwner: indexed(address)})
OwnershipTransferred: event({_previousOwner: indexed(address), _newOwner: indexed(address)})

#ADMIN
AdminAdded: event({_who: indexed(address)})
AdminRemoved: event({_who: indexed(address)})

#PAUSABLE
Paused: event()
Unpaused: event()

#TRANSFER STATE
TokenReleased: event({_currentState: bool})

#ERC20
Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})

#MINTABLE
Mint: event({_to: indexed(address), _amount: uint256})
MintFinished: event()

#BURNABLE
Burn: event({_burner: indexed(address), _value: uint256})

#RECLAIMABLE
EtherClaimed: event() #todo
TokenReclaimed: event() #todo


#OWNABLE
owner: public(address)

#ADMIN
admins: public(map(address, bool))

#PAUSABLE
paused: public(bool)

#TRANSFER STATE
transferLocked: public(bool)

#ERC20
name: public(bytes32)
symbol: public(bytes32)
totalSupply: public(uint256)
maximumSupply: public(uint256)
decimals: public(int128)
balances: public(map(address, uint256))
allowed: public(map(address, map(address, uint256)))

#MINTABLE
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
    assert not self.paused, "You may not renounce ownership when the contract is paused."

    log.OwnershipRenounced(msg.sender)
    self.owner = ZERO_ADDRESS

@public 
def transferOwnership(_newOwner: address):
    """
    @dev Allows the current owner to transfer control of the contract to a newOwner.
    @param _newOwner The address to transfer ownership to.
    """
    assert msg.sender == self.owner, "Access is denied."
    assert not self.paused, "You may not transfer ownership when the contract is paused."
    assert _newOwner != ZERO_ADDRESS, "Invalid owner supplied."

    log.OwnershipTransferred(msg.sender, _newOwner)
    self.owner = _newOwner

#ADMIN
# This feature enables to create multiple contract administrators.

@private
@constant
def isAdmin(_who: address) -> bool:
    """
    @notice Checks if an address is an administrator.
    @param _who The address to check if it is an admin.
    """

    if _who == self.owner:
        return True

    return self.admins[_who]


@public
def addAdmin(_address: address) -> bool:
    """
    @notice Adds the specified address to the list of administrators.
    @param _address The address to add to the administrator list.
    """

    assert _address != ZERO_ADDRESS, "Invalid address."
    assert not _address == self.owner, "The owner cannot be added to or removed from the administrator list."
    assert not self.admins[_address], "This address is already an administrator."

    self.admins[_address] = True

    log.AdminAdded(_address)

    return True

@public 
def removeAdmin(_address: address) -> bool:
    """
    @notice Removes the specified address from the list of administrators.
    @param _address The address to remove from the administrator list.
    """

    assert _address != ZERO_ADDRESS, "Invalid address."
    assert not _address == self.owner, "The owner cannot be added to or removed from the administrator list."
    assert self.admins[_address], "This address isn't an administrator."

    self.admins[_address] = False

    log.AdminRemoved(_address)

    return True

#PAUSABLE
# This feature enables you to create pausable mechanism 
# to stop in case of emergency.

@public
def pause():
    """
    @notice Pauses the contract
    """

    assert msg.sender == self.owner, "Access is denied."
    assert not self.paused, "The contract is already paused."

    self.paused = True
    log.Paused()

@public
def unpause():
    """
    @notice Unpauses the contract.
    """

    assert msg.sender == self.owner, "Access is denied."
    assert self.paused, "The contract is already unpaused."

    self.paused = False

    log.Unpaused()


#TRANSFER STATE
@private
@constant
def canTransfer(_who: address) -> bool:    
    """
    @notice Checks if the supplied address is able to perform transfers.
    @param _who The address to check against if the transfer is allowed.
    """

    if(self.paused or self.transferLocked):
        return self.isAdmin(_who)
 
    return True

@public
def enableTransfers():
    """
    @notice This function enables token transfers for everyone.
    """
    assert msg.sender == self.owner, "Access is denied."
    assert not self.paused, "You cannot enable transfers when contract is paused."
    assert self.transferLocked, "The transfer state is already enabled."

    self.transferLocked = False
    log.TokenReleased(False)

@public 
def disableTransfers():
    """
    @notice This function disables token transfers for everyone.
    """

    assert msg.sender == self.owner, "Access is denied."
    assert not self.paused, "You cannot disable transfers when contract is paused."
    assert not self.transferLocked, "The transfer state is already disabled."

    self.transferLocked = True
    log.TokenReleased(True)


#ERC 20
@public
def __init__(_name: bytes32, _symbol: bytes32, _totalSupply: uint256, _maximumSupply: uint256, _decimals: int128):
    """
    @dev Initializes this contract.
    """

    assert _maximumSupply >= _totalSupply, "Sorry but the total supply cannot be more than maximum supply."

    self.name = _name
    self.symbol = _symbol
    self.totalSupply = _totalSupply
    self.maximumSupply = _maximumSupply
    self.decimals = _decimals

    self.balances[msg.sender] = self.totalSupply
    self.owner = msg.sender
    self.paused = False
    self.transferLocked = True


@public
@constant
def balanceOf(_owner: address) -> uint256:
    return self.balances[_owner]

@public
def transfer(_to: address, _amount: uint256) -> bool:
    """
    @notice Transfers the specified value of the tokens to the destination address. 
    Transfers can only happen when the transfer state is enabled. 
    @param _to The destination wallet address to transfer funds to.
    @param _value The amount of tokens to send to the destination address.
    """

    assert self.canTransfer(msg.sender), "Could not complete this request because transfer state is locked or paused."

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
    Transfers can only happen when the transfer state is enabled. 
    @param _from The address to transfer funds from.
    @param _to The address to transfer funds to.
    @param _value The amount of tokens to transfer.
    """
    assert self.canTransfer(msg.sender), "Could not complete this request because transfer state is locked or paused."

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
    This can only be done when the contract is not paused. 
    @param _spender The address which is approved to spend on behalf of the sender.
    @param _value The amount of tokens approve to spend. 
    """

    assert not self.paused, "Sorry but the contract is paused."

    self.allowed[msg.sender][_spender] = _amount
    log.Approval(msg.sender, _spender, _amount)
    return True

@public
def increaseApproval(_spender: address, _addedValue: uint256) -> bool:
    """
    @notice Increases the approval of the spender.
    This can only be done when the contract is not paused. 
    @param _spender The address which is approved to spend on behalf of the sender.
    @param _addedValue The added amount of tokens approved to spend.
    """

    assert not self.paused, "Sorry but the contract is paused."

    self.allowed[msg.sender][_spender] += _addedValue
    log.Approval(msg.sender, _spender, self.allowed[msg.sender][_spender])
    return True

@public
def decreaseApproval(_spender: address, _subtractedValue: uint256) -> bool:
    """
    @notice Decreases the approval of the spender.
    This can only be done when the contract is not paused. 
    @param _spender The address of the spender to decrease the allocation from.
    @param _subtractedValue The amount of tokens to subtract from the approved allocation.
    """

    assert not self.paused, "Sorry but the contract is paused."

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

#MINTABLE
@public
@constant
def cap() -> uint256:
    return self.maximumSupply

@public
def finishMinting() -> bool:
    """
    @notice Function to stop minting new tokens.
    @return True if the operation was successful.
    """

    assert self.isAdmin(msg.sender), "Access is denied."
    assert not self.mintingFinished, "The minting was already finished."

    self.mintingFinished = True
    log.MintFinished()
    return True

@public
def mint(_to: address, _amount: uint256) -> bool:
    """
    @notice Function to mint tokens
    @param _to The address that will receive the minted tokens.
    @param _amount The amount of tokens to mint.
    @return A boolean that indicates if the operation was successful.
    """

    assert self.canTransfer(msg.sender)

    assert self.isAdmin(msg.sender), "Access is denied."
    assert self.totalSupply + _amount <= self.maximumSupply, "You cannot print those many tokens."
    assert not self.mintingFinished, "Minting cannot be performed anymore."

    self.totalSupply += _amount
    self.balances[_to] += _amount

    log.Mint(_to, _amount)
    log.Transfer(ZERO_ADDRESS, _to, _amount)

    return True

#BURNABLE
@public
def burn(_value: uint256):
    """
    @notice Burns the supplied amount of tokens from the sender wallet.
    @param _value The amount of token to be burned.
    """

    assert self.canTransfer(msg.sender), "Could not complete this request because transfer state is locked or paused."
    assert _value <= self.balances[msg.sender], "You don't have that many tokens to burn."

    self.balances[msg.sender] -= _value
    self.totalSupply -= _value

    log.Burn(msg.sender, _value)
    log.Transfer(msg.sender, ZERO_ADDRESS, _value)
