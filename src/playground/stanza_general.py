import logging

import pydash as _
import stanza
from pydash import chain as c
from pydash import flow
from stanza.models.common.doc import END_CHAR, START_CHAR, Document, Sentence, Word
from toolz import pipe

LOGGING_LEVEL = logging.getLevelName(logging.WARNING)

stanza.download(lang='en', logging_level=LOGGING_LEVEL)
stanza.download(lang='pl', logging_level=LOGGING_LEVEL)

nlp = stanza.Pipeline(
    lang='en',
    processors='tokenize,mwt,pos,lemma,depparse,ner',
    logging_level=LOGGING_LEVEL,
    use_gpu=True,
)
doc: Document = nlp('John was needing to meet her at home. He needs it')

words: list[Word] = list(doc.iter_words())

excluded_fields = {START_CHAR, END_CHAR}
fields = [field for field in words[0].to_dict() if field not in excluded_fields]
maxes = {field: max(_.map_(words, flow(c().get(field), str, len))) for field in fields}

for sent in doc.sentences:
    print(f'{sent.id}:')
    for ent in sent.ents:
        print(f'{ent.text}: {ent.type}')

for word in words:
    word_dict = word.to_dict()
    print(  # noqa: T201
        *[
            f'{field}: {word_dict.get(field, '-') :<{maxi}}' for field, maxi in maxes.items()
        ],
        sep=' ' * 4,
    )


# print(
#     f'id: {word.id}',
#     f'word: {word.text:<{15}}',
#     f'upos: {word.upos:<5}',
#     f'xpos: {word.xpos:<5}',
#     f'feats: {word.feats or '_'}',
#     f'lemma: {word.lemma}',
#     sep=' '*4,
# )
