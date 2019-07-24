from spacy.symbols import NOUN, PROPN, PRON, NUM, AUX, ADJ, ADV, ADP, PUNCT, VERB, NAMES, CONJ, IDS, SYM, CCONJ, SCONJ,X
import re
CONJUNTION_TOKENS = ["と", "や"]

ADP_POS = ["CONJ", "CCONJ", "ADP"]
ADP_POS_IDS = [CONJ, CCONJ, ADP]
MEANING_POS = ["NOUN", "PROPN", "NUM", "ADJ", "ADV", "VERB", "CONJ", "CCONJ", "PUNCT", "X"]
MEANING_POS_IDS = [NOUN, PROPN, NUM, ADJ, ADV, VERB, PUNCT , CONJ, CCONJ, SCONJ, PUNCT, X]
KEEP_POS_IDS = [NOUN, PROPN, NUM, ADJ, ADV, VERB, X]
KEEP_POS = ["NOUN", "PROPN", "NUM", "ADJ", "ADV", "VERB", "X"]
FILTER_TOKEN_POS = ["AUX", "SCONJ"]
CONNECT_SYMBOLS_POS = [PUNCT, SYM]


EXCEPT_POS_OF_POS = {
    ADJ: [NOUN, NUM],
    ADV: [ADJ, NUM, NOUN],
    NUM: [NOUN],
    PRON: [NOUN],
    NOUN: []
}



CONNECT_SYMBOLS_PATTERN = "(-|・|&|\'|=|.)"
CONNECT_SYMBOLS = CONNECT_SYMBOLS_PATTERN[1:-1].split("|")

VERB_PHRASE_PATTERN = '((( (NOUN|ADJ))( (AUX))?)*( (VERB))+( (AUX))*)'
NOUN_PHRASE_PATTERN = '(( (DET))?( (ADV))*(( (NOUN|ADJ))( (AUX))?)*( (NOUN|PROPN|NUM|X))+(( {})?( (NOUN|PROPN|NUM|X)))*)'\
    .format(CONNECT_SYMBOLS_PATTERN)
CHUNKS_PATTERN = '({}+|{}|( (PUNCT))+|( (SYM))+|( (PRON))+|( (ADP|SCONJ|CONJ|CCONJ))+|(( (ADV))*(( (NOUN|ADJ))( (AUX))?))+)'\
                        .format(VERB_PHRASE_PATTERN,NOUN_PHRASE_PATTERN)

COMPILED_CHUNKS_PATTERN = re.compile(CHUNKS_PATTERN)

# coding: utf8
STOP_WORDS = set("""
あそこ
あっ
あの
あのかた
あの人
あり
あります
ある
あれ
あり
い
いう
います
いる
言わ
う
うち
え
お
および
おり
おります
か
かつて
から
が
き
ここ
こちら
こと
この
これ
これら
さ
さらに
し
しかし
する
ず
せ
せる
そこ
そして
その
その他
その後
それ
それぞれ
それで
そうです
た
ただし
たち
ため
たり
だ
だっ
だれ
つ
て
で
でき
できる
です
では
でも
と
という
といった
とき
ところ
として
とともに
とも
と共に
どこ
どの
な
なお
なかっ
ながら
なく
なっ
など
なに
なら
なり
なる
なん
に
において
における
について
にて
によって
により
による
に対して
に対する
に関する
の
ので
のみ
のだ
は
ば
へ
ほか
ほとんど
ほど
ます
また
または
まで
も
もの
ものの
や
よ
よう
より
ら
られ
られる
れ
れる
れて
を
何
及び  
彼
彼女
我々
特に
私
私達
貴方
貴方方
今回
のです
いただく
ください
いかが
とにかく
かも
ね
""".split())

REMOVE_VERB = set("""
下さる
楽しむ
予定
訪問
参加
好き
探す
訪れる
見付ける
見る
試す
言う
居る
分る
解る
来る
行く
思う
在る
""".split())

REMOVE_ADJ = set("""
好き
""".split())

