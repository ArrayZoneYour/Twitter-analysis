# -*- coding: utf-8 -*
# author: ArrayZoneYour

from collections import OrderedDict

punctuation = list(set('''
, .... ... .. . ? !!! !! ! ?! " ' ?? ???
'''.split()))
# print(punctuation)


def my_split(s, ds):
    res = [s]
    for d in ds:
        t = []
        list(map(lambda x: t.extend(x.split(d)), res))
        res = t
    return [x for x in res if x]


def record_punctuation(list_, record):
    i = 0
    # record = [0] * len(punctuation)
    while i < len(list_):
        for p in punctuation:
            if list_[i].endswith(p):
                list_[i] = list_[i].rstrip(p)
                record[p] += 1
        i += 1
    return [x for x in list_ if x], record

# print((mySplit('a,b||||m,c', ',|')))
# user = {}
# d = OrderedDict({'....': 0, '!!': 0, '..': 0, '.': 0, '?': 0, "'": 0,
#                  '!!!': 0, '!': 0, ',': 0, '...': 0, '"': 0, '?!': 0})
# tryin, d = record_punctuation(['who', 'am', 'I?'], d)
# user['5620'] = d
# print(user)