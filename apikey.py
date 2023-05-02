from aws_cdk import (
    core,
    aws_apigatewayv2 as apigw,
)

class MyStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the HTTP API
        api = apigw.HttpApi(self, "MyHttpApi")

        # Create the API key
        api_key = apigw.CfnApiKey(self, "MyApiKey",
            api_key_name="MyApiKey",
            enabled=True,
            generate_distinct_id=True,
            value="my-api-key-value"
        )

        # Attach the API key to the HTTP API
        apigw.CfnDeployment(self, "MyDeployment",
            api_id=api.http_api_id,
            stage_name=api.default_stage.stage_name,
            stage_variables={
                "ApiKeyId": api_key.ref
            }
        )
