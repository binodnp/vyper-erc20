const { ether } = require('./helpers/ether');
const MintableToken = artifacts.require('./mintable_token.vyper');
const { assertRevert } = require('./helpers/assertRevert');
const BigNumber = web3.BigNumber;

contract('MintableToken', function ([owner, anotherAccount]) {
  const minter = owner;
  const cap = ether(1000);
  const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';

  beforeEach(async function () {
    this.token = await MintableToken.new(web3.fromAscii("Name"), web3.fromAscii("SYMBOL"), 0, cap, 18, { from: owner });
  });

  describe('as a basic mintable token', function () {
    describe('after token creation', function () {
      it('sender should be token owner', async function () {
        const tokenOwner = await this.token.owner({ from: owner });
        tokenOwner.should.equal(owner);
      });
    });

    describe('minting finished', function () {
      describe('when the token minting is not finished', function () {
        it('returns false', async function () {
          const mintingFinished = await this.token.mintingFinished();
          assert.equal(mintingFinished, false);
        });
      });

      describe('when the token is minting finished', function () {
        beforeEach(async function () {
          await this.token.finishMinting({ from: owner });
        });

        it('returns true', async function () {
          const mintingFinished = await this.token.mintingFinished();
          assert.equal(mintingFinished, true);
        });
      });
    });

    describe('finish minting', function () {
      describe('when the sender is the token owner', function () {
        const from = owner;

        describe('when the token minting was not finished', function () {
          it('finishes token minting', async function () {
            await this.token.finishMinting({ from });

            const mintingFinished = await this.token.mintingFinished();
            assert.equal(mintingFinished, true);
          });

          it('emits a mint finished event', async function () {
            const { logs } = await this.token.finishMinting({ from });

            assert.equal(logs.length, 1);
            assert.equal(logs[0].event, 'MintFinished');
          });
        });

        describe('when the token minting was already finished', function () {
          beforeEach(async function () {
            await this.token.finishMinting({ from });
          });

          it('reverts', async function () {
            await assertRevert(this.token.finishMinting({ from }));
          });
        });
      });

      describe('when the sender is not the token owner', function () {
        const from = anotherAccount;

        describe('when the token minting was not finished', function () {
          it('reverts', async function () {
            await assertRevert(this.token.finishMinting({ from }));
          });
        });

        describe('when the token minting was already finished', function () {
          beforeEach(async function () {
            await this.token.finishMinting({ from: owner });
          });

          it('reverts', async function () {
            await assertRevert(this.token.finishMinting({ from }));
          });
        });
      });
    });

    describe('mint', function () {
      const amount = 100;

      describe('when the sender has the minting permission', function () {
        const from = minter;

        describe('when the token minting is not finished', function () {
          it('mints the requested amount', async function () {
            await this.token.mint(owner, amount, { from });

            const balance = await this.token.balanceOf(owner);
            assert.equal(balance, amount);
          });

          it('emits a mint and a transfer event', async function () {
            const { logs } = await this.token.mint(owner, amount, { from });
            
            assert.equal(logs.length, 2);
            assert.equal(logs[0].event, 'Mint');
            assert.equal(logs[0].args._to, owner);
            assert.equal(logs[0].args._amount, amount);
            assert.equal(logs[1].event, 'Transfer');
            assert.equal(logs[1].args._from, ZERO_ADDRESS);
            assert.equal(logs[1].args._to, owner);
            assert.equal(logs[1].args._value, amount);
          });
        });

        describe('when the token minting is finished', function () {
          beforeEach(async function () {
            await this.token.finishMinting({ from: owner });
          });

          it('reverts', async function () {
            await assertRevert(this.token.mint(owner, amount, { from }));
          });
        });
      });

      describe('when the sender has not the minting permission', function () {
        const from = anotherAccount;

        describe('when the token minting is not finished', function () {
          it('reverts', async function () {
            await assertRevert(this.token.mint(owner, amount, { from }));
          });
        });

        describe('when the token minting is already finished', function () {
          beforeEach(async function () {
            await this.token.finishMinting({ from: owner });
          });

          it('reverts', async function () {
            await assertRevert(this.token.mint(owner, amount, { from }));
          });
        });
      });
    });
  });
});
