import os

from parser import preprocess, parser

DIRECTORY = "sentences"

def parse_sentence(text, verbose=False):
    sentence = input("Sentence ") if text is None else text
    s = preprocess(sentence)
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        if verbose:
            print(e)
        return 0
    if not trees:
        if verbose:
            print("Could not parse sentence '{}'".format(sentence.strip()))
        return 0
    # Print each tree with noun phrase chunks
    if verbose:
        for tree in trees:
            tree.pretty_print()
    return 1

def parse_sentences(verbose=False):
    total = 0
    correct = 0
    for file in os.listdir(DIRECTORY):
        total += 1
        with open(os.path.join(DIRECTORY, file)) as f:
            sentence = f.read()
        correct += parse_sentence(sentence, verbose)
    print("Parsing score: {}/{}".format(correct, total))


def chunk_sentence(text, verbose=False):
    sentence = input("Sentence ") if text is None else text
    s = preprocess(sentence)
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        if verbose:
            print(e)
        return
    if not trees:
        if verbose:
            print("Could not parse sentence '{}'".format(sentence.strip()))
        return
    # Print each subtree
    chunks = []
    tree = trees[0]
    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        if subtree.height() > 3:
            if any(subtree.subtrees(lambda t: t.label() == "NP")):
                continue
        chunks.append(subtree)
    return chunks

def chunk_sentences(verbose=False):
    for file in os.listdir(DIRECTORY):
        with open(os.path.join(DIRECTORY, file)) as f:
            sentence = f.read()
        print("Sentence: {}".format(sentence.strip()))
        print("Chunks: ", end="")
        print(*chunk_sentence(sentence, verbose), sep=" // ")
        print()
