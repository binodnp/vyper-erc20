const {
    assertRevert
} = require('./helpers/assertRevert');
const BasicToken = artifacts.require('./erc20_standard_token.vyper');

contract('erc20_standard_token', function ([owner, recipient, anotherAccount]) {
    const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';

    beforeEach(async function () {
        this.token = await BasicToken.new(web3.fromAscii("Name"), web3.fromAscii("SYMBOL"), 100, 18);
    });

    describe('total supply', function () {
        it('returns the total amount of tokens', async function () {
            const totalSupply = await this.token.totalSupply();

            assert.equal(totalSupply.toNumber(), 100);
        });
    });

    describe('balanceOf', function () {
        describe('when the requested account has no tokens', function () {
            it('returns zero', async function () {
                const balance = await this.token.balanceOf(anotherAccount);

                assert.equal(balance.toNumber(), 0);
            });
        });

        describe('when the requested account has some tokens', function () {
            it('returns the total amount of tokens', async function () {
                const balance = await this.token.balanceOf(owner);

                assert.equal(balance.toNumber(), 100);
            });
        });
    });

    describe('transfer', function () {
        describe('when the recipient is not the zero address', function () {
            const to = recipient;

            describe('when the sender does not have enough balance', function () {
                const amount = 101;

                it('reverts', async function () {
                    await assertRevert(this.token.transfer(to, amount, {
                        from: anotherAccount
                    }));
                });
            });

            describe('when the sender has enough balance', function () {
                const amount = 100;

                it('transfers the requested amount', async function () {
                    await this.token.transfer(to, amount, {
                        from: owner
                    });

                    const senderBalance = await this.token.balanceOf(owner);
                    assert.equal(senderBalance, 0);

                    const recipientBalance = await this.token.balanceOf(to);
                    assert.equal(recipientBalance, amount);
                });

                it('emits a transfer event', async function () {
                    const {
                        logs
                    } = await this.token.transfer(to, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Transfer');
                    assert.equal(logs[0].args._from, owner);
                    assert.equal(logs[0].args._to, to);
                    assert(logs[0].args._value.eq(amount));
                });
            });
        });

        describe('when the recipient is the zero address', function () {
            const to = ZERO_ADDRESS;

            it('reverts', async function () {
                await assertRevert(this.token.transfer(to, 100, {
                    from: anotherAccount
                }));
            });
        });
    });
});
