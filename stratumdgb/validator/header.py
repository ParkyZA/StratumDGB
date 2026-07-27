import struct

from stratumdgb.logger import logger


class HeaderBuilder:


    @staticmethod

    def build(job, merkle_root, ntime, nonce):


        """
        Build the 80-byte block header from mining job.
        """


        version = struct.pack("<I", job.version)
        prev_hash = bytes.fromhex(job.previousblockhash)[::-1]
        merkle = merkle_root[::-1]

        logger.info(f"Version: {len(version)} bytes")
        logger.info(f"Prev Hash: {len(prev_hash)} bytes")
        logger.info(f"Merkle: {len(merkle)} bytes")


        timestamp = bytes.fromhex(ntime)[::-1]
        bits = bytes.fromhex(job.bits)[::-1]
        nonce_bytes = bytes.fromhex(nonce)[::-1]


        logger.info(f"Timestamp: {len(timestamp)} bytes")
        logger.info(f"Bits: {len(bits)} bytes")
        logger.info(f"Nonce: {len(nonce_bytes)} bytes")


        header = (
            version +
            prev_hash +
            merkle +
            timestamp +
            bits +
            nonce_bytes
        )


        logger.info(f"Header length: {len(header)} bytes")
        logger.info(f"Block Header: {header.hex()}")


        return header
