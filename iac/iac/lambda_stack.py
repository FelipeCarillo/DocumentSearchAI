from constructs import Construct

import aws_cdk.aws_iam as iam
from aws_cdk import aws_lambda as _lambda, Duration


class LambdaStack(Construct):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        ENVIROMMENT: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Creating a layer
        layer = _lambda.LayerVersion(
            self,
            "LambdaLayer",
            code=_lambda.Code.from_asset("lambda_layers"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
        )

        # Creating a Authorizer Lambda function
        self.authorizer = self.__create_lambda_function(
            "authorizer", ENVIROMMENT, layer
        )

        # Creating a Lambda function
        self.scan_file = self.__create_lambda_function("scan_file", ENVIROMMENT, layer)

        # Textract requires the Lambda function to have an execution role with the following permissions
        self.scan_file.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "textract:DetectDocumentText",
                    "textract:GetDocumentTextDetection",
                    "textract:StartDocumentTextDetection",
                ],
                resources=["*"],
            )
        )

        # Creating a Lambda function
        self.document_search = self.__create_lambda_function(
            "document_search", ENVIROMMENT, layer
        )

        # Creating a Lambda function
        self.list_files = self.__create_lambda_function(
            "list_files", ENVIROMMENT, layer
        )

        # Creating a Lambda function
        self.upload_file = self.__create_lambda_function(
            "upload_file", ENVIROMMENT, layer
        )

        # Creating a Lambda function
        self.delete_file = self.__create_lambda_function(
            "delete_file", ENVIROMMENT, layer
        )

    def __create_lambda_function(
        self, name: str, ENVIROMMENT: dict, LAYER: _lambda.LayerVersion
    ) -> _lambda.Function:

        code = _lambda.Code.from_asset(f"../src/modules/{name}")
        handler = f"app.{name}.lambda_handler"

        return _lambda.Function(
            self,
            f"{name.title()}_{ENVIROMMENT['STACK_NAME']}",
            function_name=f"{name.title()}_{ENVIROMMENT['STACK_NAME']}",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler=handler,
            code=code,
            layers=[LAYER],
            environment=ENVIROMMENT,
            timeout=Duration.seconds(15),
            memory_size=512,
        )
