# fire-incidents-etl
Repository for the ETL process responsible for ingesting, transforming, storing, and analyzing data of fire incidents in the city of San Francisco


# Create a local PostgreSQL database with Docker

1 - Ensure you have Docker installed in you machine
2 - Go to the `local_database` folder
3 - Execute the following command on the terminal to build the database image:

```
docker build -t local-postgres-db ./
```

4 - Execute the following command to create the container with the database

```
docker run -d --name local-postgresdb-container -p 5432:5432 local-postgres-db
```

5 - Database details:


# Create a local environment:

1 - 

```
python -m venv venv
```

2 - Activate (command for MacOS)

```
source venv/bin/activate
```

3 - Install the dependencies

```
pip install -r requirements.txt
```


# ETL with dbt

1 -

```
dbt init fire_incident_etl
```

2 - Configure the database:

```
// Enter a number: 1
// host (hostname for the instance): localhost    
// port [5432]: 
// user (dev username): postgres
// pass (dev password): example_password
// dbname (default database that dbt will build objects in): local_db
// schema (default schema that dbt will build objects in): public
// threads (1 or more) [1]: 1
```

3 - To run the project:

```
cd fire_incident_etl
```

```
dbt build
```


# Ingestion process

Running the process

```
cd ingestion
```

```
python fire_incidents_ingestion.py -if input/Fire_Incidents_20250505.csv
```
