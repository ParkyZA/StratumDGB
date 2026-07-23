import json

from stratumdgb.validator import ShareValidator
from stratumdgb.logger import logger
from stratumdgb.extranonce import generate_extranonce1

class StratumProtocol:


    def __init__(self, client, job_manager):

        self.client = client
        self.job_manager = job_manager
        self.validator = ShareValidator(job_manager)



    async def handle(self, message):

        try:

            request = json.loads(message)

        except json.JSONDecodeError:

            logger.warning(
                f"Invalid JSON from {self.client.address}: {message}"
            )

            return


        method = request.get("method")

        request_id = request.get("id")


        logger.info(
            f"Method {method} from {self.client.address}"
        )


        if method == "mining.configure":

            await self.configure(request_id)


        elif method == "mining.subscribe":

            await self.subscribe(request_id)


        elif method == "mining.submit":

            await self.submit(
                request_id,
                request.get("params")
            )


        elif method == "mining.authorize":

            await self.authorize(
                request_id,
                request.get("params")
            )


        else:

            logger.warning(
                f"Unknown method: {method}"
            )

    async def configure(self, request_id):

        response = {

            "id": request_id,

            "result": {

                "version-rolling": True,

                "version-rolling.mask": "ffffffff"

            },

            "error": None

        }


        await self.client.send(
            json.dumps(response)
        )


        logger.info(
            "Version rolling configured"
        )


    async def subscribe(self, request_id):

        self.client.subscription_id = "dgb-worker"

        self.client.extranonce1 = generate_extranonce1()


        response = {

            "id": request_id,

            "result": [

                [

                    [
                        "mining.set_difficulty",
                        "dgb-difficulty"
                    ],

                    [
                        "mining.notify",
                        "dgb-notify"
                    ]

                ],

                self.client.extranonce1,

                self.client.extranonce2_size

            ],

            "error": None

        }


        await self.client.send(
            json.dumps(response)
        )


        logger.info(
            f"Subscription sent to {self.client.address}"
        )



    async def authorize(self, request_id, params):

        if params and len(params) >= 1:

            self.client.worker = params[0]

            self.client.authorized = True

        response = {

            "id": request_id,

            "result": True,

            "error": None

        }

        await self.client.send(
            json.dumps(response)
        )

        await self.set_difficulty(1)

        await self.notify()

        logger.info(
            f"Worker authorized: {self.client.worker}"
        )


    async def set_difficulty(self, difficulty):

        message = {

            "id": None,

            "method": "mining.set_difficulty",

            "params": [difficulty]

        }

        await self.client.send(
             json.dumps(message)
        )

        logger.info(
            f"Difficulty set to {difficulty} for {self.client.address}"
        )
    async def notify(self):

        job = self.job_manager.current_job

        message = {

            "id": None,

            "method": "mining.notify",

            "params": [

                job.job_id,

                job.previousblockhash,

                job.coinb1,

                job.coinb2,

                job.merkle_branches,

                f"{job.version:08x}",

                job.bits,

                f"{job.curtime:08x}",

                job.clean_jobs

            ]

        }


        await self.client.send(
            json.dumps(message)
        )

        logger.info(
            f"Mining.notify sent for height {job.template['height']}"
        )


    async def submit(self, request_id, params):

        worker_name = params[0] if params else "unknown"

        logger.info(
            f"Share submitted by {self.client.address}: {params}"
        )


        valid, reason = self.validator.validate(self.client, params)


        response = {

            "id": request_id,

            "result": valid,

            "error": None if valid else reason

        }


        await self.client.send(
            json.dumps(response)
        )


        if valid:

            logger.info(
                f"Accepted share from worker={params[0]}, job={params[1]}"

            )

        else:

            logger.warning(
                f"Rejected share from {worker_name}:  {reason}"
            )
