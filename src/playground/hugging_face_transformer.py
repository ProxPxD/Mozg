import os

import torch

from playground.paths import RESOURCES

hugging_face_resources = RESOURCES / 'hugging_face'
hugging_face_resources.mkdir(exist_ok=True)
os.environ['HF_HUB_CACHE'] = str(hugging_face_resources)

import json

from gliner2 import AutoExtractor

settings = dict(
    map_location=str(torch.accelerator.current_accelerator()),
)
extractor = AutoExtractor.from_pretrained('fastino/gliner2.5-base-v1', **settings)
# extractor = AutoExtractor.from_pretrained('fastino/gliner2.5-multi-v1'. **settings)

# text = '''
# Siemens opened a new AI research centre in Berlin.
# The facility will develop machine learning systems for
# industrial applications. While Maersk opened a research centre in Kopenhagen.
# '''

# schema = (
#     extractor.create_schema()
#     .entities({
#         'organization': 'An organization, company, institution, or other group',
#         'location': 'A geographical location',
#         'technology': 'A technology, technical field, or computational method',
#         'research': 'A research activity or research topic',
#     })
#     .relations({
#         'located_in': 'An organization or facility is physically located in a place',
#         'researches': 'An organization or facility conducts research into a topic',
#     })
# )

# result = model.extract(text, schema)

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

text = '''
John is going to visit me on Saturday at 14:30 every week
'''
results = extractor.extract(text, schema, include_confidence=True)

print(results)
print(json.dumps(results, indent=4))
