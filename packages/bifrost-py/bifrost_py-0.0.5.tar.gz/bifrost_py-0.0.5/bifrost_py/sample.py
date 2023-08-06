from web3 import Web3
import json
from bifrost import Bifrost

SIGNER_PK = "b961c45b00dbc70e11cacc8e9ae15cd889ac98df2e38ec2fcafc37ddbe31721e"
FACTORY_ADDRESS = "0xb442b6b2F19cd70799B3987DfA069a8b7c9EA6B3"
RPC_URL = "https://rinkeby.infura.io/v3/"
BIFROST_FACTORY = "0xb442b6b2F19cd70799B3987DfA069a8b7c9EA6B3"
ERC20_ADDRESS = "0x46324Fde2E0347aEa72BA2A085b30E68556ac294"

try:
    from local_settings import *
except ModuleNotFoundError:
    pass

w3Provider = Web3.HTTPProvider(RPC_URL)
w3 = Web3(w3Provider)
signer_account = w3.eth.account.privateKeyToAccount(SIGNER_PK)

bifrost = Bifrost(BIFROST_FACTORY, signer_account, w3Provider)

address_salt = 3
address = bifrost.getAddress(address_salt)
address_is_deployed = bifrost.isDeployed(address_salt)
print('''
    Signer: %s
    Salt: %s
    Address: %s
    IsDeployed: %s 
''' % (signer_account.address, address_salt, address, address_is_deployed))

amount = int(.1 * 10 ** 18)

# Transfer ETH
# address shoul have more than .1 (amount) ETH
tx = bifrost.makeCall(address_salt, signer_account.address, amount)
print('ETH transfer: ', tx.hex())
w3.eth.waitForTransactionReceipt(tx)

# Transfer ERC20
# address shoul have more than .1 (amount) ERC20
ERC20_abi = json.load(open('./abi/IERC20.json', 'r'))
ERC20 = w3.eth.contract(

    abi=ERC20_abi
)
call = ERC20.encodeABI('transfer', args=(signer_account.address, amount))
tx = bifrost.makeCall(address_salt, ERC20_ADDRESS, 0, call)
print('ERC20 transfer: ', tx.hex())


