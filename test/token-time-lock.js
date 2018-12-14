const { latestTime } = require('./helpers/latestTime');
const { increaseTimeTo, duration } = require('./helpers/increaseTime');
const { expectThrow } = require('./helpers/expectThrow');

const BigNumber = web3.BigNumber;

require('chai')
  .use(require('chai-bignumber')(BigNumber))
  .should();

const MintableToken = artifacts.require('mintable_token.vyper');
const TokenTimelock = artifacts.require('token_timelock.vyper');

contract('TokenTimelock', function ([_, owner, beneficiary]) {
  const amount = new BigNumber(100);

  beforeEach(async function () {
    this.token = await MintableToken.new(web3.fromAscii("Name"), web3.fromAscii("SYMBOL"), 0, 10000000, 18, { from: owner });
    this.releaseTime = (await latestTime()) + duration.years(1);
    this.timelock = await TokenTimelock.new(this.token.address, beneficiary, this.releaseTime);
    await this.token.mint(this.timelock.address, amount, { from: owner });
  });

  it('initializes with correct balance', async function () {
    const balance = await this.token.balanceOf(this.timelock.address);
    balance.should.be.bignumber.equal(amount);
  });

  it('cannot be released before time limit', async function () {
    await expectThrow(this.timelock.release({from: beneficiary}));
  });

  it('cannot be released just before time limit', async function () {
    await increaseTimeTo(this.releaseTime - duration.seconds(3));
    await expectThrow(this.timelock.release({from: beneficiary}));
  });

  it('can be released just after limit', async function () {
    await increaseTimeTo(this.releaseTime + duration.seconds(1));
    await this.timelock.release({from: beneficiary});
    const balance = await this.token.balanceOf(beneficiary);
    balance.should.be.bignumber.equal(amount);
  });

  it('can be released after time limit', async function () {
    await increaseTimeTo(this.releaseTime + duration.years(1));
    await this.timelock.release({from: beneficiary});
    const balance = await this.token.balanceOf(beneficiary);
    balance.should.be.bignumber.equal(amount);
  });

  it('cannot be released twice', async function () {
    await increaseTimeTo(this.releaseTime + duration.years(1));
    await this.timelock.release({from: beneficiary});
    await expectThrow(this.timelock.release({from: beneficiary}));
    const balance = await this.token.balanceOf(beneficiary);
    balance.should.be.bignumber.equal(amount);
  });
});
