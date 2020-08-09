# Workaround For CFN_EventBusPolicy_Bug156

This workaround uses CloudFormation Custom Resource to implement creation, delete and update of EventBusPolicy. The Custom Resource has parameter called 'TheCondition' instead of 'Condition' as the latter collides with CloudFormation intrinsic function.

## Usage

`$ zip function.zip lambda_function.py`

`$ aws s3 mb s3://mylambdacodebucket`

`$ aws s3 cp function.zip s3://mylambdacodebucket/`

Update CustomResourceEventBusPolicyTemplate.yaml to replace **S3Bucket** and **PrincipalOrgID**

Create stack in CloudFormation console using CustomResourceEventBusPolicyTemplate.yaml

