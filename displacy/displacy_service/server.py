#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import falcon
import spacy
import json

from .parse import Parse, Entities


try:
  unicode
except NameError:
  unicode = str


_models = {}


def get_model(model_name):
    if model_name not in _models:
        _models[model_name] = spacy.load(model_name)
    return _models[model_name]


class ParseServer(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text', 'displaCyEX is the new displaCy.')
        model_name = json_data.get('model', 'en')
        collapse_punctuation = json_data.get('collapse_punctuation', True)
        collapse_phrases = json_data.get('collapse_phrases', True)

        try:
            model = get_model(model_name)
            parse = Parse(model, text, collapse_punctuation, collapse_phrases)
            resp.body = json.dumps(parse.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500


class EntityServer(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        req_body = req.stream.read()
        json_data = json.loads(req_body.decode('utf8'))
        text = json_data.get('text', 'displaCyEX is the new displaCy.')
        model_name = json_data.get('model', 'en')
        try:
            model = get_model(model_name)
            entities = Entities(model, text)
            resp.body = json.dumps(entities.to_json(), sort_keys=True, indent=2)
            resp.content_type = b'text/string'
            resp.append_header(b'Access-Control-Allow-Origin', b"*")
            resp.status = falcon.HTTP_200
        except:
            resp.status = falcon.HTTP_500


APP = falcon.API()
parse_server = ParseServer()
ner_server = EntityServer()
APP.add_route('/dep', parse_server)
APP.add_route('/ent', ner_server)
