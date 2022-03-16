import csv
from collections import Counter

with open('mainFile.csv', 'w', newline='', encoding="utf-8") as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(['Title', 'Recommendations'])

    with open("5mostCommonWords.csv", 'r', encoding='utf8') as titleKey, open('5mostCommonGames.csv', 'r', encoding='utf8') as wordKey:
        # creating the reader objects
        titleKeyReader = csv.reader(titleKey)
        wordKeyReader = csv.reader(wordKey)
        # walking past the header lines
        next(titleKeyReader)
        next(wordKeyReader)

        titleKeyDict = {rows[1]: rows[2] for rows in titleKeyReader}
        wordKeyDict = {rows[1]: rows[2] for rows in wordKeyReader}
        for key in titleKeyDict:
            titleList = []
            wordsList = titleKeyDict[key].split()
            for word in wordsList:
                games = wordKeyDict.get(word).replace('[','').replace(']','').replace("'","").replace("'","") # due to how the file was formatted, the string needed to be cleaned
                titleList.extend(games.split(', '))
            
            # try to remove all iterations of our title from the list (and if it doesnt exist just continue as normal
            try:
                while True:
                    titleList.remove(key)
            except Exception:
                pass
            recommendations = Counter(titleList).most_common(5)  # find the 5 most occurring games

            # create the final recommendations list
            finalList = []
            while len(recommendations) != 0:
                finalList.append(recommendations.pop(0)[0]) # get the first element in the tuple and put it into our finalList
            csvWriter.writerow([key, finalList])  # write to the csv file

