import csv

# creates a file with all the reviews for each individual game merged together
fileName = "combined_Reviews.csv"
with open(fileName, 'w', newline='', encoding="utf-8") as csvfile:
    csvWriter = csv.writer(csvfile)
    csvWriter.writerow(['Number', 'Title', 'Review'])

    with open("finished_word_tokens.csv", 'r', encoding='utf8') as read_obj:
        csvReader = csv.reader(read_obj)
        next(csvReader)
        num = 0
        currentTitle = ""
        reviewWordChunk = []
        for row in csvReader:

            newTitle = row[1]
            # for the first iteration
            if currentTitle == "":
                currentTitle = newTitle
            # finds the review
            review = row[3]

            # if the current title and the new title are the same, then add to the array
            if currentTitle == newTitle:
                reviewWordChunk.append(review)

            else:
            #else add to the new csv file
                number = num
                num = num + 1
                finalReview = "".join(reviewWordChunk)
                newRow = [number, currentTitle, finalReview]
                csvWriter.writerow(newRow)
                currentTitle = newTitle
                # empty the array
                reviewWordChunk.clear()
                # start the list on the new game review
                reviewWordChunk.append(review)

