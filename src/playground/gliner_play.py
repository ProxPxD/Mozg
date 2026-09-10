import os

import torch

from playground.anal_lib import Analizer
from playground.paths import RESOURCES

hugging_face_resources = RESOURCES / 'hugging_face'
hugging_face_resources.mkdir(exist_ok=True)
os.environ['HF_HUB_CACHE'] = str(hugging_face_resources)
os.environ['TRANSFORMERS_OFFLINE'] = '0'

import json

from gliner2 import AutoExtractor

settings = dict(
    map_location=str(torch.accelerator.current_accelerator()),
)
extractor = AutoExtractor.from_pretrained('fastino/gliner2.5-base-v1', **settings)
# extractor = AutoExtractor.from_pretrained('fastino/gliner2.5-multi-v1'. **settings)


schema = (extractor.create_schema()
    .entities({
        'person': 'names of people mentioned',
        'time': 'time, dates, years, hours',
        'date': 'date, years, months, days',
        'day-time': 'time in a day, hours, minutes, seconds, time of the day',
        'freq': 'frequency',
    })
    # .structure('appointment')
    #     .field('patient', dtype='str')
    #     .field('doctor', dtype='str')
    #     .field('date')
    #     .field('time')
    #     .field('type', dtype='str', choices=['checkup', 'followup', 'consultation'])
)

analizer = Analizer(
    extractor,
    run=lambda text: extractor.extract(text, schema, include_confidence=True),
    format_output=lambda results: json.dumps(results, indent=4),
)

