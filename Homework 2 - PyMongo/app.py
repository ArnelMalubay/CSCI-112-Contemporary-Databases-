import functions as fn 
from pymongo import MongoClient
from pprint import pprint

if __name__ == "__main__":
    client = MongoClient("172.31.92.209", 27017)
    database = "sample"
    n = 5
    assessment = "exam"
    outputs = fn.find_classes(client, database, n, assessment)
    
    for output in outputs:
        pprint(output)
        