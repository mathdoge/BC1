import json

p = r'd:\BC1\模块B_智能制造与工业质检.ipynb'
d = json.load(open(p, encoding='utf-8'))
patched = False
for c in d['cells']:
    if c['cell_type'] == 'code' and c['source'] and c['source'][0].startswith('# ===== B2'):
        src = ''.join(c['source'])
        old = ("# 4. 按图像名划分训练/验证集(8:2)\n"
               "imgs = df['filename'].unique()\n"
               "tr, va = train_test_split(imgs, test_size=0.2, random_state=42)")
        new = ("# 4. 按图像名划分训练/验证集(8:2, 按类别分层抽样,保证每类都有验证样本)\n"
               "img_cls = df.drop_duplicates('filename').set_index('filename')['class']\n"
               "imgs = img_cls.index.to_numpy()\n"
               "tr, va = train_test_split(imgs, test_size=0.2, random_state=42,\n"
               "                          stratify=img_cls.values)")
        if old in src:
            src = src.replace(old, new)
            c['source'] = src.splitlines(keepends=True)
            patched = True
            print('B2 patched')
        elif 'stratify' in src:
            patched = True
            print('already patched')
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved, patched =', patched)
