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


def compute_similarities(movies_dict, movies_to_idx):

    sim_dict = {}

    for movie in movies_dict:
    #TODO: see how it is computed in pearson similarity



"""
This method adds the information about the rating to the movies saved in the dictionary data structure.
"""
def retrieve_ratings(movies_dict, movies_to_idx):

    with open("dataset/ratings.csv", "r", encoding='utf-8') as file:
        next(file)
        csvFile = csv.reader(file)
        for line in csvFile:
            if len(line) == 4:
                user_id, movie_id, rating, timestamp = line

                if "Ratings" not in movies_dict[movie_id]:
                    movies_dict[movie_id]["Ratings"] = np.zeros(100005, dtype=float)
                    movies_dict[movie_id]["OHE_ratings"] = np.zeros(100005, dtype=float)

                movies_dict[user_id]["OHE_ratings"][int(user_id)-1] = 1
                movies_dict[movie_id]["Ratings"][int(user_id)-1] = float(rating)

    for movie in movies_dict:
        mean = np.mean(movies_dict[movie]["Ratings"])
        movies_dict[movie]["Ratings"] -= mean
        movies_dict[movie]["Mean"] = mean

    compute_similarities(movies_dict, movies_to_idx)

