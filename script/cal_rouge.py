import numpy
from nlp import load_metric
from pytorch_transformers import BertTokenizer
tok = BertTokenizer.from_pretrained('bert-base-cased')
r_metric = load_metric('rouge')

import sys

print(str(sys.argv))

best_ckpt = '_best'
DATASET = sys.argv[1]
VERSION = sys.argv[2]
MODEL = sys.argv[3]

print('ref dir: ', '/home/yegong/losin/glge/data/%s/%s_data/org_data/test.tgt' % (VERSION, DATASET))
with open('/home/yegong/losin/glge/data/%s/%s_data/org_data/test.tgt' % (VERSION, DATASET), encoding='utf-8') as fin:
    references = [' '.join(tok.tokenize(line.strip().lower())).replace(' ##','').replace('<X_SEP>','') for line in fin.readlines()]

try:
    with open('/home/yegong/losin/glge/outputs/%s/%s/%s_%s/score_ck%s_pelt1.0_test_beam4.txt' % (VERSION, MODEL, DATASET, MODEL, best_ckpt) ,encoding='utf-8') as fin:
        predictions = [line.strip().lower().replace('<X_SEP>','') for line in fin.readlines()]
    print('pred dir: ', '/home/yegong/losin/glge/outputs/%s/%s/%s_%s/score_ck%s_pelt1.0_test_beam4.txt' % (VERSION, MODEL, DATASET, MODEL, best_ckpt))
except FileNotFoundError:
    with open('/home/yegong/losin/glge/outputs/%s/%s/%s_%s/score_ck%s_pelt1.2_test_beam5.txt' % (VERSION, MODEL, DATASET, MODEL, best_ckpt) ,encoding='utf-8') as fin:
         predictions = [line.strip().lower().replace('<X_SEP>','') for line in fin.readlines()]
    print('pred dir: ', '/home/yegong/losin/glge/outputs/%s/%s/%s_%s/score_ck%s_pelt1.2_test_beam5.txt' % (VERSION, MODEL, DATASET, MODEL, best_ckpt))

res = r_metric.compute(predictions, references, rouge_types=['rouge1', 'rouge2', 'rougeL'], use_agregator=True)

print('%.2f/%.2f/%.2f'% (res['rouge1'].mid.fmeasure * 100., res['rouge2'].mid.fmeasure  * 100., res['rougeL'].mid.fmeasure  * 100.))