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
    
    try:
        if action == 'start':
            start_rds_response = start_rds_instances(dbclusteridentifier)
            start_ecs_response = start_ecs_tasks(cluster, service_names, service_desired_count)
            
            response_body = {
                'statusCode': 200,
                'body': json.dumps("Script execution completed. See CloudWatch logs for complete output"),
                'start_rds_response': start_rds_response,
                'start_ecs_response': start_ecs_response,
                'errorLogs': get_error_logs()
            }
        elif action == 'stop':
            stop_rds_response = stop_rds_instances(dbclusteridentifier)
            stop_ecs_response = stop_ecs_tasks(cluster, service_names, service_desired_count)
            
            response_body = {
                'statusCode': 200,
                'body': json.dumps("Script execution completed. See CloudWatch logs for complete output"),
                'stop_rds_response': stop_rds_response,
                'stop_ecs_response': stop_ecs_response,
                'errorLogs': get_error_logs()
            }
        else:
            response_body = {
                'statusCode': 400,
                'body': json.dumps("Invalid action: {0}".format(action))
            }
    except Exception as e:
        logger.error("An error occurred: {0}".format(str(e)))
        response_body = {
            'statusCode': 500,
            'body': json.dumps("An error occurred: {0}".format(str(e))),
            'errorLogs': get_error_logs()
        }

    return response_body




   
### start rds instances
def start_rds_instances(dbclusteridentifier):
    try:
        rds.start_db_cluster(DBClusterIdentifier=dbclusteridentifier)
        logger.info('Success :: start_db_instance ' + dbclusteridentifier) 
        return {
            'statusCode': 200,
            'body': json.dumps("started:OK")
        }
    except ClientError as e:
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps("Error starting RDS instances: " + str(e))
        }

### start ecs tasks
def start_ecs_tasks(cluster, service_names, service_desired_count):
    try:
        for service_name in service_names.split(","):
            response = client.update_service(
                cluster=cluster,
                service=service_name,
                desiredCount=service_desired_count
            )
            logger.info("Updated {0} service in {1} cluster with desired count set to {2} tasks".format(service_name, cluster, service_desired_count))
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': "Successfully updated ECS tasks",
                'new_desired_count': service_desired_count
            })
        }
    except Exception as e:
        logger.error("Error updating ECS tasks: {0}".format(str(e)))
        return {
            'statusCode': 500,
            'body': json.dumps("Error updating ECS tasks: " + str(e))
        }

### stop rds instances
def stop_rds_instances(dbclusteridentifier):
    try:
        rds.stop_db_cluster(DBClusterIdentifier=dbclusteridentifier)
        logger.info('Success :: stop_db_instance ' + dbclusteridentifier)
        return {
            'statusCode': 200,
            'body': json.dumps("stopped:OK")
        }
    except ClientError as e:
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps("Error stopping RDS instances: " + str(e))
        }

### stop ecs tasks
def stop_ecs_tasks(cluster, service_names, service_desired_count):
    try:
        for service_name in service_names.split(","):
            response = client.update_service(
                cluster=cluster,
                service=service_name,
                desiredCount=service_desired_count
            )
            logger.info("Updated {0} service in {1} cluster with desired count set to {2} tasks".format(service_name, cluster, service_desired_count))
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': "Successfully updated ECS tasks",
                'new_desired_count': service_desired_count
            })
        }
    except Exception as e:
        logger.error("Error updating ECS tasks: {0}".format(str(e)))
        return {
            'statusCode': 500,
            'body': json.dumps("Error updating ECS tasks: " + str(e))
        }


### Get CloudWatch logs for the Lambda function
def get_error_logs():
    log_group_name = '/aws/lambda/{0}'.format(os.environ['AWS_LAMBDA_FUNCTION_NAME'])
    logs_client = boto3.client('logs')
    
    try:
        response = logs_client.describe_log_streams(
            logGroupName=log_group_name,
            orderBy='LastEventTime',
            descending=True,
            limit=1
        )
        
        if 'logStreams' in response and len(response['logStreams']) > 0:
            log_stream_name = response['logStreams'][0]['logStreamName']
            
            response = logs_client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                startFromHead=True
            )
            
            error_logs = []
            for event in response['events']:
                error_logs.append(event['message'])
            
            return error_logs
    except Exception as e:
        logger.error("An error occurred while retrieving CloudWatch logs: {0}".format(str(e)))

    return []
