import base58
import hashlib

def address_to_script_pubkey(address):
    """
    Convert a DigiByte Base58 address into a standard P2PKH scriptPubKey.
    """

    decoded = base58.b58decode_check(address)

    version = decoded[0]

    pubkey_hash = decoded[1:]


    script_pubkey = (
        b"\x76"          # OP_DUP
        b"\xa9"          # OP_HASH160
        b"\x14"          # Push 20 bytes
        + pubkey_hash
        + b"\x88"        # OP_EQUALVERIFY
        + b"\xac"        # OP_CHECKSIG
    )


    return script_pubkey
