import configparser
import pathlib
import redshift_connector
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
TABLE_NAME = "reddit"

def connect_to_redshift():
    try:
        rds_conn = redshift_connector.connect(
            host = HOST,
            database = DATABASE,
            user = USERNAME,
            is_serverless=True,
            serverless_acct_id = ACCOUNT_ID,
            serverless_work_group = REDSHIFT_SERVERLESS_WORKGROUP
            )
    except Exception as e:
        print(f"failed to connect to redshsift serverless. Error {e}")
        sys.exit(1)


def download_redshift_data(rds_conn):
    """Download data from Redshift table to CSV"""
    with rds_conn:
        curr = rds_conn.cursor()
        curr.execute(
            """SELECT * FROM {TABLE_NAME};"""
        )
        result = curr.fetchall()
        headers = [col[0] for col in curr.description]
        result.insert(0, tuple(headers))
        fp = open("/tmp/redshift_output.csv", "w")
        myFile = csv.writer(fp)
        myFile.writerows(result)
        fp.close()


if __name__ == "__main__":
    rds_conn = connect_to_redshift()
    download_redshift_data(rds_conn)