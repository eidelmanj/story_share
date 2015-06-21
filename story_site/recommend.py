### Basic Recommender Systems for Stories based on User Preferences



### TEST CASE
users = {
    "test1" : {
        "1" : 3.0,
        "35" : 2.0,
        "27" : 3.0,
        "46" : 4.0,
        "21" : 1.0
        },
    "test2" : {
        "1" : 2.0,
        "35" : 5.0,
        "27" : 3.0,
        "46" : 4.0,
        "21" : 4.0
        },
    "test3" : {
        "1" : 4.0,
        "35" : 3.0,
        "27" : 2.0,
        "46" : 1.0,
        "21" : 5.0
    },

    "test4" : {
        "1" : 5.0,
        "35" : 5.0,
        "27" : 3.0,
        "46" : 4.0,
        "21" : 5.0
    },

    "test5" : {
        "1" : 1.0,
        "35" : 2.0,
        "27" : 1.0,
        "46" : 3.0,
        "21" : 1.0
    },

}



# Computes the minkowski distance between 2 vectors.
def minkowski(xVec, yVec, r, ignoreNulls = True):
    assert (len(xVec) == len(yVec)), "Cannot compute distance between vectors of different sizes"
    r = float(r)

    sum = 0
    for i in xVec:
        if not ignoreNulls:
            sum = sum + ((xVec[i] - yVec[i]) ** r)

        else:
            if xVec[i] != 0 and yVec[i] != 0:
                sum = sum + ((xVec[i] - yVec[i]) ** r)

    return sum ** (1/r)



# Computes n nearest neighbours with a value of r for the minkowski distance metric
def nNearestNeighbours(username, users, r, n=10, getAll = False):
    # TODO - Add assert that r is valid and n is valid

    distances = []

    for user in users:
        if user != username:
            distance = minkowski(users[username], users[user], r)
            distances.append((distance, user))
    distances.sort()

    if getAll:
        return distances
        
    return distances[:n]


# Gives a prediction of how a user would rank each item based on the users most similar to them
# Simply a weighted average of 10 most similar users' rankings
# TODO - Make this a WEIGHTED average. Right now it's just the average
def estimateRankingVec(neighbours, users):
    assert (len(users)>0), "No users were given, therefore no prediction can be made"

    # TODO - assert that all users have keys for all possible stories
    keyList = users.values()[0].keys() # We assume that all users have keys for all possible stories


    estimatedRankings = []
    for key in keyList:
        totalRanks = 0
        for userPair in neighbours:
            user = userPair[1]
            totalRanks += users[user][key]


        estimatedRankings.append((float(totalRanks) / float(len(neighbours)), key))
    
    return estimatedRankings
    
    


neighbours = nNearestNeighbours("test1", users, 2)
print estimateRankingVec(neighbours, users)


