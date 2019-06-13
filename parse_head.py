import re
from pprint import pprint
import numpy as np

FILE = r'C:\Users\wolf\Documents\Visual MODFLOW Flex\Projects\expand\expand.data\MODFLOW\NumericalGrid_refined_2_refined_refined\Run6\MODFLOW-2005\Wall depth.LST'

with open(FILE, mode='r', encoding='utf-8') as file:
    content = file.read()
content = content.split('              HEAD IN LAYER   1 AT END OF TIME STEP   1 IN STRESS PERIOD    1')[1]
content = content.split('              HEAD IN LAYER   2 AT END OF TIME STEP   1 IN STRESS PERIOD    1')[0]
content = content.split(
    '............................................................'
    '............................................................')[1]
content = ' '.join(content.splitlines())
content = re.sub(' +', ' ', content)
content = re.sub(' \d{1,2} ', ' ', content)
heads = list(map(float, content.split()[:-1]))

heads = np.asarray(heads, dtype=np.float_)
heads = heads.reshape((44, 44))

pprint(heads)
pprint(len(heads))

print(heads[0, 0])
