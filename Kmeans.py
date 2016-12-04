# -*- coding: utf-8 -*
# author: ArrayZoneYour

from numpy import *
import matplotlib.pyplot as plt


def loadDataSet(fileName):      #general function to parse tab -delimited floats
    dataMat = []                #assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine)) #map all elements to float()
        dataMat.append(fltLine)
    return dataMat


# 计算两个向量之间的欧氏距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


def randCent(dataSet, k):
    n = shape(dataSet)[1]
    print(dataSet)
    centroids = mat(zeros((k, n)))#create centroid mat
    print(centroids)
    for j in range(n):#create random cluster centers, within bounds of each dimension
        minJ = min(x[j] for x in dataSet)
        rangeJ = float(max(x[j] for x in dataSet) - minJ)
        centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))
    # print(centroids)
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))# 创建矩阵来生命数据点
                                      # 对于每个数据点和节点计算他们的误差平方来进行评估
    points = list()
    centroids = createCent(dataSet, k)
    print(centroids)
    cluster_changed = True
    while cluster_changed:
        cluster_changed = False
        for i in range(m):
            # 将每个数据点分配至最近的节点
            min_dist = inf; minIndex = -1
            # 算出当前数据点到每个节点的距离
            for j in range(k):
                # 遍历获得最近节点编号及距离
                distJI = distMeas(centroids[j], dataSet[i])
                if distJI < min_dist:
                    min_dist = distJI; minIndex = j
            # clusterAssment [节点编号 欧氏距离]
            # print(clusterAssment[i, 0])
            if clusterAssment[i, 0] != minIndex:
                cluster_changed = True
            clusterAssment[i, :] = minIndex, min_dist**2
        # print(clusterAssment)
        # print(clusterAssment[0].item(0))
        for cent in range(k):# 重新计算节点
            # 取出节点下的所有数据点
            s = 0
            while s < len(dataSet):
                if clusterAssment[s, 0] == cent:
                    points.append(dataSet[s])
                s += 1
            # print('该节点下的数据点', points)
            # print('DataSet', dataSet)
            # print('模拟取出dataSet', nonzero(a))
            ptsInClust = array(points)
            points = []
            # 将质心指定为平均值，成为新的簇质心
            centroids[cent] = mean(ptsInClust, axis=0)
        print('节点', centroids)
    return centroids, clusterAssment

# ---------------------------------------------------------
# 二维聚类完成
# res = distEclud(array([0, 0, 0, 0]), array([1, 1, 1, 1]))

# datMat = loadDataSet('testSet.txt')
# print(datMat)
# myCentroids, clustAssing = kMeans(datMat, 4)
# print(myCentroids[:, 0])
# plt.plot(myCentroids[:, 0], myCentroids[:, 1], 'ro')
# plt.plot([x[0] for x in datMat], [x[1] for x in datMat], 'r+')
# # print([x[0] for x in datMat])
# plt.show()

# print(myCentroids, clustAssing)
# randCent(datMat, 2)
# print(res)
# ---------------------------------------------------------
# 四维聚类的支持函数测试样例
# 测试距离函数
# res = distEclud(array([4, 1, 1, 1]), array([0, 0, 0, 0]))
# print(res)
# 测试随机点生成函数
# res = randCent([array([4, 1, 1, 1]), array([0, 0, 0, 10])], 2)
# print(res)
