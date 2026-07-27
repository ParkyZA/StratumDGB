import hashlib

from stratumdgb.logger import logger


from .header import HeaderBuilder
from .coinbase import CoinbaseBuilder
from .merkle import MerkleTree



class ShareValidator:

    def __init__(self, job_manager):

        self.job_manager = job_manager

        self.submitted_shares = set()


    def validate(self, client, params):

        if not params or len(params) < 5:

            logger.warning(
                "Malformed share submission"
            )

            return False, "Malformed submission"


        worker = params[0]
        job_id = params[1]
        extranonce2 = params[2]
        ntime = params[3]
        nonce = params[4]

        version = params[5] if len(params) > 5 else None

        logger.info(
            f"Validating share: worker={worker} job={job_id} nonce={nonce}, version={version}"
        )


        job = self.job_manager.get_current_job()


        if job is None:

            return False, "No active job"


        if job_id != job.job_id:

            return False, "Unknown job"


        share_key = (
            worker,
            job_id,
            extranonce2,
            ntime,
            nonce
        )


        if share_key in self.submitted_shares:

            return False, "Duplicate share"


        self.submitted_shares.add(
            share_key
        )

        coinbase_hash = CoinbaseBuilder.build(
            job,
            client.extranonce1,
            extranonce2
        )

        logger.info(
            f"Coinbase hash: {coinbase_hash.hex()}"
        )


        merkle_root = MerkleTree.calculate(
            coinbase_hash,
            job.merkle_branches
        )

        logger.info(
            f"Merkle root: {merkle_root.hex()}"
        )


        header = HeaderBuilder.build(
            job,
            merkle_root,
            ntime,
            nonce
        )

        logger.info(f"Header: {header.hex()}")


        header_hash = hashlib.sha256(
            hashlib.sha256(header).digest()
        ).digest()

        logger.info(
            f"Header Hash: {header_hash[::-1].hex()}"
        )

        hash_int = int.from_bytes(
            header_hash,
            byteorder="little"
        )

        logger.info(
            f"Hash Integer: {hash_int}"
        )

        logger.info(
            "Header hashing completed successfully."
        )


        return True, None
