
# Find the top n classes with the highest average score on a specified assessment type

def find_classes(client, database, n, assessment):
    grades = client[database].grades
    result = grades.aggregate([
        {"$unwind" : "$scores"
        },
        {"$match" : {
                "scores.type" : assessment
                    }
        },
        {"$group" : {
                "_id" : "$class_id",
                "avg_score" : {"$avg" : "$scores.score"}
                    }
        },
        {"$sort" : {
               "avg_score" : -1
                   }
        },
        {"$limit" : n}
    ])
    return result
