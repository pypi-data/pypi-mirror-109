import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.aws-iam",
    "version": "1.108.0",
    "description": "CDK routines for easily assigning correct and minimal IAM permissions",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_iam",
        "aws_cdk.aws_iam._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_iam._jsii": [
            "aws-iam@1.108.0.jsii.tgz"
        ],
        "aws_cdk.aws_iam": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.core==1.108.0",
        "aws-cdk.region-info==1.108.0",
        "constructs>=3.3.69, <4.0.0",
        "jsii>=1.30.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved",
        "Framework :: AWS CDK",
        "Framework :: AWS CDK :: 1"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
