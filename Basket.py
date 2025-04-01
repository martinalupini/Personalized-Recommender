from IICF import *
from UUCF import *

# basket is a list of ids
def top_N_recommendations_basket(basket, movie_dict, sim_dict, only_positive=True, N=10):
    recommendations = {}
    for item in basket:

        for movie in movie_dict:

            # Skipping items already in basket
            if movie in basket:
                continue

            if movie not in recommendations:
                recommendations[movie] = 0.0

            sim = sim_dict[(item, movie)]

            if sim > 0 or not only_positive:
                recommendations[movie] += sim


    sorted_dict = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    top_N = dict(islice(sorted_dict.items(), N))

    return top_N


def top_N_recommendations_hybrid(user, user_dict, movies_dict, sim_dict, movies_to_idx, weight_IICF=0.5, weight_UUCF=0.5, N=10):
    recommendations = {}
    for movie in movies_dict:

        # Not suggesting movies already watched by the user
        if movie in user_dict[user]["Movies_rated"]:
            continue

        user_score, _ = predict_rating(user, movie, user_dict, movies_to_idx)
        recommendations[movie] = weight_IICF * predict_score_IICF(user, movie, user_dict, sim_dict) + weight_UUCF * user_score

    sorted_dict = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    top_N = dict(islice(sorted_dict.items(), N))

    return top_N