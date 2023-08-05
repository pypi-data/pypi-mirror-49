import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-watchful",
    "version": "0.3.0",
    "description": "Watching your CDK apps since 2019",
    "url": "https://github.com/eladb/cdk-watchful",
    "long_description_content_type": "text/markdown",
    "author": "Elad Ben-Israel<elad.benisrael@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/eladb/cdk-watchful"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_watchful",
        "cdk_watchful._jsii"
    ],
    "package_data": {
        "cdk_watchful._jsii": [
            "cdk-watchful@0.3.0.jsii.tgz"
        ],
        "cdk_watchful": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.14.0",
        "publication>=0.0.3",
        "aws-cdk.aws-apigateway~=1.0,>=1.0.0",
        "aws-cdk.aws-cloudwatch~=1.0,>=1.0.0",
        "aws-cdk.aws-cloudwatch-actions~=1.0,>=1.0.0",
        "aws-cdk.aws-dynamodb~=1.0,>=1.0.0",
        "aws-cdk.aws-events~=1.0,>=1.0.0",
        "aws-cdk.aws-events-targets~=1.0,>=1.0.0",
        "aws-cdk.aws-lambda~=1.0,>=1.0.0",
        "aws-cdk.aws-sns~=1.0,>=1.0.0",
        "aws-cdk.aws-sns-subscriptions~=1.0,>=1.0.0",
        "aws-cdk.core~=1.0,>=1.0.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
