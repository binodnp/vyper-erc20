const {
    assertRevert
} = require('./helpers/assertRevert');
const StandardTokenMock = artifacts.require('./erc20_standard_token.vyper');;

contract('erc20_standard_token', function ([owner, recipient, anotherAccount]) {
    const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000';

    beforeEach(async function () {
        this.token = await StandardTokenMock.new(web3.fromAscii("Name"), web3.fromAscii("SYMBOL"), 100, 18);
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

                assert.equal(balance, 100);
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
                        from: owner
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
                    from: owner
                }));
            });
        });
    });

    describe('approve', function () {
        describe('when the spender is not the zero address', function () {
            const spender = recipient;

            describe('when the sender has enough balance', function () {
                const amount = 100;

                it('emits an approval event', async function () {
                    const {
                        logs
                    } = await this.token.approve(spender, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Approval');
                    assert.equal(logs[0].args._owner, owner);
                    assert.equal(logs[0].args._spender, spender);
                    assert(logs[0].args._value.eq(amount));
                });

                describe('when there was no approved amount before', function () {
                    it('approves the requested amount', async function () {
                        await this.token.approve(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount);
                    });
                });

                describe('when the spender had an approved amount', function () {
                    beforeEach(async function () {
                        await this.token.approve(spender, 1, {
                            from: owner
                        });
                    });

                    it('approves the requested amount and replaces the previous one', async function () {
                        await this.token.approve(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount);
                    });
                });
            });

            describe('when the sender does not have enough balance', function () {
                const amount = 101;

                it('emits an approval event', async function () {
                    const {
                        logs
                    } = await this.token.approve(spender, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Approval');
                    assert.equal(logs[0].args._owner, owner);
                    assert.equal(logs[0].args._spender, spender);
                    assert(logs[0].args._value.eq(amount));
                });

                describe('when there was no approved amount before', function () {
                    it('approves the requested amount', async function () {
                        await this.token.approve(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount);
                    });
                });

                describe('when the spender had an approved amount', function () {
                    beforeEach(async function () {
                        await this.token.approve(spender, 1, {
                            from: owner
                        });
                    });

                    it('approves the requested amount and replaces the previous one', async function () {
                        await this.token.approve(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount);
                    });
                });
            });
        });

        describe('when the spender is the zero address', function () {
            const amount = 100;
            const spender = ZERO_ADDRESS;

            it('approves the requested amount', async function () {
                await this.token.approve(spender, amount, {
                    from: owner
                });

                const allowance = await this.token.allowance(owner, spender);
                assert.equal(allowance.toNumber(), amount);
            });

            it('emits an approval event', async function () {
                const {
                    logs
                } = await this.token.approve(spender, amount, {
                    from: owner
                });

                assert.equal(logs.length, 1);
                assert.equal(logs[0].event, 'Approval');
                assert.equal(logs[0].args._owner, owner);
                assert.equal(logs[0].args._spender, spender);
                assert(logs[0].args._value.eq(amount));
            });
        });
    });

    describe('transfer from', function () {
        const spender = recipient;

        describe('when the recipient is not the zero address', function () {
            const to = anotherAccount;

            describe('when the spender has enough approved balance', function () {
                beforeEach(async function () {
                    await this.token.approve(spender, 100, {
                        from: owner
                    });
                });

                describe('when the owner has enough balance', function () {
                    const amount = 100;

                    it('transfers the requested amount', async function () {
                        await this.token.transferFrom(owner, to, amount, {
                            from: spender
                        });

                        const senderBalance = await this.token.balanceOf(owner);
                        assert.equal(senderBalance.toNumber(), 0);

                        const recipientBalance = await this.token.balanceOf(to);
                        assert.equal(recipientBalance.toNumber(), amount);
                    });

                    it('decreases the spender allowance', async function () {
                        await this.token.transferFrom(owner, to, amount, {
                            from: spender
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), 0);
                    });

                    it('emits a transfer event', async function () {
                        const {
                            logs
                        } = await this.token.transferFrom(owner, to, amount, {
                            from: spender
                        });

                        assert.equal(logs.length, 1);
                        assert.equal(logs[0].event, 'Transfer');
                        assert.equal(logs[0].args._from, owner);
                        assert.equal(logs[0].args._to, to);
                        assert(logs[0].args._value.eq(amount));
                    });
                });

                describe('when the owner does not have enough balance', function () {
                    const amount = 101;

                    it('reverts', async function () {
                        await assertRevert(this.token.transferFrom(owner, to, amount, {
                            from: spender
                        }));
                    });
                });
            });

            describe('when the spender does not have enough approved balance', function () {
                beforeEach(async function () {
                    await this.token.approve(spender, 99, {
                        from: owner
                    });
                });

                describe('when the owner has enough balance', function () {
                    const amount = 100;

                    it('reverts', async function () {
                        await assertRevert(this.token.transferFrom(owner, to, amount, {
                            from: spender
                        }));
                    });
                });

                describe('when the owner does not have enough balance', function () {
                    const amount = 101;

                    it('reverts', async function () {
                        await assertRevert(this.token.transferFrom(owner, to, amount, {
                            from: spender
                        }));
                    });
                });
            });
        });

        describe('when the recipient is the zero address', function () {
            const amount = 100;
            const to = ZERO_ADDRESS;

            beforeEach(async function () {
                await this.token.approve(spender, amount, {
                    from: owner
                });
            });

            it('reverts', async function () {
                await assertRevert(this.token.transferFrom(owner, to, amount, {
                    from: spender
                }));
            });
        });
    });

    describe('decrease approval', function () {
        describe('when the spender is not the zero address', function () {
            const spender = recipient;

            describe('when the sender has enough balance', function () {
                const amount = 100;

                it('emits an approval event', async function () {
                    const {
                        logs
                    } = await this.token.decreaseApproval(spender, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Approval');
                    assert.equal(logs[0].args._owner, owner);
                    assert.equal(logs[0].args._spender, spender);
                    assert(logs[0].args._value.eq(0));
                });

                describe('when there was no approved amount before', function () {
                    it('keeps the allowance to zero', async function () {
                        await this.token.decreaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance, 0);
                    });
                });

                describe('when the spender had an approved amount', function () {
                    const approvedAmount = amount;

                    beforeEach(async function () {
                        await this.token.approve(spender, approvedAmount, {
                            from: owner
                        });
                    });

                    it('decreases the spender allowance subtracting the requested amount', async function () {
                        await this.token.decreaseApproval(spender, approvedAmount - 5, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), 5);
                    });

                    it('sets the allowance to zero when all allowance is removed', async function () {
                        await this.token.decreaseApproval(spender, approvedAmount, {
                            from: owner
                        });
                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance, 0);
                    });

                    it('sets the allowance to zero when more than the full allowance is removed', async function () {
                        await this.token.decreaseApproval(spender, approvedAmount + 5, {
                            from: owner
                        });
                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance, 0);
                    });
                });
            });

            describe('when the sender does not have enough balance', function () {
                const amount = 101;

                it('emits an approval event', async function () {
                    const {
                        logs
                    } = await this.token.decreaseApproval(spender, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Approval');
                    assert.equal(logs[0].args._owner, owner);
                    assert.equal(logs[0].args._spender, spender);
                    assert(logs[0].args._value.eq(0));
                });

                describe('when there was no approved amount before', function () {
                    it('keeps the allowance to zero', async function () {
                        await this.token.decreaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance, 0);
                    });
                });

                describe('when the spender had an approved amount', function () {
                    beforeEach(async function () {
                        await this.token.approve(spender, amount + 1, {
                            from: owner
                        });
                    });

                    it('decreases the spender allowance subtracting the requested amount', async function () {
                        await this.token.decreaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), 1);
                    });
                });
            });
        });

        describe('when the spender is the zero address', function () {
            const amount = 100;
            const spender = ZERO_ADDRESS;

            it('decreases the requested amount', async function () {
                await this.token.decreaseApproval(spender, amount, {
                    from: owner
                });

                const allowance = await this.token.allowance(owner, spender);
                assert.equal(allowance, 0);
            });

            it('emits an approval event', async function () {
                const {
                    logs
                } = await this.token.decreaseApproval(spender, amount, {
                    from: owner
                });

                assert.equal(logs.length, 1);
                assert.equal(logs[0].event, 'Approval');
                assert.equal(logs[0].args._owner, owner);
                assert.equal(logs[0].args._spender, spender);
                assert(logs[0].args._value.eq(0));
            });
        });
    });

    describe('increase approval', function () {
        const amount = 100;

        describe('when the spender is not the zero address', function () {
            const spender = recipient;

            describe('when the sender has enough balance', function () {
                it('emits an approval event', async function () {
                    const {
                        logs
                    } = await this.token.increaseApproval(spender, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Approval');
                    assert.equal(logs[0].args._owner, owner);
                    assert.equal(logs[0].args._spender, spender);
                    assert(logs[0].args._value.eq(amount));
                });

                describe('when there was no approved amount before', function () {
                    it('approves the requested amount', async function () {
                        await this.token.increaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount);
                    });
                });

                describe('when the spender had an approved amount', function () {
                    beforeEach(async function () {
                        await this.token.approve(spender, 1, {
                            from: owner
                        });
                    });

                    it('increases the spender allowance adding the requested amount', async function () {
                        await this.token.increaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount + 1);
                    });
                });
            });

            describe('when the sender does not have enough balance', function () {
                const amount = 101;

                it('emits an approval event', async function () {
                    const {
                        logs
                    } = await this.token.increaseApproval(spender, amount, {
                        from: owner
                    });

                    assert.equal(logs.length, 1);
                    assert.equal(logs[0].event, 'Approval');
                    assert.equal(logs[0].args._owner, owner);
                    assert.equal(logs[0].args._spender, spender);
                    assert(logs[0].args._value.eq(amount));
                });

                describe('when there was no approved amount before', function () {
                    it('approves the requested amount', async function () {
                        await this.token.increaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount);
                    });
                });

                describe('when the spender had an approved amount', function () {
                    beforeEach(async function () {
                        await this.token.approve(spender, 1, {
                            from: owner
                        });
                    });

                    it('increases the spender allowance adding the requested amount', async function () {
                        await this.token.increaseApproval(spender, amount, {
                            from: owner
                        });

                        const allowance = await this.token.allowance(owner, spender);
                        assert.equal(allowance.toNumber(), amount + 1);
                    });
                });
            });
        });

        describe('when the spender is the zero address', function () {
            const spender = ZERO_ADDRESS;

            it('approves the requested amount', async function () {
                await this.token.increaseApproval(spender, amount, {
                    from: owner
                });

                const allowance = await this.token.allowance(owner, spender);
                assert.equal(allowance.toNumber(), amount);
            });

            it('emits an approval event', async function () {
                const {
                    logs
                } = await this.token.increaseApproval(spender, amount, {
                    from: owner
                });

                assert.equal(logs.length, 1);
                assert.equal(logs[0].event, 'Approval');
                assert.equal(logs[0].args._owner, owner);
                assert.equal(logs[0].args._spender, spender);
                assert(logs[0].args._value.eq(amount));
            });
        });
    });
});
