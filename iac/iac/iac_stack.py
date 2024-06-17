import os
from constructs import Construct

import aws_cdk
from aws_cdk import Stack, aws_s3 as s3, aws_lambda as _lambda, aws_lambda_event_sources

from .s3_stack import S3Stack
from .lambda_stack import LambdaStack
from .apigateway_stack import ApiGatewayStack


class IacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        STACK_NAME = os.environ.get("STACK_NAME")

        # Get the environment variables
        ENVIROMMENT = {
            "STAGE": os.environ.get("STAGE"),
            "AWS_BUCKET_NAME": os.environ.get("AWS_BUCKET_NAME"),
            "ES_API_KEY": os.environ.get("ES_API_KEY"),
            "ES_CLOUD_ID": os.environ.get("ES_CLOUD_ID"),
            "ES_INDEX_NAME": os.environ.get("ES_INDEX_NAME"),
        }

        # Create the Lambda stack
        lambda_stack = LambdaStack(self, f"{STACK_NAME}_LambdaStack", ENVIROMMENT)

        # Create the S3 stack
        s3_stack = S3Stack(self, f"{STACK_NAME}_S3Stack", ENVIROMMENT)

        # Set the Lambda permission and trigger
        s3_stack.set_lambda_permission(lambda_stack.scan_file)
        s3_stack.set_lambda_trigger(lambda_stack.scan_file)

        # Create the API Gateway stack
        api_gateway_stack = ApiGatewayStack(self, f"{STACK_NAME}_ApiGatewayStack", ENVIROMMENT)

        # Add the Lambda integration
        api_gateway_stack.add_lambda_integration(lambda_stack.document_search, "document_search")


