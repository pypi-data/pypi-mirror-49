Bifrost
---

__important__: Work-In-Progress. No production software.

TOC
+ [Install](#install)
    - [Install form PIP](#install-from-pypi)
    - [Install from Sources](#install-from-sources)
+ [Usage](#usage)
    - [Create Wallet](#create-wallet)
    - [Transfer ETH](#transfer-eth)
    - [Transfer ERC20](#transfer-erc20)
+ [Note](#note)

# Install 

## Install from PyPI 

```
# Virtualenv
(pyenv)$ pip install bifrost

# Main Python shell
$ sudo -H pip install bifrost 
```

## Install from sources

```bash
# Ubuntu 18.04+
# Required packages
sudo apt install -y python3-dev git virtualenv

# Create and activate virtualenv
$ virtualenv -p python3 pyenv
(pyenv) $ source pyenv/bin/activate

# clone Repo
(pyenv) $ git clone https://gitlab.com/dtecdeal/lab/bifrost /path/to/destination/folder
(pyenv) $ cd /path/to/destination/folder/Python
(pyenv) $ python setup.py install
```

# Usage 

## Create wallet

```python

import os
from web3 import Web3
from bifrost import Bifrost

SIGNER_PK = os.environ.get('SIGNER_PK', "{default-signer-pk}")
FACTORY_ADDRESS = os.environ.get('FACTORY_ADDRESS', "{default-factory-address}")
RPC_URL = os.environ.get('RPC_URL', "{default-RPC-URL}")
BIFROST_FACTORY = os.environ.get('BIFROST_FACTORY', "{bifrost-factory}")


w3Provider = Web3.HTTPProvider(RPC_URL)
w3 = Web3(w3Provider)
signer_account = w3.eth.account.privateKeyToAccount(SIGNER_PK)

bifrost = Bifrost(BIFROST_FACTORY, signer_account, w3Provider)

address_salt = 1
address = bifrost.getAddress(address_salt)
address_is_deployed = bifrost.isDeployed(address_salt)

print('''
    Signer: %s
    Salt: %s
    Address: %s
    IsDeployed: %s 
''' % (signer_account.address, address_salt, address, address_is_deployed))
```
## Transfer `ETH`

```python
import os
from web3 import Web3
from bifrost import Bifrost

SIGNER_PK = os.environ.get('SIGNER_PK', "{default-signer-pk}")
FACTORY_ADDRESS = os.environ.get('FACTORY_ADDRESS', "{default-factory-address}")
RPC_URL = os.environ.get('RPC_URL', "{default-RPC-URL}")
BIFROST_FACTORY = os.environ.get('BIFROST_FACTORY', "{bifrost-factory}")

w3Provider = Web3.HTTPProvider(RPC_URL)
w3 = Web3(w3Provider)
signer_account = w3.eth.account.privateKeyToAccount(SIGNER_PK)

bifrost = Bifrost(BIFROST_FACTORY, signer_account, w3Provider)

address_salt = 1

amount = int(.1 * 10 ** 18)

# Transfer ETH
# address should have more than .1 (amount) ETH
tx = bifrost.makeCall(address_salt, signer_account.address, amount)
print('ETH transfer: ', tx.hex())
w3.eth.waitForTransactionReceipt(tx)
```

## Transfer ERC20

```python
import os
import json
from web3 import Web3
from bifrost import Bifrost

SIGNER_PK = os.environ.get('SIGNER_PK', "{default-signer-pk}")
FACTORY_ADDRESS = os.environ.get('FACTORY_ADDRESS', "{default-factory-address}")
RPC_URL = os.environ.get('RPC_URL', "{default-RPC-URL}")
BIFROST_FACTORY = os.environ.get('BIFROST_FACTORY', "{bifrost-factory}")
ERC20_ADDRESS = os.environ.get('ERC20_ADDRESS', '{default-ERC20-address}')


w3Provider = Web3.HTTPProvider(RPC_URL)
w3 = Web3(w3Provider)
signer_account = w3.eth.account.privateKeyToAccount(SIGNER_PK)

bifrost = Bifrost(BIFROST_FACTORY, signer_account, w3Provider)

address_salt = 1

amount = int(.1 * 10 ** 18)
# Transfer ERC20
# address should have more than .1 (amount) ERC20
ERC20_abi = json.load(open('path/to/abi/IERC20.json', 'r'))
ERC20 = w3.eth.contract(abi=ERC20_abi)
call = ERC20.encodeABI('transfer', args=(signer_account.address, amount))
tx = bifrost.makeCall(address_salt, ERC20_ADDRESS, 0, call)
print('ERC20 transfer: ', tx.hex())
```

#### Note
Following error
```
{'code': -32000, 'message': 'gas required exceeds allowance (7447619) or always failing transaction'}
```
Mostly related with `always failing transaction`


_Made it with ❤ by __DTecDeal___
