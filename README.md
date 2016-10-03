<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# spaCy services

This repository provides REST microservices for Explosion AI's [interactive demos](https://demos.explosion.ai) and visualisers.

## [displaCy server](displacy)

A simple [Falcon](https://falconframework.org/) app for exposing a spaCy dependency parser and spaCy named entity recognition model as a REST microservice, formatted for the [displaCy.js](https://github.com/explosion/displacy) and [displaCy ENT](https://github.com/explosion/displacy-ent) visualiser.

The service exposes two endpoints that accept POST requests.

### `POST` `/dep/`

Example request:
```json
{
    "text": "They ate the pizza with anchovies",
    "model":"en",
    "collapse_punctuation": 0,
    "collapse_phrases": 0
}
```

Example response:

```json
{
    "arcs": [
        { "dir": "left", "start": 0, "end": 1, "label": "nsubj" },
        { "dir": "right", "start": 1, "end": 2, "label": "dobj" },
        { "dir": "right", "start": 1, "end": 3, "label": "prep" },
        { "dir": "right", "start": 3, "end": 4, "label": "pobj" },
        { "dir": "left", "start": 2, "end": 3, "label": "prep" }
    ],
    "words": [
        { "tag": "PRP", "text": "They" },
        { "tag": "VBD", "text": "ate" },
        { "tag": "NN", "text": "the pizza" },
        { "tag": "IN", "text": "with" },
        { "tag": "NNS", "text": "anchovies" }
    ]
}
```

### `POST` `/ent/`

Example request:

```json
{
    "text": "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.",
    "model": "en"
}
```

Example response:

```json
[
    { "end": 20, "start": 5,  "type": "PERSON" },
    { "end": 67,  "start": 61, "type": "ORG" },
    { "end": 75, "start": 71, "type": "DATE" }
]
```

## [sense2vec server](sense2vec)

A simple [Falcon](https://falconframework.org/) app for exposing a sense2vec model as a REST microservice, as used in the [sense2vec demo](https://github.com/explosion/sense2vec-demo)

The service exposes a single endpoint over GET:

```
GET /{word|POS}
```

Example query:

```
GET /natural_language_processing%7CNOUN
```

Example response:

```json
[
    {
        "score": 0.1,
        "key": "computational_linguistics|NOUN",
        "text": "computational linguistics",
        "count": 20,
        "head": "linguistics"
    }
]
```
