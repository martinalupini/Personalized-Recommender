def write_top_k_neighbours(top_k_neigh, f):
    i = 1
    for neighbours in top_k_neigh:
        f.write(str(i) + ") id: " + neighbours + ", sim: " + str(round(top_k_neigh[neighbours], 6)) + '\n')
        i += 1


def write_top_k_most_similar(top_k_neigh, movie_dict, f):
    i = 1
    for item in top_k_neigh:
        f.write(str(i) + ") id: " + item + ", title: " + movie_dict[item]["Title"] + ", sim: " + str(round(top_k_neigh[item], 6)) + '\n')
        i += 1


def print_recommendations(rating_list, movie_dict, file):
    index = 1
    for movie in rating_list:
        file.write(str(index) + ") ID: " + movie + " Title: " + movie_dict[movie]["Title"] + ",\ngenres: " + str(movie_dict[movie]["Genres_list"]) +
                   "\nRating prediction: " + str(round(rating_list[movie], 6)) + "\n**********************************\n")
        index += 1

