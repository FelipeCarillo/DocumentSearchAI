#!/usr/bin/env python3
import os
import dotenv

import aws_cdk as cdk

from iac.iac_stack import IacStack

dotenv.load_dotenv()

app = cdk.App()

AWS_ACCOUNT_ID = os.environ["AWS_ACCOUNT_ID"]
AWS_REGION = os.environ["AWS_REGION"]

ENVIROMMENT = {
    "STACK_NAME": os.environ["STACK_NAME"],
    "STAGE": os.environ["STAGE"],
    "BUCKET_NAME": os.environ["BUCKET_NAME"],
    "ES_API_KEY": os.environ["ES_API_KEY"],
    "ES_CLOUD_ID": os.environ["ES_CLOUD_ID"],
    "ES_INDEX_NAME": os.environ["ES_INDEX_NAME"],
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
