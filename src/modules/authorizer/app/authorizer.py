import os
import jwt


def generate_policy(principal_id: str, effect: str, resource: str) -> dict:
    """
    Generates a policy
    """
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource,
                }
            ],
        },
    }


def lambda_handler(event, context):
    """
    This is a Lambda Authorizer
    """

    token = event["Authorization"]
    method_arn = event["methodArn"]

    try:
        jwt.decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return generate_policy("user", "Deny", method_arn)
    except jwt.InvalidTokenError:
        return generate_policy("user", "Deny", method_arn)

    return generate_policy("user", "Allow", method_arn)
