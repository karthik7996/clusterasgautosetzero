import boto3
import os
import boto3
import os
import logging
import json
import urllib3



slack_url = os.environ['slack_url']
teams_url = os.environ['teams_url']
asg_name = os.environ['asg_name']


def lambda_handler(event, context):
    # your code here
    client = boto3.client('autoscaling')
    response = client.update_auto_scaling_group(
        AutoScalingGroupName= asg_name,
        MinSize=0,
        MaxSize=9,
        DesiredCapacity=0
    )
    message = "Cluster AutoScaling Group Set to Zero."+"\n"+ "Cluster-Asg-Name: " + str(asg_name) +"\n"+ "MinSize :" + 'Zero(0)' +"\n"+ "MaxSize :" + 'Zero(0)' +"\n" + "DesiredCapacity :" + 'Zero(0)'
    #message = "Cluster AutoScaling Group Set to Zero."+"\n"+ "ASG-NAME: " + str(asg_name)
    post_to_slack(message)
    return response

def post_to_slack(message):
    webhook_url = slack_url
    teams_webhook_url = teams_url
    slack_data = {'text': message}
    http = urllib3.PoolManager()
    headers={'Content-Type': 'application/json'}
    encoded_data = json.dumps(slack_data).encode('utf-8')
    response = http.request('POST',webhook_url,body=encoded_data,headers=headers)
    response1 = http.request('POST',teams_webhook_url,body=encoded_data,headers=headers)
    return True