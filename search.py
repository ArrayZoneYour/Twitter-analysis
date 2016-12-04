# -*- coding: utf-8 -*
# author: ArrayZoneYour

from numpy import *
from Kmeans import distEclud


def search(dict1, histroy, user_):
    minDist = inf
    user_find = 0
    # index = 0
    for user in histroy:
        if user == user_:
            continue
        i = 11
        while 80 > i > 10:
            dist = distEclud(array(dict1), array(histroy[user][i:i+10]))
            if dist < minDist:
                minDist = dist
                user_find = user
                # index = i
                order = histroy[user][i:i+10]
                predict = histroy[user][i-11:i-1]
            i += 1
    return minDist, user_find, order, predict
