# Ambiente Stack: Airflow 3 + dbt Core + Postgres (Local / On-Premise)

Este repositório contém uma infraestrutura de desenvolvimento local baseada em contêineres Docker para orquestração de dados com **Apache Airflow 3** e modelagem/transformação de dados com **dbt Core (Postgres)**.

O objetivo deste projeto é fornecer um ambiente isolado, robusto e pré-configurado para o desenvolvimento de pipelines de dados modernos (ELT).

---

## 🚀 Arquitetura da Stack

O ambiente é orquestrado via [docker-compose.yml](file:///c:/Estudos/Python/ambiente_stack_hsrc/docker-compose.yml) e conta com os seguintes serviços:

1. **`postgres_airflow`**: Banco de dados PostgreSQL 17 dedicado para armazenar os metadados do Apache Airflow.
2. **`airflow-init`**: Inicializa o banco de dados do Airflow (migrações) e cria o usuário administrador padrão (`admin`).
3. **`airflow-dag-processor`**: Componente do Airflow 3 encarregado de processar e parsear os arquivos de DAGs de forma isolada.
4. **`airflow-api-server`**: O servidor da API e interface web do Airflow 3 (exposto na porta `8080`).
5. **`airflow-scheduler`**: Agendador que monitora as DAGs e dispara a execução das tarefas.
6. **`dbt`**: Um container Docker com o dbt Core e o conector `dbt-postgres` instalados via Poetry. Fica em execução contínua (`sleep infinity`) para permitir a execução interativa de comandos de desenvolvimento.

---

## 📁 Estrutura do Projeto

```text
ambiente_stack_hsrc/
├── .envexample            # Exemplo de variáveis de ambiente
├── .env                   # Variáveis de ambiente ativas (não versionado)
├── docker-compose.yml     # Orquestração dos containers da Stack
├── pyproject.toml         # Configuração do Poetry (raiz)
├── airflow/               # Estrutura do Apache Airflow
│   ├── Dockerfile         # Dockerfile customizado para o Airflow com Poetry
│   ├── pyproject.toml     # Gerenciamento de pacotes do Airflow (Poetry)
│   ├── requirements.txt   # Dependências do Airflow (instaladas via pip)
│   ├── dags/              # Pasta local para suas DAGs (volume compartilhado)
│   │   └── dag_teste_simples.py
│   └── plugins/           # Pasta local para Plugins do Airflow
└── dbt/                   # Estrutura do dbt
    ├── Dockerfile         # Dockerfile para o container do dbt
    ├── pyproject.toml     # Dependências do dbt (Poetry)
    ├── profiles.yml       # Configuração de conexão do dbt (Postgres)
    └── projeto_northwind/ # Projeto dbt Northwind para desenvolvimento
        ├── dbt_project.yml
        ├── models/
        └── ...
```

---

## 🛠️ Pré-requisitos

Para rodar este ambiente, você precisará de:

* **Docker** instalado.
* **Docker Compose** (normalmente integrado ao Docker Desktop).
* **Git** para versionamento.
* *Opcional*: **Poetry** (caso queira gerenciar as dependências locais na sua máquina física).

---

## ⚙️ Configuração Passo a Passo

### 1. Preparar o Arquivo de Variáveis de Ambiente
Crie uma cópia do arquivo `.envexample` com o nome `.env`:
```bash
cp .envexample .env
```

Abra o arquivo `.env` e configure os parâmetros necessários. O projeto diferencia as conexões da seguinte forma:
- **`POSTGRES_*`**: Credenciais do banco de dados alvo onde o **dbt** fará a leitura/gravação dos dados (pode ser um banco local ou uma instância remota/RDS).
- **`AIRFLOW_POSTGRES_*`**: Credenciais da instância PostgreSQL dedicada aos metadados do **Airflow** (rodando localmente via docker-compose).

### 2. Inicializar e Subir a Stack
Com as variáveis configuradas, inicie todos os containers em segundo plano:
```bash
docker compose up --build -d
```

> 💡 **Nota**: A primeira execução pode demorar alguns minutos para construir as imagens customizadas (`airflow` e `dbt`) e baixar as dependências.

---

## 🏃 Utilizando a Stack

### 1. Apache Airflow 3
Após a conclusão da inicialização, o Airflow estará acessível no navegador:
* **URL**: [http://localhost:8080](http://localhost:8080)
* **Usuário padrão**: `admin`
* **Senha padrão**: `admin123` (ou a senha que você definir em `AIRFLOW_ADMIN_PASSWORD` no `.env`)

As DAGs e os plugins são sincronizados em tempo real do seu computador para o container através das pastas locais:
- `./airflow/dags/` (contém uma DAG de teste `dag_teste_simples.py`)
- `./airflow/plugins/`

---

### 2. dbt Core
O container do `dbt` compartilha o diretório `./dbt` local. Como ele é mantido ativo por padrão, você pode executar todos os comandos interativos diretamente dentro dele usando `docker compose exec`:

* **Testar conexão com o banco de dados (Postgres)**:
  ```bash
  docker compose exec dbt dbt debug
  ```

* **Executar os modelos dbt**:
  ```bash
  docker compose exec dbt dbt run
  ```

* **Executar os testes de dados**:
  ```bash
  docker compose exec dbt dbt test
  ```

* **Gerar a documentação do dbt**:
  ```bash
  docker compose exec dbt dbt docs generate
  ```

---

## 🛑 Parando o Ambiente

Para parar e remover os contêineres e redes da stack:
```bash
docker compose down
```

Se desejar apagar também os volumes de dados locais persistidos (como o banco de dados de metadados do Airflow):
```bash
docker compose down -v
```
