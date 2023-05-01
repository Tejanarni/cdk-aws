import sys
import botocore
import boto3
import json
import logging
from botocore.exceptions import ClientError

rds = boto3.client('rds')
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
	action = event.get('action')
	if ('stop' == action):
		stop_rds_instances(dbInstance)  	 
	elif (action == 'start'):
		start_rds_instances(dbInstance)

	return {
    	'statusCode': 200,
    	'body': json.dumps("Script execution completed. See Cloudwatch logs for complete output")
	}	

### stop rds instances
def stop_rds_instances(dbInstance):
	try:
		#rds.stop_db_instance(DBInstanceIdentifier=dbInstance)
		rds.stop_db_cluster(DBClusterIdentifier=dbInstance)
		logger.info('Success :: stop_db_instance ' + dbInstance) 
	except ClientError as e:
		logger.error(e)   
	return "stopped:OK"

def start_rds_instances(dbInstance):
	try:
		#rds.start_db_instance(DBInstanceIdentifier=dbInstance)
		rds.start_db_cluster(DBClusterIdentifier=dbInstance)
		logger.info('Success :: start_db_instance ' + dbInstance) 
	except ClientError as e:
		logger.error(e)   
	return "started:OK"
