from __future__ import unicode_literals, print_function
try:
    from urllib.parse import unquote
except ImportError:
    from urllib2 import unquote

import ujson as json
import spacy
import sense2vec

import falcon
from falcon_cors import CORS


from .similarity import Similarity



class SimilarityService(object):
    '''Expose a sense2vec handler as a GET service for falcon.'''
    def __init__(self):
        self.handler = Similarity(
            spacy.load('en', parser=False, entity=False),
            sense2vec.load())

    def on_get(self, req, resp, query=''):
        return json.dumps(self.handler(unquote(query)))


def load():
    '''Load the sense2vec model, and return a falcon API object that exposes
    the SimilarityService.
    '''
    cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
    app = falcon.API(middleware=[cors.middleware])
    app.add_route('/{query}', SimilarityService())
    return app


