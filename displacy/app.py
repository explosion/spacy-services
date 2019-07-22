# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
import spacy
from displacy.mercury_english_query import en_parse_deps
from ja_text_analyser import analyze_ja_text
JA_MODEL = "ja"

MODELS = {
    "en_core_web_sm": spacy.load("en_core_web_sm"),
    JA_MODEL:spacy.load("ja_ginza")
}


def get_model_desc(nlp, model_name):
    """Get human-readable model name, language name and version."""
    lang_cls = spacy.util.get_lang_class(nlp.lang)
    lang_name = lang_cls.__name__
    model_version = nlp.meta["version"]
    return "{} - {} (v{})".format(lang_name, model_name, model_version)


@hug.get("/models")
def models():
    return {name: get_model_desc(nlp, name) for name, nlp in MODELS.items()}


@hug.post("/dep")
def dep(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get dependencies for displaCy visualizer."""
    options = {
        "collapse_punct": collapse_punctuation,
        "collapse_phrases": collapse_phrases,
    }
    nlp = MODELS[model]
    doc = nlp(text)

    if model.startswith("en_"):
        return en_parse_deps(doc, options)
    elif model == JA_MODEL:
        return analyze_ja_text.parse_deps(doc, options)
    return spacy.displacy.parse_deps(doc, options)


@hug.post("/ent")
def ent(text: str, model: str):
    """Get entities for displaCy ENT visualizer."""
    nlp = MODELS[model]
    doc = nlp(text)
    return [
        {"start": ent.start_char, "end": ent.end_char, "label": ent.label_}
        for ent in doc.ents
    ]


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8080)
