import os

from src.core.helpers.functions.DocumentStore import DocumentStore
from src.core.helpers.functions.DocumentLouder import DocumentLoader


def lambda_handler(event, context):
    """
    This function is the entry point for the Lambda function.
    """
    try:
        # Get the bucket name and object name from the event
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        object_name = event["Records"][0]["s3"]["object"]["key"]

        # Get the AWS region from the environment variables
        aws_region = os.environ.get("AWS_REGION")

        # Create an instance of the DocumentLoader class
        document_loader = DocumentLoader(
            bucket_name=bucket_name,
            object_name=object_name,
            aws_region=aws_region,
        )

        # Load the text from the input document
        documents = document_loader.load()

        es_index_name = f"{bucket_name}-{object_name.split('.')[0]}-index"

        # Create an instance of the DocumentStore class
        document_store = DocumentStore(es_index_name=es_index_name)

        # Store the text in the Elasticsearch database
        document_store.store(documents)

        print(f"Document {object_name} stored in Elasticsearch index {es_index_name}.")

    except Exception as e:
        print(f"Error: {e}")
