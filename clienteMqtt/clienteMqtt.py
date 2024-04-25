import asyncio, ssl, certifi, logging, os
import aiomqtt

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')

async def contador():
    count = 0
    while True:
        await asyncio.sleep(3)
        count += 1
        logging.info(f'Contador: {count}')

async def main():
    servidor = os.getenv('SERVIDOR', 'localhost')
    tópico_subs_1 = os.getenv('TOPICO_SUBS_1', 'topic/subs/1')
    tópico_subs_2 = os.getenv('TOPICO_SUBS_2', 'topic/subs/2')
    tópico_pub = os.getenv('TOPICO_PUB', 'topic/pub')
    
    tls_context = ssl.create_default_context(cafile=certifi.where())

    async with aiomqtt.Client(
        servidor,
        port=8883,
        tls_context=tls_context,
    ) as client:
        await asyncio.gather(
            client.subscribe(tópico_subs_1),
            client.subscribe(tópico_subs_2),
            publicador(client, tópico_pub),
            contador(),
        )

async def publicador(client, tópico):
    count = 0
    while True:
        await asyncio.sleep(5)
        count += 1
        await client.publish(tópico, f'Contador: {count}')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Detenido por el usuario.")
