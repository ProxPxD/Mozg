import os
from pathlib import Path

resources_path = Path(__file__).parent.parent.parent / 'resources' / 'hanlp'

os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HANLP_HOME'] = str(resources_path)


import hanlp  # noqa: E402
import hanlp.pretrained  # noqa: E402

nlp = hanlp.load(
    hanlp.pretrained.mtl.UD_ONTONOTES_TOK_POS_LEM_FEA_NER_SRL_DEP_SDP_CON_XLMR_BASE,
)

result = nlp('John gave Mary a book.')

result.pretty_print()
