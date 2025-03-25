__author__ = 'Martina Lupini'

import csv
import numpy as np
import numpy.ma as ma
import math


def retrieve_movies_IICF():
    movies_dict = {}

    with open("dataset/movies.csv", "r", encoding='utf-8') as file:
        # skips the first line
        next(file)
        csvFile = csv.reader(file)
        for line in csvFile:
            if len(line) == 3:
                movie_id, title, genres = line
                genres = genres.split('|')

                # Saving movie info
                movies_dict[movie_id] = {"Title": title, "Genres_list": genres}

    # Mapping between genres and indexes
    movies_to_idx = {ch: idx for idx, ch in enumerate(movies_dict)}

    return movies_dict, movies_to_idx


def compute_similarities(movies_dict):

    sim_dict = np.zeros((len(movies_dict), len(movies_dict)))

    for movie in movies_dict:
        for movie_2 in movies_dict:

            # No need to compute similarity for the same user
            if movie == movie_2:
                continue

            # The similarity is simmetric so no need to compute it again
            if int(movie_2) < int(movie):
                sim_dict[int(movie)-1][int(movie_2)-1] = sim_dict[int(movie_2)-1][int(movie)-1]
                continue

            users_in_common = np.logical_and(movies_dict[movie]['OHE_ratings'], movies_dict[movie_2]['OHE_ratings'])

            """  DO WE NEED TO INCLUDE THAT?????????????????????
            num_movies_in_common = np.count_nonzero(users_in_common)

            if num_movies_in_common <= 1:
                return 0.0, 0.0
            """

            # Selecting only the ratings of the movies in common
            masked_vectors_1 = ma.masked_array(movies_dict[movie]['Ratings'], users_in_common)
            masked_vectors_2 = ma.masked_array(movies_dict[movie_2]['Ratings'], users_in_common)

            numerator = np.dot(masked_vectors_1, masked_vectors_2.T)

            denominator = math.sqrt(np.power(masked_vectors_1, 2).sum()) * math.sqrt(np.power(masked_vectors_2, 2).sum())
            if denominator == 0:
                return 0.0, 0.0

            sim_dict[int(movie)-1][int(movie_2)-1] = float(numerator / denominator)

    return sim_dict



"""
This method adds the information about the rating to the movies saved in the dictionary data structure.
"""
def retrieve_ratings_IICF(movies_dict):
    user_dict = {}
    with open("dataset/ratings.csv", "r", encoding='utf-8') as file:
        next(file)
        csvFile = csv.reader(file)
        for line in csvFile:
            if len(line) == 4:
                user_id, movie_id, rating, timestamp = line

                if "Ratings" not in movies_dict[movie_id]:
                    movies_dict[movie_id]["Ratings"] = np.zeros(100005, dtype=float)
                    movies_dict[movie_id]["OHE_ratings"] = np.zeros(100005, dtype=float)

                movies_dict[movie_id]["OHE_ratings"][int(user_id)-1] = 1
                movies_dict[movie_id]["Ratings"][int(user_id)-1] = float(rating)

                if user_id not in user_dict:
                    user_dict[user_id] = {}
                    user_dict[user_id]["Movies_rated"] = {}
                user_dict[user_id]["Movies_rated"][movie_id] = {"Rating": float(rating), "Timestamp": timestamp}

    for movie in movies_dict:
        # Handling the case the movie has no ratings
        if "Ratings" not in movies_dict[movie]:
            movies_dict[movie]["Ratings"] = np.zeros(100005, dtype=float)
            movies_dict[movie]["OHE_ratings"] = np.zeros(100005, dtype=float)
            movies_dict[movie]["Mean"] = 0.0
            continue
        mean = np.mean(movies_dict[movie]["Ratings"])
        movies_dict[movie]["Ratings"] -= mean
        movies_dict[movie]["Mean"] = mean

    sim_dict = compute_similarities(movies_dict)

    return user_dict, sim_dict

