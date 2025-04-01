def write_top_k_neighbours(top_k_neigh, f):
    for neighbours in top_k_neigh:
        f.write("id: " + neighbours + ", sim: " + str(top_k_neigh[neighbours]) + '\n')


def write_top_k_most_similar(top_k_neigh, movie_dict, f):
    for item in top_k_neigh:
        f.write("id: " + item + ", title: " + movie_dict[item]["Title"] + ", sim: " + str(top_k_neigh[item]) + '\n')


def print_recommendations(rating_list, movie_dict, file):
    index = 1
    for movie in rating_list:
        file.write(str(index) + ") ID: " + movie + " Title: " + movie_dict[movie]["Title"] +
                   "\nRating prediction: " + str(rating_list[movie]) + "\n**********************************\n")
        index += 1

