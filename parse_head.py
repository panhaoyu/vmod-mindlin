import re
from pprint import pprint
import numpy as np

FILE = r'C:\Users\wolf\Documents\Visual MODFLOW Flex\Projects\expand\expand.data\MODFLOW\NumericalGrid_refined_2_refined_refined\Run6\MODFLOW-2005\Wall depth.LST'


def get_heads(file=FILE):
    with open(file, mode='r', encoding='utf-8') as f:
        content = f.read()
    content = content.split('              HEAD IN LAYER   1 AT END OF TIME STEP   1 IN STRESS PERIOD    1')[1]
    content = content.split('              HEAD IN LAYER   2 AT END OF TIME STEP   1 IN STRESS PERIOD    1')[0]
    content = content.split(
        '............................................................'
        '............................................................')[1]
    content = ' '.join(content.splitlines())
    content = re.sub(' +', ' ', content)
    content = re.sub(' \d{1,2} ', ' ', content)
    heads = list(map(float, content.split()[:-1]))
    return np.asarray(heads, dtype=np.float_).reshape((44, 44))
