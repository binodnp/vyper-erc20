const BigNumber = web3.BigNumber;

require('chai')
  .use(require('chai-bignumber')(BigNumber))
  .should();

const DetailedERC20Mock = artifacts.require('./erc20_standard_token.vyper');

contract('erc20_standard_token', accounts => {
  let detailedERC20 = null;

  const _name = 'My Detailed ERC20';
  const _symbol = 'MDT';
  const _decimals = 18;
  const _totalSupply = 100;

  beforeEach(async function () {
    detailedERC20 = await DetailedERC20Mock.new(web3.fromAscii(_name), web3.fromAscii(_symbol), _totalSupply, _decimals);
  });

  it('has a name', async function () {
    const name = web3.toUtf8(await detailedERC20.name());
    name.should.be.equal(_name);
  });

  it('has a symbol', async function () {
    const symbol = web3.toUtf8(await detailedERC20.symbol());
    symbol.should.be.equal(_symbol);
  });

  it('has an amount of decimals', async function () {
    const decimals = await detailedERC20.decimals();
    decimals.should.be.bignumber.equal(_decimals);
  });
});
