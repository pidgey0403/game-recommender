import spacy
from spacy.lang.en import English
import pandas as pd
import csv

# REPLACE WITH YOUR FILE PATH
filePath = "/Users/alexn/Documents/metacritic_game_user_comments.csv"
dataset = pd.read_csv(filePath)

remove_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                "these",
                "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
                "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
                "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
                "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
                "again",
                "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
                "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "level", "game", "platform",
                "designer", "developer", "games", "platforms", "designers", "program", "map", "maps", "overworld",
                "dlc",
                "dlcs", "fun", "funniest"]

nlp = spacy.load("en_core_web_lg")  # will need lg for word vectors

X = dataset.iloc[:, 0:5].values

from spacy_langdetect import LanguageDetector
from spacy.language import Language


@Language.factory('language_detector')
def language_detector(nlp, name):
    return LanguageDetector()


nlp.add_pipe("language_detector", last=True)

commentsArr = dataset.iloc[:, 4].values

# excluded categories include: pronouns, determinates (the, a), punctuation, and whatever ADT is
lExclude = ['PRON', 'DET', 'PUNCT', 'ADT']
SPOILER_PHRASE = "This review contains spoilers, click expand to view."
REMOVE_TAGS = ['FW']
remove_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
                "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
                "these",
                "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
                "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
                "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
                "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
                "again",
                "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
                "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
                "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "level", "game", "platform",
                "designer", "developer", "games", "platforms", "designers", "program", "map", "maps", "overworld",
                "dlc",
                "dlcs", "fun", "funniest"]

CleanCommentsArr = []


def cleanComment(comment):
    # Remove spoiler warning
    comment = comment.replace(SPOILER_PHRASE, '')

    newComment = []

    doc = nlp(comment)

    # remove non english sentances rather than attempting to translate them
    if doc._.language['language'] != 'en':
        return False

    for token in doc:

        # TO DO:
        # - Remove uneccesary game related terms
        # - Join two part nouns

        # remove decided lexical categories to exclode, as well as 500 most common words
        if token.pos_ in lExclude or token.tag_ in REMOVE_TAGS or token.is_stop or token.is_space or token.text in remove_words:
            continue

        # turn token into its base form (although makes it no longer an nlp token and just a string, idk why)
        token = token.lemma_
        token = token.lower()

        newComment.append(token)

    return " ".join(newComment)  # returns string


# Removes all words effected by a negative word (such as not) - Robyn
def cleanNegated(comment):
    doc = nlp(comment)
    for token in doc:

        # looks to see if a negative dependancy affects the current token
        children = token.children
        for dependant in token.children:  # no clue why I cant say children here but it breaks everything
            if dependant.dep_ == "neg" or dependant.text == "no":
                # if so, remove all words associated with it.
                removeList = [i.text for i in children]
                removeList.append(token.text)

        # removing the bvad words
        splitComment = comment.split()
        try:
            removedComment = [item for item in splitComment if item not in removeList]
        except:
            removedComment = splitComment

    return " ".join(removedComment)  # returns string


# REMOVES tokens with vector scores past a certain threshold - gabby
def cleanSimilar(comment):  # takes in type List or Doc
    doc = nlp(comment)
    removeList = []  # create empty list that stores the tokens to be deleted
    for token in doc:
        removedComment = list(word.text for word in doc)
        i = 0
        for i in range(0, len(doc)):
            j = i + 1
            for j in range(i + 1, len(doc)):
                # if doc[i].similarity(doc[j]) > 0.45:
                try:
                    if (not doc[i].is_oov and doc[j].is_oov) and doc[i].similarity(doc[j]) > 0.55:
                        # if (not doc[i].is_oov and doc[j].is_oov) and doc[i].similarity(doc[j]) > 0.55:
                        removeList.append(doc[j].text)
                except:
                    continue
            try:
                removedComment = [item for item in removedComment if
                                  item not in removeList]  # add tokens to list if they are not similar
            except:
                removedComment = comment.split()
        doc = nlp(" ".join(removedComment))
    return doc  # returns type Doc


# Cleaning to be done per comment review

def finalCleaning(comment):
    prelim = cleanComment(comment)
    if prelim:
        noNeg = cleanNegated(prelim)

    if prelim and noNeg:
        final = cleanSimilar(noNeg)

    # only do shit if comment wasnt rejected
    if prelim and noNeg and final:
        CleanCommentsArr.append(" ".join(final.text))
        return final


# field names
header = ['Number', 'Title', 'UserScore', 'Review']

fileName = "updated_dataset.csv"
# writing to our new csv file
with open(fileName, 'w', newline='', encoding="utf-8") as csvfile:
    # creating a writer object
    csvWriter = csv.writer(csvfile)
    # write the header
    csvWriter.writerow(header)

    # read our dataset
    with open(filePath, 'r', encoding='utf8') as read_obj:
        csvReader = csv.reader(read_obj)
        next(csvReader)
        # iterate row by row
        # num = 0
        for row in csvReader:
            currentNum = row[0]
            if row[3] == "10":
                # number = num
                # num = num + 1
                title = row[1]
                userScore = row[3]
                review = row[4]
                review = finalCleaning(review)
                if review:
                    newRow = [currentNum, title, userScore, review]
                    csvWriter.writerow(newRow)
