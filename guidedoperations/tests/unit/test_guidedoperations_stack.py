import aws_cdk as core
import aws_cdk.assertions as assertions

from guidedoperations.guidedoperations_stack import GuidedoperationsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in guidedoperations/guidedoperations_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GuidedoperationsStack(app, "guidedoperations")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
