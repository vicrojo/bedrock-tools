#!/usr/bin/env python3
import os
import aws_cdk as cdk
from bedrock_tools.success_case_validator_stack import SuccessCaseValidatorStack

app = cdk.App()
SuccessCaseValidatorStack(app, "BedrockTools-SuccessCaseValidatorStack")

app.synth()
