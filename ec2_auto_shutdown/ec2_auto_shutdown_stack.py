from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct

class Ec2AutoShutdownStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the Lambda function
        shutdown_lambda = _lambda.Function(
            self, "Ec2AutoShutdownFunction",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("ec2_auto_shutdown/lambda"),
            timeout=Duration.seconds(60)
        )

        # Optional: Add a CloudWatch Event rule to trigger the Lambda every day at 6 PM UTC
        rule = events.Rule(
            self, "DailyShutdownRule",
            schedule=events.Schedule.cron(minute="0", hour="18")  # 18:00 UTC daily
        )
        rule.add_target(targets.LambdaFunction(shutdown_lambda))
