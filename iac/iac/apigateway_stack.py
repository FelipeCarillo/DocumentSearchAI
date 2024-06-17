from constructs import Construct
from typing import Any, Dict, Tuple

from aws_cdk import aws_apigateway as apigateway, aws_lambda as _lambda, aws_iam as iam


class ApiGatewayStack(Construct):
    root_resource: apigateway.IResource

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        ENVIROMMENT: Dict[str, str],
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        name = "api_gateway"

        # Create the Rest API
        api_gateway = apigateway.RestApi(
            self,
            ENVIROMMENT["STACK_NAME"] + "_" + name.title(),
            rest_api_name=ENVIROMMENT["STACK_NAME"] + "_" + name.title(),
            description=f"This is the API Gateway for the {ENVIROMMENT['STACK_NAME']} stack",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
                "allow_headers": apigateway.Cors.DEFAULT_HEADERS,
            },
            deploy_options=apigateway.StageOptions(stage_name="prod"),
        )

        root_resource = ENVIROMMENT["STACK_NAME"].lower().replace("_", "-")

        self.root_resource = api_gateway.root.add_resource(
            root_resource,
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
                "allow_headers": apigateway.Cors.DEFAULT_HEADERS,
            },
        )

    def add_lambda_integration(
        self, lambda_function: _lambda.Function, method: str
    ) -> None:

        self.root_resource.add_resource(
            method,
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS,
                "allow_headers": apigateway.Cors.DEFAULT_HEADERS,
            },
        ).add_method(
            method,
            apigateway.LambdaIntegration(
                lambda_function,
            ),
        )
