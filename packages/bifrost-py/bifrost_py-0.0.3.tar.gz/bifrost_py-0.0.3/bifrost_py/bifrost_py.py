import os
import json
import web3

# HERE LOCATION
HERE = os.path.dirname(os.path.abspath(__file__))


class Bifrost:

    def __init__(self, factory, signer_account, provider):
        self.w3 = web3.Web3(provider)
        abiFactory = json.load(
            open(os.path.join(HERE, 'abi/Bifrost.json'), 'r')
        )
        self.factory = self.w3.eth.contract(
            address=factory,
            abi=abiFactory
        )
        self.abiProxy = json.load(
            open(os.path.join(HERE, 'abi/BifrostProxy.json'), 'r')
        )
        self.signer = signer_account
    
    def getAddress(self, salt, signer_account=None):
        _signer = self.signer if signer_account is None else signer_account
        address = self.factory.functions.getDeploymentAddress(salt, _signer.address).call()
        return self.w3.toChecksumAddress(address)

    def isDeployed(self, salt, signer_account=None):
        address = self.getAddress(salt, signer_account)
        proxy = self.w3.eth.contract(
            address=address,
            abi=self.abiProxy
        )
        try:
            exist = proxy.functions.exist().call()
        except web3.exceptions.BadFunctionCallOutput:
            exist = False
        return exist

    def makeCall(self, salt, destination, value, data=None, signer_account=None):
        _signer = self.signer if signer_account is None else signer_account
        _data = b'' if data is None else data
        # Generate TX
        tx = self.factory.functions.makeCall(salt, destination, value, _data).buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(_signer.address),
            'from': _signer.address
        })
        # Sign TX
        signed_tx = self.signer.signTransaction(tx)
        # Send TX
        return self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
