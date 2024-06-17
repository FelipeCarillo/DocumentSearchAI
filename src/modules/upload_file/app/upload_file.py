import os

from src.core.helpers.functions.S3Manager import S3Manager
from src.core.helpers.http.http import HTTPRequest, Created


def lambda_handler(event, context):
    """
    This function is responsible for listing the files in the S3 bucket.
    """

    request = HTTPRequest(event)

    try:

        # Get the bucket name from the environment variables
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

        # Create an instance of the S3Manager class
        s3_file = S3Manager(bucket_name=bucket_name)

        # Upload the file to the S3 bucket
        file = s3_file.upload_file(
            file_name=request.body["file_name"],
            file_body=request.body["file_body"],
            content_type=request.body["content_type"],
        )

        # Return the response
        return Created("File uploaded successfully", file).to_dict()

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
