# Weather ETL with Apache Airflow

## Project Overview

This repository contains an **Apache Airflow** DAG that implements a **Weather ETL (Extract-Transform-Load)** pipeline that runs every 30 minutes:

1. **Extract**: Fetch current weather data for a list of cities (e.g., Tucson, New York, London) from the **OpenWeather API**.  
2. **Transform**: Parse the raw JSON and convert it into a structured CSV file (`weather_transformed.csv`).  
3. **Load**: Upload the CSV file to an **Amazon S3** bucket (e.g., `ajeet-weather-data-airflow`).  
4. **Notify**: Send an email notification once the upload is successful.

Below is a high-level architectural diagram:

![Airflow_ETL](https://github.com/user-attachments/assets/858e8e14-7c5e-421d-b0af-57d75e5440b4)

