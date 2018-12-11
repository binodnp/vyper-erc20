const Token = artifacts.require('./erc20_standard_token.vyper');
const BigNumber = require('bignumber.js');
const EVMRevert = require('./helpers/EVMRevert').EVMRevert;
const ether = require('./helpers/ether').ether;

require('chai')
  .use(require('chai-as-promised'))
  .use(require('chai-bignumber')(BigNumber))
  .should();

contract('erc20_standard_token', function (accounts) {
  describe('Token Creation Ruleset', () => {
    it('must correctly deploy with correct parameters and state variables.', async () => {
      const name = "Example Token";
      const symbol = "EXA";
      const totalSupply = ether(1000000000);
      const decimals = 18;

      let token = await Token.new(web3.fromAscii(name), web3.fromAscii(symbol), totalSupply, decimals);

      assert.equal(web3.toUtf8(await token.name()), name);
      assert.equal(web3.toUtf8(await token.symbol()), symbol);
      assert.equal((await token.decimals()).toNumber(), 18);

      (await token.totalSupply()).should.bignumber.equal(totalSupply);
      (await token.balanceOf(accounts[0])).should.bignumber.equal(totalSupply);
    });
  });
});