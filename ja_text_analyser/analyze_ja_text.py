import spacy
# from spacy.symbols import NOUN, PROPN, PRON, NUM, AUX, ADJ, ADV, ADP, PUNCT, VERB, NAMES, CONJ, IDS, SYM, CCONJ, SCONJ
from spacy.displacy import get_doc_settings
from .utils import *
import re
EMPTY_INDEX = -1
from copy import deepcopy

def ja_pos_regex_matches(doc, pattern):
    """
    Extract sequences of consecutive tokens from a spacy-parsed doc whose
    part-of-speech tags match the specified regex pattern.

    Args:
        doc (:class:`spacy.tokens.Doc` or :class:`spacy.tokens.Span`)
        pattern (str): Pattern of consecutive POS tags whose corresponding words
            are to be extracted, inspired by the regex patterns used in NLTK's
            `nltk.chunk.regexp`. Tags are uppercase, from the universal tag set;
            delimited by < and >, which are basically converted to parentheses
            with spaces as needed to correctly extract matching word sequences;
            white space in the input doesn't matte
            Examples (see ``constants.POS_REGEX_PATTERNS``):

            * noun phrase: r'<DET>? (<NOUN>+ <ADP|CONJ>)* <NOUN>+'
            * compound nouns: r'<NOUN>+'
            * verb phrase: r'<VERB>?<ADV>*<VERB>+'
            * prepositional phrase: r'<PREP> <DET>? (<NOUN>+<ADP>)* <NOUN>+'

    Yields:
        :class:`spacy.tokens.Span`: the next span of consecutive tokens from ``doc`` whose
        parts-of-speech match ``pattern``, in order of apperance
    """
    # standardize and transform the regular expression pattern...
    pattern = re.sub(r"\s", "", pattern)
    pattern = re.sub(r"<([A-Z]+)\|([A-Z]+)>", r"( (\1|\2))", pattern)
    pattern = re.sub(r"<([A-Z]+)\|([A-Z]+)\|([A-Z]+)>", r"( (\1|\2|\3))", pattern)
    pattern = re.sub(r"<([A-Z]+)\|([A-Z]+)\|([A-Z]+)\|([A-Z]+)>", r"( (\1|\2|\3|\4))", pattern)

    # pattern = re.sub(r"<([A-Z]+)>", r"( \1)", pattern)
    pattern = re.sub(r"<(.+?)>", r"( (\1))", pattern)

    tags = ""

    for tok in doc:
        if tok.pos in CONNECT_SYMBOLS_POS and tok.text in CONNECT_SYMBOLS:
            tags += " " + tok.text
        else:
            tags += " " + tok.pos_
    for m in re.finditer(pattern, tags):
        start_index = tags[0: m.start()].count(" ")
        end_index = tags[0: m.end()].count(" ")
        yield doc[start_index: end_index], (start_index, end_index)

def _chunk_doc( doc):
    for chunk_spans,(start, end) in ja_pos_regex_matches(doc, pattern=CHUNKS_PATTERN):
        chunk = {"pos": chunk_spans[0].pos_,
                 "start": start,
                 "end": end,
                 "text": "".join([tok.lemma_ for tok in chunk_spans])}

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
                yield chunk
                continue
        yield chunk
        continue

def convert2EN(chunks_tokens):

    # Convert to English structure
    num_adp = 0
    adp_idx = -1
    for index, chunk in enumerate(chunks_tokens["chunks"]):
        if chunk["pos"] == NAMES[ADP]:
            num_adp += 1
            adp_idx = index
    tokens = []
    chunks = []

    if num_adp > 1:
        return {"chunks": chunks_tokens["chunks"],
                "tokens": chunks_tokens["tokens"]}
    elif adp_idx < 0:
        for chunk in chunks_tokens["chunks"]:
            start_idx = chunk["start"]
            end_idx = chunk["end"]
            if chunk["pos"] in EXCEPT_CHUNKS:
                tokens.append(_get_token_dict_from_chunk_dict(chunk))

            else:
                [tokens.append(t) for t in chunks_tokens["tokens"][start_idx:end_idx] if t["pos"] in MEANING_POS]
            chunks.append(chunk)
    else:
        # Processing right chunks
        start = 0
        end = 0
        for right_chunk in chunks_tokens["chunks"][adp_idx + 1:]:
            start_idx = right_chunk["start"]
            end_idx = right_chunk["end"]
            if right_chunk["pos"] in EXCEPT_CHUNKS:
                tokens.append(_get_token_dict_from_chunk_dict(right_chunk))

            else:
                [tokens.append(t) for t in chunks_tokens["tokens"][start_idx:end_idx] if t["pos"] in MEANING_POS]
            end += end_idx - start_idx
            add_chunk = deepcopy(right_chunk)
            add_chunk["start"] = start
            add_chunk["end"] = end
            chunks.append(add_chunk)
            start = end

        # Processing ADP
        tokens.append(_get_token_dict_from_chunk_dict(chunks_tokens["chunks"][adp_idx]))
        end += 1
        add_chunk = deepcopy(chunks_tokens["chunks"][adp_idx])
        add_chunk["start"] = start
        add_chunk["end"] = end
        chunks.append(add_chunk)
        start = end

        # Processing left chunks
        for left_chunk in chunks_tokens["chunks"][:adp_idx]:
            start_idx = left_chunk["start"]
            end_idx = left_chunk["end"]
            if left_chunk["pos"] in EXCEPT_CHUNKS:
                tokens.append(_get_token_dict_from_chunk_dict(left_chunk))

            else:
                [tokens.append(t) for t in chunks_tokens["tokens"][start_idx:end_idx] if t["pos"] in MEANING_POS]
            end += end_idx - start_idx
            add_chunk = deepcopy(left_chunk)
            add_chunk["start"] = start
            add_chunk["end"] = end
            chunks.append(add_chunk)
            start = end

    return {"chunks": chunks,
            "tokens": tokens}

def _get_token_dict(token):
    return {
        "text": token.lemma_,
        "pos": token.pos_
    }

def _get_token_dict_from_chunk_dict(chunk):
    return {
        "text": chunk["text"],
        "pos": chunk["pos"]
    }

def run_analysis(doc):
    chunks = []
    for chunk in _chunk_doc(doc):
        chunks.append(chunk)
    return {"chunks": chunks,
            "tokens": [_get_token_dict(t) for t in doc]}

def run_analysis_and_convert2EN(doc):
    chunks_tokens = run_analysis(doc)
    return convert2EN(chunks_tokens)

def collapse_punct(chunks_tokens):

    # Processing chunks
    start = 0
    end = 1
    collapsed_chunks = []
    if len(chunks_tokens["chunks"]) < 2:
        collapsed_chunks = chunks_tokens["chunks"]
    else:
        for index, chunk in enumerate(chunks_tokens["chunks"][1:], start=1):
            if chunk["pos"] == NAMES[PUNCT]:
                end += 1
            else:
                add_chunk = {"pos": chunks_tokens["chunks"][start]["pos"],
                             "start": chunks_tokens["chunks"][start]["start"],
                             "end": chunks_tokens["chunks"][start]["end"],
                             "text": "".join([chunk["text"] for chunk in chunks_tokens["chunks"][start:end]])}
                start = index
                end = index + 1
                collapsed_chunks.append(add_chunk)
        add_chunk = {"pos": chunks_tokens["chunks"][start]["pos"],
                     "start": chunks_tokens["chunks"][start]["start"],
                     "end": chunks_tokens["chunks"][start]["end"],
                     "text": "".join([chunk["text"] for chunk in chunks_tokens["chunks"][start:end]])}
        collapsed_chunks.append(add_chunk)

    # Processing tokens
    collapsed_tokens = []
    start = 0
    end = 1
    if len(chunks_tokens["tokens"]) < 2:
        collapsed_tokens = chunks_tokens["tokens"]
    else:
        for index, token in enumerate(chunks_tokens["tokens"][1:], start=1):
            if token["pos"] == NAMES[PUNCT]:
                end += 1
            else:
                add_token = {"pos": chunks_tokens["tokens"][start]["pos"],
                             "text": "".join([chunk["text"] for chunk in chunks_tokens["tokens"][start:end]])}
                start = index
                end = index + 1
                collapsed_tokens.append(add_token)
        add_token = {"pos": chunks_tokens["tokens"][start]["pos"],
                     "text": "".join([chunk["text"] for chunk in chunks_tokens["tokens"][start:end]])}
        collapsed_tokens.append(add_token)

    return {"chunks": collapsed_chunks, "tokens": collapsed_tokens}

def summary_ja_doc(doc):
    doc = doc.doc
    start = 0
    end = len(doc)
    while doc[start].pos not in MEANING_POS_IDS and start != end:
        start += 1

    while (doc[end - 1].pos not in MEANING_POS_IDS or doc[end - 1].lemma_ in REMOVE_VERB or doc[end - 1].lemma_ in REMOVE_ADJ)\
            and start != end:
        end -= 1
    if start == end:
        return doc
    else:
        return doc[start:end]

def parse_deps(doc, options):
    if options.get("summary", True):
        doc = summary_ja_doc(doc)
    chunks_tokens = run_analysis_and_convert2EN(doc)
    if options.get("collapse_punct",True):
        chunks_tokens = collapse_punct(chunks_tokens)
    if options.get("collapse_phrases", False):
        words = [{"text": token["text"], "tag": token["pos"]} for token in chunks_tokens["chunks"]]
        return {"words": words, "arcs": [], "settings": get_doc_settings(doc.doc)}
    else:
        words = [{"text": token["text"], "tag": token["pos"]} for token in chunks_tokens["tokens"]]
        return {"words": words, "arcs": [], "settings": get_doc_settings(doc.doc)}

def print_chunks_tokens(chunks_tokens):
    print("-------------chunks-------------")
    for chunk in chunks_tokens["chunks"]:
        print(chunk["text"], chunk["pos"], chunk["start"], chunk["end"])
    print("-------------tokens-------------")
    for chunk in chunks_tokens["tokens"]:
        print(chunk["text"], chunk["pos"])