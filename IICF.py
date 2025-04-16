__author__ = 'Martina Lupini'

from itertools import islice


"""
This method computes top k most similar items rated by a target user.
"""
def top_k_similar_items(user, item, user_dict, sim_dict, k=20):
    similarities = {}
    for movie in user_dict[user]["Movies_rated"].keys():
        # Skipping if is the same movie as item
        if movie == item:
            continue

        if (item, movie) in sim_dict:
            sim = sim_dict[(item, movie)]
        elif (movie, item) in sim_dict:
            sim = sim_dict[(movie, item)]
        else:
            sim = 0

        # Considering only positive similarities
        if sim > 0:
            similarities[movie] = sim

    # Sorting the dictionary based on the similarity (descending order)
    sorted_dict = dict(sorted(similarities.items(), key=lambda item: item[1], reverse=True))

    # If there are not 20 elements then we select a smaller neighbourhood
    if len(sorted_dict) < k:
        k = len(sorted_dict)

    # Returning only the first k elements
    neighbours = dict(islice(sorted_dict.items(), k))

    return neighbours, similarities


"""
This method predicts the rating of a movie given a user.
"""
def predict_score_IICF(user, item, user_dict, sim_dict):
    # Obtaining the top k most similar items
    neighbours, _ = top_k_similar_items(user, item, user_dict, sim_dict)

    # If there are no similar items then the predicted rating is 0
    if len(neighbours) == 0:
        return 0.0

    numerator = 0.0
    denominator = 0.0
    for elem in neighbours:
        if (elem, item) in sim_dict:
            sim = sim_dict[(elem, item)]
        elif (item, elem) in sim_dict:
            sim = sim_dict[(item, elem)]
        else:
            continue
        numerator += sim * user_dict[user]["Movies_rated"][elem]["Rating"]
        denominator += abs(sim)

    if denominator == 0:
        return 0.0

    return float(numerator / denominator)


"""
This method returns the top N recommendations calculated using IICF.
"""
def top_N_recommendations_IICF(user, user_dict, movies_dict, sim_dict, N=10):
    recommendations = {}
    for movie in movies_dict:

        # Not suggesting movies already watched by the user
        if movie in user_dict[user]["Movies_rated"]:
            continue

        recommendations[movie] = predict_score_IICF(user, movie, user_dict, sim_dict)

    sorted_dict = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))

    # Returning only the first N elements
    top_N = dict(islice(sorted_dict.items(), N))

    return top_N
