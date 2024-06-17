from constructs import Construct
from typing import Any, Dict, Tuple

import aws_cdk
from aws_cdk import aws_lambda as _lambda, aws_s3 as s3, aws_lambda_event_sources


class S3Stack(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        ENVIROMMENT: Dict[str, str],
        **kwargs: Dict[str, Any]
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating a development S3 bucket
        self.dev_bucket = s3.Bucket(
            self,
            ENVIROMMENT["AWS_BUCKET_NAME"] + "_DevBucket",
            bucket_name=ENVIROMMENT["AWS_BUCKET_NAME"] + "-dev",
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
        )

        # Creating a production S3 bucket
        self.prod_bucket = s3.Bucket(
            self,
            ENVIROMMENT["AWS_BUCKET_NAME"] + "_Bucket",
            bucket_name=ENVIROMMENT["AWS_BUCKET_NAME"],
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
        )

    def set_lambda_permission(self, lambda_function: _lambda.Function) -> None:
        self.prod_bucket.grant_read_write(lambda_function)

    def set_lambda_trigger(self, lambda_function: _lambda.Function) -> None:
        lambda_function.add_event_source(
            aws_lambda_event_sources.S3EventSource(
                self.prod_bucket, events=[s3.EventType.OBJECT_CREATED]
            )
        )
