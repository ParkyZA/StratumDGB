import hashlib


class MerkleTree:

    @staticmethod
    def calculate(coinbase_hash, branches):
        """
        Calculate the merkle root from the coinbase hash
        and the merkle branches supplied by getblocktemplate().
        """

        merkle = coinbase_hash

        for branch in branches:

            merkle = hashlib.sha256(
                hashlib.sha256(
                    merkle + bytes.fromhex(branch)
                ).digest()
            ).digest()

        return merkle
