__author__ = 'Martina Lupini'

import numpy as np
import numpy.ma as ma
import math
from itertools import islice

def top_k_similar_items(user, item, user_dict, sim_dict, k=20):
    similarities = {}
    for movie in user_dict[user]["Movies_rated"].keys():
        # Skipping if is the same movie as item
        if movie == item:
            continue
        print(sim_dict.shape)
        sim = sim_dict[int(item)-1][int(movie)-1]
        if sim > 0:
            similarities[movie] = sim

    # Sorting the dictionary based on the similarity (descending order)
    sorted_dict = dict(sorted(similarities.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first k elements
    neighbours = dict(islice(sorted_dict.items(), k))

    return neighbours


def predict_score_IICF(user, item, user_dict, sim_dict):

    neighbours = top_k_similar_items(user, item, user_dict, sim_dict)

    if len(neighbours) == 0:
        return 0.0

    numerator = 0.0
    denominator = 0.0
    for elem in neighbours:
        print(sim_dict.shape)
        sim = sim_dict[int(elem)-1][int(item)-1]
        numerator += sim * user_dict[user]["Movies_rated"][elem]["Rating"]
        denominator += math.abs(sim)

    return float(numerator / denominator)


def top_N_recommendations_IICF(user, user_dict, movies_dict, sim_dict, N=10):
    recommendations = {}
    for movie in movies_dict:

        # Not suggesting movies already watched by the user
        if movie in user_dict[user]["Movies_rated"]:
            continue

        recommendations[movie] = predict_score_IICF(user, movie, user_dict, sim_dict)

    sorted_dict = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first k elements
    top_N = dict(islice(sorted_dict.items(), N))

    return top_N
