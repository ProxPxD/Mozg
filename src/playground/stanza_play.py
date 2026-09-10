from io import StringIO
import logging

from playground.anal_lib import Analizer
from playground.paths import RESOURCES

resources_path = RESOURCES / 'stanza'
resources_path.mkdir(exist_ok=True)

import pydash as _
import stanza
from pydash import chain as c
from pydash import flow
from stanza.models.common.doc import END_CHAR, FEATS, LEMMA, START_CHAR, Document, Word

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


def format_output(doc: Document) -> str:
    words: list[Word] = [word for word in doc.iter_words()]
    excluded_fields = {START_CHAR, END_CHAR}  #, LEMMA, FEATS}
    fields = [field for field in words[0].to_dict() if field not in excluded_fields]
    maxes = {field: max(_.map_(words, flow(c().get(field), str, len))) for field in fields}
    output = StringIO()
    print(f'{doc.lang}', file=output)
    for sent in doc.sentences:
        print(f'{" " * 2}{sent.index}) {sent.text}', file=output)
        for ent in sent.ents:
            print(f'{" " * 4}{ent.text}: {ent.type}', file=output)

    print(f'{doc.lang}', file=output)
    for sent in doc.sentences:
        print(f'{" " * 2}{sent.index}) {sent.text}', file=output)
        for word in sent.words:
            if word.upos == 'PUNCT':
                continue
            word_dict = word.to_dict()
            print(' ' * 4, end='', file=output)
            print(
                *[f'{field}: {word_dict.get(field, "-"):<{maxi}}' for field, maxi in maxes.items()],
                sep=' ' * 2,
                file=output,
            )
    return output.getvalue()


analizer = Analizer(
    nlp,
    run=lambda text: nlp(Document([], text=text)),
    format_output=format_output,
)
