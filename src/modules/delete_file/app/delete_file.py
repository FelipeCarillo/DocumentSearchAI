import os

from src.core.helpers.functions.S3Manager import S3Manager
from src.core.helpers.functions.Authorizer import Authorizer
from src.core.helpers.functions.DocumentStore import DocumentStore
from src.core.helpers.http.http import (
    HTTPRequest,
    Created,
    InternalServerError,
    Unauthorized,
)


def lambda_handler(event, context):
    """
    This function is responsible for deleting a file from the S3 bucket.
    """

    request = HTTPRequest(event)

    try:
        Authorizer().authorize(request.headers["Authorization"])

        # Get the bucket name from the environment variables
        bucket_name = os.environ.get("AWS_BUCKET_NAME")

        # Create an instance of the S3Manager class
        s3_file = S3Manager(bucket_name=bucket_name)

        # Delete the file from the S3 bucket
        file = s3_file.delete_file(request.parameters["file_name"])

        # Create an instance of the DocumentStore class
        document_store = DocumentStore(
            es_index_name=f"{bucket_name}-{request.parameters['file_name'].split('.')[0]}-index"
        )

        # Delete the document from the Elasticsearch database
        document_store.delete()

        # Return the response
        return Created("File uploaded successfully", file).to_dict()

    except Unauthorized as e:
        return e.to_dict()
    except Exception as e:
        return InternalServerError("Error", str(e)).to_dict()
