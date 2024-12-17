from datetime import datetime
import pickle
import requests
from sklearn.ensemble import IsolationForest
import pandas as pd
import time

from loguru import logger

def run_treinamento_modelo():
    
    estado = "TREINAR_MODELO"
    ultima_timestamp = 0
    
    while True:
        logger.info("Iniciando...")
        time.sleep(10)
        if estado == "TREINAR_MODELO":
            lista_registros = listar_todos_os_registros()
            if len(lista_registros) == 0:
                continue
            ultima_timestamp = lista_registros[-1]['timestamp']
            df = pd.DataFrame(lista_registros)
            df['velocidade'] = pd.to_numeric(df['velocidade'])
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df['diferenca_velocidade'] = df['velocidade'].diff()  # Variação de velocidade
            df['diferenca_tempo'] = df['timestamp'].diff()  # Diferença de tempo em segundos

            df['aceleracao'] = df['diferenca_velocidade'] / df['diferenca_tempo']

            df = df.dropna()

            colunas = df[['velocidade', 'aceleracao']]

            isolation_forest = IsolationForest(contamination=0.1, random_state=42)
            isolation_forest.fit_predict(colunas)
            logger.warning("NOVO MODELO TREINADO")
            exportar_modelo(isolation_forest)
            estado = "AGUARDAR_MAIS_DADOS"

        elif estado == "AGUARDAR_MAIS_DADOS":
            logger.info(f"Listando registros a partir de {ultima_timestamp}")
            items = listar_registros_a_partir_de_timestamp(ultima_timestamp)
            if len(items) > 500:
                logger.info("Alterando estado para TREINAR_MODELO")
                estado = "TREINAR_MODELO"

def exportar_modelo(modelo):
    with open(f"modelos/{datetime.now().strftime('%Y%m%d%H%M%S')}.p","wb") as f:
        logger.warning("MODELO SALVO")
        pickle.dump(modelo,f)

def listar_todos_os_registros():
    lista_registros = requests.get("http://127.0.0.1:8000/api/listar-registros")
    return lista_registros.json()

def listar_registros_a_partir_de_timestamp(timestamp):
    lista_registros_timestamp = requests.post(
        "http://127.0.0.1:8000/api/listar-registros-a-partir-de-timestamp",
        json = {"timestamp":timestamp}
        )
    return lista_registros_timestamp.json()