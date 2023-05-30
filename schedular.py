import sys
import botocore
import boto3
import json
import logging
from botocore.exceptions import ClientError

rds = boto3.client('rds')
client = boto3.client('ecs')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


### extract all event parameters 

def lambda_handler(event, context):
    logger.info("Event: " + str(event))

    body = json.loads(event['body'])
    action = body.get('action')
    dbclusteridentifier = body['rds']['clusteridentifier']
    cluster = body['ecs']['cluster']
    service_names = body['ecs']['service_names']
    service_desired_count = int(body['ecs']['service_desired_count'])
    
    if ('start' == action):
        start_rds_instances(dbclusteridentifier)
        start_ecs_tasks(cluster, service_names, service_desired_count)
    
    elif (action == 'stop'):
        stop_rds_instances(dbclusteridentifier)
        stop_ecs_tasks(cluster, service_names, service_desired_count)


    return {
        'statusCode': 200,
        'body': json.dumps("Script execution completed. See Cloudwatch logs for complete output")
    }   
