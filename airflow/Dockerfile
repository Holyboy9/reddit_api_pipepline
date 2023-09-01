FROM apache/airflow:2.7.0 

ENV AIRFLOW_HOME=/opt/airflow

USER $AIRFLOW_UID

COPY requirements.txt .
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r requirements.txt

SHELL ["/bin/bash", "-o", "pipefail", "-e", "-u", "-x", "-c"]

WORKDIR $AIRFLOW_HOME

