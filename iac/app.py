#!/usr/bin/env python3
import os
import dotenv

import aws_cdk as cdk

from iac.iac_stack import IacStack

dotenv.load_dotenv()

app = cdk.App()

AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
AWS_REGION = os.environ.get("AWS_REGION")

ENVIROMMENT = {
    "STACK_NAME": os.environ.get("STACK_NAME"),
    "STAGE": os.environ.get("STAGE"),
    "AWS_BUCKET_NAME": os.environ.get("AWS_BUCKET_NAME"),
    "ES_API_KEY": os.environ.get("ES_API_KEY"),
    "ES_CLOUD_ID": os.environ.get("ES_CLOUD_ID"),
    "ES_INDEX_NAME": os.environ.get("ES_INDEX_NAME"),
}

IacStack(
    scope=app,
    construct_id=f"{ENVIROMMENT['STACK_NAME']}Stack",
    ENVIROMMENT=ENVIROMMENT,
    env=cdk.Environment(
        account=AWS_ACCOUNT_ID,
        region=AWS_REGION,
    ),
)

app.synth()
