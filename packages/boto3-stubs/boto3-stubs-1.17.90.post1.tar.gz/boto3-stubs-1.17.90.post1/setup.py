from os.path import abspath, dirname

from setuptools import setup

LONG_DESCRIPTION = open(dirname(abspath(__file__)) + "/README.md", "r").read()


setup(
    name="boto3-stubs",
    version="1.17.90.post1",
    packages=["boto3-stubs"],
    url="https://github.com/vemel/mypy_boto3_builder",
    license="MIT License",
    author="Vlad Emelianov",
    author_email="vlad.emelianov.nz@gmail.com",
    description="Type annotations for boto3 1.17.90, generated by mypy-boto3-buider 4.16.1",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
    keywords="boto3 type-annotations boto3-stubs mypy mypy-stubs typeshed autocomplete auto-generated",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_data={"boto3-stubs": ["py.typed", "*.pyi", "*/*.pyi"]},
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://mypy-boto3-builder.readthedocs.io/en/latest/",
        "Source": "https://github.com/vemel/mypy_boto3_builder",
        "Tracker": "https://github.com/vemel/mypy_boto3_builder/issues",
    },
    install_requires=[
        "typing_extensions; python_version < '3.8'",
    ],
    extras_require={
        "all": [
            "mypy-boto3-accessanalyzer==1.17.90.post1",
            "mypy-boto3-acm==1.17.90.post1",
            "mypy-boto3-acm-pca==1.17.90.post1",
            "mypy-boto3-alexaforbusiness==1.17.90.post1",
            "mypy-boto3-amp==1.17.90.post1",
            "mypy-boto3-amplify==1.17.90.post1",
            "mypy-boto3-amplifybackend==1.17.90.post1",
            "mypy-boto3-apigateway==1.17.90.post1",
            "mypy-boto3-apigatewaymanagementapi==1.17.90.post1",
            "mypy-boto3-apigatewayv2==1.17.90.post1",
            "mypy-boto3-appconfig==1.17.90.post1",
            "mypy-boto3-appflow==1.17.90.post1",
            "mypy-boto3-appintegrations==1.17.90.post1",
            "mypy-boto3-application-autoscaling==1.17.90.post1",
            "mypy-boto3-application-insights==1.17.90.post1",
            "mypy-boto3-applicationcostprofiler==1.17.90.post1",
            "mypy-boto3-appmesh==1.17.90.post1",
            "mypy-boto3-apprunner==1.17.90.post1",
            "mypy-boto3-appstream==1.17.90.post1",
            "mypy-boto3-appsync==1.17.90.post1",
            "mypy-boto3-athena==1.17.90.post1",
            "mypy-boto3-auditmanager==1.17.90.post1",
            "mypy-boto3-autoscaling==1.17.90.post1",
            "mypy-boto3-autoscaling-plans==1.17.90.post1",
            "mypy-boto3-backup==1.17.90.post1",
            "mypy-boto3-batch==1.17.90.post1",
            "mypy-boto3-braket==1.17.90.post1",
            "mypy-boto3-budgets==1.17.90.post1",
            "mypy-boto3-ce==1.17.90.post1",
            "mypy-boto3-chime==1.17.90.post1",
            "mypy-boto3-cloud9==1.17.90.post1",
            "mypy-boto3-clouddirectory==1.17.90.post1",
            "mypy-boto3-cloudformation==1.17.90.post1",
            "mypy-boto3-cloudfront==1.17.90.post1",
            "mypy-boto3-cloudhsm==1.17.90.post1",
            "mypy-boto3-cloudhsmv2==1.17.90.post1",
            "mypy-boto3-cloudsearch==1.17.90.post1",
            "mypy-boto3-cloudsearchdomain==1.17.90.post1",
            "mypy-boto3-cloudtrail==1.17.90.post1",
            "mypy-boto3-cloudwatch==1.17.90.post1",
            "mypy-boto3-codeartifact==1.17.90.post1",
            "mypy-boto3-codebuild==1.17.90.post1",
            "mypy-boto3-codecommit==1.17.90.post1",
            "mypy-boto3-codedeploy==1.17.90.post1",
            "mypy-boto3-codeguru-reviewer==1.17.90.post1",
            "mypy-boto3-codeguruprofiler==1.17.90.post1",
            "mypy-boto3-codepipeline==1.17.90.post1",
            "mypy-boto3-codestar==1.17.90.post1",
            "mypy-boto3-codestar-connections==1.17.90.post1",
            "mypy-boto3-codestar-notifications==1.17.90.post1",
            "mypy-boto3-cognito-identity==1.17.90.post1",
            "mypy-boto3-cognito-idp==1.17.90.post1",
            "mypy-boto3-cognito-sync==1.17.90.post1",
            "mypy-boto3-comprehend==1.17.90.post1",
            "mypy-boto3-comprehendmedical==1.17.90.post1",
            "mypy-boto3-compute-optimizer==1.17.90.post1",
            "mypy-boto3-config==1.17.90.post1",
            "mypy-boto3-connect==1.17.90.post1",
            "mypy-boto3-connect-contact-lens==1.17.90.post1",
            "mypy-boto3-connectparticipant==1.17.90.post1",
            "mypy-boto3-cur==1.17.90.post1",
            "mypy-boto3-customer-profiles==1.17.90.post1",
            "mypy-boto3-databrew==1.17.90.post1",
            "mypy-boto3-dataexchange==1.17.90.post1",
            "mypy-boto3-datapipeline==1.17.90.post1",
            "mypy-boto3-datasync==1.17.90.post1",
            "mypy-boto3-dax==1.17.90.post1",
            "mypy-boto3-detective==1.17.90.post1",
            "mypy-boto3-devicefarm==1.17.90.post1",
            "mypy-boto3-devops-guru==1.17.90.post1",
            "mypy-boto3-directconnect==1.17.90.post1",
            "mypy-boto3-discovery==1.17.90.post1",
            "mypy-boto3-dlm==1.17.90.post1",
            "mypy-boto3-dms==1.17.90.post1",
            "mypy-boto3-docdb==1.17.90.post1",
            "mypy-boto3-ds==1.17.90.post1",
            "mypy-boto3-dynamodb==1.17.90.post1",
            "mypy-boto3-dynamodbstreams==1.17.90.post1",
            "mypy-boto3-ebs==1.17.90.post1",
            "mypy-boto3-ec2==1.17.90.post1",
            "mypy-boto3-ec2-instance-connect==1.17.90.post1",
            "mypy-boto3-ecr==1.17.90.post1",
            "mypy-boto3-ecr-public==1.17.90.post1",
            "mypy-boto3-ecs==1.17.90.post1",
            "mypy-boto3-efs==1.17.90.post1",
            "mypy-boto3-eks==1.17.90.post1",
            "mypy-boto3-elastic-inference==1.17.90.post1",
            "mypy-boto3-elasticache==1.17.90.post1",
            "mypy-boto3-elasticbeanstalk==1.17.90.post1",
            "mypy-boto3-elastictranscoder==1.17.90.post1",
            "mypy-boto3-elb==1.17.90.post1",
            "mypy-boto3-elbv2==1.17.90.post1",
            "mypy-boto3-emr==1.17.90.post1",
            "mypy-boto3-emr-containers==1.17.90.post1",
            "mypy-boto3-es==1.17.90.post1",
            "mypy-boto3-events==1.17.90.post1",
            "mypy-boto3-finspace==1.17.90.post1",
            "mypy-boto3-finspace-data==1.17.90.post1",
            "mypy-boto3-firehose==1.17.90.post1",
            "mypy-boto3-fis==1.17.90.post1",
            "mypy-boto3-fms==1.17.90.post1",
            "mypy-boto3-forecast==1.17.90.post1",
            "mypy-boto3-forecastquery==1.17.90.post1",
            "mypy-boto3-frauddetector==1.17.90.post1",
            "mypy-boto3-fsx==1.17.90.post1",
            "mypy-boto3-gamelift==1.17.90.post1",
            "mypy-boto3-glacier==1.17.90.post1",
            "mypy-boto3-globalaccelerator==1.17.90.post1",
            "mypy-boto3-glue==1.17.90.post1",
            "mypy-boto3-greengrass==1.17.90.post1",
            "mypy-boto3-greengrassv2==1.17.90.post1",
            "mypy-boto3-groundstation==1.17.90.post1",
            "mypy-boto3-guardduty==1.17.90.post1",
            "mypy-boto3-health==1.17.90.post1",
            "mypy-boto3-healthlake==1.17.90.post1",
            "mypy-boto3-honeycode==1.17.90.post1",
            "mypy-boto3-iam==1.17.90.post1",
            "mypy-boto3-identitystore==1.17.90.post1",
            "mypy-boto3-imagebuilder==1.17.90.post1",
            "mypy-boto3-importexport==1.17.90.post1",
            "mypy-boto3-inspector==1.17.90.post1",
            "mypy-boto3-iot==1.17.90.post1",
            "mypy-boto3-iot-data==1.17.90.post1",
            "mypy-boto3-iot-jobs-data==1.17.90.post1",
            "mypy-boto3-iot1click-devices==1.17.90.post1",
            "mypy-boto3-iot1click-projects==1.17.90.post1",
            "mypy-boto3-iotanalytics==1.17.90.post1",
            "mypy-boto3-iotdeviceadvisor==1.17.90.post1",
            "mypy-boto3-iotevents==1.17.90.post1",
            "mypy-boto3-iotevents-data==1.17.90.post1",
            "mypy-boto3-iotfleethub==1.17.90.post1",
            "mypy-boto3-iotsecuretunneling==1.17.90.post1",
            "mypy-boto3-iotsitewise==1.17.90.post1",
            "mypy-boto3-iotthingsgraph==1.17.90.post1",
            "mypy-boto3-iotwireless==1.17.90.post1",
            "mypy-boto3-ivs==1.17.90.post1",
            "mypy-boto3-kafka==1.17.90.post1",
            "mypy-boto3-kendra==1.17.90.post1",
            "mypy-boto3-kinesis==1.17.90.post1",
            "mypy-boto3-kinesis-video-archived-media==1.17.90.post1",
            "mypy-boto3-kinesis-video-media==1.17.90.post1",
            "mypy-boto3-kinesis-video-signaling==1.17.90.post1",
            "mypy-boto3-kinesisanalytics==1.17.90.post1",
            "mypy-boto3-kinesisanalyticsv2==1.17.90.post1",
            "mypy-boto3-kinesisvideo==1.17.90.post1",
            "mypy-boto3-kms==1.17.90.post1",
            "mypy-boto3-lakeformation==1.17.90.post1",
            "mypy-boto3-lambda==1.17.90.post1",
            "mypy-boto3-lex-models==1.17.90.post1",
            "mypy-boto3-lex-runtime==1.17.90.post1",
            "mypy-boto3-lexv2-models==1.17.90.post1",
            "mypy-boto3-lexv2-runtime==1.17.90.post1",
            "mypy-boto3-license-manager==1.17.90.post1",
            "mypy-boto3-lightsail==1.17.90.post1",
            "mypy-boto3-location==1.17.90.post1",
            "mypy-boto3-logs==1.17.90.post1",
            "mypy-boto3-lookoutequipment==1.17.90.post1",
            "mypy-boto3-lookoutmetrics==1.17.90.post1",
            "mypy-boto3-lookoutvision==1.17.90.post1",
            "mypy-boto3-machinelearning==1.17.90.post1",
            "mypy-boto3-macie==1.17.90.post1",
            "mypy-boto3-macie2==1.17.90.post1",
            "mypy-boto3-managedblockchain==1.17.90.post1",
            "mypy-boto3-marketplace-catalog==1.17.90.post1",
            "mypy-boto3-marketplace-entitlement==1.17.90.post1",
            "mypy-boto3-marketplacecommerceanalytics==1.17.90.post1",
            "mypy-boto3-mediaconnect==1.17.90.post1",
            "mypy-boto3-mediaconvert==1.17.90.post1",
            "mypy-boto3-medialive==1.17.90.post1",
            "mypy-boto3-mediapackage==1.17.90.post1",
            "mypy-boto3-mediapackage-vod==1.17.90.post1",
            "mypy-boto3-mediastore==1.17.90.post1",
            "mypy-boto3-mediastore-data==1.17.90.post1",
            "mypy-boto3-mediatailor==1.17.90.post1",
            "mypy-boto3-meteringmarketplace==1.17.90.post1",
            "mypy-boto3-mgh==1.17.90.post1",
            "mypy-boto3-mgn==1.17.90.post1",
            "mypy-boto3-migrationhub-config==1.17.90.post1",
            "mypy-boto3-mobile==1.17.90.post1",
            "mypy-boto3-mq==1.17.90.post1",
            "mypy-boto3-mturk==1.17.90.post1",
            "mypy-boto3-mwaa==1.17.90.post1",
            "mypy-boto3-neptune==1.17.90.post1",
            "mypy-boto3-network-firewall==1.17.90.post1",
            "mypy-boto3-networkmanager==1.17.90.post1",
            "mypy-boto3-nimble==1.17.90.post1",
            "mypy-boto3-opsworks==1.17.90.post1",
            "mypy-boto3-opsworkscm==1.17.90.post1",
            "mypy-boto3-organizations==1.17.90.post1",
            "mypy-boto3-outposts==1.17.90.post1",
            "mypy-boto3-personalize==1.17.90.post1",
            "mypy-boto3-personalize-events==1.17.90.post1",
            "mypy-boto3-personalize-runtime==1.17.90.post1",
            "mypy-boto3-pi==1.17.90.post1",
            "mypy-boto3-pinpoint==1.17.90.post1",
            "mypy-boto3-pinpoint-email==1.17.90.post1",
            "mypy-boto3-pinpoint-sms-voice==1.17.90.post1",
            "mypy-boto3-polly==1.17.90.post1",
            "mypy-boto3-pricing==1.17.90.post1",
            "mypy-boto3-qldb==1.17.90.post1",
            "mypy-boto3-qldb-session==1.17.90.post1",
            "mypy-boto3-quicksight==1.17.90.post1",
            "mypy-boto3-ram==1.17.90.post1",
            "mypy-boto3-rds==1.17.90.post1",
            "mypy-boto3-rds-data==1.17.90.post1",
            "mypy-boto3-redshift==1.17.90.post1",
            "mypy-boto3-redshift-data==1.17.90.post1",
            "mypy-boto3-rekognition==1.17.90.post1",
            "mypy-boto3-resource-groups==1.17.90.post1",
            "mypy-boto3-resourcegroupstaggingapi==1.17.90.post1",
            "mypy-boto3-robomaker==1.17.90.post1",
            "mypy-boto3-route53==1.17.90.post1",
            "mypy-boto3-route53domains==1.17.90.post1",
            "mypy-boto3-route53resolver==1.17.90.post1",
            "mypy-boto3-s3==1.17.90.post1",
            "mypy-boto3-s3control==1.17.90.post1",
            "mypy-boto3-s3outposts==1.17.90.post1",
            "mypy-boto3-sagemaker==1.17.90.post1",
            "mypy-boto3-sagemaker-a2i-runtime==1.17.90.post1",
            "mypy-boto3-sagemaker-edge==1.17.90.post1",
            "mypy-boto3-sagemaker-featurestore-runtime==1.17.90.post1",
            "mypy-boto3-sagemaker-runtime==1.17.90.post1",
            "mypy-boto3-savingsplans==1.17.90.post1",
            "mypy-boto3-schemas==1.17.90.post1",
            "mypy-boto3-sdb==1.17.90.post1",
            "mypy-boto3-secretsmanager==1.17.90.post1",
            "mypy-boto3-securityhub==1.17.90.post1",
            "mypy-boto3-serverlessrepo==1.17.90.post1",
            "mypy-boto3-service-quotas==1.17.90.post1",
            "mypy-boto3-servicecatalog==1.17.90.post1",
            "mypy-boto3-servicecatalog-appregistry==1.17.90.post1",
            "mypy-boto3-servicediscovery==1.17.90.post1",
            "mypy-boto3-ses==1.17.90.post1",
            "mypy-boto3-sesv2==1.17.90.post1",
            "mypy-boto3-shield==1.17.90.post1",
            "mypy-boto3-signer==1.17.90.post1",
            "mypy-boto3-sms==1.17.90.post1",
            "mypy-boto3-sms-voice==1.17.90.post1",
            "mypy-boto3-snowball==1.17.90.post1",
            "mypy-boto3-sns==1.17.90.post1",
            "mypy-boto3-sqs==1.17.90.post1",
            "mypy-boto3-ssm==1.17.90.post1",
            "mypy-boto3-ssm-contacts==1.17.90.post1",
            "mypy-boto3-ssm-incidents==1.17.90.post1",
            "mypy-boto3-sso==1.17.90.post1",
            "mypy-boto3-sso-admin==1.17.90.post1",
            "mypy-boto3-sso-oidc==1.17.90.post1",
            "mypy-boto3-stepfunctions==1.17.90.post1",
            "mypy-boto3-storagegateway==1.17.90.post1",
            "mypy-boto3-sts==1.17.90.post1",
            "mypy-boto3-support==1.17.90.post1",
            "mypy-boto3-swf==1.17.90.post1",
            "mypy-boto3-synthetics==1.17.90.post1",
            "mypy-boto3-textract==1.17.90.post1",
            "mypy-boto3-timestream-query==1.17.90.post1",
            "mypy-boto3-timestream-write==1.17.90.post1",
            "mypy-boto3-transcribe==1.17.90.post1",
            "mypy-boto3-transfer==1.17.90.post1",
            "mypy-boto3-translate==1.17.90.post1",
            "mypy-boto3-waf==1.17.90.post1",
            "mypy-boto3-waf-regional==1.17.90.post1",
            "mypy-boto3-wafv2==1.17.90.post1",
            "mypy-boto3-wellarchitected==1.17.90.post1",
            "mypy-boto3-workdocs==1.17.90.post1",
            "mypy-boto3-worklink==1.17.90.post1",
            "mypy-boto3-workmail==1.17.90.post1",
            "mypy-boto3-workmailmessageflow==1.17.90.post1",
            "mypy-boto3-workspaces==1.17.90.post1",
            "mypy-boto3-xray==1.17.90.post1",
        ],
        "essential": [
            "mypy-boto3-cloudformation==1.17.90.post1",
            "mypy-boto3-dynamodb==1.17.90.post1",
            "mypy-boto3-ec2==1.17.90.post1",
            "mypy-boto3-lambda==1.17.90.post1",
            "mypy-boto3-rds==1.17.90.post1",
            "mypy-boto3-s3==1.17.90.post1",
            "mypy-boto3-sqs==1.17.90.post1",
        ],
        "accessanalyzer": ["mypy-boto3-accessanalyzer==1.17.90.post1"],
        "acm": ["mypy-boto3-acm==1.17.90.post1"],
        "acm-pca": ["mypy-boto3-acm-pca==1.17.90.post1"],
        "alexaforbusiness": ["mypy-boto3-alexaforbusiness==1.17.90.post1"],
        "amp": ["mypy-boto3-amp==1.17.90.post1"],
        "amplify": ["mypy-boto3-amplify==1.17.90.post1"],
        "amplifybackend": ["mypy-boto3-amplifybackend==1.17.90.post1"],
        "apigateway": ["mypy-boto3-apigateway==1.17.90.post1"],
        "apigatewaymanagementapi": ["mypy-boto3-apigatewaymanagementapi==1.17.90.post1"],
        "apigatewayv2": ["mypy-boto3-apigatewayv2==1.17.90.post1"],
        "appconfig": ["mypy-boto3-appconfig==1.17.90.post1"],
        "appflow": ["mypy-boto3-appflow==1.17.90.post1"],
        "appintegrations": ["mypy-boto3-appintegrations==1.17.90.post1"],
        "application-autoscaling": ["mypy-boto3-application-autoscaling==1.17.90.post1"],
        "application-insights": ["mypy-boto3-application-insights==1.17.90.post1"],
        "applicationcostprofiler": ["mypy-boto3-applicationcostprofiler==1.17.90.post1"],
        "appmesh": ["mypy-boto3-appmesh==1.17.90.post1"],
        "apprunner": ["mypy-boto3-apprunner==1.17.90.post1"],
        "appstream": ["mypy-boto3-appstream==1.17.90.post1"],
        "appsync": ["mypy-boto3-appsync==1.17.90.post1"],
        "athena": ["mypy-boto3-athena==1.17.90.post1"],
        "auditmanager": ["mypy-boto3-auditmanager==1.17.90.post1"],
        "autoscaling": ["mypy-boto3-autoscaling==1.17.90.post1"],
        "autoscaling-plans": ["mypy-boto3-autoscaling-plans==1.17.90.post1"],
        "backup": ["mypy-boto3-backup==1.17.90.post1"],
        "batch": ["mypy-boto3-batch==1.17.90.post1"],
        "braket": ["mypy-boto3-braket==1.17.90.post1"],
        "budgets": ["mypy-boto3-budgets==1.17.90.post1"],
        "ce": ["mypy-boto3-ce==1.17.90.post1"],
        "chime": ["mypy-boto3-chime==1.17.90.post1"],
        "cloud9": ["mypy-boto3-cloud9==1.17.90.post1"],
        "clouddirectory": ["mypy-boto3-clouddirectory==1.17.90.post1"],
        "cloudformation": ["mypy-boto3-cloudformation==1.17.90.post1"],
        "cloudfront": ["mypy-boto3-cloudfront==1.17.90.post1"],
        "cloudhsm": ["mypy-boto3-cloudhsm==1.17.90.post1"],
        "cloudhsmv2": ["mypy-boto3-cloudhsmv2==1.17.90.post1"],
        "cloudsearch": ["mypy-boto3-cloudsearch==1.17.90.post1"],
        "cloudsearchdomain": ["mypy-boto3-cloudsearchdomain==1.17.90.post1"],
        "cloudtrail": ["mypy-boto3-cloudtrail==1.17.90.post1"],
        "cloudwatch": ["mypy-boto3-cloudwatch==1.17.90.post1"],
        "codeartifact": ["mypy-boto3-codeartifact==1.17.90.post1"],
        "codebuild": ["mypy-boto3-codebuild==1.17.90.post1"],
        "codecommit": ["mypy-boto3-codecommit==1.17.90.post1"],
        "codedeploy": ["mypy-boto3-codedeploy==1.17.90.post1"],
        "codeguru-reviewer": ["mypy-boto3-codeguru-reviewer==1.17.90.post1"],
        "codeguruprofiler": ["mypy-boto3-codeguruprofiler==1.17.90.post1"],
        "codepipeline": ["mypy-boto3-codepipeline==1.17.90.post1"],
        "codestar": ["mypy-boto3-codestar==1.17.90.post1"],
        "codestar-connections": ["mypy-boto3-codestar-connections==1.17.90.post1"],
        "codestar-notifications": ["mypy-boto3-codestar-notifications==1.17.90.post1"],
        "cognito-identity": ["mypy-boto3-cognito-identity==1.17.90.post1"],
        "cognito-idp": ["mypy-boto3-cognito-idp==1.17.90.post1"],
        "cognito-sync": ["mypy-boto3-cognito-sync==1.17.90.post1"],
        "comprehend": ["mypy-boto3-comprehend==1.17.90.post1"],
        "comprehendmedical": ["mypy-boto3-comprehendmedical==1.17.90.post1"],
        "compute-optimizer": ["mypy-boto3-compute-optimizer==1.17.90.post1"],
        "config": ["mypy-boto3-config==1.17.90.post1"],
        "connect": ["mypy-boto3-connect==1.17.90.post1"],
        "connect-contact-lens": ["mypy-boto3-connect-contact-lens==1.17.90.post1"],
        "connectparticipant": ["mypy-boto3-connectparticipant==1.17.90.post1"],
        "cur": ["mypy-boto3-cur==1.17.90.post1"],
        "customer-profiles": ["mypy-boto3-customer-profiles==1.17.90.post1"],
        "databrew": ["mypy-boto3-databrew==1.17.90.post1"],
        "dataexchange": ["mypy-boto3-dataexchange==1.17.90.post1"],
        "datapipeline": ["mypy-boto3-datapipeline==1.17.90.post1"],
        "datasync": ["mypy-boto3-datasync==1.17.90.post1"],
        "dax": ["mypy-boto3-dax==1.17.90.post1"],
        "detective": ["mypy-boto3-detective==1.17.90.post1"],
        "devicefarm": ["mypy-boto3-devicefarm==1.17.90.post1"],
        "devops-guru": ["mypy-boto3-devops-guru==1.17.90.post1"],
        "directconnect": ["mypy-boto3-directconnect==1.17.90.post1"],
        "discovery": ["mypy-boto3-discovery==1.17.90.post1"],
        "dlm": ["mypy-boto3-dlm==1.17.90.post1"],
        "dms": ["mypy-boto3-dms==1.17.90.post1"],
        "docdb": ["mypy-boto3-docdb==1.17.90.post1"],
        "ds": ["mypy-boto3-ds==1.17.90.post1"],
        "dynamodb": ["mypy-boto3-dynamodb==1.17.90.post1"],
        "dynamodbstreams": ["mypy-boto3-dynamodbstreams==1.17.90.post1"],
        "ebs": ["mypy-boto3-ebs==1.17.90.post1"],
        "ec2": ["mypy-boto3-ec2==1.17.90.post1"],
        "ec2-instance-connect": ["mypy-boto3-ec2-instance-connect==1.17.90.post1"],
        "ecr": ["mypy-boto3-ecr==1.17.90.post1"],
        "ecr-public": ["mypy-boto3-ecr-public==1.17.90.post1"],
        "ecs": ["mypy-boto3-ecs==1.17.90.post1"],
        "efs": ["mypy-boto3-efs==1.17.90.post1"],
        "eks": ["mypy-boto3-eks==1.17.90.post1"],
        "elastic-inference": ["mypy-boto3-elastic-inference==1.17.90.post1"],
        "elasticache": ["mypy-boto3-elasticache==1.17.90.post1"],
        "elasticbeanstalk": ["mypy-boto3-elasticbeanstalk==1.17.90.post1"],
        "elastictranscoder": ["mypy-boto3-elastictranscoder==1.17.90.post1"],
        "elb": ["mypy-boto3-elb==1.17.90.post1"],
        "elbv2": ["mypy-boto3-elbv2==1.17.90.post1"],
        "emr": ["mypy-boto3-emr==1.17.90.post1"],
        "emr-containers": ["mypy-boto3-emr-containers==1.17.90.post1"],
        "es": ["mypy-boto3-es==1.17.90.post1"],
        "events": ["mypy-boto3-events==1.17.90.post1"],
        "finspace": ["mypy-boto3-finspace==1.17.90.post1"],
        "finspace-data": ["mypy-boto3-finspace-data==1.17.90.post1"],
        "firehose": ["mypy-boto3-firehose==1.17.90.post1"],
        "fis": ["mypy-boto3-fis==1.17.90.post1"],
        "fms": ["mypy-boto3-fms==1.17.90.post1"],
        "forecast": ["mypy-boto3-forecast==1.17.90.post1"],
        "forecastquery": ["mypy-boto3-forecastquery==1.17.90.post1"],
        "frauddetector": ["mypy-boto3-frauddetector==1.17.90.post1"],
        "fsx": ["mypy-boto3-fsx==1.17.90.post1"],
        "gamelift": ["mypy-boto3-gamelift==1.17.90.post1"],
        "glacier": ["mypy-boto3-glacier==1.17.90.post1"],
        "globalaccelerator": ["mypy-boto3-globalaccelerator==1.17.90.post1"],
        "glue": ["mypy-boto3-glue==1.17.90.post1"],
        "greengrass": ["mypy-boto3-greengrass==1.17.90.post1"],
        "greengrassv2": ["mypy-boto3-greengrassv2==1.17.90.post1"],
        "groundstation": ["mypy-boto3-groundstation==1.17.90.post1"],
        "guardduty": ["mypy-boto3-guardduty==1.17.90.post1"],
        "health": ["mypy-boto3-health==1.17.90.post1"],
        "healthlake": ["mypy-boto3-healthlake==1.17.90.post1"],
        "honeycode": ["mypy-boto3-honeycode==1.17.90.post1"],
        "iam": ["mypy-boto3-iam==1.17.90.post1"],
        "identitystore": ["mypy-boto3-identitystore==1.17.90.post1"],
        "imagebuilder": ["mypy-boto3-imagebuilder==1.17.90.post1"],
        "importexport": ["mypy-boto3-importexport==1.17.90.post1"],
        "inspector": ["mypy-boto3-inspector==1.17.90.post1"],
        "iot": ["mypy-boto3-iot==1.17.90.post1"],
        "iot-data": ["mypy-boto3-iot-data==1.17.90.post1"],
        "iot-jobs-data": ["mypy-boto3-iot-jobs-data==1.17.90.post1"],
        "iot1click-devices": ["mypy-boto3-iot1click-devices==1.17.90.post1"],
        "iot1click-projects": ["mypy-boto3-iot1click-projects==1.17.90.post1"],
        "iotanalytics": ["mypy-boto3-iotanalytics==1.17.90.post1"],
        "iotdeviceadvisor": ["mypy-boto3-iotdeviceadvisor==1.17.90.post1"],
        "iotevents": ["mypy-boto3-iotevents==1.17.90.post1"],
        "iotevents-data": ["mypy-boto3-iotevents-data==1.17.90.post1"],
        "iotfleethub": ["mypy-boto3-iotfleethub==1.17.90.post1"],
        "iotsecuretunneling": ["mypy-boto3-iotsecuretunneling==1.17.90.post1"],
        "iotsitewise": ["mypy-boto3-iotsitewise==1.17.90.post1"],
        "iotthingsgraph": ["mypy-boto3-iotthingsgraph==1.17.90.post1"],
        "iotwireless": ["mypy-boto3-iotwireless==1.17.90.post1"],
        "ivs": ["mypy-boto3-ivs==1.17.90.post1"],
        "kafka": ["mypy-boto3-kafka==1.17.90.post1"],
        "kendra": ["mypy-boto3-kendra==1.17.90.post1"],
        "kinesis": ["mypy-boto3-kinesis==1.17.90.post1"],
        "kinesis-video-archived-media": ["mypy-boto3-kinesis-video-archived-media==1.17.90.post1"],
        "kinesis-video-media": ["mypy-boto3-kinesis-video-media==1.17.90.post1"],
        "kinesis-video-signaling": ["mypy-boto3-kinesis-video-signaling==1.17.90.post1"],
        "kinesisanalytics": ["mypy-boto3-kinesisanalytics==1.17.90.post1"],
        "kinesisanalyticsv2": ["mypy-boto3-kinesisanalyticsv2==1.17.90.post1"],
        "kinesisvideo": ["mypy-boto3-kinesisvideo==1.17.90.post1"],
        "kms": ["mypy-boto3-kms==1.17.90.post1"],
        "lakeformation": ["mypy-boto3-lakeformation==1.17.90.post1"],
        "lambda": ["mypy-boto3-lambda==1.17.90.post1"],
        "lex-models": ["mypy-boto3-lex-models==1.17.90.post1"],
        "lex-runtime": ["mypy-boto3-lex-runtime==1.17.90.post1"],
        "lexv2-models": ["mypy-boto3-lexv2-models==1.17.90.post1"],
        "lexv2-runtime": ["mypy-boto3-lexv2-runtime==1.17.90.post1"],
        "license-manager": ["mypy-boto3-license-manager==1.17.90.post1"],
        "lightsail": ["mypy-boto3-lightsail==1.17.90.post1"],
        "location": ["mypy-boto3-location==1.17.90.post1"],
        "logs": ["mypy-boto3-logs==1.17.90.post1"],
        "lookoutequipment": ["mypy-boto3-lookoutequipment==1.17.90.post1"],
        "lookoutmetrics": ["mypy-boto3-lookoutmetrics==1.17.90.post1"],
        "lookoutvision": ["mypy-boto3-lookoutvision==1.17.90.post1"],
        "machinelearning": ["mypy-boto3-machinelearning==1.17.90.post1"],
        "macie": ["mypy-boto3-macie==1.17.90.post1"],
        "macie2": ["mypy-boto3-macie2==1.17.90.post1"],
        "managedblockchain": ["mypy-boto3-managedblockchain==1.17.90.post1"],
        "marketplace-catalog": ["mypy-boto3-marketplace-catalog==1.17.90.post1"],
        "marketplace-entitlement": ["mypy-boto3-marketplace-entitlement==1.17.90.post1"],
        "marketplacecommerceanalytics": ["mypy-boto3-marketplacecommerceanalytics==1.17.90.post1"],
        "mediaconnect": ["mypy-boto3-mediaconnect==1.17.90.post1"],
        "mediaconvert": ["mypy-boto3-mediaconvert==1.17.90.post1"],
        "medialive": ["mypy-boto3-medialive==1.17.90.post1"],
        "mediapackage": ["mypy-boto3-mediapackage==1.17.90.post1"],
        "mediapackage-vod": ["mypy-boto3-mediapackage-vod==1.17.90.post1"],
        "mediastore": ["mypy-boto3-mediastore==1.17.90.post1"],
        "mediastore-data": ["mypy-boto3-mediastore-data==1.17.90.post1"],
        "mediatailor": ["mypy-boto3-mediatailor==1.17.90.post1"],
        "meteringmarketplace": ["mypy-boto3-meteringmarketplace==1.17.90.post1"],
        "mgh": ["mypy-boto3-mgh==1.17.90.post1"],
        "mgn": ["mypy-boto3-mgn==1.17.90.post1"],
        "migrationhub-config": ["mypy-boto3-migrationhub-config==1.17.90.post1"],
        "mobile": ["mypy-boto3-mobile==1.17.90.post1"],
        "mq": ["mypy-boto3-mq==1.17.90.post1"],
        "mturk": ["mypy-boto3-mturk==1.17.90.post1"],
        "mwaa": ["mypy-boto3-mwaa==1.17.90.post1"],
        "neptune": ["mypy-boto3-neptune==1.17.90.post1"],
        "network-firewall": ["mypy-boto3-network-firewall==1.17.90.post1"],
        "networkmanager": ["mypy-boto3-networkmanager==1.17.90.post1"],
        "nimble": ["mypy-boto3-nimble==1.17.90.post1"],
        "opsworks": ["mypy-boto3-opsworks==1.17.90.post1"],
        "opsworkscm": ["mypy-boto3-opsworkscm==1.17.90.post1"],
        "organizations": ["mypy-boto3-organizations==1.17.90.post1"],
        "outposts": ["mypy-boto3-outposts==1.17.90.post1"],
        "personalize": ["mypy-boto3-personalize==1.17.90.post1"],
        "personalize-events": ["mypy-boto3-personalize-events==1.17.90.post1"],
        "personalize-runtime": ["mypy-boto3-personalize-runtime==1.17.90.post1"],
        "pi": ["mypy-boto3-pi==1.17.90.post1"],
        "pinpoint": ["mypy-boto3-pinpoint==1.17.90.post1"],
        "pinpoint-email": ["mypy-boto3-pinpoint-email==1.17.90.post1"],
        "pinpoint-sms-voice": ["mypy-boto3-pinpoint-sms-voice==1.17.90.post1"],
        "polly": ["mypy-boto3-polly==1.17.90.post1"],
        "pricing": ["mypy-boto3-pricing==1.17.90.post1"],
        "qldb": ["mypy-boto3-qldb==1.17.90.post1"],
        "qldb-session": ["mypy-boto3-qldb-session==1.17.90.post1"],
        "quicksight": ["mypy-boto3-quicksight==1.17.90.post1"],
        "ram": ["mypy-boto3-ram==1.17.90.post1"],
        "rds": ["mypy-boto3-rds==1.17.90.post1"],
        "rds-data": ["mypy-boto3-rds-data==1.17.90.post1"],
        "redshift": ["mypy-boto3-redshift==1.17.90.post1"],
        "redshift-data": ["mypy-boto3-redshift-data==1.17.90.post1"],
        "rekognition": ["mypy-boto3-rekognition==1.17.90.post1"],
        "resource-groups": ["mypy-boto3-resource-groups==1.17.90.post1"],
        "resourcegroupstaggingapi": ["mypy-boto3-resourcegroupstaggingapi==1.17.90.post1"],
        "robomaker": ["mypy-boto3-robomaker==1.17.90.post1"],
        "route53": ["mypy-boto3-route53==1.17.90.post1"],
        "route53domains": ["mypy-boto3-route53domains==1.17.90.post1"],
        "route53resolver": ["mypy-boto3-route53resolver==1.17.90.post1"],
        "s3": ["mypy-boto3-s3==1.17.90.post1"],
        "s3control": ["mypy-boto3-s3control==1.17.90.post1"],
        "s3outposts": ["mypy-boto3-s3outposts==1.17.90.post1"],
        "sagemaker": ["mypy-boto3-sagemaker==1.17.90.post1"],
        "sagemaker-a2i-runtime": ["mypy-boto3-sagemaker-a2i-runtime==1.17.90.post1"],
        "sagemaker-edge": ["mypy-boto3-sagemaker-edge==1.17.90.post1"],
        "sagemaker-featurestore-runtime": [
            "mypy-boto3-sagemaker-featurestore-runtime==1.17.90.post1"
        ],
        "sagemaker-runtime": ["mypy-boto3-sagemaker-runtime==1.17.90.post1"],
        "savingsplans": ["mypy-boto3-savingsplans==1.17.90.post1"],
        "schemas": ["mypy-boto3-schemas==1.17.90.post1"],
        "sdb": ["mypy-boto3-sdb==1.17.90.post1"],
        "secretsmanager": ["mypy-boto3-secretsmanager==1.17.90.post1"],
        "securityhub": ["mypy-boto3-securityhub==1.17.90.post1"],
        "serverlessrepo": ["mypy-boto3-serverlessrepo==1.17.90.post1"],
        "service-quotas": ["mypy-boto3-service-quotas==1.17.90.post1"],
        "servicecatalog": ["mypy-boto3-servicecatalog==1.17.90.post1"],
        "servicecatalog-appregistry": ["mypy-boto3-servicecatalog-appregistry==1.17.90.post1"],
        "servicediscovery": ["mypy-boto3-servicediscovery==1.17.90.post1"],
        "ses": ["mypy-boto3-ses==1.17.90.post1"],
        "sesv2": ["mypy-boto3-sesv2==1.17.90.post1"],
        "shield": ["mypy-boto3-shield==1.17.90.post1"],
        "signer": ["mypy-boto3-signer==1.17.90.post1"],
        "sms": ["mypy-boto3-sms==1.17.90.post1"],
        "sms-voice": ["mypy-boto3-sms-voice==1.17.90.post1"],
        "snowball": ["mypy-boto3-snowball==1.17.90.post1"],
        "sns": ["mypy-boto3-sns==1.17.90.post1"],
        "sqs": ["mypy-boto3-sqs==1.17.90.post1"],
        "ssm": ["mypy-boto3-ssm==1.17.90.post1"],
        "ssm-contacts": ["mypy-boto3-ssm-contacts==1.17.90.post1"],
        "ssm-incidents": ["mypy-boto3-ssm-incidents==1.17.90.post1"],
        "sso": ["mypy-boto3-sso==1.17.90.post1"],
        "sso-admin": ["mypy-boto3-sso-admin==1.17.90.post1"],
        "sso-oidc": ["mypy-boto3-sso-oidc==1.17.90.post1"],
        "stepfunctions": ["mypy-boto3-stepfunctions==1.17.90.post1"],
        "storagegateway": ["mypy-boto3-storagegateway==1.17.90.post1"],
        "sts": ["mypy-boto3-sts==1.17.90.post1"],
        "support": ["mypy-boto3-support==1.17.90.post1"],
        "swf": ["mypy-boto3-swf==1.17.90.post1"],
        "synthetics": ["mypy-boto3-synthetics==1.17.90.post1"],
        "textract": ["mypy-boto3-textract==1.17.90.post1"],
        "timestream-query": ["mypy-boto3-timestream-query==1.17.90.post1"],
        "timestream-write": ["mypy-boto3-timestream-write==1.17.90.post1"],
        "transcribe": ["mypy-boto3-transcribe==1.17.90.post1"],
        "transfer": ["mypy-boto3-transfer==1.17.90.post1"],
        "translate": ["mypy-boto3-translate==1.17.90.post1"],
        "waf": ["mypy-boto3-waf==1.17.90.post1"],
        "waf-regional": ["mypy-boto3-waf-regional==1.17.90.post1"],
        "wafv2": ["mypy-boto3-wafv2==1.17.90.post1"],
        "wellarchitected": ["mypy-boto3-wellarchitected==1.17.90.post1"],
        "workdocs": ["mypy-boto3-workdocs==1.17.90.post1"],
        "worklink": ["mypy-boto3-worklink==1.17.90.post1"],
        "workmail": ["mypy-boto3-workmail==1.17.90.post1"],
        "workmailmessageflow": ["mypy-boto3-workmailmessageflow==1.17.90.post1"],
        "workspaces": ["mypy-boto3-workspaces==1.17.90.post1"],
        "xray": ["mypy-boto3-xray==1.17.90.post1"],
    },
    zip_safe=False,
)
