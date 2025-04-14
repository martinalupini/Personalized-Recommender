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

    # Mapping between movies and indexes
    movies_to_idx = {ch: idx for idx, ch in enumerate(movies_dict)}

    return movies_dict, movies_to_idx


def compute_similarities(movies_dict):
    sim_dict = {}
    pos_sim = 0
    #file = open("files/sim_pos.txt", "w")
    print("compute_similarities")
    start_time = time.time()

    # Generating only unique pairs of movies since the relationship is symmetric
    movie_pairs = combinations(movies_dict.keys(), 2)

    for movie, movie_2 in movie_pairs:

        users_in_common = movies_dict[movie]["Users_who_rated"] & movies_dict[movie_2]["Users_who_rated"]

        if len(users_in_common) > 0:
            numerator = 0.0
            for user in users_in_common:
                numerator += (movies_dict[movie]["Ratings"][user] * movies_dict[movie_2]["Ratings"][user])

            denominator = movies_dict[movie]["Denominator"] * movies_dict[movie_2]["Denominator"]
            sim = numerator / denominator if denominator != 0 else 0.0

            if math.isclose(sim, 0, abs_tol=1e-10):
                continue

            if sim > 0:
                pos_sim += 1
                #file.write(movie + ":"+movie_2+":"+str(sim)+"\n")

            sim_dict[(movie, movie_2)] = sim

    print("--- %s seconds ---" % (time.time() - start_time))
    #file.close

    return sim_dict, pos_sim


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
        avg_rating = avg_rating / len(user_dict[user]["Movies_rated"])
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
                    movies_dict[movie_id]["Ratings"] = {}
                    movies_dict[movie_id]["Users_who_rated"] = set()
                    movies_dict[movie_id]["rating_vect"] = []

                movies_dict[movie_id]["Ratings"][user_id] = float(rating)
                movies_dict[movie_id]["Users_who_rated"].add(user_id)
                movies_dict[movie_id]["rating_vect"].append(float(rating))

                if user_id not in user_dict:
                    user_dict[user_id] = {}
                    user_dict[user_id]["Movies_rated"] = {}
                    user_dict[user_id]["OHE_ratings"] = np.zeros(len(movies_to_idx), dtype=float)
            user_dict[user_id]["OHE_ratings"][movies_to_idx[movie_id]] = 1
            user_dict[user_id]["Movies_rated"][movie_id] = {"Rating": float(rating), "Timestamp": timestamp}

    for movie in movies_dict:
        if "Ratings" not in movies_dict[movie]:
            movies_dict[movie]["Users_who_rated"] = set()
            movies_dict[movie]["rating_vect"] = []
            movies_dict[movie]["Ratings"] = {}
            movies_dict[movie]["Mean"] = 0.0
            movies_dict[movie]["Denominator"] = 0.0
            continue

        mean = np.mean(movies_dict[movie]["rating_vect"])
        for user in movies_dict[movie]["Users_who_rated"]:
            movies_dict[movie]["Ratings"][user] -= mean
        movies_dict[movie]["Mean"] = mean
        movies_dict[movie]["Denominator"] = np.linalg.norm([movies_dict[movie]["Ratings"][user] for user in movies_dict[movie]["Users_who_rated"]])

    create_ratings_vector(user_dict, movies_to_idx)

    return user_dict

