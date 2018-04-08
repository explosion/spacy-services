<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# sense2vec

Serve a [sense2vec](https://github.com/explosion/sense2vec) and find the most
similar terms for a given query. Supports setting the "sense" (part-of-speech
tag or entity label) manually, as well as auto-detection using spaCy's English
lemmatizer and similarity scores. For a usage example, see the
[sense2vec demo](https://explosion.ai/demos/sense2vec).

## Installation

```bash
pip install -r requirements.txt
python app.py
```

You'll also need to download the Reddit vectors model, unpack the archive and
place the data in a `reddit_vectors-1.1.0` directory.
[See here](https://github.com/explosion/sense2vec) for details and installation
instructions.

## API

### GET `/senses`

Get a list of available senses, i.e. part-of-speech tags and entity labels.

#### Example response:

```json
[
    "auto",
    "ADJ",
    "NOUN",
    "VERB",
    "PERSON",
    "ORG"
]
```

### POST `/find`

Find similar terms for a given term and optional sense.

#### Example request

```json
{
    "word": "natural language processing",
    "sense":"NOUN",
    "n_results": 200
}
```

| Name | Type | Description |
| --- | --- | --- |
| `word` | string | The term to look up. |
| `sense` | string | The sense. Defaults to `'auto'`. |
| `n_results` | number | Number of results to return. Defaults to `200`. |

#### Example response

```json
{
    "text": "natural language processing",
    "sense": "NOUN",
    "results": [
        {
            "text": "machine learning",
            "score": 0.8986966609954834,
            "count": 1825
        },
        {
            "text": "computer vision",
            "score": 0.8636297583580017,
            "count": 625
        }
    ]
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | The term text. |
| `sense` | string | The sense, i.e. part-of-speech tag or entity label. |
| `results` | list | The most similar terms. |
| `score` | number | The similarity score. |
| `count` | number | The total frequency count. |

## Usage Example (JavaScript)

```javascript
function findSimilar(word, sense = 'auto') {
    const options = {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ word, sense })
    };
    fetch('/find', options)
        .then(res => res.json())
        .then(({ results }) => {
            console.log(results);
        });
}
```
