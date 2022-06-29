from scripts.helpful_scripts import get_account, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import config, interface, accounts, network


def get_weth(accounts = None):
    #mint weth by deploying eth
    #abi
    #address
    if accounts:
        account = accounts 
    else:
       account = get_account()

    weth = interface.WethInterface(
            config['networks'][network.show_active()]['weth_token']
            )

    tx = weth.deposit({'from' : account, 'value' : 0.1 * 1e18})
    print('Recieved 0.1 WETH')
    return tx

def main():
    get_weth()
