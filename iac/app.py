#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.iac_stack import IacStack


app = cdk.App()

STACK_NAME = os.environ.get("STACK_NAME")

AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
AWS_REGION = os.environ.get("AWS_REGION")

IacStack(
    app,
    STACK_NAME,
    env=cdk.Environment(
        account=AWS_ACCOUNT_ID,
        region=AWS_REGION,
    ),
)

app.synth()
