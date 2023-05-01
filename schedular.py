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

##son input :  stop-instances
#{
# "action": "start",
# "dbInstance": "rds-tmt"
#}
#Json input :  stop-instances
#{
#  "action": "stop",
#  "dbInstance": "rds-tmt"
#}
##

def lambda_handler(event, context):
    logger.info("Event: " + str(event))

    dbInstance = event.get('dbInstance')
    cluster = event.get('cluster')
    service_names = event.get('service_names')
    service_desired_count = event.get('service_desired_count')
    action = event.get('action')
    
    if ('stop' == action):
        stop_rds_instances(dbInstance)         
    elif (action == 'start'):
        start_rds_instances(dbInstance)
    elif (ecs == 'true'):
        update_ecs_tasks(ecstasks)

    return {
        'statusCode': 200,
        'body': json.dumps("Script execution completed. See Cloudwatch logs for complete output")
    }   

### stop rds and ecs instances
def stop_rds_instances(dbInstance):
    try:
        #rds.stop_db_instance(DBInstanceIdentifier=dbInstance)
        rds.stop_db_cluster(DBClusterIdentifier=dbInstance)
        logger.info('Success :: stop_db_instance ' + dbInstance) 

    except ClientError as e:
        logger.error(e)   
    return "stopped:OK"


## start rds and ecs instances

def start_rds_instances(dbInstance):
    try:
        #rds.start_db_instance(DBInstanceIdentifier=dbInstance)
        rds.start_db_cluster(DBClusterIdentifier=dbInstance)
        logger.info('Success :: start_db_instance ' + dbInstance) 
    except ClientError as e:
        logger.error(e)   
    return "started:OK"


## start rds and ecs instances

def update_ecs_tasks(ecstasks):
    # cluster = event["cluster"]
    # service_names = event["service_names"]
    # service_desired_count = int(event["service_desired_count"])

    for service_name in service_names.split(","):
        response = client.update_service(
            cluster=cluster,
            service=service_name,
            desiredCount=service_desired_count
        )

        logger.info("Updated {0} service in {1} cluster with desire count set to {2} tasks".format(service_name, cluster, service_desired_count))

    return {
        'statusCode': 200,
        'new_desired_count': service_desired_count
    }
