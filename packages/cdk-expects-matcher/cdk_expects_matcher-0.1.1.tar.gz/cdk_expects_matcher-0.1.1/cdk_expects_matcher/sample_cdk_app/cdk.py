from aws_cdk import (
    core,
    aws_s3 as s3
)
app = core.App()


class MainStack(core.Stack):
    def __init__(self, scope: core.Construct, **kwargs):
        super(MainStack, self).__init__(
            scope=scope,
            id=MainStack.__name__,
            **kwargs
        )

        s3.Bucket(
            self, 'TheNewBucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY,
        )


MainStack(
    scope=app
)

app.synth()
