import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-redshift",
    "version": "1.0.0",
    "description": "The CDK Construct Library for AWS::Redshift",
    "url": "https://github.com/awslabs/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/awslabs/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_redshift",
        "aws_cdk.aws_redshift._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_redshift._jsii": [
            "aws-redshift@1.0.0.jsii.tgz"
        ],
        "aws_cdk.aws_redshift": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.14.0",
        "publication>=0.0.3",
        "aws-cdk.core~=1.0,>=1.0.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
