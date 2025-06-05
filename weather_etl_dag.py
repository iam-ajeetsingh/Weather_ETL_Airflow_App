from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import json
import os
import sqlite3
import boto3


default_args = {
    'owner': 'ajeet',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

cities = ["Tucson", "New York", "London"]
api_key = <your_openweather_api_key>


raw_data_dir = "/tmp/weather_raw"
os.makedirs(raw_data_dir, exist_ok=True)

def extract():
    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        res = requests.get(url)
        data = res.json()
        with open(f"{raw_data_dir}/{city}.json", "w") as f:
            json.dump(data, f)

def transform():
    weather_data = []
    for city in cities:
        file_path = f"{raw_data_dir}/{city}.json"
        with open(file_path, "r") as f:
            data = json.load(f)

            # Skip if API returned an error (e.g., city not found or quota exceeded)
            if "main" not in data or data.get("cod") != 200:
                print(f"Skipping {city} due to error: {data.get('message', 'unknown error')}")
                continue

            weather_data.append({
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'datetime': datetime.utcnow()
            })

    if not weather_data:
        raise ValueError("No valid weather data to transform.")

    df = pd.DataFrame(weather_data)
    df.to_csv("/tmp/weather_transformed.csv", index=False)

"""
def load():
    df = pd.read_csv("/tmp/weather_transformed.csv")
    conn = sqlite3.connect('/tmp/weather_data.db')
    df.to_sql('weather', conn, if_exists='append', index=False)
    conn.close()
"""


def load():
    s3 = boto3.client('s3')
    local_file = "/tmp/weather_transformed.csv"
    bucket_name = "ajeet-weather-data-airflow"  # Use your actual bucket name
    s3_key = f"weather-data/weather_{datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

    try:
        s3.upload_file(local_file, bucket_name, s3_key)
        print(f"✅ Uploaded to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        raise Exception(f"❌ Failed to upload to S3: {str(e)}")


with DAG(
    dag_id='weather_etl_dag',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    #schedule_interval=timedelta(days=1),
    schedule_interval=timedelta(minutes=30),
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='extract_weather_data',
        python_callable=extract
    )

    task2 = PythonOperator(
        task_id='transform_weather_data',
        python_callable=transform
    )

    task3 = PythonOperator(
        task_id='load_weather_data',
        python_callable=load
    )

    task1 >> task2 >> task3

