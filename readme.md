
# Vyper ERC20 Contracts  

Welcome to Vyper ERC20 contracts. 

You will find several Vyper ERC20 contract implementations in this project. We've ported some Open Zeppelin tests with minimum changes.

## Before You Clone This Repository ...

This project requires the the following dependencies to be present before you can actually start developing and contributing to this repository.

**Prerequisites**

- Pthon3
- NodeJS
- Truffle
- Ganache

Since Vyper compiler is a beta software, there could be some breaking changes in the future. We, therefore, strongly encourage you to keep a close eye on [the official Vyper documentation](https://vyper.readthedocs.io/en/v0.1.0-beta.5/installing-vyper.html) if things go south.

## Setting up the Development Environment

**Clone the Project**

Since you've already installed the dependencies, you can now clone the project from GitHub.

```bash
cd path/to/a/desired/directory
git clone http://github.com/binodnp/vyper-erc20
cd vyper-erc20
```

**Create a Virtual Environment**
```bash
virtualenv -p python3 --no-site-packages env
source env/bin/activate
```


**Clone and Make Vyper**

```bash
git clone https://github.com/ethereum/vyper.git
cd vyper
make
make test
```  

If you see some error messages here, you might have missed to activate the virtual environment. Type:

```bash
source env/bin/activate
```



**Restore NPM Packages**

NPM is need to write and truffle tests (in JavaScript of course).
```bash
npm install
```

## How to's?

**How to Run Vyper to Build a Contract?**

On the project root, type the following in the terminal:

```bash
vyper ./contracts/burnable_token.v.py
```

The above command will compile the burnable token contract.

**What does Truper Actually Do?**

Instead of using *Vyper*, you could use **truper** to compile contracts and generate the build outputs to the `build` directory. This helps you write, run, and migrate **truffle tests** in JavaScript.

> Note that for truper to work properly, Vyper contract files must end with `.v.py` file extension(s). Also note that truper will generate the build artifacts (files) to have `.vyper.json` extension.

Open the terminal panel and type `truper` to build contracts.

**Truffle Tests**

Open the terminal panel and type `truffle test` to see the test results.

> Please note that you would need to first compile the contracts using the command `truper` before you can run your tests. 

**Contracts**



**erc20_standard_token.v.py**

Standard ERC20 token with some additional details. Open Zeppelin tests ported: 
- BasicToken.test.js
- DetailedERC20.test.js
- MintableToken.behaviour.js
- MintableToken.test.js
- StandardToken.test.js

**burnable_token.v.py**

Standard Detailed ERC20 token with Burnable feature. Open Zeppelin tests ported:

- BurnableToken.behaviour.js
- BurnableToken.test.js

**mintable_token.v.py**
Detailed ERC20 token with Ownable, Cap, and Mintable features. Open Zeppelin tests ported:

- MintableToken.behaviour.js
- MintableToken.test.js
- CappedToken.behaviour.js
- CappedToken.test.js


**pausable_token.v.py**

Detailed ERC20 token with Ownable and Pausable feature. Open Zeppelin tests ported: PausableToken.test.js

**lockable_token.v.py**
ERC20 token with Ownable, Burnable, Mintable, and Transfer Lock features.



**License**

Apache 2.0

**Additional Links**

- [Vyper Documentation](https://vyper.readthedocs.io/en/v0.1.0-beta.5/installing-vyper.html)
- [Truper Repository](https://github.com/maurelian/truper)
- [Online Vyper Compiler](http://vyper.online/)
- [Open Zeppelin Solidity](https://github.com/OpenZeppelin/openzeppelin-solidity)
- [Truffle Suite of Tools](https://truffleframework.com)