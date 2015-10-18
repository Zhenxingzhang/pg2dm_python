class NaiveBayesClassifer:
    """ a classifier will be built from files with the bucketPrefix
    excluding the file with textBucketNumber. dataFormat is a
    string that describes how to interpret each line of the data
    files. For example, for the iHealth data the format is:
    "attr attr attr attr class"
    """

    def __init__(self, bucketPrefix, testBucketNumber, data_format):
        total = 0
        classes = {}
        counts = {}

        #reading the data in from the file
        self.format = data_format.strip().split('\t')
        # prior probability for each hypothesis (category, probability value)
        self.prior = {}
        # conditional probabilities of each observation in each hypothesis {hypothesis_name : {attribute_class:{obs1: prob, obs2: prob...}}}
        self.conditional = {}


        # for each of the buckets numbered 1 through 10:
        for i in range(1, 11):
        #if it is not the bucket we should ignore, read in the data
            if i != testBucketNumber:
                filename = "%s-%02i" % (bucketPrefix, i)
                f = open(filename)
                lines = f.readlines()
                f.close()
                for line in lines:
                    fields = line.strip().split('\t')
                    ignore = []
                    vector = []
                    for i in range(len(fields)):
                        if self.format[i] == 'num':
                            vector.append(float(fields[i]))
                        elif self.format[i] == 'attr':
                            vector.append(fields[i])
                        elif self.format[i] == 'comment':
                            ignore.append(fields[i])
                        elif self.format[i] == 'class':
                            category = fields[i]
                    # now process this instance
                    total += 1
                    classes.setdefault(category, 0)
                    counts.setdefault(category, {})
                    classes[category] += 1
                    # now process each attribute of the instance
                    col = 0
                    for columnValue in vector:
                        col += 1
                        counts[category].setdefault(col, {})
                        counts[category][col].setdefault(columnValue,0)
                        counts[category][col][columnValue] += 1
        #print classes, counts
        #
        # ok done counting. now compute probabilities
        #
        # first prior probabilities p(h)
        #
        for (category, count) in classes.items():
            self.prior[category] = float(count) / total
        #
        # now compute conditional probabilities p(h|D)
        #
        for (category, columns) in counts.items():
            self.conditional.setdefault(category, {})
            for (col, valueCounts) in columns.items():
                self.conditional[category].setdefault(col, {})
                for (attrValue, count) in valueCounts.items():
                    self.conditional[category][col][attrValue] = (float(count)  / classes[category])
        print self.conditional

    def classify(self, itemVector):
        """Return hypothesis class we think item Vector is in"""
        results = []
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attribute in itemVector:
                if not attribute  in self.conditional[category][col]:
                    prob =0
                else:
                    prob = prob * self.conditional[category][col][attribute]
                    col += 1

            results.append((prob, category))
        return(max(results)[1])
        #return(results)

    def testBucket(self, bucketPrefix, bucketNumber):
        """Evaluate the classifier with data from the file
        bucketPrefix-bucketNumber"""

        filename = "%s-%02i" % (bucketPrefix, bucketNumber)
        f = open(filename)
        lines = f.readlines()
        totals = {}
        f.close()
        loc = 1
        for line in lines:
            loc += 1
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1
            for i in range(len(self.format)):
                  if self.format[i] == 'num':
                      vector.append(float(data[i]))
                  elif self.format[i] == 'attr':
                      vector.append(data[i])
                  elif self.format[i] == 'class':
                      classInColumn = i
            theRealClass = data[classInColumn]
            classifiedAs = self.classify(vector)
            totals.setdefault(theRealClass, {})
            totals[theRealClass].setdefault(classifiedAs, 0)
            totals[theRealClass][classifiedAs] += 1
        return totals

def tenfold(bucketPrefix, dataFormat):
    results = {}
    for i in range(1, 11):
        c = NaiveBayesClassifer(bucketPrefix, i, dataFormat)
        t = c.testBucket(bucketPrefix, i)
        for (key, value) in t.items():
            results.setdefault(key, {})
            for (ckey, cvalue) in value.items():
                results[key].setdefault(ckey, 0)
                results[key][ckey] += cvalue

    # now print results
    categories = list(results.keys())
    categories.sort()
    print(   "\n            Classified as: ")
    header =    "             "
    subheader = "               +"
    for category in categories:
        header += "% 10s   " % category
        subheader += "-------+"
    print (header)
    print (subheader)
    total = 0.0
    correct = 0.0
    for category in categories:
        row = " %10s    |" % category
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += " %5i |" % count
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print("\n%5.3f percent correct" %((correct * 100) / total))
    print("total of %i instances" % total)

#bayes_classifier = NaiveBayesClassifer('../data/iHealth/i', 10, "attr\tattr\tattr\tattr\tclass")
#
# print bayes_classifier.classify(['health', 'moderate', 'moderate', 'yes'])
# print bayes_classifier.classify(['both', 'sedentary', 'moderate', 'yes'])
#tenfold('../data/iHealth/i', "attr\tattr\tattr\tattr\tclass")

tenfold("../data/mpgData/mpgData","class\tnum\tnum\tnum\tnum\tnum\tcomment")
