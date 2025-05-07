import os
from dotenv import load_dotenv
import findspark
import re
from pyspark.sql import SparkSession

from ingestion.schema import fire_incidents_schema

load_dotenv()
findspark.init()

def to_snake_case(name):
    name = name.strip().lower()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", "_", name)
    return name

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("WriteToPostgres") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.5.4") \
        .getOrCreate()

    df = spark.read.csv(
        "input/Fire_Incidents_20250505.csv",
        header=True,
        schema=fire_incidents_schema,
        timestampFormat="yyyy/MM/dd hh:mm:ss a",
        nullValue=""
    )

    df_renamed = df.select([df[col].alias(to_snake_case(col)) for col in df.columns])

    df_renamed.write \
        .format("jdbc") \
        .option(
            "url",
            f"jdbc:postgresql://{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}"
        ) \
        .option("dbtable", os.getenv('raw_table')) \
        .option("user", os.getenv("user")) \
        .option("password", os.getenv("password")) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()
