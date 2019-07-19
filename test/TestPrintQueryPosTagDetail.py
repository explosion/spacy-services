import unittest
from displacy.mercury_english_query import summarize_doc
import spacy


class TestPrintToken(unittest.TestCase):

    english_nlp = spacy.load("en_core_web_sm")

    def print_token_labels(self, spacy_doc):
        for token in spacy_doc:
            print(token.text,token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)


    def test_summarized_pattern1(self):
        sentence1 = "May in France"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

    def test_summarized_pattern2(self):
        sentence1 = "white night"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match =   summarize_doc(spacy_doc)

        self.assertEqual(match.text, "white night")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADJ', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern_2(self):
        sentence1 = "I like white night"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "white night")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADJ', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern3(self):
        sentence1 = "swimming"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "swimming")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern3(self):
        sentence1 = "I love swimming"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "swimming")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['VERB']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern4(self):
        sentence1 = "beach"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "beach")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN']
        self.assertEqual(POS, EXPTECTED_POS)

    def test_tag_regex_matches_pattern4(self):
        sentence1 = "This is a very nice beach"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "very nice beach")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADV', 'ADJ', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern5(self):
        sentence1 = "Eiffel tower"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "Eiffel tower")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'NOUN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_tag_regex_matches_pattern5(self):
        sentence1 = "I want to visit Eiffel tower"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "Eiffel tower")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['PROPN', 'NOUN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_summarized_pattern6(self):
        sentence1 = "sex tour"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "sex tour")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'NOUN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_tag_regex_matches_pattern6(self):
        sentence1 = "I would like to join a sex tour"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "sex tour")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'NOUN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_summarized_pattern6(self):
        sentence1 = "Hermitage museum"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "Hermitage museum")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'NOUN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_tag_regex_matches_pattern6(self):
        sentence1 = "I would like to visit Hermitage museum"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "Hermitage museum")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['PROPN', 'NOUN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_summarized_pattern7(self):
        sentence1 = "luxury hotel"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "luxury hotel")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern7(self):
        sentence1 = "I enjoy staying in a luxury hotel"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

#        self.print_token_labels(spacy_doc)

        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "luxury hotel")
        # only "luxury hotel" is important => return the longest phrase (containing noun?)
        # ==> token.dep_ == pobj

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern8(self):
        sentence1 = "very nice beach"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "very nice beach")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADV', 'ADJ', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern8(self):
        sentence1 = "This is a very nice beach"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "very nice beach")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADV', 'ADJ', 'NOUN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern9(self):
        sentence1 = "restaurant in Yokohama"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "restaurant in Yokohama")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern9(self):
        sentence1 = "I'm searching for a restaurant in Yokohama"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

#        self.print_token_labels(spacy_doc)
        self.assertEqual(match.text, "restaurant in Yokohama")
        # only "restaurant in Yokohama" is important
        # token.dep_ == pobj

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern10(self):
        sentence1 = "France in May"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "France in May")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_tag_regex_matches_pattern10(self):
        sentence1 = "I plan to visit France in May"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "France in May")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern11(self):
        sentence1 = "nightlife in Europe"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "nightlife in Europe")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_tag_regex_matches_pattern11(self):
        sentence1 = "I enjoy nightlife in Europe"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "nightlife in Europe")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)

    def test_summarized_pattern12(self):
        sentence1 = "street food in Thailand"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "street food in Thailand")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern12(self):
        sentence1 = "I would like to try street food in Thailand"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "street food in Thailand")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern13(self):
        sentence1 = "Vietnamese restaurants in Yokohama"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "Vietnamese restaurants in Yokohama")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADJ', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern13(self):
        sentence1 = "I'm searching for Vietnamese restaurants in Yokohama"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

#        self.print_token_labels(spacy_doc)

        self.assertEqual(match.text, "Vietnamese restaurants in Yokohama")
        # Actual output: "searching for Vietnamese restaurants in Yokohama"
        # Preferred output: "Vietnamese restaurants in Yokohama"
        # 'VBG' should not be merged with 'NNP|NNS|NN\\b'? How?

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADJ', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern14(self):
        sentence1 = "beautiful temples in Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "beautiful temples in Asia")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADJ', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern14(self):
        sentence1 = "what are beautiful temples in Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "beautiful temples in Asia")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['ADJ', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)

    def test_summarized_pattern15(self):
        sentence1 = "towers in Vietnam"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "towers in Vietnam")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)

    def test_tag_regex_matches_pattern15(self):
        sentence1 = "I want to visit towers in Vietnam"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "towers in Vietnam")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern16(self):
        sentence1 = "very nice beaches in Southeast Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "very nice beaches in Southeast Asia")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['ADV', 'ADJ', 'NOUN', 'ADP', 'PROPN', 'PROPN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_tag_regex_matches_pattern16(self):
        sentence1 = "I visited very nice beaches in Southeast Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "very nice beaches in Southeast Asia")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['ADV', 'ADJ', 'NOUN', 'ADP', 'PROPN', 'PROPN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_summarized_pattern17(self):
        sentence1 = "bar pub club shop in Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "bar pub club shop in Asia")

        POS = [token.pos_ for token in match]
        EXPECTED_POS = ['NOUN', 'NOUN', 'NOUN', 'NOUN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPECTED_POS)


    def test_summarized_pattern18(self):
        sentence1 = "Paris"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "Paris")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern18(self):
        sentence1 = "I like Paris"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "Paris")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern18(self):
        sentence1 = "Eiffel Tower"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "Eiffel Tower")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern18(self):
        sentence1 = "I will visit Eiffel Tower"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "Eiffel Tower")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern19(self):
        sentence1 = "Tokyo in January"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "Tokyo in January")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern19(self):
        sentence1 = "I will visit Tokyo in January"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "Tokyo in January")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern20(self):
        sentence1 = "France in July"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "France in July")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern20(self):
        sentence1 = "I will visit France in July"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

        self.assertEqual(match.text, "France in July")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['PROPN', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern21(self):
        sentence1 = "swimming in Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)

#        self.print_token_labels(spacy_doc)

        self.assertEqual(match.text, "swimming in Asia")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['VERB', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern21(self):
        sentence1 = "I enjoyed swimming in Asia"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "swimming in Asia")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['VERB', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern22(self):
        sentence1 = "walking in Paris"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "walking in Paris")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['VERB', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern22(self):
        sentence1 = "I enjoy walking in Paris"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "walking in Paris")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['VERB', 'ADP', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_summarized_pattern23(self):
        sentence1 = "mountains and beaches in Da Nang"
        spacy_doc = TestPrintToken.english_nlp(sentence1)
        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "mountains and beaches in Da Nang")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'CCONJ', 'NOUN', 'ADP', 'PROPN', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)


    def test_tag_regex_matches_pattern23(self):
        sentence1 = "I would like to visit mountains and beaches in Da Nang"
        spacy_doc = TestPrintToken.english_nlp(sentence1)

#        self.print_token_labels(spacy_doc)

        match = summarize_doc(spacy_doc)
        self.assertEqual(match.text, "mountains and beaches in Da Nang")

        POS = [token.pos_ for token in match]
        EXPTECTED_POS = ['NOUN', 'CCONJ', 'NOUN', 'ADP', 'PROPN', 'PROPN']
        self.assertEqual(POS, EXPTECTED_POS)
