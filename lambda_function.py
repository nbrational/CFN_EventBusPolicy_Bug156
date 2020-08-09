import json
import boto3
from botocore.vendored import requests

SUCCESS = "SUCCESS"
FAILED = "FAILED"

def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def lambda_handler(event, context):
    print('Loading function')
    print('Imported Boto3 Version %s' % boto3.__version__)
    cloudwatch_events = boto3.client('events')
    print("Received event: " + json.dumps(event, indent=2))
    responseData={}
    if(event['RequestType'] == 'Create'):
        try:
            print("Request Type:",event['RequestType'])
            print("Action:",event['ResourceProperties']['Action'])
            print("Principal:",event['ResourceProperties']['Principal'])
            print("StatementId:",event['ResourceProperties']['StatementId'])
            print("Condition.Type:",event['ResourceProperties']['TheCondition']['Type'])
            print("Condition.Key:",event['ResourceProperties']['TheCondition']['Key'])
            print("Condition.Value:",event['ResourceProperties']['TheCondition']['Value'])
            print("Processing Request based on Custom resource data")

            # Put an event rule
            print("Adding permission..")
            responseData = cloudwatch_events.put_permission(
                Action=event['ResourceProperties']['Action'],
                Principal=event['ResourceProperties']['Principal'],
                StatementId=event['ResourceProperties']['StatementId'],
                Condition={
                    'Type': event['ResourceProperties']['TheCondition']['Type'],
                    'Key': event['ResourceProperties']['TheCondition']['Key'],
                    'Value': event['ResourceProperties']['TheCondition']['Value']
                }
            )
            print(responseData)
            print("Sending response to custom resource")
            send(event, context, SUCCESS, responseData)
        except Exception as e:
            print('Failed to process:', e)
            send(event, context, FAILED, responseData)
    elif(event['RequestType'] == 'Delete'):
        try:
            print("Request Type:",event['RequestType'])
            print("Action:",event['ResourceProperties']['Action'])
            print("Principal:",event['ResourceProperties']['Principal'])
            print("StatementId:",event['ResourceProperties']['StatementId'])
            print("Condition.Type:",event['ResourceProperties']['TheCondition']['Type'])
            print("Condition.Key:",event['ResourceProperties']['TheCondition']['Key'])
            print("Condition.Value:",event['ResourceProperties']['TheCondition']['Value'])
            print("Processing Request based on Custom resource data")

            # Delete an event rule
            print("Removing permission..")
            responseData = cloudwatch_events.remove_permission(
                StatementId=event['ResourceProperties']['StatementId']
            )
            print(responseData)
            print("Sending response to custom resource")
            send(event, context, SUCCESS, responseData)
        except Exception as e:
            print('Failed to process:', e)
            send(event, context, FAILED, responseData)           
    elif (event['RequestType'] == 'Update'):
        try:
            print("Request Type:",event['RequestType'])
            print("Action:",event['ResourceProperties']['Action'])
            print("Principal:",event['ResourceProperties']['Principal'])
            print("StatementId:",event['ResourceProperties']['StatementId'])
            print("Condition.Type:",event['ResourceProperties']['TheCondition']['Type'])
            print("Condition.Key:",event['ResourceProperties']['TheCondition']['Key'])
            print("Condition.Value:",event['ResourceProperties']['TheCondition']['Value'])
            print("Processing Request based on Custom resource data")

            # Delete an event rule
            print("Removing permission..")
            responseData = cloudwatch_events.remove_permission(
                StatementId=event['ResourceProperties']['StatementId']
            )
            print(responseData)

            # Put an event rule
            print("Adding permission..")
            responseData = cloudwatch_events.put_permission(
                Action=event['ResourceProperties']['Action'],
                Principal=event['ResourceProperties']['Principal'],
                StatementId=event['ResourceProperties']['StatementId'],
                Condition={
                    'Type': event['ResourceProperties']['TheCondition']['Type'],
                    'Key': event['ResourceProperties']['TheCondition']['Key'],
                    'Value': event['ResourceProperties']['TheCondition']['Value']
                }
            )
            print(responseData)
            print("Sending response to custom resource")
            send(event, context, SUCCESS, responseData)
        except Exception as e:
            print('Failed to process:', e)
            send(event, context, FAILED, responseData)
