import warnings

import gliner_play
import stanza_play
from termcolor import colored

warnings.filterwarnings(
    'ignore',
    message='.*pynvml package is deprecated.*',
)
warnings.filterwarnings(
    'ignore',
    message='Checkpoint uses legacy list-valued extra_special_tokens metadata.*',
    category=UserWarning,
)

warnings.filterwarnings('ignore', category=UserWarning)

#######################

# Orig test sentences
# sentences = [
#     'John was needing to meet her at home on Saturday at 14:30 every week',
#     'Będę mógł chcieć planować, żebyś spała',
#     'wiem to, że wiesz',
#     'da psu nożem jabłko',
# ]

sentences = [
    'bring me coffee',

    'en obdurate - zatwardziały',
    '''
    en:
    - scaffolding - rusztowanie
    - scaffold - szafot/rusztowanie/szubienica
    '''.strip(),
]

module_files = {
    # 'stanza': stanza_play,
    'gliner2': gliner_play,
}

analizers = {name: module.analizer for name, module in module_files.items()}

SENTENCE = colored('SENTENCE', 'yellow')
print()
for sentence in sentences:
    print(f'\n{SENTENCE}: {colored(sentence, 'blue')}')
    for name, analizer in analizers.items():
        print(f'--- {name} -------')
        result, output = analizer(sentence)
        print(output)
