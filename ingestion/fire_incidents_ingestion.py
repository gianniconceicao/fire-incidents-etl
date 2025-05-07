import os
import argparse
import logging
from config import setup_logging, get_script_arguments
from dotenv import load_dotenv
import findspark
import re
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import psycopg2

from schema import fire_incidents_schema

# Initializes logging
setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()
findspark.init()

def to_snake_case(name):
    name = name.strip().lower()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name

def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv('host'),
        port=os.getenv('port'),
        dbname=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password')
    )

if __name__ == "__main__":
    logger.info("Process started")

    vars = get_script_arguments()

    input_file = vars["input_file"]
    ingestion_date = vars["ingestion_date"]
    
    logger.info(
        f"Process arguments: input_file = '{input_file}' and ingestion_date = {ingestion_date}"
    )

    try:
        logger.info("Creating Spark Session...")
        spark = SparkSession.builder \
            .appName("WriteToPostgres") \
            .config("spark.jars.packages", "org.postgresql:postgresql:42.5.4") \
            .getOrCreate()

        logger.info("Reading input file...")
        df = spark.read.csv(
            input_file,
            header=True,
            schema=fire_incidents_schema,
            timestampFormat="yyyy/MM/dd hh:mm:ss a",
            nullValue=""
        )

        logger.info("Reading completed.")


        logger.info("Starting data transformations...")
        df_renamed = df.select([df[col].alias(to_snake_case(col)) for col in df.columns])
        df_renamed = df_renamed.withColumn(
            'incident_date',
            F.to_date(F.col('incident_date'), "yyyy/MM/dd")
        )

        if ingestion_date:
            df_renamed = df_renamed.filter(
                F.col('incident_date') == F.to_date(F.lit(ingestion_date), "yyyy/MM/dd") 
            )
        
        print(df_renamed.count())
        
        logger.info("Trasnformations completed, creating staging table for ingestion...")
        df_renamed.write \
            .format("jdbc") \
            .option(
                "url",
                f"jdbc:postgresql://{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}"
            ) \
            .option("dbtable", os.getenv('raw_temp_table')) \
            .option("user", os.getenv("user")) \
            .option("password", os.getenv("password")) \
            .option("driver", "org.postgresql.Driver") \
            .mode("overwrite") \
            .save()
        logger.info("Starting table created on Postgres...")


        logger.info(
            "Creating Postgres connection and inserting data from the staging table into the "
            "final destination..."
        )
        conn = get_pg_connection()
        cur = conn.cursor()

        column_list = ", ".join(df_renamed.columns)
        cur.execute(f"""
            INSERT INTO fire_incidents ({column_list})
            SELECT {column_list}
            FROM {os.getenv('raw_temp_table')}
            ON CONFLICT (incident_number) DO NOTHING;
        """)
        conn.commit()
        logger.info("New data added to main table... Dropping staging table")

        cur.execute(f"DROP TABLE {os.getenv('raw_temp_table')};")
        conn.commit()

        logger.info("Staging table deleted.")
        logger.info("Process completed.")

    except Exception as e:
        print("Erro durante o processo:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
        print("Conexão encerrada com segurança.")