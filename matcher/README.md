<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# Matcher

Check token patterns for spaCy's [rule-based `Matcher`](https://spacy.io/usage/linguistic-features#rule-based-matching)
against a text and return the matches in the text, as well as the individual
tokens and whether they're part of a match. For a usage example, see the
[Rule-based Matcher Explorer demo](https://explosion.ai/demos/matcher).

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
    "en_core_web_sm": "English - en_core_web_sm (v2.0.0)"
}
```

### POST `/match`

Match a pattern and return the matches and tokens.

#### Example request

```json
{
    "text": "A match is a tool for starting a fire. Typically, modern matches are made of small wooden sticks or stiff paper. ",
    "model":"en_core_web_sm",
    "pattern": [
        {
            "POS": "ADJ",
            "OP": "?"
        },
        {
            "LEMMA": "match",
            "POS": "NOUN"
        },
        {
            "LEMMA": "be"
        }
    ]
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | The text to match on. |
| `model` | string | The statistical model to use for tokenization. |
| `pattern` | list | The token pattern to match. Each object in the list describes one token and is keyed by token attributes. |

#### Example response

```json
{
    "matches": [
        {
            "start": 2,
            "end": 10,
            "label": "MATCH"
        },
        {
            "start": 50,
            "end": 68,
            "label": "MATCH"
        }
    ],
    "tokens": [
        {
            "start": 0,
            "end": 1,
            "label": "TOKEN"
        },
        {
            "start": 2,
            "end": 7,
            "label": "MATCH"
        },
        {
            "start": 8,
            "end": 10,
            "label": "MATCH"
        },
        {
            "start": 11,
            "end": 12,
            "label": "TOKEN"
        },
        {
            "start": 13,
            "end": 17,
            "label": "TOKEN"
        },
        {
            "start": 18,
            "end": 21,
            "label": "TOKEN"
        },
        {
            "start": 22,
            "end": 30,
            "label": "TOKEN"
        },
        {
            "start": 31,
            "end": 32,
            "label": "TOKEN"
        },
        {
            "start": 33,
            "end": 37,
            "label": "TOKEN"
        },
        {
            "start": 37,
            "end": 38,
            "label": "TOKEN"
        },
        {
            "start": 39,
            "end": 48,
            "label": "TOKEN"
        },
        {
            "start": 48,
            "end": 49,
            "label": "TOKEN"
        },
        {
            "start": 50,
            "end": 56,
            "label": "MATCH"
        },
        {
            "start": 57,
            "end": 64,
            "label": "MATCH"
        },
        {
            "start": 65,
            "end": 68,
            "label": "MATCH"
        },
        {
            "start": 69,
            "end": 73,
            "label": "TOKEN"
        },
        {
            "start": 74,
            "end": 76,
            "label": "TOKEN"
        },
        {
            "start": 77,
            "end": 82,
            "label": "TOKEN"
        },
        {
            "start": 83,
            "end": 89,
            "label": "TOKEN"
        },
        {
            "start": 90,
            "end": 96,
            "label": "TOKEN"
        },
        {
            "start": 97,
            "end": 99,
            "label": "TOKEN"
        },
        {
            "start": 100,
            "end": 105,
            "label": "TOKEN"
        },
        {
            "start": 106,
            "end": 111,
            "label": "TOKEN"
        },
        {
            "start": 111,
            "end": 112,
            "label": "TOKEN"
        }
    ]
}
```

| Name | Type | Description |
| --- | --- | --- |
| `matches` | list | The matches in the text. |
| `tokens` | list | The individual tokens in the text and whether they're part of a match. |
| `start` | number | Character offset the match or token *starts on*. |
| `end` | number | Character offset the match or token *ends after*. |
| `label` | string | `"MATCH"` for matched span, `"TOKEN"` for token span. |

## Usage Example (JavaScript)

```javascript
function getMatches(text, model, pattern) {
    const options = {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ text, model, pattern })
    };
    fetch('/match', options)
        .then(res => res.json())
        .then(({ tokens, matches }) => {
            console.log(tokens, matches);
        });
}
```
