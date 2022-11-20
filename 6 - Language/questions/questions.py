import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    # files = load_files("corpus")
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding="utf8") as f:
            files[filename] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by converting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized = nltk.word_tokenize(document.lower())
    return [
        word
        for word in tokenized
        if word not in nltk.corpus.stopwords.words("english") and word not in string.punctuation
    ]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set([item for sublist in documents.values() for item in sublist])
    appearances = dict()
    idfs = dict()

    for word in words:
        appearances[word] = 0
        for document in documents.values():
            if word in document:
                appearances[word] += 1
        idfs[word] = math.log(len(documents) / appearances[word])
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    for filename, document in files.items():
        tfidfs[filename] = 0
        for word in query:
            tfidfs[filename] += document.count(word) * idfs[word]
    return sorted(tfidfs.keys(), key=lambda x: tfidfs[x], reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = dict()
    for sentence, words in sentences.items():
        scores[sentence] = [0, 0]
        for word in query:
            if word in words:
                scores[sentence][0] += idfs[word]
                scores[sentence][1] += 1
        scores[sentence][1] /= len(words)
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)[:n]

if __name__ == "__main__":
    main()
