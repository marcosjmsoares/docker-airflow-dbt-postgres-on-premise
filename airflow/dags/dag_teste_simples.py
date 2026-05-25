from datetime import datetime
from airflow import DAG
from airflow.decorators import task


with DAG(
    dag_id="dag_teste_simples",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["teste", "local"],
) as dag:

    @task(task_id="ola_mundo")
    def tarefa_ola_mundo():
        print("Olá, Airflow!")
        print("DAG de teste executada com sucesso.")

    tarefa_ola_mundo()