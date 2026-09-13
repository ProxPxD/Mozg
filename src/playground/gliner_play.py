import json
import os
from typing import Any, Callable

from pydash import flow, partial
import torch
from toolz.dicttoolz import valfilter, valmap

from playground.anal_lib import Analizer
from playground.paths import RESOURCES

hugging_face_resources = RESOURCES / 'hugging_face'
hugging_face_resources.mkdir(exist_ok=True)
os.environ['HF_HUB_CACHE'] = str(hugging_face_resources)
os.environ['TRANSFORMERS_OFFLINE'] = '0'


from gliner2 import AutoExtractor

settings = dict(
    map_location=str(torch.accelerator.current_accelerator()),
)
extractor = AutoExtractor.from_pretrained('fastino/gliner2.5-base-v1', **settings)
# extractor = AutoExtractor.from_pretrained('fastino/gliner2.5-multi-v1'. **settings)


schema = (extractor.create_schema()
    .entities({
        'iso-language-code': (ISO_CODES:='ISO codes: pl, en, de, es'),
    })
    .structure('translation')
        .field('from', 'str', None, ISO_CODES)
        .field('to', 'str', None, ISO_CODES)
    .structure('action')
        .field('verb', 'str', None, 'main verb')
        .field('object', 'str', None, 'linguistical object')
        .field('modality', 'str', None, 'modality')
    #     .field('patient', dtype='str')
    #     .field('doctor', dtype='str')
    #     .field('date')
    #     .field('time')
    #     .field('type', dtype='str', choices=['checkup', 'followup', 'consultation'])
)


def filter_result(result: dict) -> dict:
    result['entities'] = valfilter(bool, result.get('entities', {}))
    return result


def format_single_entity_list(entities: list[str | dict[str, str|int]]) -> list[str]:
    match entities:
        case []: return entities  # pyright: ignore[reportReturnType]
        case [str(), *_]: return entities  # pyright: ignore[reportReturnType]
        case [dict(), *_]: return [f'{ent['text']} [{ent['confidence']:.2f}]' for ent in entities]
    raise ValueError(f'Unexpected path for: {entities}')

def format_entities(result: dict) -> dict:
    result['entities'] = valmap(format_single_entity_list, result['entities'])
    return result

format_output: Callable[[dict], str] = flow(
    filter_result,
    format_entities,
    partial(json.dumps, indent=4, ensure_ascii=False),
)

def run(text: str) -> Any:
    return extractor.extract(
        text,
        schema,
        include_confidence=True,
        # threshold=.9,
    )

analizer = Analizer(
    extractor,
    run=run,
    format_output=format_output,
)

