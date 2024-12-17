from loguru import logger
import requests
from main import ZAPI_INSTANCIA, ZAPI_CLIENT_TOKEN, ZAPI_NUMEROS, ZAPI_TOKEN


def run_aplicacao(q):
    logger.info("Iniciando Aplicação")
    while True:
        mensagem = q.get()
        logger.info(f"Nova mensagem: {mensagem}")
        enviar_via_whatsapp(mensagem)

def enviar_via_whatsapp(mensagem):
    logger.info(mensagem)

    for numero in ZAPI_NUMEROS:
        data = {
                "message":mensagem,
                "phone":numero
            }
        resposta = requests.post(
            f"https://api.z-api.io/instances/{ZAPI_INSTANCIA}/token/{ZAPI_TOKEN}/send-text",
            json = data,
            headers={"Client-Token": ZAPI_CLIENT_TOKEN}
        )
        logger.info(resposta.json())