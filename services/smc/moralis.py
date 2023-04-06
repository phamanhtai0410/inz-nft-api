from moralis import evm_api
from connect import redis_cluster
from lib import Chains, MoralisChains


class MoralisServices:

    @staticmethod
    def get_moralis_chain(chain):
        # currently testnet
        if chain == Chains.ETHEREUM:
            return MoralisChains.GOERLI
        if chain == Chains.BSC:
            return MoralisChains.BSC_TESTNET
        return MoralisChains.BSC_TESTNET

    @classmethod
    def get_nfts_list(cls, chain: str, contract_address: str, page_size=100):
        # web3 = get(web3_providers, chain)
        _api_key = redis_cluster.get('moralis:api_key')
        params = {
            "chain": 'bsc',
            "format": "decimal",
            "limit": page_size,
            # "cursor": cursor,
            "disable_total": False,
            "media_items": False,
            "normalize_metadata": True,
            # "address": web3.to_checksum_address(contract_address)
            "address": contract_address
        }

        _result = evm_api.nft.get_contract_nfts(
            api_key=_api_key,
            params=params,
        )

        return _result
