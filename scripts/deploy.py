from brownie import FundMe, accounts, network, config, MockV3Aggregator
from scripts.support_functions import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fundMe():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        priceFeed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        priceFeed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(priceFeed_address, {"from": account})
    # , publish_source=config["networks"][network.show_active()].get("verify")
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fundMe()
