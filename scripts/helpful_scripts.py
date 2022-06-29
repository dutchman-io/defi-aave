from brownie import(
    network,
    config,
    accounts,
    Contract,
    interface,
)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
        "development",
        "ganache-local",
        "mainnet-fork",
        "mainnet-fork-dev"
        ]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account(Index = None, Id= None):
    #accounts(0)
    #accounts.add('env')
    #accounts.load('id')
 
    if Index is not None:
        #print(1)
        return accounts[Index]

    if Id is not None:
        # print(2)
        return accounts.load(Id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        # print(3)
        return accounts[0]
    print('getting from brownie config')
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    """
    This is a contract that will get the contract address from the brownie config
    if defined, otherwise it will deploy with mock version of the contract and 
    return that contract adderss.
    args : contract name(string)
    Returns : brownie.network.contract.projectContract: The most recently deployed contract version.
    """
    contract_type = contract_to_mock[contract_name]
    print(f'2 {network.show_active()}')
    if network.show_active() in  LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(f'The network is {network.show_active()}')
        if len(contract_type) <= 0:
            print('Mocks is deploying')
            deploy_mocks()
        contract = contract_type[-1]
        #MockV3Aggregator[-1]
    else:
        print(f'The networks is {network.show_active()}')
        print('connecting to mocks')
        contract_address = config["networks"][network.show_active()][contract_name]
        #address
        #address
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
         )
        #MockV3Aggregator.abi
    return contract

def deploy_mocks(decimal = DECIMALS, initial_value = STARTING_PRICE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        #print("Deploying Mocks...")
        #mock_price_feed = 
        MockV3Aggregator.deploy(decimal, initial_value, {"from" : account})
        link_token = LinkToken.deploy({'from': account})
        VRFCoordinatorMock.deploy(link_token.address, {'from' : account})
    print("Mocks Deployed!")

def fund_with_link(contract_address, account =None, link_token = None, Amount = None):
    amount = config['networks'][network.show_active()]['fee']
    #print("e", amount)

    account = account if account else get_account()
    print(account)
    link_token = link_token if link_token else get_contract("link_token")
    print(contract_address, account, link_token, amount )

    #tx = link_token.transfer(contract_address, amount, {'from':account})
    
    link_token_contract = interface.LinkTokenInterface(link_token.address)
    tx = link_token_contract.transfer(contract_address, amount, {'from': account})
    
    tx.wait(1)
    print('Funding Contract')

