import os

from playground.paths import RESOURCES

resources_path = RESOURCES / 'hanlp'

os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HANLP_HOME'] = str(resources_path)


import hanlp  # noqa: E402
import hanlp.pretrained  # noqa: E402

nlp = hanlp.load(
    hanlp.pretrained.mtl.UD_ONTONOTES_TOK_POS_LEM_FEA_NER_SRL_DEP_SDP_CON_XLMR_BASE,
)

sentences = [
    'John was needing to meet her at home',
    'Będę mógł chcieć planować, żebyś spała',
]
for sentence in sentences:
    result = nlp(sentence)
    result.pretty_print()
