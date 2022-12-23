### SNS Topic ###


import aws_cdk.aws_sns as sns

# data_protection_policy: Any

cfn_topic = sns.CfnTopic(self, "MyCfnTopic",
    content_based_deduplication=False,
    data_protection_policy=data_protection_policy,
    display_name="displayName",
    fifo_topic=False,
    kms_master_key_id="kmsMasterKeyId",
    signature_version="signatureVersion",
    subscription=[sns.CfnTopic.SubscriptionProperty(
        endpoint="endpoint",
        protocol="protocol"
    )],
    tags=[CfnTag(
        key="key",
        value="value"
    )],
    topic_name="topicName"
)


####  SNS SUB ####

my_topic = sns.Topic(self, "MyTopic")

my_topic.add_subscription(subscriptions.UrlSubscription("https://foobar.com/"))



#### Alarms ####


import aws_cdk.aws_cloudwatch as cloudwatch

# alias: lambda.Alias

# or add alarms to an existing group
# blue_green_alias: lambda.Alias

alarm = cloudwatch.Alarm(self, "Errors",
    comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=alias.metric_errors()
)
deployment_group = codedeploy.LambdaDeploymentGroup(self, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    alarms=[alarm
    ]
)
deployment_group.add_alarm(cloudwatch.Alarm(self, "BlueGreenErrors",
    comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=blue_green_alias.metric_errors()
))

###Use an alarm Action in SNS


import aws_cdk.aws_cloudwatch_actions as cw_actions
# alarm: cloudwatch.Alarm


topic = sns.Topic(self, "Topic")
alarm.add_alarm_action(cw_actions.SnsAction(topic))




