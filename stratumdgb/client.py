from stratumdgb.logger import logger


class MinerClient:

    def __init__(self, reader, writer):

        self.reader = reader
        self.writer = writer

        self.address = writer.get_extra_info("peername")

        self.worker = None
        self.authorized = False

        self.subscription_id = None

        self.extranonce1 = None
        self.extranonce2_size = 4

        self.difficulty = 1

        logger.info(f"New miner connection: {self.address}")


    async def send(self, message):

        data = message + "\n"

        self.writer.write(data.encode())

        await self.writer.drain()


    async def close(self):

        logger.info(f"Closing connection: {self.address}")

        self.writer.close()

        await self.writer.wait_closed()
