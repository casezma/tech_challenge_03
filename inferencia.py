from datetime import datetime
import json
import pandas as pd
import pickle
import requests
import os
import time

from loguru import logger

def run_inferencia(q,quantidade_minima_registros):
    ultima_timestamp = 0
    
    while True:
        logger.info("Iniciando...")
        time.sleep(5)
        logger.info(f"Listando registros a partir de {ultima_timestamp}")
        registros = listar_registros_a_partir_de_timestamp(ultima_timestamp)
        if len(registros) >= quantidade_minima_registros:
            
            df = pd.DataFrame(registros)
            modelo = pegar_ultimo_modelo_disponivel()
            df['velocidade'] = pd.to_numeric(df['velocidade'])
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df['diferenca_velocidade'] = df['velocidade'].diff()  # Variação de velocidade
            df['diferenca_tempo'] = df['timestamp'].diff()  # Diferença de tempo em segundos

            df['aceleracao'] = df['diferenca_velocidade'] / df['diferenca_tempo']

            df = df.dropna()

            colunas = df[['velocidade', 'aceleracao']]

            df['anomalia'] = modelo.fit_predict(colunas)
            anomalias = df[df['anomalia'] == -1]['anomalia'].count()

            if anomalias > 0:
                logger.info("Anomalia de direção detectada...")
                q.put(f"Acelaração/Desaceleração brusca detectada.")

            else:
                logger.info("Acelaração/Desaceleração não detectada...")


def pegar_ultimo_modelo_disponivel():
    maior = None
    for item in os.listdir("modelos"):
        if ".p" in item:
            ts = datetime.strptime(item.replace(".p",""),"%Y%m%d%H%M%S")
            if maior is None or ts > maior:
                maior = ts
    if maior is None:
        return maior
    with open(f'modelos/{maior.strftime("%Y%m%d%H%M%S")}.p','rb') as f:
        return pickle.load(f)

def listar_registros_a_partir_de_timestamp(timestamp):
    lista_registros_timestamp = requests.post(
        "http://127.0.0.1:8000/api/listar-registros-a-partir-de-timestamp",
        json= {"timestamp":timestamp}
        )
    return lista_registros_timestamp.json()