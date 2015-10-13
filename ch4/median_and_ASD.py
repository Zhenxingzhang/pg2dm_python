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
        diffs = 0
        for idx in range(length):
            diffs += abs(alist[idx] - median)

        return diffs/length

def unitTest():
    list1 = [54, 72, 78, 49, 65, 63, 75, 67, 54]
    list2 = [54, 72, 78, 49, 65, 63, 75, 67, 54, 68]
    list3 = [69]
    list4 = [69, 72]
    classifier = Classifier('../data/ch4/athletesTrainingSet.txt')
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

unitTest()

