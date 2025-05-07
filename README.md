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