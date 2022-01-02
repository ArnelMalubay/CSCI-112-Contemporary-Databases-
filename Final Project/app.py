import functions as fn
from pymongo import MongoClient
from pprint import pprint

if __name__ == "__main__":
    client = MongoClient("172.31.29.253", 27017)
    
    print("Use case 1: Movies per theater per year\n")
    movies = fn.movies_per_theater(client, "project", "59a47287cfa9a3a73e51e96d", "2005")
    for movie in movies:
        pprint(movie)

    print("\nUse case 2: Number of users commenting per genre\n")
    genre_commenters = fn.commenters_by_genre(client, "project", "1/1/2011", "1/1/2021")
    for genre in genre_commenters:
        pprint(genre)

    print("\nUse case 3: Comments of a user per movie over a date range\n")
    comments = fn.user_comments_per_movie(client, "project", "Myrcella Baratheon", "1/1/1970", "1/1/2021", "1989")
    for comment in comments:
        pprint(comment)
    
    print("\nUse case 4: Award, nominations, and wins per director\n")
    awards = fn.awards_per_director(client, "project", "Craig Ross Jr.")
    for award in awards:
        pprint(award)
    
    print("\nUse case 5: Movies showing in the nearest theaters given a date over a set radius\n")
    theaters = fn.theaters_within_radius(client, "project", "1/7/2011", -75.139755, 39.916004, 50)  
    for theater in theaters:
        pprint(theater)
