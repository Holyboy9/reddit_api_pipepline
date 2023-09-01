import configparser
import pathlib
import redshift_connector
import sys
from validation import validation_input
from psycopg2 import sql


script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/configuration.conf")
BUCKET_NAME = parser.get("aws_config","bucket_name")
AWS_REGION = parser.get("aws_config","aws_region")
USERNAME = parser.get("aws_config","admin_username")
REDSHIFT_SERVERLESS_NAMESPACE = parser.get("aws_config","redshift_serverless_namespace")
DATABASE = parser.get("aws_config","redshift_database")
REDSHIFT_ROLE = parser.get("aws_config","redshift_role")
REDSHIFT_SERVERLESS_WORKGROUP = parser.get("aws_config","redshift_serverless_workgroup")
ACCOUNT_ID = parser.get("aws_config","account_id")
HOST = parser.get("aws_config","aws_host")
TABLE_NAME = "reddit"


try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Command line argument not passed. Error {e}")
    sys.exit(1)

file_path = f"s3://{BUCKET_NAME}/{output_name}.csv"
role_string = f"arn:aws:iam::{ACCOUNT_ID}:role/{REDSHIFT_ROLE}"


sql_create_table = """CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                            id varchar PRIMARY KEY,
                            title varchar(max),
                            num_comments int,
                            score int,
                            author varchar(max),
                            created_utc timestamp,
                            url varchar(max),
                            upvote_ratio float,
                            over_18 bool,
                            edited bool,
                            spoiler bool,
                            stickied bool
                        );"""


create_temp_table = """CREATE TEMP TABLE our_staging_table (LIKE {TABLE_NAME})"""
sql_copy_to_temp ="""COPY our_staging_table FROM '{file_path}' iam role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"""
delete_from_table = """DELETE FROM {TABLE_NAME} USING our_staging_table WHERE {TABLE_NAME}.id = our_staging_table.id;"""
insert_into_table = """INSERT INTO {TABLE_NAME} SELECT * FROM our_staging_table;"""
drop_temp_table = """DROP TABLE our_staging_table;"""

def main():
    """Upload file form S3 to Redshift Table"""
    validation_input(output_name)
    rds_conn = connect_to_redshift()
    load_data_to_redshift(rds_conn)



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

def load_data_to_redshift(rds_conn):
    with rds_conn:
        curr = rds_conn.cursor()
        curr.execute(sql_create_table)
        curr.execute(create_temp_table)
        curr.execute(sql_copy_to_temp)
        curr.execute(delete_from_table)
        curr.execute(insert_into_table)
        curr.execute(drop_temp_table)
        
        rds_conn.commit()


if __name__ == "__main__":
    main()
