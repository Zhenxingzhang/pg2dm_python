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
                    vector.append(int(fields[i]))
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

        #print [row[1] for row in self.data]

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
        vector = self.normalizeVector(itemVector)
        neighbors = self.nearestNeighbor(vector)
        print neighbors
        return(neighbors[1][0])

    def nearestNeighbor(self, vector):
        return min([(self.manhattan(vector, item[1]), item) for item in self.data])

    def manhattan(self, vector1, vector2):
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))


def unitTest(classifier):
    list1 = [54, 72, 78, 49, 65, 63, 75, 67, 54]
    list2 = [54, 72, 78, 49, 65, 63, 75, 67, 54, 68]
    list3 = [69]
    list4 = [69, 72]
    m1 = classifier.getMedian(list1)
    m2 = classifier.getMedian(list2)
    m3 = classifier.getMedian(list3)
    m4 = classifier.getMedian(list4)
    assert(round(m1, 3) == 65)
    assert(round(m2, 3) == 66)
    assert(round(m3, 3) == 69)
    assert(round(m4, 3) == 70.5)

    asd1 = classifier.getAbsoluteStandardDeviation(list1, m1)
    asd2 = classifier.getAbsoluteStandardDeviation(list2, m2)
    asd3 = classifier.getAbsoluteStandardDeviation(list3, m3)
    asd4 = classifier.getAbsoluteStandardDeviation(list4, m4)

    assert(round(asd1, 3) == 8)
    assert(round(asd2, 3) == 7.5)
    assert(round(asd3, 3) == 0)
    assert(round(asd4, 3) == 1.5)

    print("getMedian and getAbsoluteStandardDeviation work correctly")

classifier = Classifier('../data/ch4/athletesTrainingSet.txt')

unitTest(classifier)

#print classifier.medianAndDeviation
#classifier.normalize_column(1)
print classifier.classify([74, 190])