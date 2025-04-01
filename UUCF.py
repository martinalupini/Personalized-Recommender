__author__ = 'Martina Lupini'

import numpy as np
import numpy.ma as ma
import math
from itertools import islice


def pearson_correlation(user_1, user_2, user_dict, cut_off_value=10):
    movies_in_common = np.logical_and(user_dict[user_1]['OHE_ratings'], user_dict[user_2]['OHE_ratings'])
    num_movies_in_common = np.count_nonzero(movies_in_common)

    if num_movies_in_common <= 1:
        return 0.0, 0.0

    # Selecting only the ratings of the movies in common
    masked_vectors_1 = ma.masked_array(user_dict[user_1]['vector_ratings'], movies_in_common)
    masked_vectors_2 = ma.masked_array(user_dict[user_2]['vector_ratings'], movies_in_common)

    numerator = np.dot(masked_vectors_1, masked_vectors_2.T)

    denominator = math.sqrt(np.power(masked_vectors_1, 2).sum()) * math.sqrt(np.power(masked_vectors_2, 2).sum())
    if denominator == 0:
        return 0.0, 0.0

    weight = numerator / denominator

    # Adding significance weighting
    weight_significance = weight * (min(cut_off_value, num_movies_in_common) / cut_off_value)

    return float(weight), float(weight_significance)


def top_k_neighbours(main_user, item_of_interest, user_dict, k=20):
    weights = {}
    for user in user_dict:

        # Checking if user has rated the item
        if item_of_interest not in user_dict[user]['Movies_rated']:
            continue

        _, sim = pearson_correlation(main_user, user, user_dict)
        if sim > 0:
            weights[user] = sim

    # Sorting the dictionary based on the similarity (descending order)
    sorted_dict = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True))

    # If there are not 20 elements then we select a smaller neighbourhood
    if len(sorted_dict) < k:
        k = len(sorted_dict)

    # Returning only the first N elements
    neighbours = dict(islice(sorted_dict.items(), k))

    return neighbours, sorted_dict


def predict_rating(main_user, item, user_dict, movies_to_idx):
    avg_rating = user_dict[main_user]['average_rating']
    denominator = 0.0
    numerator = 0.0
    neighbors, _ = top_k_neighbours(main_user, item, user_dict)

    for user in neighbors:
        weight = neighbors[user]
        denominator += weight
        numerator += weight * user_dict[user]['vector_ratings'][movies_to_idx[item]]

    if denominator == 0:
        return 0.0, 0.0

    return float(avg_rating + (numerator / denominator)), numerator


def top_N_recommendations_UUCF(main_user, user_dict, movie_dict, movies_to_idx, N=10):
    score_dict = {}

    for movie in movie_dict:

        # Skipping movies already rated by the user
        if movie in user_dict[main_user]['Movies_rated']:
            continue

        score_dict[movie], _ = predict_rating(main_user, movie, user_dict, movies_to_idx)

    # Sorting the dictionary based on the similarity (descending order)
    sorted_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    recommendations = dict(islice(sorted_dict.items(), N))

    return recommendations
