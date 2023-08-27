import configparser
import pathlib
import psycopg2
from psycopg2 import sql
import csv
import sys


script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/configuration.conf")

USERNAME = parser.get("aws_config","admin_username")
DATABASE = parser.get("aws_config","redshift_database")
HOST = parser.get("aws_config","aws_host")
ACCOUNT_ID = parser.get("aws_config","account_id")
REDSHIFT_SERVERLESS_WORKGROUP = parser.get("aws_config","redshift_serverless_workgroup")

