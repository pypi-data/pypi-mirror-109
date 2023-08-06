import os
import click
import requests
import logging
import boto3
import glob

logger = logging.getLogger(__name__)

@click.command()
@click.option("--in", "-i", "in_file",
              required=True,
              help="Path to the file to be processed.",
              )
@click.option("--s3bucket", "-s3", "bucket_name", 
                default="elasticbeanstalk-ap-southeast-2-443270330641", 
                help="s3 bucket name"
             )
@click.option('--verbose', is_flag=True, help="Verbose output for debugging")
def process(in_file: str,
            bucket_name: str,
            verbose: bool):
    """This is the script to upload files to gofile & s3"""

    if verbose:
        log_formatter = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=log_formatter, level=logging.DEBUG)
   
    __upload(in_file, bucket_name)

def __upload(in_file: str, bucket_name: str):
    if os.path.isdir(in_file):  
        for file in glob.glob(f"{in_file}/*.txt"):
            __upload_s3(file, bucket_name)        
    elif os.path.isfile(in_file):  
        __upload_s3(in_file, bucket_name)
    else:  
        raise Exception("Unsupported path") 

def __upload_s3(in_file: str, bucket_name: str):
    s3 = boto3.client('s3')
    data = open(in_file, "rb")
    filename = os.path.basename(in_file)
    response = s3.put_object(ACL='public-read',
                             Body=data,
                             Bucket=bucket_name,
                             Key=filename,
                             ContentType='text/html')

    status_code = response['ResponseMetadata']['HTTPStatusCode']

    if status_code == 200:
        click.echo(f"The file download link is: https://{bucket_name}.s3.ap-southeast-2.amazonaws.com/{filename}")
    else:
        logging.error("Error in uploading to S3! The status code is %s", status_code)

if __name__ == "__main__":
    process()