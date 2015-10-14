#
#  Template -- please add code for the two functions
#              getMedian
#              getAbsoluteStandardDeviation
#
# also download the file athletesTrainingSet.txt, which you should
# put in the same folder as this file.



class Classifier:

    def __init__(self, filename):

        self.medianAndDeviation = []

        # reading the data in from the file
        f = open(filename)
        lines = f.readlines()
        f.close()
        self.format = lines[0].strip().split('\t')
        self.data = []
        for line in lines[1:]:
            fields = line.strip().split('\t')
            ignore = []
            vector = []
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(float(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i]
            self.data.append((classification, vector, ignore))
        self.rawData = list(self.data)
        #get the vector dimension
        self.v_dim = len(self.data[0][1])
        #now normalize the data;
        for idx in range(self.v_dim):
            self.normalize_column(idx)
        #
        # print [row[1] for row in self.data]

    ##################################################
    ###
    ###  FINISH THE FOLLOWING TWO METHODS

    def getMedian(self, alist):
        """return median of alist"""
        alist.sort()
        size = len(alist)
        #print size
        if size % 2 == 0:
            return (alist[(size-1)/2] + alist[size/2])/2.0
        else:
            return alist[size/2]


    def getAbsoluteStandardDeviation(self, alist, median):
        length = len(alist)
        diffs = 0.0
        for item in alist:
            diffs += abs(item - median)

        return diffs/length

    def normalize_column(self, column_idx):
        """given a column number, normalize that column in self.data"""
        # first extract values to list
        vec_column = [ v[1][column_idx] for v in self.data]
        median = self.getMedian(vec_column)
        asd = self.getAbsoluteStandardDeviation(vec_column, median)
        self.medianAndDeviation.append((median, asd))
        for v in self.data:
            v[1][column_idx] = (v[1][column_idx] - median) / asd

        # vec_column = [ v[1][column_idx] for v in self.data]
        # min_value = min(vec_column)
        # max_value = max(vec_column)
        # print min_value, max_value
        # median = min_value
        # asd = float((max_value-min_value))
        # self.medianAndDeviation.append((median, asd))
        # for v in self.data:
        #      v[1][column_idx] = (v[1][column_idx] - min_value) / asd


    def normalizeVector(self, v):
        """We have stored the median and asd for each column.
        We now use them to normalize vector v"""
        vector = list(v)
        for i in range(len(vector)):
            (median, asd) = self.medianAndDeviation[i]
            vector[i] = (vector[i] - median) / asd
        return vector

    def classify(self, itemVector):
        """Return class we think item Vector is in"""
        itemVector = self.normalizeVector(itemVector)
        neighbors = self.nearestNeighbor(itemVector)
        #print neighbors
        return(neighbors[1][0])

    def nearestNeighbor(self, vector):
        return min([(self.manhattan(vector, item[1]), item) for item in self.data])

    def manhattan(self, vector1, vector2):
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))


def unitTest():
    classifier = Classifier('../data/ch4/athletesTrainingSet.txt')
    br = ('Basketball', [72, 162], ['Brittainey Raven'])
    nl = ('Gymnastics', [61, 76], ['Viktoria Komova'])
    cl = ("Basketball", [74, 190], ['Crystal Langhorne'])
    # first check normalize function
    brNorm = classifier.normalizeVector(br[1])
    nlNorm = classifier.normalizeVector(nl[1])
    clNorm = classifier.normalizeVector(cl[1])
    assert(brNorm == classifier.data[1][1])
    assert(nlNorm == classifier.data[-1][1])
    print('normalizeVector fn OK')
    # check distance
    assert (round(classifier.manhattan(clNorm, classifier.data[1][1]), 5) == 1.16823)
    assert(classifier.manhattan(brNorm, classifier.data[1][1]) == 0)
    assert(classifier.manhattan(nlNorm, classifier.data[-1][1]) == 0)
    print('Manhattan distance fn OK')
    # Brittainey Raven's nearest neighbor should be herself
    result = classifier.nearestNeighbor(brNorm)
    assert(result[1][2]== br[2])
    # Nastia Liukin's nearest neighbor should be herself
    result = classifier.nearestNeighbor(nlNorm)
    assert(result[1][2]== nl[2])
    # Crystal Langhorne's nearest neighbor is Jennifer Lacy"
    assert(classifier.nearestNeighbor(clNorm)[1][2][0] == "Jennifer Lacy")
    print("Nearest Neighbor fn OK")
    # Check if classify correctly identifies sports
    assert(classifier.classify(br[1]) == 'Basketball')
    assert(classifier.classify(cl[1]) == 'Basketball')
    assert(classifier.classify(nl[1]) == 'Gymnastics')
    print('Classify fn OK')


def test(training_filename, test_filename):
    """Test the classifier on a test set of data"""
    classifier = Classifier(training_filename)
    f = open(test_filename)
    lines = f.readlines()
    f.close()
    numCorrect = 0.0
    for line in lines:
        data = line.strip().split('\t')
        vector = []
        classInColumn = -1
        for i in range(len(classifier.format)):
              if classifier.format[i] == 'num':
                  vector.append(float(data[i]))
              elif classifier.format[i] == 'class':
                  classInColumn = i
        theClass= classifier.classify(vector)
        prefix = '-'
        if theClass == data[classInColumn]:
            # it is correct
            numCorrect += 1
            prefix = '+'
        print("%s  %12s  %s" % (prefix, theClass, line))
    print("%4.2f%% correct" % (numCorrect * 100/ len(lines)))

#unitTest();
##
##  Here are examples of how the classifier is used on different data sets
##  in the book.
test('../data/ch4/athletesTrainingSet.txt', '../data/ch4/athletesTestSet.txt')
test("../data/ch4/irisTrainingSet.txt", "../data/ch4/irisTestSet.txt")
test("../data/ch4/mpgTrainingSet.txt", "../data/ch4/mpgTestSet.txt")