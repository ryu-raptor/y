# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader
import csv
import sys
import random
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('csv_file', nargs='?', help='csv file to fetch y data. omit then read from stdin.')
parser.add_argument('variation_file')
parser.add_argument('-t', '--template', help='jinja2 html template file for y')
parser.add_argument('-v', '--variation_config', help='select variation sequence rather random select')
parser.add_argument('-S', '--suffix', help='append suffix to output files for multipage ys.')
parser.add_argument('-c', '--css_variant', help='select css file instead of y.css')

parser.add_argument('-V', '--variation_index', help='select variation index rather random select', type=int)
parser.add_argument('-i', '--variation_indices', help='select variation indices from csv file rather random select')
parser.add_argument('-s', '--variation_sequence', help='csv file for variaiton sequence')
parser.add_argument('-l', '--limit', help='limits messages per page and do auto split page')

args = parser.parse_args()
print(args.template)
print(args.variation_index)
print(args.variation_sequence)

# classes
class Sequencer:
    def get_next(self):
        pass

class RandomSequencer(Sequencer):
    def __init__(self, f, t):
        self.f = f
        self.t = t

    def get_next(self):
        return random.randint(self.f, self.t)

class ListSequencer(Sequencer):
    def __init__(self, l):
        self.seq = l
        self.c = 0
        self.len = len(self.seq)

    def get_next(self):
        i = self.c
        self.c += 1
        return self.seq[i % self.len]

# リストをすべてシーケンサーに変換
def convert_json2sequencer(j):
    # 戻り値用
    r = {}
    for k, v in j.items():
        t = None
        if type(v) is list:
            t = ListSequencer(v)
        else:
            t = v
        r[k] = t
    return r

class CSVSequencer(Sequencer):
    def __init__(self, f):
        self.seq = list(map(lambda s: int(s), next(csv.reader(f))))
        self.c = 0
        self.len = len(self.seq)

    def get_next(self):
        i = self.c
        self.c += 1
        return self.seq[i % self.len]

csv_file = args.csv_file
limit = args.limit
css_variant = args.css_variant
file_suffix = args.suffix if args.suffix else ''
v_indices_file = args.variation_indices
v_sequence_file = args.variation_sequence

env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))

template_path = 'index.html.jinja' if not args.template else args.template

template = env.get_template(template_path)

# シーケンスファイル
v_sequence = None
if args.variation_config:
    with open(args.variation_config, 'r') as f:
        v_config = json.loads(f.read())
    v_sequence = convert_json2sequencer(v_config)

# === READING CSV ===
# file or stdin?
if csv_file:
    f = open(csv_file, 'r', encoding='utf-8')
else:
    f = sys.stdin

data = csv.reader(f)

targets = next(data)
# 位置合わせの空白を消す
targets.pop(0)
print(targets)

whole_messages = []

# 各個人のメッセージ
for individual in data:
    pack = {}
    pack['from'] = individual.pop(0)
    pack['messages'] = {}
    for t in targets:
        pack['messages'][t] = individual.pop(0)
    whole_messages.append(pack)

# closing file
if csv_file:
    f.close()
# === END READING CSV ===

# バリエーションファイル
with open(args.variation_file, 'r') as f:
    data = csv.reader(f)
    #variation = {}
    #variation['frames'] = next(data)
    variations = []
    for row in data:
        v = {}
        v['center'] = row.pop(0)
        v['frame'] = []
        for f in row:
            if f == '':
                break
            v['frame'].append(f)
        variations.append(v)

vi_seq = None
if v_indices_file:
    with open(v_indices_file, 'r') as f:
        vi_seq = CSVSequencer(f)
else:
    vi_seq = RandomSequencer(0, len(variations) - 1)

# 生成
for target in targets:
    # variaitonを引く
    page = v_sequence['page'].get_next()
    vi = page['variation']
    # center vary
    vary = {}
    vary['center'] = './' + variations[vi]['center'] + '.png'

    # フレームバリエーションシーケンサ
    vf_seq = ListSequencer(page['sequence'])

    # 一時的にmessageフィールドを追加する
    for w in whole_messages:
        w['message'] = w['messages'][target]
        # バリエーションフィールドを追加
        w['variation'] = {}
        w['variation']['frame'] = './' + variations[vi]['frame'][vf_seq.get_next()] + '.png'

    html = template.render({'messages': whole_messages, 'target': target, 'variation': vary, 'css_file_name': css_variant})

    print(target)
    with open(target + file_suffix + '.html', 'w') as f:
        f.write(str(html))
