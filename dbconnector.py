import traceback

import aiomysql

from orderdata import OrderData


class DBConnector:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.db = "scans_raw"

    async def push_data(self, order: OrderData) -> bool:
        connection = await aiomysql.connect(host=self.host,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            autocommit=True)

        sql_command = "INSERT INTO scans_raw (code, scanner, shipper) VALUES (%s, %s, %s);"
        values = (order.tracking_num, order.source, order.shipper)

        try:
            async with connection.cursor() as cur:
                await cur.execute(sql_command, values)
                await connection.ensure_closed()
            return True
        except:
            print("Failure in DBConnector")
            traceback.print_exc()
            return False
