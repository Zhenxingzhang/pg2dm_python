songs = {"Dr Dog/Fate": [2.5, 4, 3.5, 3, 5, 4, 1],
 "Phoenix/Lisztomania": [2, 5, 5, 3, 2, 1, 1],
 "Heartless Bastards/Out at Sea": [1, 5, 4, 2, 4, 1, 1],
 "Todd Snider/Don't Tempt Me": [4, 5, 4, 4, 1, 5, 1],
 "The Black Keys/Magic Potion": [1, 4, 5, 3.5, 5, 1, 1],
 "Glee Cast/Jessie's Girl": [1, 5, 3.5, 3, 4, 5, 1],
 "La Roux/Bulletproof": [5, 5, 4, 2, 1, 1, 1],
 "Mike Posner": [2.5, 4, 4, 1, 1, 1, 1],
 "Black Eyed Peas/Rock That Body": [2, 5, 5, 1, 2, 2, 4],
 "Lady Gaga/Alejandro": [1, 5, 3, 2, 1, 2, 1]}

users = {"Angelica": {"Dr Dog/Fate": "L", "Phoenix/Lisztomania": "L",
 "Heartless Bastards/Out at Sea": "D",
"Todd Snider/Don't Tempt Me": "D",
"The Black Keys/Magic Potion": "D",
"Glee Cast/Jessie's Girl": "L",
"La Roux/Bulletproof": "D",
"Mike Posner": "D",
"Black Eyed Peas/Rock That Body": "D",
"Lady Gaga/Alejandro": "L"},
 "Bill": {"Dr Dog/Fate": "L", "Phoenix/Lisztomania": "L",
 "Heartless Bastards/Out at Sea": "L",
"Todd Snider/Don't Tempt Me": "D",
"The Black Keys/Magic Potion": "L",
"Glee Cast/Jessie's Girl": "D",
"La Roux/Bulletproof": "D", "Mike Posner": "D",
 "Black Eyed Peas/Rock That Body": "D",
"Lady Gaga/Alejandro": "D"} }


def manhattan(vector1, vector2):
    """Computes the Manhattan distance between two vectors."""
    distance = 0
    total =0

    length = len(vector1)
    for idx in range(0, length):
        distance += abs(vector1[idx] - vector2[idx])
    return distance


def compute_nearest_neighbor(item_name,item_vector, item_vectors):
    """creates a sorted list of items based on their distance to item"""
    distances = []

    for otherItem in item_vectors:
        if otherItem != item_name:
            distance = manhattan(item_vector, item_vectors[otherItem])
            distances.append((distance, otherItem))
    # sort based on distance -- closest first
    distances.sort()
    return distances

def classify(user, item_name, item_vector):
    """Classify the itemName based on user ratings
    Should really have items and users as parameters"""

    #find the nearest neighbor for given songs
    nearest_song = compute_nearest_neighbor(item_name, item_vector, songs)[0][1]
    rating = users[user][nearest_song]
    return  rating

'''
We are predicting that Angelica will like Chris Cagle's I Breathe In, I Breathe Out because
that tune's nearest neighbor is Lady Gaga’s Alejandro and Angelica liked that tune.
'''

print classify('Angelica', 'Cagle', [1, 5, 2.5, 1, 1, 5, 1])