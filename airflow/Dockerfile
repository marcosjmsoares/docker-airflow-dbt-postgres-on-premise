# ============================================================
# Dockerfile do Airflow com Poetry
# Baseado na imagem oficial do Airflow (já inclui dependências
# do sistema, banco de dados e configurações padrão)
# ============================================================
FROM apache/airflow:3.1.1-python3.12

# Variáveis de ambiente
ENV AIRFLOW_HOME=/opt/airflow \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# Define o diretório de trabalho
WORKDIR /opt/airflow

# Copia o restante do projeto (DAGs, plugins, etc.)
COPY dags/ ./dags/
COPY plugins/ ./plugins/

# Porta do Airflow Webserver
EXPOSE 8080

# Inicializa o banco e sobe o webserver + scheduler
CMD ["airflow", "standalone"]