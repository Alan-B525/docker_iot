import asyncio
import logging
import os
import ssl
import aiomqtt

async def manejar_mensaje_topico_1(topico, payload):
    logging.info(f'Corrutina manejar_mensaje_topico_1 - Tópico: {topico}, Mensaje: {payload.decode()}')

async def manejar_mensaje_topico_2(topico, payload):
    logging.info(f'Corrutina manejar_mensaje_topico_2 - Tópico: {topico}, Mensaje: {payload.decode()}')

async def suscribirse_a_todos_los_mensajes(cliente, topicos):
    try:
        await asyncio.gather(*[cliente.subscribe(topico) for topico in topicos])
        logging.info(f'Suscrito a los tópicos: {", ".join(topicos)}')
        async for mensaje in cliente.messages:
            if mensaje.topic == topicos[0]:
                await manejar_mensaje_topico_1(mensaje.topic, mensaje.payload)
            elif mensaje.topic == topicos[1]:
                await manejar_mensaje_topico_2(mensaje.topic, mensaje.payload)
    except aiomqtt.MQTTError as e:
        logging.error(f'Error de MQTT: {e}')

async def publicar(cliente, topico):
    contador = 0
    try:
        while True:
            await asyncio.sleep(3)  # Incremento cada 3 segundos
            contador += 1
            await cliente.publish(topico, f'Contador: {contador}')
            await asyncio.sleep(2)  # Publicar cada 5 segundos
    except aiomqtt.MQTTError as e:
        logging.error(f'Error de MQTT al publicar en el tópico {topico}: {e}')

async def main():
    servidor = os.getenv('SERVIDOR', 'localhost')
    topico_subs_1 = os.getenv('TOPICO_SUBS_1', 'alanb/subs/1')
    topico_subs_2 = os.getenv('TOPICO_SUBS_2', 'alanb/subs/2')
    topico_pub = os.getenv('TOPICO_PUB', 'alanb/pub')
    
    tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    tls_context.verify_mode = ssl.CERT_REQUIRED
    tls_context.check_hostname = True
    tls_context.load_default_certs()

    async with aiomqtt.Client(
        servidor,
        port=8883,
        tls_context=tls_context,
    ) as cliente:
        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(suscribirse_a_todos_los_mensajes(cliente, [topico_subs_1, topico_subs_2]))
                tg.create_task(publicar(cliente, topico_pub))
        except KeyboardInterrupt:
            logging.info("Detenido por el usuario.")
        except Exception as e:
            logging.error(f'Error inesperado: {e}')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - Corrutina: %(funcName)s: %(message)s', level=logging.INFO, datefmt='%d/%m/%Y %H:%M:%S %z')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Detenido por el usuario.")
