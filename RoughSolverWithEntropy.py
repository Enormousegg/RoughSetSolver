#!/usr/bin/env python
# coding: utf-8

# In[87]:


import pandas as pd


# In[88]:


#验证用数据集合

example = [[1,2,2,3,1],[2,3,2,1,0],[1,2,2,3,0],
           [3,3,1,2,1],[1,3,2,1,0],[3,1,1,2,0],
           [3,3,2,2,1],[2,3,2,2,1],[2,3,2,1,0],
           [3,3,3,2,1]]
data = pd.DataFrame(example,index=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10'],columns=['c1','c2','c3','c4','D'],dtype=float)


# In[89]:


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


def GetI(ConditionAttribIND,DecisionAttribIND,USize):
    ans = 0
    for x in ConditionAttribIND:
        if(len(x)==1):
            continue
        csize = len(x)
        tmp = 0
        for y in DecisionAttribIND:
            count = 0
            for z in x:
                if(z in y):
                    count += 1
            if(count==0):
                continue
            tmp += (count/csize)*(1-(count/csize))
        ans += csize*csize*tmp/(USize*USize)
    return ans  


# In[90]:



# sampleList = ['C11 C12 C13','C21 C22 C23 C24 C25 C26 C27 C28','C31 C32','','D']
sampleList = ['c1','c2','c3','c4','','D']
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
        if(sample!='D'):
            index_list = data.columns.to_list()
            index_list.pop()
            for x in attri:
                index_list.remove(x)
            tmp = ''
            for x in index_list:
                tmp =tmp + x
            IND[tmp] = GetIND(index_list,data)


# In[91]:


USize = data.shape[0]

IDC = GetI(IND['empty'],IND['D'],USize)
IDC1 = GetI(IND['c1'],IND['D'],USize)
IDC2 = GetI(IND['c2'],IND['D'],USize)
IDC3 = GetI(IND['c3'],IND['D'],USize)
IDC4 = GetI(IND['c4'],IND['D'],USize)
IDC1N = GetI(IND['c2c3c4'],IND['D'],USize)
IDC2N = GetI(IND['c1c3c4'],IND['D'],USize)
IDC3N = GetI(IND['c1c2c4'],IND['D'],USize)
IDC4N = GetI(IND['c1c2c3'],IND['D'],USize)

SIGC1 = IDC1 - IDC + IDC1N
SIGC2 = IDC2 - IDC + IDC2N
SIGC3 = IDC3 - IDC + IDC3N
SIGC4 = IDC4 - IDC + IDC4N

print(SIGC1,SIGC2,SIGC3,SIGC4)

WC1 = SIGC1/(SIGC1+SIGC2+SIGC3+SIGC4)
WC2 = SIGC2/(SIGC1+SIGC2+SIGC3+SIGC4)
WC3 = SIGC3/(SIGC1+SIGC2+SIGC3+SIGC4)
WC4 = SIGC4/(SIGC1+SIGC2+SIGC3+SIGC4)

print(WC1,WC2,WC3,WC4)


# In[ ]:




