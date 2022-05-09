
# Updates From thomas-hervey
## Installation
- dependencies are installed in a pyenv virtualenv called `spacy-js-virtualenv`. Once activated, requirements.txt were installed in that virtualenv
- Most models in the services are commented out because we are only using English (for now)
- Updated hug to `hug==2.4.8` in order to prevent server errors (see comment here)[https://github.com/ines/spacy-js/issues/5#issuecomment-703893676]
---
<a href="https://explosion.ai"><img src="https://explosion.ai/assets/img/logo.svg" width="125" height="125" align="right" /></a>

# spaCy REST services

This repository includes REST microservices for various spaCy-related tasks. The
services power our [interactive demos](https://explosion.ai/demos) and can be
used as examples of exposing spaCy's capabilities as a microservice. All APIs
are built with [`hug`](https://github.com/timothycrosley/hug) and
**require Python 3**. The following services are available – for more details,
see the API docs in the respective directories.

| Service | Description | Example |
| --- | --- | -- |
| [`displacy`](displacy) | Serve a spaCy model and extract dependencies and named entities. | [🖼](https://explosion.ai/demos/displacy), [🖼](https://explosion.ai/demos/displacy-ent)|
| [`sense2vec`](sense2vec) | Serve a [sense2vec](https://github.com/explosion/sense2vec) model with automatic sense detection. | [🖼](https://explosion.ai/demos/sense2vec)
| [`matcher`](matcher) | Run a match pattern over a text and return the matches and tokens as JSON. | [🖼](https://explosion.ai/demos/matcher) |
