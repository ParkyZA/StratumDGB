from stratumdgb.logger import logger

class ShareValidator:


    def __init__(self, job_manager):

        self.job_manager = job_manager
        self.submitted_shares = set()

    def validate(self, client, params):

        # ----------------------------------------------------
        # Validate parameter count
        # ----------------------------------------------------

        if len(params) != 5:
            logger.warning("Invalid mining.submit parameters")
            return False

        worker_name, job_id, extranonce2, ntime, nonce = params

        # ----------------------------------------------------
        # Get current mining job
        # ----------------------------------------------------


        job = self.job_manager.get_current_job()


        if job is None:
            logger.warning("No active mining job")
            return False, "No active job"

        # ----------------------------------------------------
        # Verify Job ID
        # ----------------------------------------------------


        if job.job_id != job_id:
            logger.warning(f"Unknown job ID: {job_id}")
            return False, "Unknown job"

        # ----------------------------------------------------
        # Duplicate share detection
        # ----------------------------------------------------

        share_key = (
            job_id,
            extranonce2,
            ntime,
            nonce
        )

        if share_key in self.submitted_shares:
            logger.warning("Duplicate share received")
            return False, "Duplicate share"

        self.submitted_shares.add(share_key)

        # ----------------------------------------------------
        # Stage 2 begins here
        # ----------------------------------------------------
        #
        # coinbase
        # merkle root
        # block header
        # double SHA256
        # target comparison
        #
        # ----------------------------------------------------

        logger.debug(f"Share received from {worker_name} for job {job_id}")

        return True, None
