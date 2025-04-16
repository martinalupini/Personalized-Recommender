__author__ = 'Martina Lupini'

import numpy as np
from itertools import islice

"""
This method computes the Pearson correlation between two users.
"""
def pearson_correlation(user_1, user_2, user_dict, cut_off_value=10):
    movies_in_common = np.logical_and(user_dict[user_1]['OHE_ratings'], user_dict[user_2]['OHE_ratings']).astype(int)

    num_movies_in_common = np.count_nonzero(movies_in_common)

    # If the users have 0 or 1 items in common then the weight of correlation is 0
    if num_movies_in_common <= 1:
        return 0.0, 0.0

    # Selecting only the ratings of the movies in common
    masked_vectors_1 = user_dict[user_1]['vector_ratings'] * movies_in_common
    masked_vectors_2 = user_dict[user_2]['vector_ratings'] * movies_in_common

    numerator = np.dot(masked_vectors_1, masked_vectors_2.T)

    denominator = np.linalg.norm(masked_vectors_1) * np.linalg.norm(masked_vectors_2)

    if denominator == 0:
        return 0.0, 0.0

    weight = numerator / denominator

    # Adding significance weighting
    weight_significance = weight * (min(cut_off_value, num_movies_in_common) / cut_off_value)

    return float(weight), float(weight_significance)


"""
This method computes top k neighbours given a user and a movie.
"""
def top_k_neighbours(main_user, item_of_interest, user_dict, k=20):
    weights = {}
    for user in user_dict:

        # Checking if user has rated the item
        if item_of_interest not in user_dict[user]['Movies_rated']:
            continue

        # Calculating similarity value
        _, sim = pearson_correlation(main_user, user, user_dict)

        # Only considering users with positive similarity
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


"""
This method predicts the rating of a movie given a user.
"""
def predict_rating(main_user, item, user_dict, movies_to_idx):
    # Getting average rating of user
    avg_rating = user_dict[main_user]['average_rating']
    denominator = 0.0
    numerator = 0.0

    # Finding top k neighbours
    neighbors, _ = top_k_neighbours(main_user, item, user_dict)

    for user in neighbors:
        weight = neighbors[user]
        denominator += weight
        numerator += weight * user_dict[user]['vector_ratings'][movies_to_idx[item]]

    if denominator == 0:
        return 0.0, 0.0

    return float(avg_rating + (numerator / denominator)), float((numerator / denominator))


"""
This method returns the top N recommendations calculated using UUCF.
"""
def top_N_recommendations_UUCF(main_user, user_dict, movie_dict, movies_to_idx, N=10):
    score_dict = {}

    for movie in movie_dict:

        # Skipping movies already rated by the user
        if movie in user_dict[main_user]['Movies_rated']:
            continue

        # Predict rating for movie
        score_dict[movie], _ = predict_rating(main_user, movie, user_dict, movies_to_idx)

    # Sorting the dictionary based on the predicted rating (descending order)
    sorted_dict = dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    recommendations = dict(islice(sorted_dict.items(), N))

    return recommendations
