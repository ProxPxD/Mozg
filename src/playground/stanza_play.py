import logging
from io import StringIO
from typing import TextIO

from playground.anal_lib import Analizer
from playground.paths import RESOURCES

resources_path = RESOURCES / 'stanza'
resources_path.mkdir(exist_ok=True)

import pydash as _
import stanza
from pydash import chain as c
from pydash import flow
from stanza.models.common.doc import END_CHAR, LEMMA, START_CHAR, TEXT, Document, Word

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
            processors='tokenize,mwt,pos,lemma',
            use_gpu=True,
            **settings,
        )
        for lang in langs
    },
)

def print_sentences(doc: Document, *, write_to: TextIO | None = None) -> None:
    print(f'{doc.lang}', file=write_to)
    for sent in doc.sentences:
        print(f'{" " * 2}{sent.index}) {sent.text}', file=write_to)
        for ent in sent.ents:
            print(f'{" " * 4}{ent.text}: {ent.type}', file=write_to)

def print_doc(doc: Document, maxes: dict[str, int], *, write_to: TextIO | None = None) -> None:
    print(f'{doc.lang}', file=write_to)
    for sent in doc.sentences:
        if len(doc.sentences) > 1:
            print(f'{" " * 2}{sent.index}) {sent.text}', file=write_to)
        for word in sent.words:
            if word.upos == 'PUNCT':
                continue
            word_dict = word.to_dict()
            print(' ' * 4, end='', file=write_to)
            print(
                *[f'{field}: {word_dict.get(field, "-"):<{maxi}}' for field, maxi in maxes.items()],
                sep=' ' * 2,
                file=write_to,
            )

def format_output(doc: Document) -> str:
    words: list[Word] = list(doc.iter_words())
    excluded_fields = {START_CHAR, END_CHAR}  #, LEMMA, FEATS}
    # fields = [field for field in words[0].to_dict() if field not in excluded_fields]
    fields = [TEXT, LEMMA]
    maxes = {field: max(_.map_(words, flow(c().get(field), str, len))) for field in fields}
    output = StringIO()
    # print_sentences(doc, write_to=output)
    print_doc(doc, maxes, write_to=output)
    return output.getvalue()


analizer = Analizer(
    nlp,
    run=lambda text: nlp(Document([], text=text)),
    format_output=format_output,
)

