import os
from constructs import Construct

from aws_cdk import Stack

from .s3_stack import S3Stack
from .lambda_stack import LambdaStack
from .apigateway_stack import ApiGatewayStack


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get the environment variables
        ENVIROMMENT = {
            "STACK_NAME": os.environ.get("STACK_NAME"),
            "STAGE": os.environ.get("STAGE"),
            "AWS_BUCKET_NAME": os.environ.get("AWS_BUCKET_NAME"),
            "ES_API_KEY": os.environ.get("ES_API_KEY"),
            "ES_CLOUD_ID": os.environ.get("ES_CLOUD_ID"),
            "ES_INDEX_NAME": os.environ.get("ES_INDEX_NAME"),
        }

        # Create the Lambda stack
        lambda_stack = LambdaStack(
            self, f"{ENVIROMMENT['STACK_NAME']}_LambdaStack", ENVIROMMENT
        )

        # Create the S3 stack
        s3_stack = S3Stack(self, f"{ENVIROMMENT['STACK_NAME']}_S3Stack", ENVIROMMENT)

        # Set the Lambda permission to read and write the S3 bucket
        s3_stack.set_lambda_permission(lambda_stack.scan_file)
        s3_stack.set_lambda_permission(lambda_stack.list_files)

        # Set the Lambda trigger to scan the file
        s3_stack.set_lambda_trigger(lambda_stack.scan_file)

        # Create the API Gateway stack
        api_gateway_stack = ApiGatewayStack(
            self, f"{ENVIROMMENT['STACK_NAME']}_ApiGatewayStack", ENVIROMMENT
        )

        # Add the Lambda integration
        api_gateway_stack.add_lambda_integration(
            lambda_stack.document_search, "document_search"
        )
