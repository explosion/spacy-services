from spacy.tokens import Doc
from spacy.errors import Warnings, user_warning
from spacy.displacy import get_doc_settings

import re


# match order
ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_1 = "(( (RBR|RBS|RB\\b))*( (JJR|JJS|JJ\\b))*( (NNP|NNS|NN\\b))+( CC)?)+( IN)(( (RBR|RBS|RB\\b))*( (JJR|JJS|JJ\\b))*( (NNP|NNS|NN\\b))+)+"
ENGLISH_QUERY_VBG_TAG_PATTERN_PRORITY_2 = "( VBG)(( IN)( (RBR|RBS|RB\\b))*( (JJR|JJS|JJ\\b))*( (NNP|NNS|NN\\b))+)"
ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_3 = "( (RBR|RBS|RB\\b))*( (JJR|JJS|JJ\\b))*( (NNP|NNS|NN\\b))+"
ENGLISH_QUERY_VBG_TAG_PATTERN_PRIORITY_4 = "( VBG)"

COMPILED_ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_1 = re.compile(ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_1)
COMPILED_ENGLISH_QUERY_VBG_TAG_PATTERN_PRORITY_2 = re.compile(ENGLISH_QUERY_VBG_TAG_PATTERN_PRORITY_2)
COMPILED_ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_3 = re.compile(ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_3)
COMPILED_ENGLISH_QUERY_VBG_TAG_PATTERN_PRIORITY_4 = re.compile(ENGLISH_QUERY_VBG_TAG_PATTERN_PRIORITY_4)


def en_parse_deps(orig_doc, options={}):
    """Generate dependency parse in {'words': [], 'arcs': []} format.

    doc (Doc): Document do parse.
    RETURNS (dict): Generated dependency parse keyed by words and arcs.
    """
    doc = Doc(orig_doc.vocab).from_bytes(orig_doc.to_bytes(exclude=["user_data"]))
    if not doc.is_parsed:
        user_warning(Warnings.W005)
    if options.get("collapse_phrases", False):
        with doc.retokenize() as retokenizer:
            for np in list(doc.noun_chunks):
                attrs = {
                    "tag": np.root.tag_,
                    "lemma": np.root.lemma_,
                    "ent_type": np.root.ent_type_,
                }
                retokenizer.merge(np, attrs=attrs)
    if options.get("collapse_punct", True):
        spans = []
        for word in doc[:-1]:
            if word.is_punct or not word.nbor(1).is_punct:
                continue
            start = word.i
            end = word.i + 1
            while end < len(doc) and doc[end].is_punct:
                end += 1
            span = doc[start:end]
            spans.append((span, word.tag_, word.lemma_, word.ent_type_))
        with doc.retokenize() as retokenizer:
            for span, tag, lemma, ent_type in spans:
                attrs = {"tag": tag, "lemma": lemma, "ent_type": ent_type}
                retokenizer.merge(span, attrs=attrs)
    summarized_doc = summarize_doc(doc)
    if options.get("fine_grained"):
        words = [{"text": w.text, "tag": w.tag_} for w in summarized_doc]
    else:
        words = [{"text": w.text, "tag": w.pos_} for w in summarized_doc]
    arcs = []
    for word in summarized_doc:
        if word.i < word.head.i:
            arcs.append(
                {"start": word.i, "end": word.head.i, "label": word.dep_, "dir": "left"}
            )
        elif word.i > word.head.i:
            arcs.append(
                {
                    "start": word.head.i,
                    "end": word.i,
                    "label": word.dep_,
                    "dir": "right",
                }
            )

    return {"words": words, "arcs": arcs, "settings": get_doc_settings(orig_doc)}


def summarize_doc(doc):

    tags = ""
    for tok in doc:
        tags += " " + tok.tag_

    # Firstly, search for COMPILED_ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_1
    priority_1_matches = []
    for m in COMPILED_ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_1.finditer(tags):
        if m.end() > m.start():
            priority_1_matches.append(doc[tags[0: m.start()].count(" "): tags[0: m.end()].count(" ")])

    if len(priority_1_matches) == 1:
        return priority_1_matches[0]

    if len(priority_1_matches) > 1:
        # TODO remove stopwords at 2 ends then return then Span
        return doc


    # Secondly, search for ENGLISH_QUERY_VBG_TAG_PATTERN
    priority_2_matches = []
    for m in COMPILED_ENGLISH_QUERY_VBG_TAG_PATTERN_PRORITY_2.finditer(tags):
        if m.end() > m.start():
            priority_2_matches.append(doc[tags[0: m.start()].count(" "): tags[0: m.end()].count(" ")])

    if len(priority_2_matches) == 1:
        return priority_2_matches[0]

    if len(priority_2_matches) > 1:
        # TODO remove stopwords at 2 ends then return then Span
        return doc


    # Third, search for COMPILED_ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_3
    priority_3_matches = []
    for m in COMPILED_ENGLISH_QUERY_NOUN_TAG_PATTERN_PRIORITY_3.finditer(tags):
        if m.end() > m.start():
            priority_3_matches.append(doc[tags[0: m.start()].count(" "): tags[0: m.end()].count(" ")])

    if len(priority_3_matches) == 1:
        return priority_3_matches[0]

    if len(priority_3_matches) > 1:
        # TODO remove stopwords at 2 ends then return then Span
        return doc


    # Fourth, search for ENGLISH_QUERY_VBG_TAG_PATTERN_PRIORITY_4
    priority_4_matches = []
    for m in COMPILED_ENGLISH_QUERY_VBG_TAG_PATTERN_PRIORITY_4.finditer(tags):
        if m.end() > m.start():
            priority_4_matches.append(doc[tags[0: m.start()].count(" "): tags[0: m.end()].count(" ")])

    if len(priority_4_matches) == 1:
        return priority_4_matches[0]


    # Else return the doc
    return doc
