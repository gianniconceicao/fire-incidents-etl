# fire-incidents-etl
Este repositório é ser um exemplo prático de um processo para ingestão, transformação e análise de dados de dados de incidentes de incêndio na cidade de São Francisco utilizando dados publicos disponíveis em: https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric/about_data

# Estrutura do projeto
O projeto é dividido em duas etapas principais:

### 1 - Ingestão de dados
Processo responsável por ler os arquivos CSV de input e escrevê-los em um banco Postgres de destino.

Etapas do processo:

* Leitura do CSV de input utilizando Spark e primeira validação feita ao adicionar o schema correto para leitura da informação
* Os nomes das colunas são alteradas para `snake_case`
* Realização de filtros com base no argumentos de input
* Dados são salvos em uma tabela temporária no banco Postgres local.
* É executado um comando do tipo `INSERT ... ON CONFLICT DO NOTHING` para inserir os novos dados à tabela final tendo a coluna `incident_number` como sendo a chave primária, não podendo haver valores repetidos.
* Tabela temporária é deletada

Resumo sobre o processo

* Processo presente na pasta `fire_incident_ingestion`
* Tecnologias:
    * Spark (pySpark) para leitura e validações dos arquivos de entrada
    * Postgres como datawarehouse
* Estrutura de arquivos:
    * Pasta `input`: Pasta onde o arquivo de input é adicionado (neste caso, ele pode ser baixado manualmente no link disponível acima)
    * `fire_incidents_ingestion.py`: Arquivo principal do processo contendo a logica de ingestão dos dados e validações.
    * `schema.py`: Arquivo auxiliar contendo o schema Spark para a leitura correta dos dados de entrada
    * `config.py`: Arquivo contendo configurações do processo como configuração de logs e argumentos do projeto.
    * `create_raw_fire_incidents.sql`: Arquivo contendo o comando SQL utilizado para criação inicial da tabela raw no banco Postgres

### 2 - Transformações dos dados
Processo responsável por criar um modelo medallion de dados, limpando os dados nas camadas bronze e prata e criando análises e insights na camada gold.

Como exemplo, na camada gold foram criadas análises e queries indicando o numero total de incidentes, número de incidentes com e sem ferimentos e mortes.

* Processo presente na pasta `fire_incident_transformations`
* Tecnologias:
    * dbt para criação do data lake
    * Postgres como datawarehouse para transformações
* Estrutura de modelos do dbt:
    * Pasta `bronze`: Leitura dos arquivos raw populados pelo processo de ingestão e realização da uma primeira camada de limpeza de dados, removendo registros onde `neighborhood_district` e `battalion` estão vazios.
    * Pasta `silver`: Segunda camada de normalização e limpeza dos dados (para este exemplo estamos apenas selecionando certas colunas desejadas).
    * Pasta `gold`: Camada de dados análises de negócios e geração de insights

# Como executar o projeto completo

Para execução do projeto é considerando que na máquina já está instalado:
* Python
* Docker
* Spark

A seguir estão as etapas sequenciais para execução do projeto:

### 0 - Criação do arquivo `.env`

Etapa 0 do projeto, criar um novo arquivo `.env` na raíz do projeto e inserior o conteúdo do arquivo `.env_DEV`.

### 1 - Criação do banco de dados local
Para criação do banco de dados Postgres local será utilizado o arquivo `Dockerfile` presente na pasta `local_database`.

* 1.1 - Va para a pasta `local_database`

* 1.2 - Execute the following command on the terminal to build the database image (por motivos de simplicidade o nome do banco e senha estão presentes no arquivo):

```
docker build -t local-postgres-db ./
```

* 1.3 - Execute the following command to create the container with the database

```
docker run -d --name local-postgresdb-container -p 5432:5432 local-postgres-db
```

* 1.4 - Os detalhes da conexão com o banco estão presentes no arquivo `.env_DEV`

### 2 - Criação do ambiente virtual Python

* 2.1 - Na pasta raiz do projeto crie o virtual environment:

```
python -m venv venv
```

* 2.2 - Activate the virtual environment (command for MacOS)

```
source venv/bin/activate
```

* 2.3 - Install the dependencies

```
pip install -r requirements.txt
```

### 3 - Execução do processo de ingestão

* 3.1 - Vá para o folder contendo os arquivos do processo:

```
cd fire_incident_ingestion
```

* 3.2 - Utilize o comando SQL presente em `create_raw_fire_incidents.sql` para criar a tabela no banco Postgres local.

* 3.3 - Execute o processo com o comando:

```
python fire_incidents_ingestion.py -if input/Fire_Incidents_20250505.csv
```

Substitua `input/Fire_Incidents_20250505.csv` pelo caminho relativo e nome do arquivo que foi baixado no link acima.

O process também aceita um segundo argumento, `--ingestion-date`. Este argumento pode ser utilizado casa seja necessário selecionar apenas dados de terminado dia para casos de reprocessamento. O formato é `YYYY/MM/DD`.


### 4 - Execução do processo de transformação

* 4.1 - Vá para o folder contendo os arquivos do processo:

```
cd fire_incident_transformations
```

* 4.2 - Execute o processo dbt com o comando:

```
dbt build
```

# TODOs

Estas são algumas modificações e melhorias no processo para serem feitas no futuro (considerando que este é um processo para prática e não tem o objetivo de ir para produção)

* Process de ingestão
    * Adicionar comentários ao longo do código para auxiliar o entendimento
    * Adicionar documentação às funções

* Process de ingestão
    * Adicionar comentários às queries dos modelos dbt
    * Adicionar novos modelos nas camadas silver e gold com base em regras de negócios

* Outros
    * Adicionar orquestração com Airflow