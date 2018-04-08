<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# displaCy

Serve one or more [spaCy models](https://spacy.io/models) and extract syntactic
dependencies, part-of-speech tags and/or entities. For usage examples, see the
[displaCy](https://explosion.ai/demos/displacy) and
[displaCy ENT](https://explosion.ai/demos/displacy-ent) demos.

## Installation

```bash
pip install -r requirements.txt
python app.py
```

## API

### GET `/models`

Get a list of available models and their human-readable name, keyed by model
name.

#### Example response

```json
{
    "en_core_web_sm": "English - en_core_web_sm (v2.0.0)",
    "de_core_news_sm": "German - de_core_news_sm (v2.0.0)",
    "es_core_news_sm": "Spanish - es_core_news_sm (v2.0.0)"
}
```

### POST `/dep`

#### Example request

```json
{
    "text": "They ate the pizza with anchovies",
    "model":"en_core_web_sm",
    "collapse_punctuation": false,
    "collapse_phrases": true
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | Text to be parsed. |
| `model` | string | Name of the model used. |
| `collapse_punctuation` | boolean | Merge punctuation onto the preceding token? |
| `collapse_phrases` | boolean | Merge noun chunks and named entities into single tokens? |

#### Example response

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

| Name | Type | Description |
| --- | --- | --- |
| `arcs` | array | Data to generate the arrows. |
| `dir` | string | Direction of arrow (`"left"` or `"right"`). |
| `start` | number | Offset of word the arrow *starts on*. |
| `end` | number | Offset of word the arrow *ends on*. |
| `label` | string | Dependency label. |
| `words` | array | Data to generate the words. |
| `tag` | string | Part-of-speech tag. |
| `text` | string | Token text. |

### POST `/ent`

#### Example request

```json
{
    "text": "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.",
    "model": "en"
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | Text to be parsed. |
| `model` | string | Name of model to use. |

#### Example response

```json
[
    { "end": 20, "start": 5,  "label": "PERSON" },
    { "end": 67, "start": 61, "label": "ORG" },
    { "end": 75, "start": 71, "label": "DATE" }
]
```

| Name | Type | Description |
| --- | --- | --- |
| `start` | number | Character offset the entity *starts on*. |
| `end` | number | Character offset the entity *ends after*. |
| `label` | string | Entity label. |

## Usage Example (JavaScript)

```javascript
function getEntities(text, model) {
    const options = {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ text, model })
    };
    fetch('/ent', options)
        .then(res => res.json())
        .then(entities => {
            console.log(entities);
        });
}
```
