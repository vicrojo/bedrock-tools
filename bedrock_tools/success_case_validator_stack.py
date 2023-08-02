from aws_cdk import (
    Stack,
    Duration,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_events,
    aws_events_targets
)
from constructs import Construct

class SuccessCaseValidatorStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_role = _iam.Role(scope=self, id='bedrock-tools-role',
                                assumed_by =_iam.ServicePrincipal('lambda.amazonaws.com'),
                                role_name='bedrock-tools-lambda-role',
                                managed_policies=[
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaVPCAccessExecutionRole'),
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole'),
                                _iam.ManagedPolicy.from_managed_policy_name(self,
                                    'BedRockAccess','BedrockFullAccess')
                                ])
        
        lambdaLayer = _lambda.LayerVersion(self, 'lambda-layer',
                  code = _lambda.AssetCode('lambda/layer/'),
                  compatible_runtimes = [_lambda.Runtime.PYTHON_3_10],
        )
        
        success_case_validator_lambda  = _lambda.Function(
            self, 'SuccessCaseValidator-Lambda',
            runtime=_lambda.Runtime.PYTHON_3_10,
            function_name='SuccessCaseValidator-lambda',
            description='Success Case ValidatorLambda Function',
            code=_lambda.Code.from_asset('./lambda/code'),
            handler='success_case_validator.lambda_handler',
            role=lambda_role,
            layers = [lambdaLayer],
            environment={
                'NAME': 'success_case_validator'
            },
            timeout=Duration.seconds(300),
            memory_size=1024,
        )
        
        one_minute_rule = aws_events.Rule(
            self, "one_minute_rule",
            schedule=aws_events.Schedule.rate(Duration.minutes(1)),
        )

        # Add target to Cloudwatch Event
        one_minute_rule.add_target(
            aws_events_targets.LambdaFunction(success_case_validator_lambda))
