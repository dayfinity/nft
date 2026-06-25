```python id="x7nt52"
from web3 import Web3
from datetime import datetime
import json
import uuid


class NetworkProfile:

    def __init__(self):
        self.name = "base"
        self.chain_id = 8453
        self.rpc_url = "https://mainnet.base.org"

    def as_dict(self):
        return {
            "name": self.name,
            "chain_id": self.chain_id
        }


class AssetContext:

    def __init__(self):
        self.asset_type = "NFT"
        self.operation = "mint"
        self.group = "collection"

    def export(self):
        return {
            "asset_type": self.asset_type,
            "operation": self.operation,
            "group": self.group
        }


class ContractSigner:

    def __init__(
        self,
        private_key,
        contract_address
    ):
        self.network = NetworkProfile()

        self.web3 = Web3(
            Web3.HTTPProvider(
                self.network.rpc_url
            )
        )

        self.private_key = private_key

        self.account = (
            self.web3.eth.account.from_key(
                private_key
            )
        )

        self.contract_address = (
            Web3.to_checksum_address(
                contract_address
            )
        )

        self.context = AssetContext()

    def connected(self):

        return self.web3.is_connected()

    def wallet_address(self):

        return self.account.address

    def next_nonce(self):

        return (
            self.web3.eth.get_transaction_count(
                self.account.address
            )
        )

    def current_gas_price(self):

        return self.web3.eth.gas_price

    def metadata(self):

        return {
            "id": str(uuid.uuid4()),
            "timestamp": (
                datetime.utcnow().isoformat()
            ),
            "network": (
                self.network.as_dict()
            ),
            "context": (
                self.context.export()
            )
        }

    def encoded_data(self):

        payload = json.dumps(
            self.metadata()
        ).encode()

        return "0x" + payload.hex()

    def build_transaction(self):

        return {
            "to": self.contract_address,
            "value": 0,
            "gas": 175000,
            "gasPrice": (
                self.current_gas_price()
            ),
            "nonce": (
                self.next_nonce()
            ),
            "chainId": (
                self.network.chain_id
            ),
            "data": (
                self.encoded_data()
            )
        }

    def sign_transaction(
        self,
        transaction
    ):

        return (
            self.web3.eth.account.sign_transaction(
                transaction,
                self.private_key
            )
        )

    def create_report(
        self,
        signed_tx
    ):

        report = {
            "wallet": (
                self.wallet_address()
            ),
            "network": (
                self.network.name
            ),
            "NFT": (
                self.context.asset_type
            ),
            "mint": (
                self.context.operation
            ),
            "collection": (
                self.context.group
            ),
            "hash": (
                signed_tx.hash.hex()
            )
        }

        return report

    def display_report(
        self,
        report
    ):

        print(
            json.dumps(
                report,
                indent=2
            )
        )


def initialize():

    private_key = (
        "YOUR_PRIVATE_KEY"
    )

    contract_address = (
        "0x1234567890123456789012345678901234567890"
    )

    return ContractSigner(
        private_key,
        contract_address
    )


def run():

    signer = initialize()

    if not signer.connected():
        raise RuntimeError(
            "Network connection unavailable"
        )

    transaction = (
        signer.build_transaction()
    )

    signed_tx = (
        signer.sign_transaction(
            transaction
        )
    )

    report = (
        signer.create_report(
            signed_tx
        )
    )

    print(
        "Contract interaction signed"
    )

    signer.display_report(
        report
    )

    print(
        "Network:",
        signer.network.name
    )

    print(
        "Asset:",
        signer.context.asset_type
    )

    print(
        "Action:",
        signer.context.operation
    )

    print(
        "Group:",
        signer.context.group
    )

    print(
        "Transaction Hash:"
    )

    print(
        signed_tx.hash.hex()
    )


if __name__ == "__main__":
    run()
```
