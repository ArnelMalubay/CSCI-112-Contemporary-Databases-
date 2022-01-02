#!/usr/bin/env python3

import boto3

# for read_csv
import pandas as pd

def insert_csv(ddb_table_name, csv_fileName):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(ddb_table_name)
    
    # convert csv to dataframe
    # from [1]
    df = pd.read_csv(csv_fileName)

    # convert dataframe to dictionary
    # from [2]
    items = df.to_dict('records')
    
    for x in items:
        table.put_item(Item=x)
        
if __name__ == '__main__':
    insert_csv('infections', 'InfectionsData.csv')