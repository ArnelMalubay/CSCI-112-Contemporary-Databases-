from datetime import datetime
from datetime import timedelta

def movies_per_theater(client, database, theater, year = None):
    movies = client[database].movies
    
    start_year_string = "1/1/" + year + " 0:0:0"
    start_year = datetime.strptime(start_year_string, "%m/%d/%Y %H:%M:%S")
    end_year_string = "12/31/" + year + " 0:0:0"
    end_year = datetime.strptime(end_year_string, "%m/%d/%Y %H:%M:%S")
    
    if year is None:
        match_query = {
            "theaters.theater_id" : theater,
        }
    else:
        match_query = {
            "theaters.theater_id" : theater,
            "released" : {
                "$gte" : start_year,
                "$lte" : end_year
            }
        }

    results = movies.aggregate([
        {
            "$unwind" : "$theaters"
        },
        {
            "$match" : match_query
        },
        {
            "$project" : {
                "_id" : {
                    "title" : "$title"
                },
                "date" : "$released"
            }
        }, {
            "$sort" : {
                "date" : 1
            }
        }
    ])
    
    return results

def commenters_by_genre(client, database, start, end):
    movies = client[database].movies
    
    start_string = start + " 0:0:0"
    end_string = end + " 0:0:0"
    
    start_date = datetime.strptime(start_string, "%m/%d/%Y %H:%M:%S")
    end_date = datetime.strptime(end_string, "%m/%d/%Y %H:%M:%S")
    
    results = movies.aggregate([
        {
            "$unwind": "$genres"
        },
        {
            "$unwind": "$comments"
        },
        {
            "$match" : {
                "comments.date" : {
                    "$gte" : start_date,
                    "$lte" : end_date
                }
            }
        },
        {
            "$group": {
                "_id": "$genres",
                "commenters": {
                    "$addToSet": "$comments.user"
                }
            }
        },
        {
            "$project": {
                "num_commenters": {
                    "$size": "$commenters"
                }
            }
        },
        {
            "$sort" : {
                "num_commenters" : -1
            }
        }
    ])
    
    return results

def user_comments_per_movie(client, database, username, start, end, movie=None):
    movies = client[database].movies
    
    start_string = start + " 0:0:0"
    end_string = end + " 0:0:0"
    
    start_date = datetime.strptime(start_string, "%m/%d/%Y %H:%M:%S")
    end_date = datetime.strptime(end_string, "%m/%d/%Y %H:%M:%S")
    
    if movie is None:
        match_query = {
            "$match" : {
                "comments.user.name" : username,
                "comments.date" : {
                    "$gte" : start_date,
                    "$lte" : end_date
                }
            }
        }
    else: 
        match_query = {
            "$match" : {
                "comments.user.name" : username,
                "title" : movie,
                "comments.date" : {
                    "$gte" : start_date,
                    "$lte" : end_date
                }
            }
        }
    
    results = movies.aggregate([
        {
            "$unwind" : "$comments"
        },
        match_query,
        {
            "$project" : {
                "_id" : 0,
                "user_id" : "$comments.user.user_id",
                "username" : username,
                "title" : 1,
                "date" : "$comments.date",
                "text" : "$comments.text",
                "comment_id" : "$comments.comment_id",
            }  
        },
        {
            "$sort" : {
                "date" : -1
            }
        }
    ])
    
    return results

def awards_per_director(client, database, director):
    movies = client[database].movies

    results = movies.aggregate([
        {
            "$unwind" : "$directors"
        },
        {
            "$match" : {
                "directors.name" : director
            }
        },
        {
            "$group" : {
                "_id" : {
                    "director" : "$directors.name"
                },
                "awards" : {
                    "$sum" : "$awards.wins"
                },
                "nominations" : {
                    "$sum" : "$awards.nominations"
                }
            }
        }
    ])
    
    return results


def theaters_within_radius(client, database, date, lon = None, lat = None, radius = None):
    movies = client[database].movies
    current = datetime.strptime(f"{date} 0:0:0", "%m/%d/%Y %H:%M:%S")

    # for the purposes of this project, we will assume that all movies run for 20 consecutive weeks starting from their release date
    screening_time = timedelta(weeks = 20) 

    filter_movie_date = {
        "$match": {
            "released": {
                "$gte": current - screening_time,
                "$lte": current
            }
        }
    }
    
    unwind = {
        "$unwind": "$theaters"
    }
    
    project = {
        "$project": {
            "title" : 1,
            "released" : 1,
            "theater_id" : "$theaters.theater_id",
            "location" : "$theaters.location"
        }
    }
    
    # note: Since each theater has a unique location, it suffices to just fetch the first location
    push = {
        "$group" : {
            "_id" : "$theater_id",
            "location" : {
                "$first" : "$location"
            },
            "movies" : {
                "$push" : {
                    "title" : "$title",
                    "released" : "$released"
                }
            }
        }
    }
    
    if (lon is None) or (lat is None) or (radius is None):
        results = movies.aggregate([
            filter_movie_date,
            unwind,
            project,
            push
    ])
    else:
        # filters all theaters within a given radius of a given location
        # Source: https://docs.mongodb.com/manual/tutorial/calculate-distances-using-spherical-geometry-with-2d-geospatial-indexes/
        equatorial_radius = 6378.137
        filter_theaters = {
            "$match" : {
                "location.geo.coordinates" : {
                    "$geoWithin": {
                        "$centerSphere": [
                            [lon, lat],
                            radius / equatorial_radius
                        ]
                    }
                }
            }
        }
        results = movies.aggregate([
            filter_movie_date,
            unwind,
            project,
            push,
            filter_theaters
    ])
    
    return results
