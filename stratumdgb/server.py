import asyncio

from stratumdgb.client import MinerClient
from stratumdgb.logger import logger
from stratumdgb.protocol import StratumProtocol

class StratumServer:

    def __init__(self, job_manager, host="0.0.0.0", port=3333):

        self.job_manager = job_manager

        self.host = host
        self.port = port

        self.server = None

        self.clients = []

    async def broadcast_job(self):

        logger.info(
            f"Broadcasting new job to {len(self.clients)} miners"
        )

        for client in self.clients:

            if client.authorized:

                logger.info(
                    f"Sending job to authorized miner {client.address}"
                )

                await client.protocol.notify()

                logger.info(
                f"New job sent to {client.address}"
                )

    async def start(self):

        self.server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port,
            reuse_address=True,

        )

        address = self.server.sockets[0].getsockname()

        logger.info(f"Stratum server listening on {address}")


        async with self.server:
            await self.server.serve_forever()


    async def handle_client(self, reader, writer):

        logger.info(">>> ENTERED handle_client() <<<")

        try:

            client = MinerClient(reader, writer)

            protocol = StratumProtocol(
                client,
                self.job_manager
            )

            logger.info("Protocol initialization complete")

            client.protocol = protocol


            logger.info("Protocol created")

            self.clients.append(client)


            while True:

                logger.info("Waiting for miner data...")


                data = await reader.readline()

                logger.info(f"Received bytes: {data}")

                if not data:
                    break

                message = data.decode().strip()

                logger.info(f"RAW MESSAGE: {message}")

                await protocol.handle(message)


        except Exception as e:

            logger.exception(
                f"Client error {client.address}"
            )


        finally:

            await client.close()

            if client in self.clients:
                self.clients.remove(client)

            logger.info(
                f"Disconnected: {client.address}"
            )
