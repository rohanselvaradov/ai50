import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    outbound_links = list(corpus[page])
    all_links = list(corpus.keys())
    random_selection = {l: 1 / len(all_links) for l in all_links}
    if len(outbound_links) == 0:
        return random_selection
    follow_selection = {l: 1 / len(outbound_links) if l in outbound_links else 0 for l in all_links}
    distribution = {}
    for page in random_selection:
        distribution[page] = follow_selection[page] * damping_factor + random_selection[page] * (1 - damping_factor)
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    counts = {page: 0 for page in all_pages}
    current_page = random.choice(all_pages)
    for i in range(n): # first sample done already, maybe need to edit
        counts[current_page] += 1
        distribution = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(distribution.keys()), list(distribution.values()), k=1)[0]
    proportions = {page: count / n for page, count in counts.items()}
    return proportions


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    scores = {page: 1 / len(corpus) for page in corpus.keys()}
    while True:
        new_scores = {}
        for page in corpus:
            summation = 0
            for other_page in corpus:
                if page in corpus[other_page]:
                    summation += scores[other_page] / len(corpus[other_page])
                elif len(corpus[other_page]) == 0:
                    summation += scores[other_page] / len(corpus)
            new_score = (1 - damping_factor) / len(corpus) + damping_factor * summation
            new_scores[page] = new_score
        difference = max([abs(new_scores[i] - scores[i]) for i in scores])
        if difference < 0.001:
            break
        scores = new_scores.copy()
    return scores

if __name__ == "__main__":
    main()
