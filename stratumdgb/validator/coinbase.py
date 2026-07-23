import hashlib


class CoinbaseBuilder:

    @staticmethod
    def build(job, extranonce1, extranonce2):
        """
        Build a temporary coinbase transaction.

        For now this is only a placeholder.
        Later we'll insert the real coinbase script.
        """

        data = (
            job.job_id
            + extranonce1
            + extranonce2
        ).encode()

        return hashlib.sha256(data).digest()
