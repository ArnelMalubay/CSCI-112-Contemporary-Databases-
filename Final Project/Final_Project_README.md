# Group 4 - Final Project

##### Creating a virtual environment
To create a virtual environment run
`python3 -m venv ./.env`
Activate it with 
`source .env/bin/activate`
Install dependencies with
`pip install -r requirements.txt`
To close the environment when you're done, run `deactivate`

##### Importing and Sharding the Data
*This assumes that you already have a sharded cluster in MongoDB. Before proceeding, ensure that the movies dataset, “movies_final.json” has been uploaded to your Cloud9 Dev Environment.*
Run the following commands on the Mongo Shell one line at a time.
`use project`
`db.movies.createIndex(   { "_id" :  "hashed" },   { "background" : true })`
`sh.enableSharding("project")`
`sh.shardCollection("project.movies", { "_id" : "hashed"}, false, {"numInitialChunks" : 3})`
Then, run the following on your terminal to import the dataset into MongoDB.
`mongoimport --db='project' --collection='movies' --file='movies_final.json' --jsonArray`
To verify that the dataset has now been imported and sharded, run the following on your Mongo Shell.
`use project`
`db.movies.getShardDistribution()`

##### Running the Scripts
*Make sure that "app.py" and "functions.py" are uploaded into your folder.*
To run the scripts, simply type the following on your terminal.
`python app.py`

##### Access Patterns
*NOTE:  All dates must be in the format "%m/%d/%Y,”  eg. "1/7/2011". Inputs enclosed in [ ]’s are optional and can be left blank as seen fit.*
1. Identify the number of movies in a theater for a given year
    * Function: movies_per_theater()
    * Input: Theater, [Year]
    * Output: Aggregated count of movies
    * Use Case: A theater owner wants to know the number of movies they screened for an annual report. They might also want to check out other theaters or other years for comparison.

2. Identify the number of users commenting on movies per genre
    * Function: get_commenter_count_by_genre()
    * Input: Start Date, End Date
    * Output: Aggregated count of users per genre
    * Use Case: A film scholar or a film production company might want to know which film genres get the most engagement from users in terms of comments.

3. Identify the comments of a user per movie over a given date range
    * Function: user_comments_per_movie()
    * Input: User, Start Date, End Date, [Movie] 
    * Output: Comments
    * Use Case: The database manager might want to check the comments of a specific user for movies for regulation and censorship.

4. Identify the award nominations and wins per director
    * Function: awards_per_director()
    * Input: Director
    * Output: Nominations, Wins
    * Use Case: A film enthusiast might want to know the nominations and wins of each director to compare which one bagged more awards.

5. Identify movies showing in the nearest theater at a given date and a set radius
    * Function: theaters_within_radius()
    * Input: Date, Longitude, Latitude, [Radius] (radius must be in terms of kilometers)
    * Output: Movies, Theaters
    * Use Case: A moviegoer might want to find movies to watch near them. Depending on their transportation methods, they might want to opt for theaters close to their location or they might be fine with farther locations.


