import aws_cdk as core
import aws_cdk.assertions as assertions

from ec2_auto_shutdown.ec2_auto_shutdown_stack import Ec2AutoShutdownStack

# example tests. To run these tests, uncomment this file along with the example
# resource in ec2_auto_shutdown/ec2_auto_shutdown_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Ec2AutoShutdownStack(app, "ec2-auto-shutdown")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
