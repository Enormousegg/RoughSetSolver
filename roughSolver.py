#!/usr/bin/env python
# coding: utf-8

# In[251]:


import pandas as pd
from jenkspy import JenksNaturalBreaks


# In[252]:


#自然断点处理数据

dataD = pd.read_csv('juece.csv',index_col = 0)

x = dataD['综合归一化'].to_list()

jnb = JenksNaturalBreaks(nb_class=5)
jnb.fit(x)
NewD = jnb.labels_
NewD += 1


data = pd.read_csv('相等间隔.csv',index_col = 0)

data = data.drop(columns='D')
data = data.drop('自然断点',axis=1)

data.insert(loc=len(data.columns),column='D',value=NewD)


# In[253]:


def GetDict(index_list,data):
    ans = dict()
    for index,row in data.iterrows():
        key = ''
        for x in index_list:
            key += str(row['%s'%x])
        if(ans.get(key)):
            ans[key].append(index)
        else:
            ans[key]=[index]
    return ans  

def GetIND(attri,data):
    if(len(attri)==0):
        index_list = data.columns.to_list()
        index_list.pop()
        ans = GetDict(index_list,data)
    elif(attri[0] == 'D'):
        index_list = ['D']
        ans = GetDict(index_list,data)
    else:
        index_list = data.columns.to_list()
        index_list.pop()
        for x in attri:
            index_list.remove(x)
        ans = GetDict(index_list,data)
    return ans.values()
        
def GetPositive(ConditionAttribIND,DecisionAttribIND):
    ans = list()
    count = 0
    for x in ConditionAttribIND:
        if(len(x)==1):
            ans.extend(x)
            count += 1
            continue
        for y in DecisionAttribIND:
            if(set(x)<set(y)):
                ans.extend(x)
                break  
    return ans


# In[254]:



sampleList = ['C11 C12 C13','C21 C22 C23 C24 C25 C26 C27 C28','C31 C32','','D']
IND = dict()
for sample in sampleList:
    if(sample == "NORMAL"):#默认存在的不可分辨集合
        for x in data.columns.to_list():
            attri = [x]
            IND[x]  = GetIND(attri,data)
        attri = []
        IND['empty'] = GetIND(attri,data)
        attri = ['D']
        IND['D'] = GetIND(attri,data)
        break
    elif(sample==''):
        attri = []
        IND['empty'] = GetIND(attri,data)
    elif(sample!="OVER"):#特殊不可分辨集合
        attri = sample.split()
        IND[sample]  = GetIND(attri,data)


# In[255]:


posDict = dict()
for key in IND:
    if(key!='D'):
        posDict[key] = GetPositive(IND[key],IND['D'])

USize = data.shape[0]
ImportanceDict = dict()
for key in posDict:
    ImportanceDict[key] = (len(posDict['empty'])-len(posDict[key]))
# print(ImportanceDict)

WeightDict = dict()
SumImportance = 0;
for value in ImportanceDict.values():
    SumImportance += value
for key in ImportanceDict:
    WeightDict[key] = ImportanceDict[key]/SumImportance
print(WeightDict)


# In[256]:


#计算二级指标
def GetSecond(dataIn,attriList):
    data = dataIn.copy()
    for index,row in dataIn.iteritems():
        if index in attriList:
            continue
        data = data.drop(index,axis=1)

    sampleList = ['NORMAL']
    IND = dict()
    for sample in sampleList:
        if(sample == "NORMAL"):#默认存在的不可分辨集合
            for x in data.columns.to_list():
                attri = [x]
                IND[x]  = GetIND(attri,data)
            attri = []
            IND['empty'] = GetIND(attri,data)
            attri = ['D']
            IND['D'] = GetIND(attri,data)
            break
        elif(sample==''):
            attri = []
            IND['empty'] = GetIND(attri,data)
        elif(sample!="OVER"):#特殊不可分辨集合
            attri = sample.split()
            IND[sample]  = GetIND(attri,data)
    posDict = dict()
    for key in IND:
        if(key!='D'):
            posDict[key] = GetPositive(IND[key],IND['D'])

    USize = data.shape[0]
    ImportanceDict = dict()
    for key in posDict:
        ImportanceDict[key] = (len(posDict['empty'])-len(posDict[key]))
        
    WeightDict = dict()
    SumImportance = 0;
    for value in ImportanceDict.values():
        SumImportance += value
    for key in ImportanceDict:
        WeightDict[key] = ImportanceDict[key]/SumImportance
#     print(WeightDict)

    return WeightDict


# In[257]:


C1Weight = GetSecond(data,['C11','C12','C13','D'])
C2Weight = GetSecond(data,['C21','C22','C23','C24','C25','C26','C27','C28','D'])
C3Weight = GetSecond(data,['C31','C32','D'])

TotalWeight = dict()

#C1
for key in C1Weight:
    TotalWeight[key] = C1Weight[key]*WeightDict['C11 C12 C13']

#C2
for key in C2Weight:
    TotalWeight[key] = C2Weight[key]*WeightDict['C21 C22 C23 C24 C25 C26 C27 C28']
    
#C3
for key in C3Weight:
    TotalWeight[key] = C3Weight[key]*WeightDict['C31 C32']
    
print(TotalWeight)


# In[ ]:




