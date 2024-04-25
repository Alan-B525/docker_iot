import asyncio, logging, os, aiomysql, json, traceback
import aiomqtt

logging.basicConfig(format='%(asctime)s - cliente mqtt - %(levelname)s:%(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

async def main():

    async with aiomqtt.Client(
        os.environ['SERVIDOR'],
        port=1883,
    ) as client:
        await client.subscribe(os.environ['TOPICO'])
        async for message in client.messages:
            logging.info(str(message.topic) + ": " + message.payload.decode("utf-8"))
            datos=json.loads(message.payload.decode('utf8'))
            sql = "INSERT INTO `mediciones` (`sensor_id`, `temperatura`, `humedad`) VALUES (%s, %s, %s)"
            try:
                conn = await aiomysql.connect(host=os.environ["MARIADB_SERVER"], port=3306,
                                            user=os.environ["MARIADB_USER"],
                                            password=os.environ["MARIADB_USER_PASS"],
                                            db=os.environ["MARIADB_DB"])
            except Exception as e:
                logging.error(traceback.format_exc())

            cur = await conn.cursor()

            async with conn.cursor() as cur:
                try:
                    await cur.execute(sql, (message.topic, datos['temperatura'], datos['humedad']))
                    await conn.commit()
                    await cur.close()
                    await conn.ensure_closed()
                except Exception as e:
                    logging.error(traceback.format_exc())
                    # Logs the error appropriately. 

if __name__ == "__main__":
    asyncio.run(main())
