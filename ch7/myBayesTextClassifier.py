__author__ = 'zhenxing'

import os, codecs, math

class BayesTextClassifier:
    def __init__(self, training_dir):
        self.vocabulary ={}
        self.prob = {}
        self.stopwords = []
        self.total = {}
        categories = os.listdir(training_dir)
        self.categories = [filename for filename in categories if os.path.isdir(training_dir+'/'+filename)]

        for category in self.categories:
            print ('    ' + category)
            (self.prob[category], self.total[category]) = self.Parse_Docs(training_dir, category)
            #print(totalwords)

        # calculate the conditional probability for each word
        vocablength = len(self.vocabulary)

        for category in self.categories:
            denominator = self.total[category] + vocablength
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                self.prob[category][word] = (float(count+1)/denominator)
        print ("DONE TRAINING\n\n")


    def Parse_Docs(self, training_dir, category):
        reading_dir = training_dir + '/' + category
        files = os.listdir(reading_dir)
        total = 0
        counts = {}
        for file in files:
            f = codecs.open(reading_dir + '/' + file, 'r', 'iso8859-1')
            for line in f:
                tokens = line.split()
                for token in tokens:
                    token= token.strip('\'".,?:-')
                    token = token.lower()
                    if token != '' and not token in self.stopwords:
                        self.vocabulary.setdefault(token, 0)
                        self.vocabulary[token] +=1
                        counts.setdefault(token, 0)
                        counts[token] += 1
                        total +=1
            f.close()
        return counts, total

    def classify(self, doc):
        f = codecs.open(doc, 'r', 'iso8859-1')
        predict_categories = {}

        for line in f:
            tokens = line.split()
            for token in tokens:
                token= token.strip('\'".,?:-')
                token = token.lower()
                if token in self.vocabulary:
                    for category in self.categories:
                        predict_categories.setdefault(category, 0.0)
                        if self.prob[category][token] == 0:
                            print("%s %s" % (category, token))
                        predict_categories[category] += math.log(self.prob[category][token])
        f.close()
        results =list(predict_categories.items())
        results.sort(key=lambda tuple: tuple[1], reverse = True)
        return results[0][0]

    def testCategory(self, directory, category):
        reading_dir = directory+ '/' + category
        files = os.listdir(reading_dir)
        total = 0
        correct = 0
        for file in files:
            total += 1
            result = self.classify(reading_dir+'/' + file)
            if result == category:
                correct += 1
        return (correct, total)

    def test(self, testdir):
        """Test all files in the test directory--that directory is
        organized into subdirectories--each subdir is a classification
        category"""
        categories = os.listdir(testdir)
        #filter out files that are not directories
        categories = [filename for filename in categories if
                      os.path.isdir(testdir +'/'+ filename)]

        print categories
        correct = 0
        total = 0
        for category in categories:
            print(".")
            (catCorrect, catTotal) = self.testCategory(testdir, category)
            print(category, catCorrect, catTotal)
            correct += catCorrect
            total += catTotal
        print("\n\nAccuracy is  %f%%  (%i test instances)" %((float(correct) / total) * 100, total))

trainingdir = '../large_data/20news-bydate/20news-bydate-train'
testingdir = '../large_data/20news-bydate/20news-bydate-test'
# category ='alt.atheism'

textclassifier = BayesTextClassifier(trainingdir)

# textclassifier.Parse_Docs(trainingdir, category)

# test_doc = testingdir + '/alt.atheism/53257'
# predict_class=textclassifier.classify(test_doc)
# print predict_class

#print textclassifier.testCategory(testingdir, category)

textclassifier.test(testingdir)