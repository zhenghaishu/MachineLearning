#-*-coding:utf-8-*-
import pdb
import math

user_items = dict()
user_tags = dict()
item_tags = dict()
tag_items = dict()

def addValueToMat(mat, key, value):
    if key not in mat:
        mat[key] = dict()
        mat[key][value] = 1
    else:
        if value not in mat[key]:
            mat[key][value] = 1
        else:
            mat[key][value] += 1

def InitStat():
    data_file = open('tagdata.txt')
    line = data_file.readline()
    while line:
        terms = line.split("\t")
        user = terms[0]
        item = terms[1]
        tag = terms[2]

        addValueToMat(user_items, user, item)
        addValueToMat(user_tags, user, tag)
        addValueToMat(item_tags, item, tag)
        addValueToMat(tag_items, tag, item)
        
        line = data_file.readline()

    data_file.close()

# 计算推荐列表
def Recommend(user):
    recommend_list = dict()
    tagged_item = user_items[user]
    for tag, wu in user_tags[user].items():
        for item, wi in tag_items[tag].items():
            if item not in tagged_item:
                if item not in recommend_list:
                    recommend_list[item] = wu * wi
                else:
                    recommend_list[item] += wu * wi
    return sorted(recommend_list.items(), key = lambda a:a[1], reverse = True)

# 统计标签流行度
def TagPopularity():
    tagFreq = {}
    for user in user_tags.keys():
        for tag in user_tags[user].keys():
            if tag not in tagFreq:
                tagFreq[tag] = 1
            else:
                tagFreq[tag] += 1
    return sorted(tagFreq.items(), key = lambda a:a[1], reverse = True)


#计算余弦相似度
def CosineSim(item_tags,i,j):
    ret = 0
    for tag,w in item_tags[i].items():     #求物品i,j的标签交集数目
        if tag in item_tags[j]:
            ret += w * item_tags[j][tag]
            
    if ret == 0:
        return 0
    
    ni = 0
    nj = 0
    for tag, wi in item_tags[i].items():      #统计 i 的标签数目
        ni += wi * wi
    for tag, wj in item_tags[j].items():      #统计 j 的标签数目
        nj += wj * wj

    return ret/math.sqrt(ni * nj)          #返回余弦值

def Diversity(item_tags, recommend_items):
    ret = 0
    n = 0

    for i in dict(recommend_items).keys():
        for j in dict(recommend_items).keys():
            if i == j:
                continue
            ret += CosineSim(item_tags, i ,j)
            n += 1
    return ret / n
    
InitStat()

recommend_list = Recommend("刘一")
print("推荐列表： %s" % recommend_list)

tagFreq = TagPopularity()
print("标签流行度：%s" % tagFreq)

diversity = Diversity(item_tags, recommend_list)
print("列表多样性：%s" % diversity)
