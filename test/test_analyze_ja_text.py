from ja_text_analyser.analyze_ja_text import *
from ja_text_analyser.utils import VERB_CHUNK_PATTERN
import jaconv
import unittest
import spacy


class TestJaTextAnalysis(unittest.TestCase):

    def test_regex(self):

        text = "アジアのバー・パブ・クラブショップ"
        text = jaconv.normalize(text)
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks = []
        for chunk_doc, _ in ja_pos_regex_matches(doc, pattern=CHUNKS_PATTERN):
            chunks.append(chunk_doc.text)
        expect = ['アジア', 'の', 'バー・パブ・クラブショップ']
        self.assertEqual(chunks, expect)

    def test_regex_2(self):

        text = "東南アジアのとても素敵なビーチ"
        text = jaconv.normalize(text)
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks = []
        for chunk_doc,_ in ja_pos_regex_matches(doc, pattern=CHUNKS_PATTERN):
            chunks.append(chunk_doc.text)
        expect = ['東南アジア', 'の', 'とても素敵なビーチ']
        self.assertEqual(chunks, expect)

    def test_regex_3(self):
        text = "豪華で美しいホテル"
        text = jaconv.normalize(text)
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks = []
        for chunk_doc,_ in ja_pos_regex_matches(doc, pattern=CHUNKS_PATTERN):
            chunks.append(chunk_doc.text)
        expect = ['豪華で美しいホテル']
        self.assertEqual(chunks, expect)

    def test_regex_4(self):

        text = "1月の東京"
        text = jaconv.normalize(text)
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks = []
        for chunk_doc,_ in ja_pos_regex_matches(doc, pattern=CHUNKS_PATTERN):
            chunks.append(chunk_doc.text)
        expect = ['1月', 'の', '東京']
        self.assertEqual(chunks, expect)

    def test_regex_5(self):

        text = "豪華だが美しいホテル"
        text = jaconv.normalize(text)
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks = []
        for chunk_doc,_ in ja_pos_regex_matches(doc, pattern=CHUNKS_PATTERN):
            chunks.append(chunk_doc.text)
        expect = ['豪華だ', 'が', '美しいホテル']
        self.assertEqual(chunks, expect)

    def test_regex_for_verb_phrase_5(self):

        text = "彼はこの本を注意深く読んだ"
        text = jaconv.normalize(text)
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks = []
        for chunk_doc,_ in ja_pos_regex_matches(doc, pattern=VERB_CHUNK_PATTERN):
            chunks.append(chunk_doc.text)
        expect = ["注意深く読んだ"]
        self.assertEqual(chunks, expect)

    def test_run_analysis(self):

        text = "1月の東京,彼はこの本を注意深く読んだ"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks_tokens = run_analysis(doc)
        chunk_pos = [chunk["pos"] for chunk in chunks_tokens["chunks"]]
        expect_chunk_pos = ['NOUN', 'ADP', 'PROPN', 'PUNCT', 'PRON', 'ADP', 'NOUN', 'ADP', 'VERB']

        self.assertEqual(chunk_pos, expect_chunk_pos)

    def test_run_analysis_2(self):

        text = "ダナンの海と山"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks_tokens = run_analysis(doc)
        chunk_pos = [chunk["pos"] for chunk in chunks_tokens["chunks"]]
        expect_chunk_pos = ['PROPN', 'ADP', 'NOUN', 'CCONJ', 'NOUN']
        self.assertEqual(chunk_pos, expect_chunk_pos)

    def test_run_analysis_with_object_label(self):

        text = "庵美術館"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks_tokens = run_analysis(doc)
        chunk_pos = [chunk["pos"] for chunk in chunks_tokens["chunks"]]
        expect_chunk_pos = ['NOUN']
        self.assertEqual(chunk_pos, expect_chunk_pos)

    def test_convert2EN(self):

        text = "ダナンの海と山"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        chunks_tokens = run_analysis(doc)
        en_chunks_tokens = convert2EN(chunks_tokens)
        chunk_pos = [chunk["pos"] for chunk in en_chunks_tokens["chunks"]]
        expect_chunk_pos = ['NOUN', 'CCONJ', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(chunk_pos, expect_chunk_pos)

    def test_parser_deps(self):

        text = "ダナンの海と山"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        options = {}
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]
        expect_tags = ['NOUN', 'CCONJ', 'NOUN', 'ADP', 'PROPN']
        expect_words = ['海', 'と', '山', 'の', 'ダナン']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)

    def test_parser_deps_with_collapse_phrases(self):

        text = "アジアのバー・パブ・クラブショップ"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        options = {
            "collapse_punct": False,
            "collapse_phrases": True,
        }
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]

        expect_tags = ['NOUN', 'ADP', 'PROPN']
        expect_words = ['バー・パブ・クラブショップ', 'の', 'アジア']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)

    def test_parser_deps_with_non_collapse_phrases(self):

        text = "アジアのバー・パブ・クラブショップ"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        options = {
            "collapse_punct": False,
            "collapse_phrases": False,
        }
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]

        expect_tags = ['NOUN', 'PUNCT', 'NOUN', 'PUNCT', 'NOUN', 'NOUN', 'ADP', 'PROPN']
        expect_words = ['バー', '・', 'パブ', '・', 'クラブ', 'ショップ', 'の', 'アジア']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)

    def test_parser_deps_with_collapse_punct_and_non_collapse_phrases(self):

        text = "アジアのバー・パブ・クラブショップ"
        nlp =spacy.load("ja_ginza")
        doc = nlp(text)
        options = {
            "collapse_punct": True,
            "collapse_phrases": False,
        }
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]

        expect_tags = ['NOUN', 'NOUN', 'NOUN', 'NOUN', 'ADP', 'PROPN']
        expect_words = ['バー・', 'パブ・', 'クラブ', 'ショップ', 'の', 'アジア']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)


    def test_summary_ja_text(self):

        text ="セックスツアーに想いください"
        nlp = spacy.load("ja_ginza")
        doc = nlp(text)
        options = {
            "collapse_punct": True,
            "collapse_phrases": False,
            "summary": True,
        }
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]

        expect_tags = ['NOUN', 'NOUN']
        expect_words =['セックス', 'ツアー']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)

    def test_summary_ja_text_2(self):

        text ="横浜でレストランを探しています"
        nlp = spacy.load("ja_ginza")
        doc = nlp(text)
        options = {
            "collapse_punct": True,
            "collapse_phrases": True,
            "summary": True,
        }
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]

        expect_tags = ['NOUN', 'ADP', 'PROPN']
        expect_words = ['レストラン', 'で', '横浜']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)
    def test_summary_ja_text_3(self):

        text ="アジアの美しいテンプレートとは"
        nlp = spacy.load("ja_ginza")
        doc = nlp(text)
        options = {
            "collapse_punct": True,
            "collapse_phrases": False,
            "summary": True,
        }
        parser_result = parse_deps(doc, options)
        words = []
        tags = []
        [words.append(token["text"]) or tags.append(token["tag"]) for token in parser_result["words"]]

        expect_tags = ['ADJ', 'NOUN', 'ADP', 'PROPN']
        expect_words = ['美しい', 'テンプレート', 'の', 'アジア']

        self.assertEqual(tags, expect_tags)
        self.assertEqual(words, expect_words)
