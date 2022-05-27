from brownie import FundMe
from scripts.support_functions import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrace_fee = fund_me.getEntranceFee()
    print(f"The current entry fee is {entrace_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrace_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
