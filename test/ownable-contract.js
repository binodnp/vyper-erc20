const { shouldBehaveLikeOwnable } = require('./ownable.behavior.js');

const Ownable = artifacts.require('./mintable_token.vyper');

contract('Ownable', function (accounts) {
  beforeEach(async function () {
    this.ownable = await Ownable.new(web3.fromAscii("Name"), web3.fromAscii("SYMBOL"), 10000, 10000, 18);
  });

  shouldBehaveLikeOwnable(accounts);
});
