import asyncio
import traceback

from dbconnector import DBConnector
from orderdata import OrderData


class EOLServer:
    def __init__(self):
        self.address = '10.51.50.1'
        self.port = 8089
        self.loop = asyncio.get_event_loop()
        self.db_connector = DBConnector()

    async def handle_connection(self, reader, writer):
        # we want to get the following data:
        # shipping tracking code
        # scanner info (based on port)
        #
        # then build an OrderData object from this
        # the order data object will automatically determine the shipper

        # then take this order data and send it to the db connector
        # in order to push the data into the local db
        data = b''
        keep_reading = True
        while keep_reading:
            try:
                data += await reader.readline()
                # Check to see if done
                if reader.at_eof():
                    keep_reading = False
            except Exception as e:
                print("Failed to accept data:")
                traceback.print_exc()
                return  # stop handling message at this point

        messages = str(data.decode("utf-8")).split("\r\n")
        ip_addr, client_id = writer.get_extra_info('peername')

        for msg in messages:
            if msg == '':
                continue  # skip entries that are empty
            order = OrderData(msg, ip_addr)
            try:
                result_success = await self.db_connector.push_data(order)
                if result_success:
                    print(f"Finished handling: {order}")
            except Exception as e:
                print("Failed to push data to db:")
                traceback.print_exc()

    def run(self):
        coro = asyncio.start_server(self.handle_connection, host=self.address, port=self.port, loop=self.loop)
        server = self.loop.run_until_complete(coro)

        print(f"Starting Server on: {self.address}")

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("Server close requested")

        server.close()
        self.loop.run_until_complete(server.wait_closed())
        self.loop.close()


if __name__ == '__main__':
    server = EOLServer()
    server.run()
