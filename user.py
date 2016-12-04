# -*- coding: utf-8 -*
# author: ArrayZoneYour
# reading the data from user_location.txt and user_tweets.txt
# 待解决问题：重复的Twitter

import xlwt
import re
import math
from XLSHelper import XLSHelper
from collections import Counter
from collections import OrderedDict
import time
import calendar
import Helper
import Kmeans
import matplotlib.pyplot as plt
import gray
import search

user_number = []
day = []


def import_txt(filename, choose='w+', encoding='utf-8'):
    f = open(filename, choose, encoding=encoding)
    return f


# test part
data = import_txt('user_location.txt', 'r')
# 用户活跃数据
users = {}
# 用户Twitter集
users_twitters = {}
# 用户Twitter高频词
users_words_frequent = {}
user_words = {}
# 用户标点使用情况统计
user_punctuation = {}
for user in data:
    user = re.sub(r'[\n UT:]', "", string=user)
    user = re.split('\t|,|', user)
    index = user[0]
    users[index] = user
    user_number.append(index)
    users_twitters[index] = []
    user_words[index] = []
# print(len(users))
# print(len(users[0]))
NUMBER, LONGITUDE, LATITUDE, SUM_TWITTER, SUM_DAY, USE_DAY, BEGIN_DAY, END_DAY, ONE_AM, THREE_AM \
    , FIVE_AM \
    , SEVEN_AM, NINE_AM, ELVEN_AM, ONE_PM, THREE_PM, FIVE_PM, SEVEN_PM, NINE_PM, ELVEN_PM, WEEKDAY \
    , WEEKEND, FREQUENCY \
    , SLEEP_DAY, SOCIAL_POT, LIFE_POT, AMUSEMENT_POT, EDU_POT, SPORTS_POT, READ_POT, WORK_POT \
    , FOOD_POT, RT_TIME, AT_TIME, EXCLAMATION_TIME, QUESTION_MARK, TEN_DAY_PREDICT = range(37)
# print(users[0][NUMBER])
t = (2010, 3, 17, 23, 59, 59, 0, 0, 0)
END_TIME = time.mktime(t)
# 整体活跃指数
frequent_pot = 0
# 整体流失指数
away_pot = 0
# 推文指数
twitter_pot = 0
# 留存指数
alive_pot = 0

data = import_txt('user_tweets.txt', 'r')
twitters = {}
index = 0
leave = 0
history_long = {}
for twitter in data:
    twitter = twitter.replace('\n', ' ')
    twitter = twitter.lower()
    twitter = Helper.my_split(twitter, '\t')
    # twitter.split('\t')
    twitters[index] = twitter
    # print(twitter)
    # print("该Twitter发布时间", twitter[3][:10], twitter[3][11:])
    user_num = twitter[0]
    # 如果没有SUM_TWITTER字段，说明读取到了下一个用户则新建SUM_TWITTER, SUM_DAY, USE_DAY, BEGIN_DAY, END_DAY字段
    #                                                      总twitter数 统计总天数 使用总天数 开始天 结束天
    if len(users[user_num]) == 3:
        users[user_num].extend([1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                                   , 0, 0, 0, 0, 0, 0, 0])
        users[user_num][END_DAY] = twitter[3][5:10]
        timeArray = time.strptime(twitter[3], "%Y-%m-%d %H:%M:%S ")
        # print(timeArray)
        endTimeStamp = int(time.mktime(timeArray))
        # print(endTimeStamp)
        endTime = 1268841599
        day = []
        history_long[user_num] = [0]*90
        if endTime - endTimeStamp > 20*24*3600:
            history_long[user_num][math.floor((END_TIME - endTimeStamp) / 86400)] += 1
            leave = 1
        else:
            history_long[user_num][0] += 1
    else:
        users[user_num][SUM_TWITTER] += 1
        if twitter[3][5:10] not in day:
            day.append(twitter[3][5:10])
            users[user_num][USE_DAY] += 1
            users[user_num][BEGIN_DAY] = twitter[3][5:10]
        timeArray = time.strptime(twitter[3], "%Y-%m-%d %H:%M:%S ")
        TimeStamp = int(time.mktime(timeArray))
        if leave and 0 < END_TIME - TimeStamp < 90*24*3600:
            history_long[user_num][math.floor((END_TIME - TimeStamp) / 86400)] += 1
        elif 0 < END_TIME - TimeStamp < 90*24*3600:
            history_long[user_num][math.floor((endTimeStamp - TimeStamp)/86400)] += 1
    users_twitters[user_num].append(twitter[2].replace('\\n', ' '))
    timeArray = time.strptime(twitter[3], "%Y-%m-%d %H:%M:%S ")
    TimeStamp = int(time.mktime(timeArray))
    weekday = calendar.weekday(int(twitter[3][0:4]), int(twitter[3][5:7]), int(twitter[3][8:10]))
    if weekday == 0 or weekday == 6:
        users[user_num][WEEKEND] += 1
    else:
        users[user_num][WEEKDAY] += 1
    users[user_num][SUM_DAY] = math.floor(endTimeStamp / 86400 - TimeStamp / 86400) + 1
    users[user_num][SLEEP_DAY] = math.floor((END_TIME - endTimeStamp) / 86400)
    hour = int(int(twitter[3][11:13]) / 2)
    users[user_num][ONE_AM + hour] += 1
    index += 1
# 第三问结果输出
xls_predict = xlwt.Workbook('utf8')
sheet1 = xls_predict.add_sheet('user_predict')
line = 1
# 行
row = 0
# 列
for user in history_long:
    if users[user][SUM_DAY] > 10:
        history = [0] * 10
        i = 0
        while i < 10:
            history[i] = history_long[user][i]
            i += 1
        # print(history_long[user])
        minDist, user_find, order, predict = search.search(history, history_long, user)
        print(history, order, predict)
        # gray.gray_predict(history)
        sheet1.write(line, row, user)
        row += 1
        sheet1.write(line, row, user_find)
        row += 1
        for day in predict:
            sheet1.write(line, row, day)
            row += 1
        sheet1.write(line, row, minDist)
        row = 0
        line += 1
xls_predict.save('user_predict.xls')

for user in users:
    # print(users[user][USE_DAY], users[user][SUM_DAY])
    users[user][FREQUENCY] = int(users[user][USE_DAY]) / int(users[user][SUM_DAY])
    if users[user][FREQUENCY] > 1:
        users[user][FREQUENCY] = 1
    frequent_pot += users[user][FREQUENCY]
    away_pot += users[user][SLEEP_DAY]
    twitter_pot += users[user][SUM_TWITTER]
    alive_pot += users[user][USE_DAY]

# print("总记录条数", len(twitters))
counter_twitter = Counter(twitters)
# print("总用户数", len(user_number))
# print("Twitter示例", twitters[10000])
# ----------------------------------------------------------
# 第一问结果输出
# xls_user = xlwt.Workbook('utf8')
# sheet1 = xls_user.add_sheet('user_pot')
# line = 1
# 行
# row = 0
# 列
# print('******************用户平均指数*****************')
# print('*******活跃指数****流失指数****老用户指数*******')
avg_frequent = frequent_pot / 68.0
avg_away = away_pot / 68.0
avg_old = alive_pot / 68.0
# sheet1.write(69, 0, '总体指数')
# sheet1.write(69, 1, avg_frequent)
# sheet1.write(69, 2, avg_away)
# sheet1.write(69, 3, avg_old)
# str_pf = "*******(%.3f)****(%.3f)****(%.3f)******" % (avg_frequent, avg_away, avg_old)
# # print(str_pf)
# sheet1.write(0, 0, '用户编号')
# sheet1.write(0, 1, '发文频率')
# sheet1.write(0, 2, '流失指数')
# sheet1.write(0, 3, '老用户指数')
# print('********************单用户指数*****************')
# print('****用户编号****活跃指数****流失指数****老用户指数*******')
# type_0_0_0 = type_0_0_1 = type_1_0_0 = type_0_1_0 = type_1_1_0 = type_1_0_1 = type_0_1_1 = type_1_1_1 = 0
# for user in users:
#     str_pf = '*******(%s)****(%.3f)****(%.3f)****(%.3f)****' % (users[user][NUMBER], users[user][FREQUENCY],
#                                                                 users[user][SLEEP_DAY], users[user][USE_DAY])
#     sheet1.write(line, row, users[user][LONGITUDE])
#     row += 1
#     sheet1.write(line, row, users[user][LATITUDE])
#     row += 1
#     sheet1.write(line, row, users[user][FREQUENCY])
#     row += 1
#     sheet1.write(line, row, users[user][SLEEP_DAY])
#     row += 1
#     sheet1.write(line, row, users[user][USE_DAY])
#     row = 0
#     line += 1
#     if users[user][FREQUENCY] > avg_frequent:
#         if users[user][SLEEP_DAY] > avg_away:
#             if users[user][USE_DAY] > avg_old:
#                 type_1_1_1 += 1
#             else:
#                 type_1_1_0 += 1
#         else:
#             if users[user][USE_DAY] > avg_old:
#                 type_1_0_1 += 1
#             else:
#                 type_1_0_0 += 1
#     else:
#         if users[user][SLEEP_DAY] > avg_away:
#             if users[user][USE_DAY] > avg_old:
#                 type_0_1_1 += 1
#             else:
#                 type_0_1_0 += 1
#         else:
#             if users[user][USE_DAY] > avg_old:
#                 type_0_0_1 += 1
#             else:
#                 type_0_0_0 += 1
#                 # print(str_pf)
# sheet1.write(80, 0, '八种用户占比,顺序type_1_1_1 type_1_1_0 type_1_0_1 t'
#                     'ype_0_1_1 type_0_0_1 type_0_1_0 type_1_0_0 type_0_0_0')
# sheet1.write(81, 0, type_1_1_1 / 68)
# sheet1.write(81, 1, type_1_1_0 / 68)
# sheet1.write(81, 2, type_1_0_1 / 68)
# sheet1.write(81, 3, type_0_1_1 / 68)
# sheet1.write(81, 4, type_0_0_1 / 68)
# sheet1.write(81, 5, type_0_1_0 / 68)
# sheet1.write(81, 6, type_1_0_0 / 68)
# sheet1.write(81, 7, type_0_0_0 / 68)
# sheet1.write(82, 0, '备注：发文频率（发文天数/使用天数【统计时间段内】） '
#                     '流失指数（最近发文时间距离采集到的Twitter集最迟日期相差的天数）'
#                     '老用户指数【已经发文的天数】')
# print('************八种用户占比**********')
# print('type_1_1_1 type_1_1_0 type_1_0_1 type_0_1_1 type_0_0_1 type_0_1_0 type_1_0_0 type_0_0_0')
# str_pf = '%.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f' % (
#     type_1_1_1 / 68, type_1_1_0 / 68, type_1_0_1 / 68, type_0_1_1 / 68, type_0_0_1 / 68, type_0_1_0 / 68,
#     type_1_0_0 / 68,
#     type_0_0_0 / 68)
# xls_user.save('user_pot.xls')
# print(str_pf)
# -----------------------------------------------------------------
STOP_WORDS = set('''a about actually after again aint always all almost already am an and another
any anyone anything are around as ask ass at away awesome
b bad be because been before being believe best better big bitch black bout but by call came can can't crazy cause come con cool could cuz
da damn dat day days de details did didn't dis do does doesn't doin doing done dont don't down dude
early el en es even ever every everyone everything fam fam! fam!! fam!!! friday glad god goin gonna good! gotta great guess guy guys
feeling few finally first from for free fun funny ha haha haha, hahah hahaha happy hard has have haven't having
he head he's hear hell hey her here high him his home how hours now. how's hot
IN I If i'd i'm i"m i'll i've i if im ima imma in into is it it! it. its it's
jus juss just kinda knw la las late let let's lil little lmao lmao! lo lol lol, loll lol. lol! long lost
mad man many may maybe me me. me! mean mi might miss more most morning much must my myself
n name next never new nice nigga niggas night no not nothing now
o oh oooh of off ok okay old omg on one only or other our out over
para person pic place play playing please por ppl pretty put que r ready real really right
same saw se send she she's should show sick since smh so soo soon sooo some someone something sorry stay still sure
take talk te tell tha than thanks that that's the their them then there there's these they thing things tho
though thought those through till tired
time to today today. today? tomorrow tonight too totally this tht true two
u un until ur us used up very
w w/ wait waiting was wat wats wanna want way we week well went were what what's where while white
who whole whoot when wht whts why will win wit with won't word work world would wow wrong wuz
y y'all ya yall yea yeah year years yes yet yo you you. you? you're your yu
1 2 2nite 3 <3 4 5 10 2010 . .. ... : ( ) - = -- --- & \'\' | ? ! ~
:) :( check ;) :p
(cont) (yea)
#ff
B*tch back beat bring called coming del feel find follow found fuck fucking hate heard hit hope
Good Get get gets gettin getting give go gone good goood going got had keep kno know
last leave left like listen live look looks looking los lot love made make makes making need people
remember said say says shit see seen sounds start stop talking try trying told took use watch watching wish working
Thank thank think too!

'''.split())
print('********************STOP_WORDS*****************')
# print(STOP_WORDS)
user_words_all = []
print('********************用户Twitter集***************')
for user_twitters in users_twitters:
    user_punctuation[user_twitters] = OrderedDict({'....': 0, '!!': 0, '..': 0, '.': 0, '?': 0, "'": 0,
                                                   '!!!': 0, '!': 0, ',': 0, '...': 0, '"': 0, '?!': 0,
                                                   '??': 0, '???': 0})
    twitters_cursor = users_twitters[user_twitters]
    for twitter in twitters_cursor:
        words = Helper.my_split(twitter, ' ')
        words, user_punctuation[user_twitters] = Helper.record_punctuation(words, user_punctuation[user_twitters])
        user_words_all.extend(words)
        user_words[user_twitters].extend(words)

# ---------------------------------------------------
# 输出单用户的高频词到Excel
wbk = xlwt.Workbook('utf8')
sheet1 = wbk.add_sheet('user_frequent_word')
line = 1
# 行
row = 0
# 列
for index in user_words:
    DEL_WORDS = []
    user_words[index][52] = 0
    user_words[index][53] = 0
    counters = Counter(user_words[index])
    # print(user_words[index].viewkeys())
    for word in counters:
        if type(word) == str and word != '' and word[0] == '@':
            # @ 52
            DEL_WORDS.append(word)
    # print(DEL_WORDS)
    # print(words)
    for STOP_WORD in STOP_WORDS:
        if counters.get(STOP_WORD):
            del counters[STOP_WORD]
            # counters.pop(STOP_WORD)
    for DEL_WORD in DEL_WORDS:
        # print(counters.get(DEL_WORD))
        user_words[index][52] += counters.get(DEL_WORD)
        users[index][AT_TIME] += counters.get(DEL_WORD)
        del counters[DEL_WORD]
    # counters.pop(key='')
    # ERROR CODE
    #         del counters[word]
    # print(counters)
    # 输出单用户的高频词
    datas = counters.most_common(20)
    # print(index, '    ', counters.get('rt'))
    # print(datas)
    users[index][RT_TIME] = counters.get('rt')
    sheet1.write(line, row, index)
    row += 1
    sheet1.write(line, row, user_words[index][52])
    row += 1
    for data in datas:
        # print(data[0], data[1])
        if data[0]:
            sheet1.write(line, row, data[0])
            row += 1
            sheet1.write(line, row, data[1])
            row += 1
    line += 1
    row = 0
    counters = dict(counters)
    # print(counters)
    for cursor in counters:
        # print(cursor)
        if cursor == 0:
            continue
        elif cursor.rstrip('.') in {'phone', 'twitter', 'tweet'}:
            users[index][SOCIAL_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'life', 'sleep', 'bed', 'house', 'ill'}:
            users[index][LIFE_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'game', 'party', 'club', 'birthday', 'bday', 'money', 'buy', 'son', 'video',
                                    'music', 'dj', 'movie', 'car'}:
            users[index][AMUSEMENT_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'baby', 'son', 'kids', 'schools', 'class'}:
            users[index][EDU_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'nike', 'sports', 'basketball', 'football', 'meatballs', 'baseball'}:
            users[index][SPORTS_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'read', 'book', 'newspaper', 'reading', 'books'}:
            users[index][READ_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'job', 'stuff', 'company'}:
            users[index][WORK_POT] += counters[cursor]
        elif cursor.rstrip('.') in {'eat', 'food', 'meal'}:
            users[index][FOOD_POT] += counters[cursor]
            # print('用户', index, '@次数', user_words[index][52])
wbk.save('user_frequent_word.xls')
# ----------------------------------------------------------
# 输出用户标点符号使用情况
line = 1
wbk = xlwt.Workbook('utf8')
sheet1 = wbk.add_sheet('punctuation')
XLSHelper.write_a_line(['user', '....', '\'', '!!!', '?', ',', '!!', '!', '"', '..', '.',
                        '...', '?!', '??', '???']
                       , sheet1, 0)
for punctuation_act in user_punctuation:
    row = 1
    sheet1.write(line, 0, punctuation_act)
    # print(user_punctuation[punctuation_act])
    for key in user_punctuation[punctuation_act]:
        # print(user_punctuation[punctuation_act])
        sheet1.write(line, row,
                     user_punctuation[punctuation_act][key] / users[punctuation_act][SUM_TWITTER])
        row += 1
        # print(user_punctuation[punctuation_act][key]),
    line += 1
wbk.save('punctuation_use.xls')

counter_all = Counter(user_words_all)
DEL_WORDS = []
user_words[index][52] = 0
for word in counter_all:
    # if type(word) == str and word.startswith('RT'):
    #     DEL_WORDS.append(word)
    #     user_words[index][53] += 1
    if type(word) == str and word != '' and word[0] == '@':
        # @ 52 RT 53
        DEL_WORDS.append(word)
        # print(DEL_WORDS)
for STOP_WORD in STOP_WORDS:
    if counter_all.get(STOP_WORD):
        del counter_all[STOP_WORD]
        # counters.pop(STOP_WORD)
for DEL_WORD in DEL_WORDS:
    # print(counters.get(DEL_WORD))
    user_words[index][52] += counter_all.get(DEL_WORD)
    del counter_all[DEL_WORD]
# -----------------------------------------------------------
# 用户聚类数据
datMat = []
for user in users:
    # users[user][AT_TIME] = user_words[user][52]
    users[user][EXCLAMATION_TIME] = user_punctuation[user]['!'] + \
                                    user_punctuation[user]['!!'] * 2 + \
                                    user_punctuation[user]['!!!'] * 3 + user_punctuation[user]['?!']
    users[user][QUESTION_MARK] = user_punctuation[user]['?'] + \
                                 user_punctuation[user]['??'] * 2 + \
                                 user_punctuation[user]['???'] * 3 + user_punctuation[user]['?!']
    row = [
            users[user][RT_TIME] / users[user][SUM_TWITTER],
           (users[user][AT_TIME] - users[user][RT_TIME]) / users[user][SUM_TWITTER],
           users[user][EXCLAMATION_TIME] / users[user][SUM_TWITTER],
           users[user][QUESTION_MARK] / users[user][SUM_TWITTER]
           ]
    datMat.append(row)
# -----------------------------------------------------------
# K-Means聚类(失败)
# print(datMat)
# myCentroids, clustAssing = Kmeans.kMeans(datMat, 3)
# plt.plot(myCentroids[:, 0], myCentroids[:, 1], 'ro')
# plt.plot([x[0] for x in datMat], [x[1] for x in datMat], 'r+')
# print([x[0] for x in datMat])
# plt.show()
# error = sum(clustAssing[:, 0])
# print(error)
# -----------------------------------------------------------
# 输出用户兴趣指数
# wbk = xlwt.Workbook('utf8')
# sheet1 = wbk.add_sheet('user_interest')
# line = 1
# 行
# row = 0
# 列
# print('*******************用户兴趣行矩阵**************************')
# print('***用户编号**社交**生活**娱乐**教育**体育**阅读**工作**美食**')
# sheet1.write(0, 0, '用户编号')
# sheet1.write(0, 1, '社交指数')
# sheet1.write(0, 2, '生活指数')
# sheet1.write(0, 3, '娱乐指数')
# sheet1.write(0, 4, '教育指数')
# sheet1.write(0, 5, '体育指数')
# sheet1.write(0, 6, '阅读指数')
# sheet1.write(0, 7, '工作指数')
# sheet1.write(0, 8, '美食指数')
# for user in users:
#     str_pf = '*%8s%4d%4d%4d%4d%4d%4d%4d%4d**' % (
#         user, users[user][SOCIAL_POT], users[user][LIFE_POT], users[user][AMUSEMENT_POT]
#         , users[user][EDU_POT], users[user][SPORTS_POT], users[user][READ_POT],
#         users[user][WORK_POT], users[user][FOOD_POT])
#     sheet1.write(line, 0, user)
#     sheet1.write(line, 1, users[user][SOCIAL_POT])
#     sheet1.write(line, 2, users[user][LIFE_POT])
#     sheet1.write(line, 3, users[user][AMUSEMENT_POT])
#     sheet1.write(line, 4, users[user][EDU_POT])
#     sheet1.write(line, 5, users[user][SPORTS_POT])
#     sheet1.write(line, 6, users[user][READ_POT])
#     sheet1.write(line, 7, users[user][WORK_POT])
#     sheet1.write(line, 8, users[user][FOOD_POT])
#     line += 1
#     print(str_pf)
# wbk.save('user_interest.xls')
# -----------------------------------------------------------
# ------------------------------------------------------
# 输出整体集合高频词到EXCEL
# users_words_frequent_all = counter_all.most_common(50)
# wbk = xlwt.Workbook('utf8')
# sheet1 = wbk.add_sheet('all_users_frequent_word')
# line = 1
# 行
# row = 0
# 列
# for word in users_words_frequent_all:
#     sheet1.write(line, row, word[0])
#     row += 1
#     sheet1.write(line, row, word[1])
#     row = 0
#     line += 1
# wbk.save('all_users_frequent_word.xls')
# --------------------------------------------------------

# users_words_frequent[index] = dict(counters)
# print(users_words_frequent[index])
# users_words_frequent[index] = dict(counters)
# print(users_twitters)
# for user_words_frequent in users_words_frequent:
#     print(users_words_frequent[user_words_frequent])

XLSHelper = XLSHelper()
XLSHelper.XLSWriter(users, 'data', 'data.xls')
# XLSHelper.XLSWriter()
