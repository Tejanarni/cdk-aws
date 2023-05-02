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

    dbclusteridentifier = event['rds']['clusteridentifier']
    cluster = event['ecs']['cluster']
    service_names = event['ecs']['service_names']
    service_desired_count = int(event['ecs']['service_desired_count'])
    action = event.get('action')
    
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
### start rds instances
def start_rds_instances(dbclusteridentifier):
    try:
        #rds.start_db_instance(dbclusteridentifierIdentifier=dbclusteridentifier)
        rds.start_db_cluster(DBClusterIdentifier=dbclusteridentifier)
        logger.info('Success :: start_db_instance ' + dbclusteridentifier) 
    except ClientError as e:
        logger.error(e)   
    return "started:OK"

### start ecs tasks
def start_ecs_tasks(cluster, service_names, service_desired_count):
    for service_name in service_names.split(","):
        try:
            response = client.update_service(
                cluster=cluster,
                service=service_name,
                desiredCount=service_desired_count
            )
            logger.info("Updated {0} service in {1} cluster with desired count set to {2} tasks".format(service_name, cluster, service_desired_count))
        except Exception as e:
            logger.error("Error updating {0} service in {1} cluster: {2}".format(service_name, cluster, e))
    return {
        'statusCode': 200,
        'new_desired_count': service_desired_count
    }

### stop rds instances
def stop_rds_instances(dbclusteridentifier):
    try:
        #rds.stop_db_instance(dbclusteridentifierIdentifier=dbclusteridentifier)
        rds.stop_db_cluster(DBClusterIdentifier=dbclusteridentifier)
        logger.info('Success :: stop_db_instance ' + dbclusteridentifier) 

    except ClientError as e:
        logger.error(e)   
    return "stopped:OK"


### stop ecs tasks
def stop_ecs_tasks(cluster, service_names, service_desired_count):
    for service_name in service_names.split(","):
        try:
            response = client.update_service(
                cluster=cluster,
                service=service_name,
                desiredCount=service_desired_count
            )
            logger.info("Updated {0} service in {1} cluster with desired count set to {2} tasks".format(service_name, cluster, service_desired_count))
        except Exception as e:
            logger.error("Error updating {0} service in {1} cluster: {2}".format(service_name, cluster, e))
    return {
        'statusCode': 200,
        'new_desired_count': service_desired_count
    }