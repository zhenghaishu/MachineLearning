# coding:utf-8

from numpy import *
import operator

# 给出训练数据以及对应的类别
def createDataSet():
    group = array([[1.0,2.0],[1.2,0.1],[0.1,1.4],[0.3,3.5]])
    labels = ['A','A','B','B']
    return group,labels

# 通过KNN进行分类
def classify(input,dataSet,labels,k):
    dataSize = dataSet.shape[0]
    
    # 计算欧氏距离
    diff = tile(input,(dataSize,1)) - dataSet
    diff2 = diff ** 2
	# 行向量分别相加，从而得到新的一个行向量
    dist2 = sum(diff2,axis = 1) 
    dist = dist2 ** 0.5
    
    # 对距离进行排序，按从小到大的规则
    distIndex = argsort(dist)

    labelCount = {}
    for i in range(k):
        label = labels[distIndex[i]]
        # 对选取的K个样本所属的类别个数进行统计
        labelCount[label] = labelCount.get(label,0) + 1
        
    # 选取出现的类别次数最多的类别
    maxCount = 0
    for key,value in labelCount.items():
        if value > maxCount:
            maxCount = value
            targetLabel = key

    return targetLabel

def test():
    dataSet,labels = createDataSet()
    input = array([1.1,0.3])
    K = 3
    output = classify(input,dataSet,labels,K)
    print("Test data:",input,"classify result:",output)
