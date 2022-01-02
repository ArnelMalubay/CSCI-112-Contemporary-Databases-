#!/usr/bin/env python3

import boto3

def updatePatientReport(patient_id, city, patient_report_url):
	dynamodb = boto3.client('dynamodb')

	# from [3]
	response = dynamodb.update_item(
		TableName = 'infections',

		# match items with the given city and patient_id
		Key = {
			'City' : {'S': city},
			'PatientId' : {'N' : patient_id}
		},

		# update the item with the given patient_report_url
		AttributeUpdates = {
			'PatientReportUrl' : {
			    'Value' : { 'S' : patient_report_url }
	}})

if __name__ == '__main__':
	updatePatientReport(
	    '1',
	    'Salem',
	    'https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord1.txt'
	)
	updatePatientReport(
	    '2',
	    'Gallup',
	    'https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord2.txt'
	)
	updatePatientReport(
	    '3',
	    'Reno',
	    'https://us-west-2-aws-staging.s3.amazonaws.com/awsu-ilt/AWS-100-DEV/v2.2/binaries/input/lab-3-dynamoDB/PatientRecord3.txt'
	)
