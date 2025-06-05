# Weather ETL with Apache Airflow

## Project Overview

This repository contains an **Apache Airflow** DAG that implements a **Weather ETL (Extract-Transform-Load)** pipeline that runs every 30 minutes:

1. **Extract**: Fetch current weather data for a list of cities (e.g., Tucson, New York, London) from the **OpenWeather API**.  
2. **Transform**: Parse the raw JSON and convert it into a structured CSV file (`weather_transformed.csv`).  
3. **Load**: Upload the CSV file to an **Amazon S3** bucket (e.g., `ajeet-weather-data-airflow`).  
4. **Notify**: Send an email notification once the upload is successful.

Below is a high-level architectural diagram and Apache Airflow UI showing the ETL DAG with 4 Tasks :

![Airflow_ETL](https://github.com/user-attachments/assets/858e8e14-7c5e-421d-b0af-57d75e5440b4)
![Weather_ETL_Pipeline](https://github.com/user-attachments/assets/9ddc9b0d-4f48-43ca-bc5c-b81d8ed0749a)

---

## Prerequisites

Before running this pipeline, make sure you have:

- **Git** (to clone and push to GitHub)  
- **Python 3.8+**  
- **AWS Account** (with permissions to write to an S3 bucket)  
- **OpenWeather API Key** (sign up at [OpenWeather](https://openweathermap.org/) and generate a key)  
- **Email Account** (e.g., Gmail) to receive notifications (Airflow will use SMTP to send email)

---

## Create & Activate a Virtual Environment
```bash
conda create -n airflow_env python=3.8
conda activate airflow_env
```

---

## Install Requirements
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
---

## Configure and start Airflow
Open two terminals:
- Terminal 1
```bash
airflow webserver --port 8080
```
- Terminal 2
```bash
airflow scheduler
```
Then visit http://localhost:8080 in your browser to open Apache Airflow UI that looks as follows: 

![Weather_ETL_Pipeline](https://github.com/user-attachments/assets/9ddc9b0d-4f48-43ca-bc5c-b81d8ed0749a)

---

##  How It Works: ETL Tasks

### Task 1: Extract Weather Data
- **Operator**: `PythonOperator`
- **Description**:  
  Fetches weather data from the OpenWeather API for the following cities:
  - Tucson
  - New York
  - London
- **Output**:  
  Saves each city’s response as a JSON file in the directory:  /tmp/weather_raw/{city}.json

---

### Task 2: Transform Weather Data
- **Description**:  
Reads the raw JSON files generated in Task 1 and filters valid entries.
- **Extracted Fields**:
  - City
  - Temperature
  - Humidity
  - Weather Description
  - Timestamp
- **Output**:  
Transformed data is saved as a CSV file:  /tmp/weather_transformed.csv

---

### Task 3: Load to AWS S3
- **Description**:  
Uploads the transformed CSV file to an AWS S3 bucket.
- **S3 Destination Folder**:  weather-data/
- **File Naming Convention**:   weather_YYYY-MM-DD_HH-MM-SS.csv
![S3_Snap](https://github.com/user-attachments/assets/07e1c98c-1846-4a32-8e0e-4c364b7bc447)

  
---

### Task 4: Send Email Notification
- **Operator**: `EmailOperator`
- **Description**:  
Sends an email notification to the configured recipient after a successful upload to S3.
---

##  Email Configuration for Airflow
In airflow.cfg, edit the [smtp] section:
```bash
[smtp]
smtp_host = smtp.gmail.com
smtp_starttls = True
smtp_ssl = False
smtp_user = your_email@gmail.com
smtp_password = your_app_password
smtp_port = 587
smtp_mail_from = your_email@gmail.com
```

## Running the Pipeline
1. Start Airflow:
```bash
airflow webserver --port 8080
airflow scheduler
```
2. Visit http://localhost:8080 for Airflow GUI
3. Toggle weather_etl_dag to ON
4. Manually trigger the DAG or wait for the schedule
5. Check:
    . File in S3 bucket
    . Email notification received


