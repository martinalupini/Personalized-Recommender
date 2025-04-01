__author__ = 'Martina Lupini'


from Retriever import *
from UUCF import *
from IICF import *
from Basket import *


def main():

    """
    movies_dict, movies_to_idx = retrieve_movies()
    user_dict = retrieve_ratings(movies_to_idx)

    rec = top_N_recommendations("1", user_dict, movies_dict, movies_to_idx)
    """
    movies_dict, movies_to_idx = retrieve_movies()
    user_dict = retrieve_ratings_IICF(movies_dict, movies_to_idx)
    sim_dict = compute_similarities(movies_dict)
    #top_N = top_N_recommendations_IICF("1", user_dict, movies_dict, sim_dict)

    top_N = top_N_recommendations_basket(["1", "100", "1003"], movies_dict, sim_dict)





if __name__ == "__main__":
    main()

