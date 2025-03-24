__author__ = 'Martina Lupini'

import csv
import numpy as np


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
        user_dict[user]["vector_ratings"][mask] -= avg_rating / len(movies_to_idx)



"""
This method adds the information about the rating to the movies saved in the dictionary data structure.
"""
def retrieve_ratings(movies_to_idx):
    user_dict = {}

    with open("dataset/ratings.csv", "r", encoding='utf-8') as file:
        next(file)
        csvFile = csv.reader(file)
        for line in csvFile:
            if len(line) == 4:
                user_id, movie_id, rating, timestamp = line

                if user_id not in user_dict:
                    user_dict[user_id] = {}
                    user_dict[user_id]["Movies_rated"] = {}
                    user_dict[user_id]["OHE_ratings"] = np.zeros(len(movies_to_idx), dtype=float)

                user_dict[user_id]["OHE_ratings"][movies_to_idx[movie_id]] = 1
                user_dict[user_id]["Movies_rated"][movie_id] = {"Rating": float(rating), "Rating_rescaled": float(rating) - 3.0, "Timestamp": timestamp}

    create_ratings_vector(user_dict, movies_to_idx)

    return user_dict

