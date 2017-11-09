<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# spaCy REST services

This repository provides REST microservices for Explosion AI's [interactive demos](https://demos.explosion.ai) and visualisers. All requests and responses are JSON-encoded as `text/string`, so all requests require the header `Content-Type: text/string`.

# Docker Packaging

This fork provides a Dockerfile that brings up a displaCy server (as documented below) using spaCy 1.9.0. To build and run locally,

```docker build -t $YOUR_TAG .```

```docker run -p 8000:8000 $YOUR_TAG```

This will start a displaCy server running on localhost:8000.

## [displaCy server](displacy)

A simple [Falcon](https://falconframework.org/) app for exposing a spaCy dependency parser and spaCy named entity recognition model as a REST microservice, formatted for the [displaCy.js](https://github.com/explosion/displacy) and [displaCy ENT](https://github.com/explosion/displacy-ent) visualiser. For more info on the rendering on the front-end that consumes the data produced by this service, see [this blog post](https://explosion.ai/blog/displacy-js-nlp-visualizer).

The service exposes two endpoints that accept POST requests, and two endpoints that accept GET requests to describe the available models and schemas.

---

### `POST` `/dep/`

`POST` to `/dep/` has been modified to only accept `text` field with a list of texts (with one or more words)
this is to accomodate 'batching' several thousand texts at once - in the case of a fetch on single words, for example

Additionally - the `POST` command allows the request param `features` - any value of which will filter the resulting `word` serialization to filter for those features

For example:

`curl -s localhost:8000/dep -d '{"text":["human"], "model":"en"}'`

will return:

```json
{
  "human": {
    "arcs": [], //empty, as there is only a single word in this text
    "words": [  //a single-member list, as this is a single word text - expect this!
      {
        "dep": 'ROOT', //root as we're a single word text!
        "ent_type": ..., //ellipses for lazyness
        "lemma": ...,
        "like_email": ...,
        "like_num": ...,
        "orth": ...,
        "pos": ...,
        "sentiment": ...,
        "shape": ...,
        "tag": ...,
        "text": ...,
        "vector": [...]
      }]
    }
}
```

woah! those are a lot of features! we can filter for the features over the wire using a request parameter:

`curl -s localhost:8000/dep?features=vector&features=orth -d '{"text":["human"], "model":"en"}'`

et voila: we only get back the features we want!

```json
{
  "human": {
    "arcs": [], //empty, as there is only a single word in this text
    "words": [  //a single-member list, as this is a single word text - expect this!
      {
        "orth": ...,
        "vector": [...]
      }]
    }
}
```

### A fun exercise

```python
import json, requests, spacy

convience = lambda x: {'text': x if isinstance(x, list) else [x], 'model': 'en'}

url = "http://localhost:8000/dep"

nlp = spacy.load('en')

madness = [token.text for token in nlp.vocab]

headers = {"content-type": "application/json"}
params = {"features": ["vector", "orth"]}

response = requests.post(url, data=json.dumps(convenience(madness)), headers=headers, params=params)

# it's true that the unwrapping logic is a little bit messy here.
# this is because we don't want to stray _too_ far from a general spaCy retval
# and it's worth noting that between the first and last keys (`human` and `vector` respectively),
# we are guaranteed to use the same constant keying for the intermediate vals
response['human']['words'][0]['vector']
```

Example request:

**note:** I didn't update the responses, sorry!

```json
{
    "text": ["They ate the pizza with anchovies"],
    "model":"en",
    "collapse_punctuation": 0,
    "collapse_phrases": 1
}
```

```json
{
    "text": ["human", "balance", "machine", "they ate the pizza with anchovies"],
    "model": "en"
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | list[string] | each list member should be a complete text to be parsed |
| `model` | string | identifier string for a model installed on the server |
| `collapse_punctuation` | boolean | Merge punctuation onto the preceding token? |
| `collapse_phrases` | boolean | Merge noun chunks and named entities into single tokens? |  


Example request using the Python [Requests library](http://docs.python-requests.org/en/master/):

```python
import json
import requests

url = "http://localhost:8000/dep"
message_text = ["They ate the pizza with anchovies"]
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en'}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
{"They ate the pizza with anchovies": {
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
    ]}
}
```

| Name | Type | Description |
| --- | --- | --- |
| `arcs` | array | data to generate the arrows |
| `dir` | string | direction of arrow (`"left"` or `"right"`) |
| `start` | integer | offset of word the arrow starts **on** |
| `end` | integer | offset of word the arrow ends **on** |
| `label` | string | dependency label |
| `words` | array | data to generate the words |
| `tag` | string | part-of-speech tag |
| `text` | string | token |

---

Curl command:

```
curl -s localhost:8000/dep -d '{"text":["Pastafarians are smarter than people with Coca Cola bottles.", "This statement is true: that statement was false"], "model":"en"}'
```

```json
{
  "arcs": [
    {
      "dir": "left",
      "end": 1,
      "label": "nsubj",
      "start": 0
    },
    {
      "dir": "right",
      "end": 2,
      "label": "acomp",
      "start": 1
    },
    {
      "dir": "right",
      "end": 3,
      "label": "prep",
      "start": 2
    },
    {
      "dir": "right",
      "end": 4,
      "label": "pobj",
      "start": 3
    },
    {
      "dir": "right",
      "end": 5,
      "label": "prep",
      "start": 4
    },
    {
      "dir": "right",
      "end": 6,
      "label": "pobj",
      "start": 5
    }
  ],
  "words": [
    {
      "tag": "NNPS",
      "text": "Pastafarians"
    },
    {
      "tag": "VBP",
      "text": "are"
    },
    {
      "tag": "JJR",
      "text": "smarter"
    },
    {
      "tag": "IN",
      "text": "than"
    },
    {
      "tag": "NNS",
      "text": "people"
    },
    {
      "tag": "IN",
      "text": "with"
    },
    {
      "tag": "NNS",
      "text": "Coca Cola bottles."
    }
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

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | text to be parsed |
| `model` | string | identifier string for a model installed on the server  |

Example request using the Python [Requests library](http://docs.python-requests.org/en/master/):

```python
import json
import requests

url = "http://localhost:8000/ent"
message_text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en'}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
[
    { "end": 20, "start": 5,  "type": "PERSON" },
    { "end": 67, "start": 61, "type": "ORG" },
    { "end": 75, "start": 71, "type": "DATE" }
]
```

| Name | Type | Description |
| --- | --- | --- |
| `end` | integer | character offset the entity ends **after** |
| `start` | integer | character offset the entity starts **on** |
| `type` | string | entity type |



```
curl -s localhost:8000/ent -d '{"text":"Pastafarians are smarter than people with Coca Cola bottles.", "model":"en"}'
```

```json
[
  {
    "end": 12,
    "start": 0,
    "type": "NORP"
  },
  {
    "end": 51,
    "start": 42,
    "type": "ORG"
  }
]
```


---

### `GET` `/models`

List the names of models installed on the server.

Example request:

```
GET /models
```

Example response:

```json
["en", "de"]
```

---

### `GET` `/{model}/schema/`

Example request:

```
GET /en/schema
```

| Name | Type | Description |
| --- | --- | --- |
| `model` | string | identifier string for a model installed on the server |

Example response:

```json
{
  "dep_types": ["ROOT", "nsubj"],
  "ent_types": ["PERSON", "LOC", "ORG"],
  "pos_types": ["NN", "VBZ", "SP"]
}
```

---

## [sense2vec server](sense2vec)

A simple [Falcon](https://falconframework.org/) app for exposing a sense2vec model as a REST microservice, as used in the [sense2vec demo](https://github.com/explosion/sense2vec-demo)

The service exposes a single endpoint over GET.

---

### `GET` `/{word|POS}`

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

| Name | Type | Description |
| --- | --- | --- |
| `score` | float | similarity to query |
| `key` | string | identifier string |
| `text` | string | human-readable token |
| `count` | integer | absolute frequency in training corpus |
| `head` | string | head word in text |
