__author__ = 'zhenxing'

import codecs
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


class recommender:
    def __init__(self, data, k=1, metric = 'pearson', n = 5):
        """ initialize recommender
        currently, if data is dictionary the recommender is initialized
        to it.
        For all other data types of data, no initialization occurs
        k is the k value for k nearest neighbor
        metric is which distance formula to use
        n is the maximum number of recommendations to make"""
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        # for some reason I want to save the name of the metric
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson
        #
        # if data is dictionary set recommender data to it
        #
        if type(data).__name__ == 'dict':
            self.data = data

    def loadBookDB(self, path=''):
        """loads the BX book dataset. Path is where the BX files are
        located"""
        self.data = {}
        i = 0
        #
        # First load book ratings into self.data
        #
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r')
        #header = f.readline().split(';')
        #print header
        for line in f:
            i += 1
            if i == 1:
                continue

            fields = line.split(';')
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            self.data[user] = currentRatings
        f.close()

        # Now load books into self.productid2name
        # Books contains isbn, title, and author among other fields
        #
        f = codecs.open(path + "BX-Books.csv", 'r')
        for line in f:
            i += 1
            if i == 1:
                continue
            # separate line into fields
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip().strip('"')
            title = title + ' by ' + author
            self.productid2name[isbn] = title
        f.close()

        # Now load user info into both self.userid2name and
        # self.username2id
        #
        f = codecs.open(path + "BX-Users.csv", 'r')
        for line in f:
            i += 1
            if i == 1:
                continue
            # separate line into fields
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            if age != 'NULL':
                value = location + ' (age: ' + age + ')'
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        print('Loading data success!')

    def pearson(self, rating1, rating2):
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

    # return (username, distance)
    def computeNearestNeighbor(self, user):
        rating1 = self.data[user]
        neighbors = []
        for item in self.data:
            rating2 = self.data[item]
            #distance = Minkowski(rating1, rating2, 3)
            distance = self.fn(rating1, rating2)
            #distance = cosine_similarity(rating1, rating2)
            neighbors.append((item, distance))
            neighbors.sort(key=lambda likelihood:likelihood[1], reverse=True)
        #print(neighbors)
        return neighbors[1:1+self.k]


    def recommend(self, user):
        recommendation = {}

        closest_users = self.computeNearestNeighbor(user)

        user_rating = self.data[user]

        #computing the weighting.
        total_weight = 0.0
        for closest_user in closest_users:
            total_weight += closest_user[1]

        #now iterate through the k nearest users
        for closest_user in closest_users:
            weight = closest_user[1]/total_weight

            neighbor = closest_user[0]

            neighbor_rating = self.data[neighbor]

            for artist in neighbor_rating:
                if artist not in user_rating:
                    if artist not in recommendation:
                        recommendation[artist] = neighbor_rating[artist] * weight
                    else:
                        recommendation[artist] += neighbor_rating[artist] * weight

        recommendations = list(recommendation.items())
        #recommendation = sorted(recommendation, key = lambda  artist_tuple:artist_tuple[1], reverse = True)
        recommendations.sort(key = lambda  artist_tuple:artist_tuple[1], reverse = True)
        return recommendations


r = recommender(users, 3)
print r.recommend('Jordyn')

r.loadBookDB('/Users/zhenxing/Documents/Training_Courses/pg2dm/pg2dm-mycode/data/')
print r.data['171118']

r.recommend('171118')

