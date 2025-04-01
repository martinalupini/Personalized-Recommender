__author__ = 'Martina Lupini'

import csv
import numpy as np
import math
from itertools import combinations
import time


def retrieve_movies():
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


def create_ratings_vector(user_dict, movies_to_idx):
    for user in user_dict:
        avg_rating = 0.0
        user_dict[user]["vector_ratings"] = np.zeros(len(movies_to_idx), dtype=float)
        for movie in user_dict[user]["Movies_rated"]:
            rating = user_dict[user]["Movies_rated"][movie]["Rating"]
            avg_rating += rating
            # Adding rating value to vector
            user_dict[user]["vector_ratings"][movies_to_idx[movie]] = rating

        # Creating a mask to subtract only elements different from 0
        mask = user_dict[user]["vector_ratings"] != 0
        avg_rating = avg_rating / len(movies_to_idx)
        user_dict[user]["vector_ratings"][mask] -= avg_rating
        user_dict[user]["average_rating"] = avg_rating



"""
This method adds the information about the rating to the movies saved in the dictionary data structure.
"""
def retrieve_ratings_IICF(movies_dict, movies_to_idx):
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
                    user_dict[user_id]["OHE_ratings"] = np.zeros(len(movies_to_idx), dtype=float)
            user_dict[user_id]["OHE_ratings"][movies_to_idx[movie_id]] = 1
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

    create_ratings_vector(user_dict, movies_to_idx)

    return user_dict

