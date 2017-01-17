import pytest
import falcon.testing
import json

from ..server import APP


class TestAPI(falcon.testing.TestCase):
    def __init__(self):
        self.api = APP


def test_deps():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/dep',
                body='''{"text": "This is a test.", "model": "en",
                         "collapse_punctuation": false, "collapse_phrases": false}''')
    result = json.loads(result.text)
    words = [w['text'] for w in result['words']]
    assert words == ["This", "is", "a", "test", "."]


def test_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/ent',
                body='''{"text": "Google is a company.", "model": "en"}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]


def test_train_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/train/ent',
                body='''{"text": "Google es una empresa.", "model": "es",
                         "tags": [{"start": 0, "len": 6, "type": "ORG"}]}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]


def test_train_and_query_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/train/ent',
                body='''{"text": "Google es una empresa.", "model": "es",
                         "tags": [{"start": 0, "len": 6, "type": "ORG"}]}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]
    result = test_api.simulate_post(path='/ent',
                body='''{"text": "Google es una empresa.", "model": "es"}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Google"), "type": "ORG"}]
