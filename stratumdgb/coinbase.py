import struct


from stratumdgb.logger import logger
from stratumdgb.address import address_to_script_pubkey
from stratumdgb.config import POOL_ADDRESS

class CoinbaseBuilder:

    def __init__(self, template):
        self.template = template

    def encode_script_number(self, value):
        """
        Encode an integer using Bitcoin Script's minimal numeric encoding.
        """
        if value == 0:
            return b""

        result = bytearray()

        while value:
            result.append(value & 0xff)
            value >>= 8

        if result[-1] & 0x80:
            result.append(0)

        return bytes(result)

    def build(self):


        logger.warning("########## COINBASE BUILDER EXECUTED ##########")

        #
        # Information from getblocktemplate
        #
        extranonce1 = b""
        height = self.template["height"]
        coinbase_value = self.template["coinbasevalue"]
        transactions = self.template["transactions"]

        logger.info(
            f"Coinbase value: {coinbase_value} ({type(coinbase_value)})"
        )

        #
        # Transaction header
        #

        version = struct.pack("<I", 1)

        input_count = b"\x01"

        prev_txid = b"\x00" * 32

        prev_index = struct.pack("<I", 0xffffffff)

        #
        # BIP34 block height
        #

        height = self.encode_script_number(height)

        height_field = bytes([len(height)]) + height

        extranonce1 = b""

        extranonce2_size = 4

        pool_flags = b"/StratumDGB/"

        script_sig_part1 = (
            height_field +
            extranonce1
        )

        script_sig_part2 = (
            pool_flags
        )

        script_sig_length = (
            len(script_sig_part1)
            + extranonce2_size
            + len(script_sig_part2)
        )

        script_sig_length_field = bytes([script_sig_length])

        coinbase_input = (
            prev_txid +
            prev_index +
            script_sig_length_field +
            script_sig_part1
        )

        sequence = struct.pack("<I", 0xffffffff)
        coinbase_input_tail = (
            script_sig_part2 +
            sequence
        )

        output_count = b"\x01"

        reward = struct.pack("<Q", coinbase_value)

        script_pubkey = b""
        script_pubkey_length = b"\x00"

        script_pubkey = address_to_script_pubkey(POOL_ADDRESS)
        logger.debug("scriptPubKey:", script_pubkey.hex())
        script_pubkey_length = bytes([len(script_pubkey)])
        reward_output = (
            reward +
            script_pubkey_length +
            script_pubkey
        )

        locktime = struct.pack("<I", 0)

        coinbase_tx = (
            version +
            input_count +
            coinbase_input +
            coinbase_input_tail +
            output_count +
            reward_output +
            locktime
        )
        logger.debug("Coinbase TX partial:")
        coinbase1 = (
            version +
            input_count +
            coinbase_input
        )

        coinbase2 = (
            coinbase_input_tail +
            output_count +
            reward_output +
            locktime
        )


        logger.debug("Coinbase1:", coinbase1.hex())
        logger.debug("Coinbase2:", coinbase2.hex())

        logger.debug("Coinbase TX partial:")
        logger.debug(coinbase_tx.hex())

        return (
            coinbase1.hex(),
            coinbase2.hex()
        )
