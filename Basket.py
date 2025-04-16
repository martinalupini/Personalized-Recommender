from IICF import *
from UUCF import *


"""
This method returns the top N recommendations calculated using Basket recommendations. Here the basket is represented as 
a list of movies' ids.
"""
def top_N_recommendations_basket(basket, movie_dict, sim_dict, only_positive=True, N=10):
    recommendations = {}
    for item in basket:

        for movie in movie_dict:

            # Skipping items already in basket
            if movie in basket:
                continue

            if movie not in recommendations:
                recommendations[movie] = 0.0

            # To compute the similarities we reuse the IICF model
            if (item, movie) in sim_dict:
                sim = sim_dict[(item, movie)]
            elif (movie, item) in sim_dict:
                sim = sim_dict[(movie, item)]
            else:
                sim = 0.0

            # If only positive similarities need to be used (only_positive == True) then the similarity is considered only if it's positive.
            # Otherwise, it is considered a priori.
            if sim > 0 or not only_positive:
                recommendations[movie] += sim

    # Sorting the dictionary based on the similarity (descending order)
    sorted_dict = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    top_N = dict(islice(sorted_dict.items(), N))

    return top_N


"""
This method returns the top N recommendations calculated using an Hybrid recommender.
"""
def top_N_recommendations_hybrid(user, user_dict, movies_dict, sim_dict, movies_to_idx, weight_IICF=0.5, weight_UUCF=0.5, N=10):
    recommendations = {}
    for movie in movies_dict:

        # Not suggesting movies already watched by the user
        if movie in user_dict[user]["Movies_rated"]:
            continue

        user_score, _ = predict_rating(user, movie, user_dict, movies_to_idx)
        recommendations[movie] = weight_IICF * predict_score_IICF(user, movie, user_dict, sim_dict) + weight_UUCF * user_score

    # Sorting the dictionary based on the predicted rating (descending order)
    sorted_dict = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    top_N = dict(islice(sorted_dict.items(), N))

    return top_N