from spacy.displacy import get_doc_settings
from .utils import *
import numpy as np
EMPTY_INDEX = -1

def ja_pos_regex_matches(doc, compiled):

    tags = ""

    for tok in doc:
        if tok.pos in CONNECT_SYMBOLS_POS and tok.text in CONNECT_SYMBOLS:
            tags += " " + tok.text
        else:
            tags += " " + tok.pos_
    for m in compiled.finditer(tags):
        start_index = tags[0: m.start()].count(" ")
        end_index = tags[0: m.end()].count(" ")
        yield doc[start_index: end_index], (start_index, end_index)


def _chunk_doc( doc):
    for chunk_spans, (start, end) in ja_pos_regex_matches(doc, compiled=COMPILED_CHUNKS_PATTERN):
        chunk = {"pos": chunk_spans[0].pos_,
                 "start": start,
                 "end": end,
                 "dep": chunk_spans.root.dep_,
                 "text": "".join([tok.orth_ for tok in chunk_spans])}

        # Check chunk is coordinating conjunction
        if chunk["text"] in CONJUNTION_TOKENS:
            chunk["pos"] = NAMES[CCONJ]
            yield chunk
            continue

        for token in chunk_spans:
            try:
                if token.pos == VERB:
                    chunk["pos"] = NAMES[VERB]
                    break
                if token.pos == PROPN:
                    chunk["pos"] = NAMES[PROPN]
                    break
                if token.pos in EXCEPT_POS_OF_POS.keys() and IDS[chunk["pos"]] not in EXCEPT_POS_OF_POS[token.pos]:
                    chunk["pos"] = NAMES[token.pos]
            except Exception as ex:
                print(str(ex))
                continue
        yield chunk


def convert2EN(tokens):

    adp_verb_idx = []
    end_idx = len(tokens)
    for idx, tok in enumerate(tokens):
        if tok["pos"] in ADP_POS or tok["pos"] == NAMES[VERB]:
            adp_verb_idx.append(idx)
    tokens = [t for t in tokens]
    new_idx = np.zeros((end_idx, 1), dtype='int64')
    old_idx = np.arange(end_idx).reshape((end_idx, 1))
    idx_list = np.append(new_idx, old_idx, axis=1)
    order = 0
    for index in adp_verb_idx[::-1]:
        start = index
        for i in range(start + 1, end_idx):
            idx_list[i][0] = order
            order += 1

        idx_list[index][0] = order
        order += 1
        end_idx = index

    for i in range(end_idx):
        idx_list[i][0] = order
        order += 1
    tokens = [x for x, _ in sorted(zip(tokens, idx_list), key=lambda x: x[1][0]) if x["pos"] not in FILTER_TOKEN_POS]
    return tokens


def _get_token_dict(token):
    if token.lemma_ in CONJUNTION_TOKENS:
        return {
            "text": token.orth_,
            "pos": NAMES[CCONJ],
            "dep": token.dep_
        }
    return {
        "text": token.orth_,
        "pos": token.pos_,
        "dep": token.dep_
    }


def run_analysis(doc, collapse_phrases=False):
    tokens = []

    if collapse_phrases:
        for tok in _chunk_doc(doc):
            tokens.append(tok)
        return tokens
    else:
        return [_get_token_dict(t) for t in doc]


def run_analysis_and_convert2EN(doc,collapse_phrases=False):
    tokens = run_analysis(doc, collapse_phrases=collapse_phrases)
    return convert2EN(tokens)


def collapse_punct(tokens):

    collapsed_tokens = []
    start = 0
    end = 1
    for index, token in enumerate(tokens[1:], start=1):
        if token["pos"] == NAMES[PUNCT]:
            end += 1
        else:
            add_token = {"pos": tokens[start]["pos"],
                         "dep": tokens[start]["dep"],
                         "text": "".join([chunk["text"] for chunk in tokens[start:end]])}
            start = index
            end = index + 1
            collapsed_tokens.append(add_token)
    add_token = {"pos": tokens[start]["pos"],
                 "dep": tokens[start]["dep"],
                 "text": "".join([chunk["text"] for chunk in tokens[start:end]])}
    collapsed_tokens.append(add_token)

    return collapsed_tokens


def collasp_adp(doc):
    spans = []
    for word in doc[:-1]:
        if word.pos not in ADP_POS_IDS or word.nbor(1).pos not in ADP_POS_IDS:
            continue
        start = word.i
        end = word.i + 1
        while end < len(doc) and doc[end].pos in ADP_POS_IDS:
            end += 1
        span = doc[start:end]
        end_idx = end - 1
        spans.append((span, doc[end_idx].pos_, doc[end_idx].tag_, doc[end_idx].lemma_, doc[end_idx].ent_type_))
    with doc.retokenize() as retokenizer:
        for span, pos, tag, lemma, ent_type in spans:
            attrs = {"pos": pos, "tag": tag, "lemma": lemma, "ent_type": ent_type}
            retokenizer.merge(span, attrs=attrs)
    return doc


def summary_ja_doc(doc):
    doc = doc.doc
    start = 0
    end = len(doc)
    while doc[start].pos not in KEEP_POS_IDS and start != end:
        start += 1

    while (doc[end - 1].pos not in KEEP_POS_IDS or doc[end - 1].lemma_ in REMOVE_VERB or doc[end - 1].lemma_ in REMOVE_ADJ)\
            and start != end:
        end -= 1
    if start == end:
        return doc
    else:
        return doc[start:end]


def parse_deps(doc, options):

    if options.get("collapse_adp", True):
        collasp_adp(doc)
    if options.get("summary", True):
        doc = summary_ja_doc(doc)
    if options.get("collapse_phrases", False):
        tokens = run_analysis_and_convert2EN(doc, collapse_phrases=True)
    else:
        tokens = run_analysis_and_convert2EN(doc, collapse_phrases=False)
    if options.get("collapse_punct", True):
        tokens = collapse_punct(tokens)

    words = [{"text": token["text"], "tag": token["pos"]} for token in tokens]
    arcs = [{"start": 0, "end": 0, "label": token["dep"], "dir": "right"}for token in tokens]

    return {"words": words, "arcs": arcs, "settings": get_doc_settings(doc.doc)}
