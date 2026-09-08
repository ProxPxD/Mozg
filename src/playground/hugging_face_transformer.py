import json
import os

from playground.paths import RESOURCES

hugging_face_resources = RESOURCES / 'hugging_face'
hugging_face_resources.mkdir(exist_ok=True)
os.environ['HF_HUB_CACHE'] = str(hugging_face_resources)


from transformers import pipeline  # noqa: E402

generator = pipeline(
    'text-generation',
    model='Qwen/Qwen2.5-1.5B-Instruct',
    device_map='auto',
)

result = generator('''
Text:
Siemens opened a new AI research centre in Berlin.

Task:
Generate semantic tags describing the important concepts,
entities and relations in this text.
Return JSON.
''')

print(result[0]['generated_text'])
