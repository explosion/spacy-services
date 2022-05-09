# coding: utf8
from __future__ import unicode_literals

import hug
from hug_middleware_cors import CORSMiddleware
import spacy


print("Loading...")
MODELS = {
    "en_core_web_sm": spacy.load("en_core_web_sm"),
    # "en_core_web_md": spacy.load("en_core_web_md"),
    # "en_core_web_lg": spacy.load("en_core_web_lg"),
    # "de_core_news_sm": spacy.load("de_core_news_sm"),
    # "es_core_news_sm": spacy.load("es_core_news_sm"),
    # "pt_core_news_sm": spacy.load("pt_core_news_sm"),
    # "fr_core_news_sm": spacy.load("fr_core_news_sm"),
    # "it_core_news_sm": spacy.load("it_core_news_sm"),
    # "nl_core_news_sm": spacy.load("nl_core_news_sm"),
    # "nb_core_news_sm": spacy.load("nb_core_news_sm"),
    # "lt_core_news_sm": spacy.load("lt_core_news_sm"),
    # 'el_core_news_sm': spacy.load('el_core_news_sm'),
}
print("Loaded!")


@hug.post("/tags")
def tags(
    text: str,
    model: str,
    collapse_punctuation: bool = False,
    collapse_phrases: bool = False,
):
    """Get all tags."""
    nlp = MODELS[model]
    doc = nlp(text)
    options = {
        "collapse_punct": collapse_punctuation,
        "collapse_phrases": collapse_phrases,
    }

    return [
        {
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "shape": token.shape_,
            "is_alpha": token.is_alpha,
            "is_stop": token.is_stop
        }
        for token in doc
    ]


if __name__ == "__main__":
    import waitress

    app = hug.API(__name__)
    app.http.add_middleware(CORSMiddleware(app))
    waitress.serve(__hug_wsgi__, port=8080)
