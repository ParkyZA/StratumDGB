import asyncio

from stratumdgb.config import Config
from stratumdgb.rpc.digibyte import DigiByteRPC
from stratumdgb.jobmanager import JobManager
from stratumdgb.server import StratumServer
from stratumdgb.logger import logger


async def job_loop(job_manager, server):

    while True:

        changed = job_manager.update_job()

        if changed:

            logger.info(
                "New job detected"
            )

            await server.broadcast_job()

        await asyncio.sleep(10)



async def main():

    logger.info("Starting StratumDGB...")


    config = Config()
    config.load()


    rpc = DigiByteRPC(config)


    job_manager = JobManager(rpc)

    job_manager.update_job()

    logger.info(
        f"Current block height: {job_manager.current_job.template['height']}"
    )


    server = StratumServer(
        job_manager,
        host="0.0.0.0",
        port=3333
    )


    asyncio.create_task(
        job_loop(job_manager, server)
    )


    await server.start()



if __name__ == "__main__":

    asyncio.run(main())
