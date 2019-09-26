import boto3

BUCKET_NAME = 'publicart-indexer'
OBJECT_PATH = 'pa-rpi1-indexer/'
FILE_NAME = 'test.txt'

import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then same as file_name
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, BUCKET_NAME, OBJECT_PATH + file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    """Exercise upload_file()"""

    # Set these values before running the program
    bucket_name = BUCKET_NAME
    file_name = FILE_NAME
    object_name = OBJECT_PATH + FILE_NAME

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # Upload a file
    response = upload_file(file_name)
    if response:
        logging.info('File was uploaded')


if __name__ == '__main__':
    main()
