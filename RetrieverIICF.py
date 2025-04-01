__author__ = 'Martina Lupini'

import csv
import numpy as np
import math
from itertools import combinations
import time



def compute_similarities(movies_dict):
    sim_dict = {}
    print("compute_similarities")
    start_time = time.time()
    # Generating only unique pairs of movies since the relationship is symmetric
    movie_pairs = combinations(movies_dict.keys(), 2)

    for movie, movie_2 in movie_pairs:

        users_in_common = movies_dict[movie]["Users_who_rated"] & movies_dict[movie_2]["Users_who_rated"]

        if len(users_in_common) <= 1:
            sim = 0.0
        else:

            numerator = 0.0
            for user in users_in_common:
                numerator += movies_dict[movie]["Ratings"][user-1] * movies_dict[movie_2]["Ratings"][user-1]

            denominator = movies_dict[movie]["Denominator"] * movies_dict[movie_2]["Denominator"]
            sim = float(numerator / denominator) if denominator != 0 else 0.0

        sim_dict[(movie, movie_2)] = sim
        sim_dict[(movie_2, movie)] = sim

    print("--- %s seconds ---" % (time.time() - start_time))
    return sim_dict



"""
This method adds the information about the rating to the movies saved in the dictionary data structure.
"""
def retrieve_ratings_IICF(movies_dict):
    user_dict = {}
    print("retrieve_ratings_IICF")
    with open("dataset/ratings.csv", "r", encoding='utf-8') as file:
        next(file)
        csvFile = csv.reader(file)
        for line in csvFile:
            if len(line) == 4:
                user_id, movie_id, rating, timestamp = line

                if "Ratings" not in movies_dict[movie_id]:
                    movies_dict[movie_id]["Ratings"] = np.zeros(100005, dtype=float)
                if "Users_who_rated" not in movies_dict[movie_id]:
                    movies_dict[movie_id]["Users_who_rated"] = set()

                movies_dict[movie_id]["Ratings"][int(user_id)-1] = float(rating)
                movies_dict[movie_id]["Users_who_rated"].add(int(user_id))

                if user_id not in user_dict:
                    user_dict[user_id] = {}
                    user_dict[user_id]["Movies_rated"] = {}
                user_dict[user_id]["Movies_rated"][movie_id] = {"Rating": float(rating), "Timestamp": timestamp}

    for movie in movies_dict:
        if "Users_who_rated" not in movies_dict[movie]:
            movies_dict[movie]["Users_who_rated"] = set()
        # Handling the case the movie has no ratings
        if "Ratings" not in movies_dict[movie]:
            movies_dict[movie]["Ratings"] = np.zeros(100005, dtype=float)
            movies_dict[movie]["Mean"] = 0.0
            movies_dict[movie]["Denominator"] = 0.0
            continue
        mean = np.mean(movies_dict[movie]["Ratings"])
        movies_dict[movie]["Ratings"] -= mean
        movies_dict[movie]["Mean"] = mean
        movies_dict[movie]["Denominator"] = math.sqrt(np.power(movies_dict[movie]['Ratings'], 2).sum())

    sim_dict = compute_similarities(movies_dict)

    return user_dict, sim_dict

