from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Enterprise ETL Pipeline").getOrCreate()

def extract_data():
    df = spark.read.format("json").load("s3://data-lake/customer_interactions/")
    df.write.parquet("data/raw/")

def transform_data():
    df = spark.read.parquet("data/raw/")
    df = df.withColumn("event_time", F.current_timestamp())
    df.write.parquet("data/processed/")

def load_data():
    df = spark.read.parquet("data/processed/")
    df.write.format("jdbc").option("url", "jdbc:redshift://aws-cluster").option("dbtable", "customer_insights").save()

default_args = {'start_date': datetime(2024, 1, 1)}
dag = DAG("etl_pipeline", default_args=default_args, schedule_interval="@daily")

task1 = PythonOperator(task_id="extract", python_callable=extract_data, dag=dag)
task2 = PythonOperator(task_id="transform", python_callable=transform_data, dag=dag)
task3 = PythonOperator(task_id="load", python_callable=load_data, dag=dag)

task1 >> task2 >> task3
