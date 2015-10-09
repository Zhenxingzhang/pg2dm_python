from math import sqrt

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
         "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},
         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},
         "Jordyn":  {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0},
         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}
        }

def manhattan(rating1, rating2):
    distance =0;
    common_rate = False;
    for key in rating1:
        if key in rating2:
            common_rate = True
            distance += abs(rating1[key]-rating2[key])
    if common_rate:
        return distance
    else:
        return -1

def Euclidean(rating1, rating2):
    distance =0;
    common_rate = False;
    for key in rating1:
        if key in rating2:
            common_rate = True
            distance += (rating1[key]-rating2[key])*(rating1[key]-rating2[key])
    if common_rate:
        return sqrt(distance)
    else:
        return -1


def Minkowski(rating1,rating2, r):
    distance =0;
    common_rate = False;
    for key in rating1:
        if key in rating2:
            common_rate = True
            distance += pow(abs(rating1[key]-rating2[key]),r)
    if common_rate:
        return pow(distance, 1.0/r)
    else:
        return -1

def computeNearestNeighbor(username, users):
    rating1 = users[username]
    neighbors = []
    for user in users:
        rating2 = users[user]
        #distance = Minkowski(rating1, rating2, 3)
        distance = pearson(rating1, rating2)
        neighbors.append((user, distance))
    neighbors.sort(key=lambda likelihood:likelihood[1], reverse=True)
    print(neighbors)
    return neighbors[1][0]

def recommend(username, users):
    closest_user = computeNearestNeighbor(username, users)
    print("closest user:"+closest_user)
    user_rating = users[closest_user]
    recommendation = []
    for artist in users[closest_user]:
        if not artist in users[username]:
            recommendation.append((artist, user_rating[artist]))

    recommendation = sorted(recommendation, key=lambda artist_tuple: artist_tuple[1], reverse = True)
    return recommendation;

def pearson(rating1, rating2):
    sum_xy = 0; sum_x = 0; sum_y = 0
    sum_xx = 0; sum_yy = 0; n = 0;
    for key in rating1:
        if key in rating2:
            sum_xy += rating1[key]*rating2[key]
            sum_x += rating1[key]
            sum_y += rating2[key]
            sum_xx += rating1[key]*rating1[key]
            sum_yy += rating2[key]*rating2[key]
            n += 1
    if n == 0:
        return -1

    molecule = sum_xy - (sum_x * sum_y) / n
    denominator = sqrt(sum_xx - (sum_x**2) / n) * sqrt(sum_yy - (sum_y**2) / n)
    if denominator == 0:
        return 0
    return float(molecule)/denominator

print( recommend('Hailey', users))
#print( pearson(users['Angelica'], users['Bill']) )
#print( pearson(users['Angelica'], users['Hailey']) )
#print( pearson(users['Angelica'], users['Jordyn']) )
#print( recommend('Chan', users))