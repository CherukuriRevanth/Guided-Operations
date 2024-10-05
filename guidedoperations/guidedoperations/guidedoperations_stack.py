from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_wafv2 as wafv2,
)
from constructs import Construct

class GuidedOperationsStack(Stack):

    def _init_(self, scope: Construct, id: str, **kwargs) -> None:
        super()._init_(scope, id, **kwargs)

        # Create an S3 bucket for your static content
        bucket = s3.Bucket(self, "GuidedOperationsBucket",
        blockPublicAccess = s3.BlockPublicAccess.BLOCK_ALL,
        encryption = s3.BucketEncryption.S3_MANAGED,
        enforceSSL = true,
        removalPolicy = cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects = true,
        serverAccessLogsPrefix = 'access_log',
        versioned = true),

        # Create a WAF Rule
        rule_property = wafv2.CfnWebACL.RuleProperty(
            name="MyRule",
            priority=1,
            action=wafv2.CfnWebACL.RuleActionProperty(
                allow={}  # Change to block={} to block requests
            ),
            statement=wafv2.CfnWebACL.RuleStatementProperty(
                byte_match_statement=wafv2.CfnWebACL.ByteMatchStatementProperty(
                    search_string="bad_bot",
                    field_to_match=wafv2.CfnWebACL.FieldToMatchProperty(
                        uri_path={}
                    ),
                    text_transformation="NONE",
                    positional_constraint="CONTAINS",
                )
            ),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="MyRuleMetric",
                sampled_requests_enabled=True,
            ),
        )

        # Create the Web ACL
        web_acl = wafv2.CfnWebACL(self, "GO-WafACL",
            scope="CLOUDFRONT",  # Use CLOUDFRONT for CloudFront integration
            default_action=wafv2.CfnWebACL.DefaultActionProperty(
                allow={}  # Change to block={} if you want to block requests by default
            ),
            rules=[rule_property],  # List of RuleProperty
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="YourWebACLMetricName",
                sampled_requests_enabled=True
            ),
            description="Web ACL for guided operations",
        )

        # Create a CloudFront distribution
        cloudfront_distribution = cloudfront.CloudFrontWebDistribution(self, "MyDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=bucket,
                    ),
                    behaviors=[cloudfront.Behavior(
                        is_default_behavior=True,
                        allowed_methods=cloudfront.CloudFrontAllowedMethods.ALL,
                        cached_methods=cloudfront.CloudFrontAllowedCachedMethods.GET_HEAD,
                    )],
                ),
            ],
            web_acl_id=web_acl.ref,  # Associate the Web ACL with the CloudFront distribution
        )

        # Output the CloudFront Distribution Domain Name
        #self.output = cloudfront_distribution.distribution_domain_name

