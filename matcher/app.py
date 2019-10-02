# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
import spacy
from spacy.matcher import Matcher


MODELS = {"en_core_web_sm": spacy.load("en_core_web_sm")}


def get_model_desc(nlp, model_name):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@hug.get("/models")
def models():
    return {name: get_model_desc(nlp, name) for name, nlp in MODELS.items()}


@hug.post("/match")
def match(text: str, model: str, pattern: list):
    nlp = MODELS[model]
    if pattern:
        matcher = Matcher(nlp.vocab)
        matcher.add("PATTERN", None, pattern)
    doc = nlp(text)
    tokens = []
    matches = []
    match_tokens = set()
    if pattern:
        for _, start, end in matcher(doc):
            if start >= end:  # filter out null matches or results of weird bug
                continue
            span = doc[start:end]
            if span[0].i in match_tokens:  # filter out overlaps
                continue
            match_tokens.update([t.i for t in span])
            matches.append(
                {"start": span.start_char, "end": span.end_char, "label": "MATCH"}
            )
    for t in doc:
        start = t.idx
        end = t.idx + len(t.text)
        label = "MATCH" if t.i in match_tokens else "TOKEN"
        tokens.append({"start": start, "end": end, "label": label})
    return {"matches": matches, "tokens": tokens}


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8080)
