import warnings
import hanlp_play
import stanza_play
import hugging_face_transformer

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

sentences = [
    'John was needing to meet her at home on Saturday at 14:30 every week',
    'Będę mógł chcieć planować, żebyś spała',
    'wiem to, że wiesz',
    'da psu nożem jabłko',
]

module_files = {
    'hanlp': hanlp_play,
    'stanza': stanza_play,
    'gliner2': gliner,
}

analizers = {name: module.analizer for name, module in module_files.items()}

print()
for sentence in sentences:
    print(f'\nSENTENCE: {sentence}')
    for name, analizer in analizers.items():
        print(f'--- {name} -------')
        result, output = analizer(sentence)
        print(output)
