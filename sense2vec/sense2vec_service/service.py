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
        print("Req", req, query)
        query = unquote(query)
        print("Get result for", query)
        result = self.handler(query)
        print("Returning", result)
        resp.body = json.dumps(result)


def load():
    '''Load the sense2vec model, and return a falcon API object that exposes
    the SimilarityService.
    '''
    print("Loading")
    cors = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True,
		allow_credentials_all_origins=True)
    app = falcon.API(middleware=[cors.middleware])
    app.add_route('/{query}', SimilarityService())
    print("Loaded!")
    return app


