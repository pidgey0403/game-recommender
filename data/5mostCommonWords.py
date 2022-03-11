import csv
import sys

def findCommon(review, num):
    wordDictionary = {}
    for word in review.split():
        if wordDictionary.get(word) is None:
            wordDictionary.update({word: 1})
        else:
            wordDictionary[word] = wordDictionary.get(word) + 1

    finalDict = {}
    inputs = 0
    for w in sorted(wordDictionary, key=wordDictionary.get, reverse=True):
        if inputs < num:
            finalDict.update({w:str(wordDictionary[w])})
            inputs = inputs + 1
    finalString = " ".join(finalDict.keys())
    return finalString



maxInt = sys.maxsize

with open("5mostCommonWords.csv", 'w', newline='', encoding="utf-8") as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(['Number', 'Title', 'Review'])

    # read the file and find the 5 most common words for each game
    with open("combined_Reviews.csv", 'r', encoding='utf8') as read_obj:
        csvReader = csv.reader(read_obj)
        next(csvReader)
        # code to avoid error of overflow
        while True:
            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt / 10)
        for row in csvReader:
            title = row[1]
            review = row[2]
            review = findCommon(review,5)
            csvWriter.writerow([row[0],title,review])






