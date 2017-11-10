import pytest
import falcon.testing
import json

from ..server import APP


class TestAPI(falcon.testing.TestCase):
    def __init__(self):
        self.api = APP

def form_deps_message(message, model="en", collapse_punctuation=False, collapse_phrases=False):
    return {"text": message,
            "model": model,
            "collapse_punctuation": collapse_punctuation,
            "collapse_phrases": collapse_phrases}

# test that we parse this message correctly - note that we have to wrap the text in a list: client responsibility
def test_deps_simple():
    test_api = TestAPI()
    test_text_zero = "This is a test."
    test_text = [test_text_zero]
    test_message = form_deps_message(test_text)
    result = test_api.simulate_post(path='/dep',
                                    body=json.dumps(test_message))
    result = json.loads(result.text)
    words = {k:[w['text'] for w in v['words']] for k,v in result.items()}
    assert words[test_text_zero] == ["This", "is", "a", "test", "."]
    assert all([word in text for word in words[text]] for text in test_message["text"])

# same as above, but with unicode and another language model
def test_deps_unicode():
    test_api = TestAPI()
    test_text_zero = u"Das ist ein großer Test."
    test_text = [test_text_zero]
    test_message = form_deps_message(test_text, model="de")
    result = test_api.simulate_post(path='/dep',
                                    body=json.dumps(test_message))
    result = json.loads(result.text)
    words = {k:[w['text'] for w in v['words']] for k,v in result.items()}
    assert words[test_text_zero] == [u"Das", u"ist", u"ein", u"großer", "Test", "."]
    assert all([word in text for word in words[text]] for text in test_message["text"])

# same as above, except we're batching multiple texts
def test_deps_multimessage():
    test_api = TestAPI()
    test_text_zero = "This is a test."
    test_text = [test_text_zero, "human", "dancer"]
    test_message = form_deps_message(test_text)
    result = test_api.simulate_post(path='/dep',
                                    body=json.dumps(test_message))
    result = json.loads(result.text)
    words = {k:[w['text'] for w in v['words']] for k,v in result.items()}
    assert words[test_text_zero] == ["This", "is", "a", "test", "."]
    assert all([word in text for word in words[text]] for text in test_message["text"])

# testing our ability to filter return keys with the `feature` param
def test_deps_featureparam():
    test_api = TestAPI()
    test_text_zero = "This is a test."
    test_text = [test_text_zero, "human", "dancer"]
    test_message = form_deps_message(test_text)
    result = test_api.simulate_post(path='/dep',
                                    body=json.dumps(test_message))
    result_init = json.loads(result.text)

    params = {"features": ["vector", "orth", "this is not a real feature in any capacity", ""]}

    result = test_api.simulate_post(path='/dep',
                                    body=json.dumps(test_message),
                                    params=params)
    result_final = json.loads(result.text)

    # are the same tokens appearing in each resp?
    assert result_final.keys() == result_init.keys()

    # is the set of feature keys available in the resp with the feature param a subset of the unfiltered resp?
    assert all({key for word in result_final[token]['words'] for key in word.keys()}.issubset(
                {key for word in result_init[token]['words'] for key in word.keys()})
               for token in result_final.keys())

    # is the set of feature keys available in the resp without the feature param not a subset of the filtered resp?
    assert all(not {key for word in result_init[token]['words'] for key in word.keys()}.issubset(
                    {key for word in result_final[token]['words'] for key in word.keys()})
                for token in result_final.keys())

    # are the features available exactly the same as the _valid_ features listed in the `params` struct?
    assert all({key for word in result_final[token]['words']
                for key in word.keys()} ^ set(params['features']) == {"this is not a real feature in any capacity", ""}
               for token in result_final.keys())

def test_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/ent',
                body='''{"text": "Francis, hit the lights.", "model": "en"}''')
    ents = json.loads(result.text)
    assert ents == [{"start": 0, "end": len("Francis"), "type": "PERSON"}]
