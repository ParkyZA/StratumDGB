from stratumdgb.logger import logger
from stratumdgb.jobs import MiningJob

class JobManager:

    def __init__(self, rpc):

        self.rpc = rpc

        self.current_job = None

        self.job_counter = 0


    def get_current_job(self):
        return self.current_job


    def update_job(self):

        new_job = self.rpc.get_block_template()


        logger.info(f"RPC HEIGHT: {new_job['height']}")
        logger.info(f"RPC PREV  : {new_job['previousblockhash']}")

        if self.current_job is None:

            self.job_counter += 1

            self.current_job = MiningJob(
                new_job,
                str(self.job_counter)
            )

            logger.debug(
                f"New mining job created: {self.current_job.job_id} created for block {new_job['height']}"
        )


            return True



        if new_job["previousblockhash"] != self.current_job.template["previousblockhash"]:

            self.job_counter += 1

            self.current_job = MiningJob(
                new_job,
                str(self.job_counter)
            )

            logger.debug(
                f"New mining job created: {self.current_job.job_id} created for block {new_job['height']}"
        )
        

            logger.debug(f"Current job: {self.current_job}")

            return True


        return False


