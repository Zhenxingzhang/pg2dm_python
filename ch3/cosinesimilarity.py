from math import sqrt

def compute_cosine_similarity(band1, band2, user_ratings):
    average_rating = {}
    for (user, rating) in user_ratings.items():
        average_rating[user] = (float(sum(rating.values())))/len(rating.values())

    num = 0.0
    dem1 = 0.0
    dem2 = 0.0
    for (user, rating) in user_ratings.items():
        #print user, rating
        if band1 in rating and band2 in rating:
            avg = average_rating[user]
            #print avg
            num += (rating[band1] - avg) * (rating[band2] - avg)
            dem1 += (rating[band1] - avg)**2
            dem2 += (rating[band2] - avg)**2

    similarity = num/(sqrt(dem1) * sqrt(dem2))

    return similarity

users3 = {"David": {"Imagine Dragons": 3, "Daft Punk": 5,
 "Lorde": 4, "Fall Out Boy": 1},
 "Matt": {"Imagine Dragons": 3, "Daft Punk": 4,
 "Lorde": 4, "Fall Out Boy": 1},
 "Ben": {"Kacey Musgraves": 4, "Imagine Dragons": 3,
 "Lorde": 3, "Fall Out Boy": 1},
 "Chris": {"Kacey Musgraves": 4, "Imagine Dragons": 4,
 "Daft Punk": 4, "Lorde": 3, "Fall Out Boy": 1},
 "Tori": {"Kacey Musgraves": 5, "Imagine Dragons": 4,
 "Daft Punk": 5, "Fall Out Boy": 3}}

print compute_cosine_similarity("Kacey Musgraves", "Daft Punk", users3)

