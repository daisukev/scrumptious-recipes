def average_rating(ratings):
    sum_of_ratings = 0
    num_ratings = len(ratings)
    for rating in ratings:
        sum_of_ratings += rating.value
    if sum_of_ratings==0 and num_ratings == 0: # if there's no ratings yet
        return None
    elif sum_of_ratings == 0: # if there is all zero ratings
        return 0.0
    else: # otherwise, return the average
        return sum_of_ratings/ num_ratings
