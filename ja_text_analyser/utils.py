from spacy.symbols import NOUN, PROPN, PRON, NUM, AUX, ADJ, ADV, ADP, PUNCT, VERB, NAMES, CONJ, IDS, SYM, CCONJ, SCONJ


MEANING_POS = ["NOUN", "PROPN", "NUM", "ADJ", "ADV", "VERB", "CONJ", "CCONJ", "PUNCT"]
MEANING_POS_IDS = [NOUN, PROPN, NUM, ADJ, ADV, VERB, CONJ, CCONJ, PUNCT, SCONJ]

CONNECT_SYMBOLS_PATTERN = "<-|・|&|\'|=|.>"
CONNECT_SYMBOLS = CONNECT_SYMBOLS_PATTERN[1:-1].split("|")
VERB_CHUNK_PATTERN = '((<NOUN|ADJ><AUX>?)*<VERB>+<AUX>*)'
CHUNKS_PATTERN = '({}+|(<DET>?<ADV>*(<NOUN|ADJ><AUX>?)*<NOUN|PROPN|NUM|X>+({}?<NOUN|PROPN|NUM|X>)*)|<PUNCT>+|<SYM>+|<PRON>+|<ADP|CONJ|CCONJ>+|(<ADV>*(<NOUN|ADJ><AUX>?))+)'\
                            .format(VERB_CHUNK_PATTERN, CONNECT_SYMBOLS_PATTERN)
CONNECT_SYMBOLS_POS = [PUNCT, SYM]
DATE_LABEL = "DATE"
OBJECT_LABELS = ["ORG", "LOC", "PERSON", "PRODUCT", "GPE"]
EXCEPT_POS_OF_POS = {
    ADJ: [NOUN, NUM],
    ADV: [ADJ, NUM, NOUN],
    NUM: [NOUN],
    PRON: [NOUN],
    NOUN: []
}
EXCEPT_CHUNKS = ["DATE", "CCONJ"]
CONJUNTION_TOKENS = ["と", "や"]
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

REMOVE_SET = set()
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

