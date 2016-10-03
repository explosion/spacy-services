<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# spaCy services

This repository provides REST microservices for Explosion AI's [interactive demos](https://demos.explosion.ai) and visualisers.

# [displaCy server](displacy)

This repository provides a simple falcon app for exposing a spaCy dependency parser and spaCy named entity recognition model as a REST microservice, formatted for the [displaCy.js](/explosion/displacy) and [displaCy ENT](/explosion/displacy-ent) visualiser.


# [sense2vec server](sense2vec)

This repository provides a simple falcon app for exposing a sense2vec model as a REST microservice, as used in the [sense2vec demo](/explosion/sense2vec-demo)

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
