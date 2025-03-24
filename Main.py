__author__ = 'Martina Lupini'

from Retriever import *
from UUCF import *


def main():
    movies_dict, movies_to_idx = retrieve_movies()
    user_dict = retrieve_ratings(movies_to_idx)



if __name__ == "__main__":
    main()

