from __future__ import unicode_literals
import base64

class Parse(object):
    def __init__(self, nlp, text, collapse_punctuation, collapse_phrases):
        self.doc = nlp(text)
        if collapse_punctuation:
            spans = []
            for word in self.doc[:-1]:
                if word.is_punct:
                    continue
                if not word.nbor(1).is_punct:
                    continue
                start = word.i
                end = word.i + 1
                while end < len(self.doc) and self.doc[end].is_punct:
                    end += 1
                span = self.doc[start : end]
                spans.append(
                    (span.start_char, span.end_char, word.tag_, word.lemma_, word.ent_type_)
                )
            for span_props in spans:
                self.doc.merge(*span_props)

        if collapse_phrases:
            for np in list(self.doc.noun_chunks):
                np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)

    # numpy can serialize this itself without loss of precision
    # but we then need to b64 the string so json can eat it.
    def serialize_vector(self, vector):
        bytes = vector.tostring()
        return base64.b64encode(bytes).decode('ascii')

    def to_json(self):
        words = [{'text': w.text, 'tag': w.tag_, 
                'orth': w.orth_, 'pos': w.pos_,
                'ent_type': w.ent_type_, 'shape': w.shape_,
                'lemma': w.lemma_, 'sentiment': w.sentiment,
                'like_num': w.like_num, 'like_email': w.like_email,
                'dep': w.dep_, 'serialized_vector': self.serialize_vector(w.vector)
                } for w in self.doc]
        arcs = []
        for word in self.doc:
            if word.i < word.head.i:
                arcs.append(
                    {
                        'start': word.i,
                        'end': word.head.i,
                        'label': word.dep_,
                        'dir': 'left'
                    })
            elif word.i > word.head.i:
                arcs.append(
                    {
                        'start': word.head.i,
                        'end': word.i,
                        'label': word.dep_,
                        'dir': 'right'
                    })
        return {'words': words, 'arcs': arcs}


class Entities(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)
     
    def to_json(self):
        return [{'start': ent.start_char, 'end': ent.end_char, 'type': ent.label_}
                for ent in self.doc.ents]
