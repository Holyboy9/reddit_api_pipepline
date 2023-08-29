from airflow import DAG
from datetime import timedelta,datetime
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

output_name = datetime.now().strftime("%Y%m%d")

default_args = {
    "owner":"airflow",
    "start_date":days_ago(1),
    "retries":1,
    "depends_on_past":False
}

dag = DAG(
  dag_id='etl_reddit_pipeline',
  default_args=default_args,
  description='My first DAG',
  schedule_interval="@daily",
  catchup=True
)

extract_reddit_data = BashOperator(
    task_id = "extract_reddit_data",
    bash_command = f"python /opt/airflow/extraction/reddit_extract.py {output_name}",
    dag=dag 
)

upload_to_S3 = BashOperator(
    task_id = "upload_to_s3",
    bash_command = f"python /opt/airflow/extraction/upload_to_s3.py {output_name}",
    dag=dag
)

upload_to_redshift = BashOperator(
    task_id = "upload_to_redshift",
    bash_command = f"python /opt/airflow/extraction/upload_from_s3_redshift.py {output_name}",
    dag=dag
)


extract_reddit_data >> upload_to_S3 >> upload_to_redshift
