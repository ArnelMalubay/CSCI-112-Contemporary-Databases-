#!/usr/bin/env python3
import boto3

def create_table(
	ddb_table_name,
	partition_key,
	sort_key
	):
	
	dynamodb = boto3.resource('dynamodb')
	
	# sort key is type "N" since the PatientId is a number
	attribute_definition = [
		{'AttributeName' : partition_key, "AttributeType": 'S'},
		{'AttributeName' : sort_key, "AttributeType" : 'N'}	
	]
	
	key_schema = [
		{'AttributeName' : partition_key, 'KeyType' : 'HASH'},
		{'AttributeName' : sort_key, 'KeyType' : 'RANGE'}
	]
	
	provisioned_throughput = {'ReadCapacityUnits' : 5, 'WriteCapacityUnits': 10}
	
	try:
		table = dynamodb.create_table(TableName = ddb_table_name,
									  KeySchema = key_schema,
									  AttributeDefinitions = attribute_definition,
									  ProvisionedThroughput = provisioned_throughput)
	except Exception as err:
		print("{0} Table cannot be created".format(ddb_table_name))

if __name__ == "__main__":
	create_table("infections", "City", "PatientId")