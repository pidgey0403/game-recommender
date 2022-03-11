import csv
import sys


def addToValueDictionary(title, review,valueDictionary):
    for word in review.split():
        # if the word doesnt exist in the dictionary
        if valueDictionary.get(word) is None:
            valueDictionary[word] = {}
            valueDictionary[word].update({'game':{title:1}})
        # word is in dictionary
        else:
            # if title doesn't exist
            if valueDictionary[word]['game'].get(title) is None:
                valueDictionary[word]['game'][title] = 1
            # if the title exists
            else:
                valueDictionary[word]['game'][title] = valueDictionary[word]['game'][title] + 1





# sort the games by # of occurrences
def mostCommonGames(valueDictionary):
    finalDict = {}
    # sorting the games in the dictionary for each word
    for word in valueDictionary:
        res = {key : dict(sorted(val.items(),reverse=True, key = lambda ele: ele[1]))
           for key, val in valueDictionary[word].items()}
        finalDict.update({word:res})
    return finalDict


# get the top5 most occuring games for each and return a dictionary object holding the word as a key and a list as the value
# does not include the number of occurrences
def top5Games(dictionary):
    returnDict = {}
    for word in dictionary:
        wordList = []
        if len(dictionary[word]['game']) > 5:
            inputNum = 0
            for key,value in dictionary[word]['game'].items():
                wordList.append(key)
                inputNum = inputNum + 1
                if inputNum == 5:
                    break
            returnDict[word] = wordList
        else:
            for key, value in dictionary[word]['game'].items():
                wordList.append(key)
            returnDict[word] = wordList
    return returnDict



maxInt = sys.maxsize

with open("5mostCommonGames.csv", 'w', newline='', encoding="utf-8") as csvfile:
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
        valueDictionary = {}
        for row in csvReader:
            title = row[1]
            review = row[2]
            addToValueDictionary(title, review, valueDictionary)
        # sort the dictionary by occurrences
        sortedDict = mostCommonGames(valueDictionary)
        # get the top 5 games in a new dictionary format
        top5 = top5Games(sortedDict)

        # write to csv file
        number = 0
        for key,value in top5.items():
            csvWriter.writerow([number, key, value])
            number = number + 1