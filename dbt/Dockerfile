FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DBT_PROFILES_DIR=/dbt

RUN pip install --no-cache-dir poetry

# Copia os arquivos de dependências primeiro (cache do Docker)
COPY pyproject.toml poetry.lock /dbt/

WORKDIR /dbt

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

# Copia o projeto inteiro
COPY . /dbt

# WORKDIR aponta para dentro da pasta do projeto dbt
WORKDIR /dbt/projeto_northwind

ENTRYPOINT ["poetry", "run", "dbt"]