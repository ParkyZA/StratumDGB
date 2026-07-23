import hashlib
from stratumdgb.logger import logger


class ShareValidator:

    def __init__(self, job_manager,client,):

        self.job_manager = job_manager
        self.client = client

    def validate(self, params):

        if len(params) != 6:
            logger.warning(
                f"Invalid parameter count: {len(params)}"
            )
            return False, "Invalid parameters"

        worker, job_id, extranonce2, ntime, nonce, version = params

        logger.info(
            f"Validating share: worker={worker} job={job_id}"
        )

        job = self.job_manager.current_job

        if job is None:
            logger.warning("No active mining job.")
            return False, "No active mining job"

        if job.job_id != job_id:
            logger.warning(
                f"Unknown job ID {job_id} (current: {job.job_id})"
            )
            return False, "Job not found"


        fields = {
            "extranonce2": extranonce2,
            "ntime": ntime,
            "nonce": nonce,
            "version": version,
        }

        for name, value in fields.items():

            if len(value) != 8:
                logger.warning(f"{name} has invalid length")
                return False, f"Invalid {name}"

        if not self.is_hex(value):
            logger.warning(f"{name} is not hexadecimal")
            return False, f"Invalid {name}"


    def is_hex(self, value):

        try:
            bytes.fromhex(value)
            return True

        except ValueError:
            return False


        logger.info(
            f"Matched job {job.job_id} at height {job.height}"
        )

        logger.debug(
            f"extranonce2={extranonce2} ntime={ntime} nonce={nonce} version={version}"
        )





        #
        # Cryptographic validation starts here
        # (next stage)
        #


        return True, None
