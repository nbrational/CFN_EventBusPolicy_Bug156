
# Workaround For CFN_EventBusPolicy_Bug156

  

## Background

The main issue is being tracked under [aws-cloudformation-coverage-roadmap issue #156](https://github.com/aws-cloudformation/aws-cloudformation-coverage-roadmap/issues/156)

## Issue Description

ChangeSet creation fails if CloudFormation stack has resource type AWS::Event::EventBusPolicy which uses Condition property. Sample template code to replicate the issue: 

    Resources:
      CompanyEventBusPolicy:
        Type: AWS::Events::EventBusPolicy
        Properties:
          Action: events:PutEvents
          Principal: '*'
          StatementId: EventBusPolicyStatement
          Condition:
            Type: StringEquals
            Key: aws:PrincipalOrgID
            Value: o-7gdn86yz4h

Reason being that property 'Condition' collides with the CloudFormation intrinsic function called '[Condition](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html)'.

## Workaround
The workaround is to use CloudFormation [Custom Resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html) to implement creation, delete and update of EventBusPolicy. 

> Custom resources enable you to write custom provisioning logic in templates that AWS CloudFormation runs anytime you create, update (if you changed the custom resource), or delete stacks.

The template for Custom Resource accepts parameter called 'TheCondition' instead of 'Condition' as the latter collides with CloudFormation intrinsic function. For example:-

    CustomEventBusPolicy:
	  Type: Custom::CustomEventBusPolicy
	  Properties:
	    ServiceToken: !GetAtt  CreateEventBusPolicyLambda.Arn
	    Region: !Ref  "AWS::Region"
	    EventBusName: ''
	    Action: events:PutEvents
	    Principal: '*'
	    StatementId: CM2PatchStatement
	    TheCondition:
	      Type: 'StringEquals'
	      Key: 'aws:PrincipalOrgID'
	      Value: 'o-6fmn73yz43'

A Lambda execution role `AWS::IAM::Role` and `AWS::Lambda::Function` can be created in the same template. Refer to file **CustomResourceEventBusPolicyTemplate.yaml**

## Usage

- Clone the repository
- Upload Custom resource Lambda code `lambda_function.py` to an S3 bucket:
- 
	    zip function.zip lambda_function.py
	    aws s3 mb s3://mylambdacodebucket
	    aws s3 cp function.zip s3://mylambdacodebucket/

- Update CustomResourceEventBusPolicyTemplate.yaml to replace **S3Bucket** and **PrincipalOrgID**

- Create stack in CloudFormation console using CustomResourceEventBusPolicyTemplate.yaml