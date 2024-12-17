import os
import subprocess
import multiprocessing
from multiprocessing import Queue
import aplicacao
import captura
import inferencia
import modelo


COM_PORT = "COM7"
QUANTIDADE_MINIMA_REGISTROS_INFERENCIA = 100
ZAPI_INSTANCIA = ""
ZAPI_TOKEN = ""
ZAPI_CLIENT_TOKEN = ""
ZAPI_NUMEROS = [""]

def run_django_server():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    subprocess.run(["python", "api/manage.py", "runserver"])

if __name__ == "__main__":

    queue_captura = Queue()
    queue_aplicacao = Queue()

    django_server_process = multiprocessing.Process(target=run_django_server)
    
    captura_process = multiprocessing.Process(target = captura.run_captura, args=(queue_captura,COM_PORT,))
    broker_process = multiprocessing.Process(target = captura.broker, args = (queue_captura,))
    
    modelo_process = multiprocessing.Process(target = modelo.run_treinamento_modelo)

    inferencia_process = multiprocessing.Process(target = inferencia.run_inferencia, args = (
        queue_aplicacao, QUANTIDADE_MINIMA_REGISTROS_INFERENCIA,))

    aplicacao_process = multiprocessing.Process(target = aplicacao.run_aplicacao, args = (queue_aplicacao,))

    django_server_process.start()
    captura_process.start()
    broker_process.start()
    modelo_process.start()
    inferencia_process.start()
    aplicacao_process.start()

    

    try:
        django_server_process.join()
        captura_process.join()
        broker_process.join()
        modelo_process.join()
        inferencia_process.join()
        aplicacao_process.join()
    except KeyboardInterrupt:

        django_server_process.terminate()
        captura_process.terminate()
        broker_process.terminate()
        modelo_process.terminate()
        inferencia_process.terminate()
        aplicacao_process.terminate()

        django_server_process.join()
        captura_process.join()
        broker_process.join()
        modelo_process.join()
        inferencia_process.join()
        aplicacao_process.join()