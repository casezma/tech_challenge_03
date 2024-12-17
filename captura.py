import obd
import time
from datetime import datetime

import requests
import traceback

from loguru import logger


def run_captura(q,com_port):
    logger.info("Iniciando captura/run...")
    for _ in range(1000):
        try:
            
            connection = obd.OBD(com_port) 
            
            if connection.status() == obd.OBDStatus.NOT_CONNECTED:
                logger.info(f"Tentando conectar a {com_port}...")
                time.sleep(1)
                continue
            logger.info(f"Conectado a {com_port}...")
            break
        except Exception as ex:
            logger.error(f"Tentando conectar a {com_port}...")
            time.sleep(1)
            
    
    while True:
        
        time.sleep(0.5)
        cmd = obd.commands.SPEED 
        response = connection.query(cmd) # send the command, and parse the response
        velocidade = float(str(response.value).replace("kilometer_per_hour","").strip())
        logger.info(f"Velocidade..{velocidade}")
        if velocidade >= 0:
            timestamp = datetime.now().timestamp()
            q.put((timestamp,velocidade))

def broker(q):
    dados = []
    while True:
        try:
            timestamp,velocidade = q.get()
            dados.append({
                "timestamp": timestamp,
                "velocidade": velocidade
            })
            if len(dados) >= 10:
                enviar_dados(dados)
                dados.clear()
        except:
            logger.info("Erro",traceback.format_exc())


def enviar_dados(dados):
    requests.post(url = "http://127.0.0.1:8000/api/criar-registro",json= {"data":dados})
    