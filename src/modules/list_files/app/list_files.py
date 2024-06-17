import os

from src.core.helpers.functions.S3Manager import S3Manager
from src.core.helpers.functions.Authorizer import Authorizer
from src.core.helpers.http.http import HTTPRequest, OK, InternalServerError


def lambda_handler(event, context):
    """
    This function is responsible for listing the files in the S3 bucket.
    """

    request = HTTPRequest(event)

    authorizer = Authorizer().authorize(request.headers["Authorization"])
    if not isinstance(authorizer, str):
        return authorizer

    try:

        # Get the bucket name from the environment variables
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

        # Create an instance of the S3Manager class
        s3_file = S3Manager(bucket_name=bucket_name)

        # List the files in the S3 bucket
        files = s3_file.list_files()

        return OK("Success", files).to_dict()

    except Exception as e:
        print(f"Error: {e}")
        return InternalServerError("Error", str(e)).to_dict()
