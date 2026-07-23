from stratumdgb.logger import logger


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


        return True, None
