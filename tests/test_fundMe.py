from scripts.support_functions import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fundMe
from brownie import network, exceptions
import pytest


def test_canFundAndWithdraw():
    account = get_account()
    fund_me = deploy_fundMe()
    entrance_fee = fund_me.getEntranceFee() + 100
    txn = fund_me.fund({"from": account, "value": entrance_fee})
    txn.wait(1)
    assert fund_me.addressToFund(account.address) == entrance_fee
    txn2 = fund_me.withdraw({"from": account})
    assert fund_me.addressToFund(account.address) == 0


def test_onlyOwnerCanWithdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fundMe()
    bad_actor = accounts.add()
    fund_me.withdraw({"from": bad_actor})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
