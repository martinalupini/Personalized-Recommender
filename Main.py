__author__ = 'Martina Lupini'

from RetrieverUUCF import *
from UUCF import *


def main():
    movies_dict, movies_to_idx = retrieve_movies()
    user_dict = retrieve_ratings(movies_to_idx)

    rec = top_N_recommendations("1", user_dict, movies_dict, movies_to_idx)



if __name__ == "__main__":
    main()

