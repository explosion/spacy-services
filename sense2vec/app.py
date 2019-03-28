# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
from spacy.lang.en import English
import sense2vec

# fmt: off
SENSES = ["auto", "ADJ", "ADP", "ADV", "AUX", "CONJ", "DET", "INTJ", "NOUN",
          "NUM", "PART", "PERSON", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM",
          "VERB", "NORP", "FACILITY", "ORG", "GPE", "LOC", "PRODUCT", "EVENT",
          "WORK_OF_ART", "LANGUAGE"]
# fmt: on

print("Loading")
LEMMATIZER = English().vocab.morphology.lemmatizer
S2V = sense2vec.load("reddit_vectors-1.1.0")
print("Loaded!")


@hug.get("/senses")
def senses():
    """Get all available 'senses', i.e. tags and labels."""
    return SENSES


@hug.post("/find")
def find(word: str, sense: str = "auto", n_results: int = 200):
    """Find similar terms for a given term and optional sense."""
    best_word, best_sense = get_best(word, sense)
    if not word or not best_word:
        return {"text": word, "sense": sense, "results": [], "count": 0}
    results = []
    seen = set([best_word, min(LEMMATIZER(best_word, best_sense))])
    similar = get_similar(best_word, best_sense, n_results)
    for (word_entry, sense_entry), score in similar:
        head = min(LEMMATIZER(word_entry, sense_entry))
        if head not in seen:
            freq, _ = S2V[format_for_s2v(word_entry, sense_entry)]
            results.append({"score": score, "text": word_entry, "count": freq})
            seen.add(head)
        if len(results) >= n_results:
            break
    return {"text": best_word, "sense": best_sense, "results": results}


def format_for_s2v(word, sense):
    return word.replace(" ", "_") + "|" + sense


def get_best(word, sense):
    if sense != "auto":  # if sense is specified, find respective entry
        if format_for_s2v(word, sense) in S2V:
            return (word, sense)
        return (None, None)
    freqs = []
    casings = [word, word.upper(), word.title()] if word.islower() else [word]
    for text in casings:  # try options
        for tag in SENSES:
            query = format_for_s2v(text, tag)
            if query in S2V:
                freqs.append((S2V[query][0], (text, tag)))
    return max(freqs)[1] if freqs else (None, None)


def get_similar(word, sense, n=100):
    query = format_for_s2v(word, sense)
    if query not in S2V:
        return []
    freq, query_vector = S2V[query]
    words, scores = S2V.most_similar(query_vector, n)
    words = [word.rsplit("|", 1) for word in words]
    # Don't know why we'd be getting unsensed entries, but fix.
    words = [entry for entry in words if len(entry) == 2]
    words = [(word.replace("_", " "), sense) for word, sense in words]
    return zip(words, scores)


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8080)
