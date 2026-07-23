from stratumdgb.coinbase import CoinbaseBuilder


class MiningJob:


    def __init__(self, template, job_id):

        self.template = template
        self.job_id = job_id

        self.height = template["height"]
        self.previousblockhash = template["previousblockhash"]
        self.version = template["version"]
        self.bits = template["bits"]
        self.curtime = template["curtime"]

        #
        # These are placeholders for now.
        # We'll populate them properly later.
        #

        builder = CoinbaseBuilder(template)
        self.coinb1, self.coinb2 = builder.build()
        self.merkle_branches = []
        self.clean_jobs = True

    def __str__(self):

        return (
            f"\n"
            f"Job ID          : {self.job_id}\n"
            f"Height          : {self.height}\n"
            f"Previous Block  : {self.previousblockhash}\n"
            f"Version         : {self.version:08x}\n"
            f"Bits            : {self.bits}\n"
            f"Time            : {self.curtime:08x}\n"
            f"Coinb1 Length   : {len(self.coinb1)}\n"
            f"Coinb2 Length   : {len(self.coinb2)}\n"
            f"Merkle Branches : {len(self.merkle_branches)}"
        )
