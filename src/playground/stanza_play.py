import logging
from pathlib import Path

import pydash as _
import stanza
from pydash import chain as c
from pydash import flow
from stanza.models.common.doc import END_CHAR, FEATS, LEMMA, START_CHAR, Document, Sentence, Word
from toolz import pipe

from playground.paths import RESOURCES

resources_path = RESOURCES / 'stanza'
resources_path.mkdir(exist_ok=True)
settings = dict(
    model_dir=str(resources_path),
    # logging_level=logging.getLevelName(logging.WARNING),
)

logging.getLogger(stanza.__name__).setLevel(logging.WARNING)


langs = ['en', 'pl']
stanza.download(lang='multilingual', **settings)
for lang in langs:
    stanza.download(lang=lang, **settings)

nlp = stanza.MultilingualPipeline(
    download_method=None,
    lang_id_config=dict(
        langid_lang_subset=langs,
    ),
    lang_configs={
        lang: dict(
            processors='tokenize,mwt,pos,lemma,depparse,ner',
            use_gpu=True,
            **settings,
        )
        for lang in langs
    },
)

raw_docs = [
    '. '.join([
        'John was needing to meet her at home',
        'I know it',
    ]),
    '. '.join([
        # 'Herbatę zrób',
        'Będę mógł chcieć planować, żebyś spała',
        'wiem to, że wiesz',
        'da psu nożem jabłko',
    ]),
]
docs: list[Document] = [Document([], text=raw_doc) for raw_doc in raw_docs]
docs = nlp(docs)

words: list[Word] = [word for doc in docs for word in doc.iter_words()]

excluded_fields = {START_CHAR, END_CHAR, LEMMA, FEATS}
fields = [field for field in words[0].to_dict() if field not in excluded_fields]
maxes = {field: max(_.map_(words, flow(c().get(field), str, len))) for field in fields}

for i, doc in enumerate(docs):
    print(f'{i+1}) {doc.lang}')
    for sent in doc.sentences:
        print(f'{' '*2}{sent.index}) {sent.text}')
        for ent in sent.ents:
            print(f'{' '*4}{ent.text}: {ent.type}')

for doc in docs:
    print(f'{i+1}) {doc.lang}')
    for sent in doc.sentences:
        print(f'{' '*2}{sent.index}) {sent.text}')
        for word in sent.words:
            if word.upos == 'PUNCT':
                continue
            word_dict = word.to_dict()
            print(' '*4, end='')
            print(  # noqa: T201
                *[f'{field}: {word_dict.get(field, "-"):<{maxi}}' for field, maxi in maxes.items()],
                sep=' ' * 2,
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
