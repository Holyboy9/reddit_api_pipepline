import boto3
import configparser
import botocore
import pathlib
import sys
from validation import validation_input


parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
parser.read(f"{script_path}/configuration.conf")
BUCKET_NAME = parser.get("aws_config","bucket_name")
AWS_REGION = parser.get("aws_config","aws_region")

try:
    output_name = sys.argv[1]
except Exception as e:
    print(f"Command line argument not passed. Error {e}")
    sys.exit(1)

FILENAME = f"{output_name}.csv"
KEY = FILENAME

def main():
    validation_input(output_name)
    conn = connect_to_s3()
    create_object_if_not_exists(conn)
    upload_file_to_s3(conn)

def connect_to_s3():
    try:
        conn = boto3.resource("s3")
        return conn
    except Exception as e:
        print(f"Can't connect to s3.Error: {e}")
        sys.exit(1)

def create_object_if_not_exists(conn):
    exists = True
    try:
        conn.meta.client.head_bucket(Bucket=BUCKET_NAME)
    except botocore.exceptions.ClientError as e:
        error_code = e.response["message"]["code"]
        if error_code == "404":
            exists = False
    if not exists:
        conn.create_bucket(
            Bucket = BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint':AWS_REGION
            }
        )
def upload_file_to_s3(conn):
    conn.meta.client.upload_file(
        Filename = "/tmp/"+FILENAME,
        Bucket = BUCKET_NAME,
        Key = FILENAME
    )

if __name__ == "_main_":
    main()