import copy
import numpy as np
import pandas as pd
import random
import time

Attributes = ['age', 'work_class', 'final_weight', 'education',
            'education_num', 'marital_status', 'occupation', 'relationship',
            'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week',
            'native_country', 'class' ]

TempQI = ['TempAge', 'TempEducationNumber']
# We use TempQI to determine QI-Clusters as not to change the original value of QI

DIF = ['DifAge', 'DifEduNum']
# We add two columns to record the difference of (MaxAge, MinAge) and (MaxEduNum, MinEduNum) to calculate LM

QI = ['age','education_num']

SV = ['occupation']

flag = 1

K = 1000

def load_data(data_path = "C:\\Users\\82581\\Desktop\\adult.data"):

    data_original = pd.read_csv(data_path, sep = ', ', engine = 'python', header = None, names = Attributes)

    '''
    ParserWarning: Falling back to the 'python' engine 
    because the 'c' engine does not support regex separators
    (separators > 1 char and different from '\s+' are interpreted as regex); 
    you can avoid this warning by specifying engine='python'.
    We therefore add engine = 'python' 
    '''

    data_nan = data_original.replace('?', np.nan)
    # We replace ? with np.nan, which can be detected and deleted automatically via dropna

    data_cleaned = data_nan.dropna().reset_index(drop = True)
 
    print('Data after cleaning is shown as below')
    # We create a new datafram from index 0 to index 30161
    print(data_cleaned)  # 30162 x 15
    return data_cleaned


if __name__ == '__main__':
    data = load_data()

'''
    We add two columns in the original data, TempAge and TempEducationNumber respectively to
    store the generalized formation of age and education_number.
    If we directly change the value in the original data, we can NOT find the original value of age
    and education_number once we start generalization. 
    Also, we set TempQI = ['TempAge', 'TempEducationNumber'] instead of ['age', 'education_number']
'''


'''
    We get the format of a clolumn in the datafram with the value being str
    By using pop, the original column is removed, here we insert to make it the same as before
'''
Native_country = data.pop('native_country')
data.insert(13, 'native_country', Native_country)

AGE = data.pop('age')
data.insert(0, 'age', AGE)

# Initialization of TempQI
# print(data.loc[:,"education_num"].max())   # age: 90 education_num: 16
# print(data.loc[:,"education_num"].min())   # age: 17 education_num: 1
data['TempAge'] = Native_country
data.loc[:, 'TempAge'] = str((16,95))
data['TempEducationNumber'] = Native_country
data.loc[:, 'TempEducationNumber'] = str((1,20))

# Initialization of DIF
data['DifAge'] = AGE
data.loc[:, 'DifAge'] = 79
data['DifEduNum'] = AGE
data.loc[:, 'DifEduNum'] = 19

print(data[QI + TempQI + SV + DIF])


def Cluster(data):
    data_temp = copy.deepcopy(data)
    Cluster = data_temp.groupby(TempQI, as_index=False).count()
    # We use groupby function to find TempQI clusters to further discuss whether they satisfy k-anonymity

    Cluster_show = Cluster[(TempQI + SV)]  
    Cluster_show.columns = ['TempAge', 'TempEducationNumber', 'Total_number']

    # We change the name of the last column to 'Total_number'
    print(Cluster_show)

    return Cluster_show
  

# We do the generalization work via traversal

def AgeGeneralization(data, AGE_array, ClusterAge, ClusterEducationNumber):
    MinAge = np.min(AGE_array)
    MaxAge = np.max(AGE_array)
    MidAge = np.median(AGE_array)
    print('Maximun, Minimun, Midian of Age is:', MaxAge, MinAge, MidAge)

    for i in range(30162):
        if data.loc[i,'TempAge'] == ClusterAge and data.loc[i,'TempEducationNumber'] == ClusterEducationNumber:
            data.loc[i,'DifAge'] = MaxAge - MinAge
            if data.loc[i,'age'] <= MidAge:
                data.loc[i,'TempAge'] = str((MinAge, MidAge))
            else:
                data.loc[i,'TempAge'] = str((MidAge + 1, MaxAge))
            
    

def EduNumGeneralization(data, EDUNUMBER_array, ClusterAge, ClusterEducationNumber):

    MinEduNum = np.min(EDUNUMBER_array)
    MaxEduNum = np.max(EDUNUMBER_array)
    MidEduNum = np.median(EDUNUMBER_array)
    print('Maximun, Minimun, Midian of Education number is:', MaxEduNum, MinEduNum, MidEduNum)

    for i in range(30162):
        if data.loc[i,'TempAge'] == ClusterAge and data.loc[i,'TempEducationNumber'] == ClusterEducationNumber:
            data.loc[i,'DifEduNum'] = MaxEduNum - MinEduNum
            if data.loc[i,'education_num'] <= MidEduNum:
                data.loc[i,'TempEducationNumber'] = str((MinEduNum, MidEduNum))
            else:
                data.loc[i,'TempEducationNumber'] = str((MidEduNum + 1, MaxEduNum))
            


# Here we judge whether the generalized data is k-anonymous after one iteration (one cluster split into two)
def Satisfiable(data):
    threshold = data['Total_number'].min()
    if threshold < K:
        return 0
    else:
        return 1


'''
    Function SequenceCount is set to record the maximun time the same non-zero number appears in a row
    e.g. For a sequence like 1 2 3 4 5 6 6 6 6 6 6 The function returns 6.
    Why we define a function like this:
    The basic idea of Mondrian is that we always find the maximun cluster and do the split.
    However, if the table after split is not k-anonymous any more, we can NOT split the cluster.
    Then we set the number of the cluster to 0 and we can proceed with the maxinum cluster of what is left.
    We proceed with the following steps until the table can NOT be split any more.
    How do we know when it's the time?
    We can see that this time the table after Mondrian algorithm remains the same, its column size included.
    So, we use SequenceCount to count the times the same table appears in a row.
    Considering we have 2 quasi-identifiers and we choose them randomly via FlipCoin, 
    we may not split the table with one of them, yet we can do so with another one.
    Consequently, we set the threshold to 10.
    We will consider it an end if the same table appears 10 times in a row.

'''
INDEX = 200

Len = np.zeros(INDEX)
Start = -1

def SequenceCount(array):
    count = 0
    for i in range(INDEX):
        if array[i] == 0:
            break
        else:
            if array[i] == array[i + 1]:
                count = count + 1
            if array[i] != array[i + 1]:
                if array[i + 1] != 0:
                    count = 0
    return count + 1


def LossAge(data):
    LMAge = 0
    for i in range(30162):
        LMAge = LMAge + (data.loc[i,'DifAge'])/79
    return LMAge

def LossEduNum(data):
    LMEduNum = 0
    for i in range(30162):
        LMEduNum = LMEduNum + (data.loc[i,'DifEduNum'])/19
    return LMEduNum


def Mondrian(data):
    data_copy = copy.deepcopy(data)
    '''
        In python, when applying '=', e.g. a = b, we will change the value of b if we change a
        That is, we will change the value of data if we use 'data_copy = data' 
        when changing the value of data_copy, which will cause LOTS OF trouble.
        Therefore, we use copy.deepcopy() to avoid things like that from happening.
    '''

    data_cluster = Cluster(data_copy)
    
    # Count > 10, we terminate the generalization process
    global Start
    Start = Start + 1
    Len[Start] = data_cluster.shape[0]
    COUNT = SequenceCount(Len)
    print('Current count: ', COUNT)

    if COUNT > 10:
        LossMetric = (LossAge(data) + LossEduNum(data))/30162
        print('The loss metric of the released table is: ', LossMetric)
        data_show = data_copy[(TempQI + SV )]
        data_show.columns = ['age', 'education_num', 'occupation']
        print('The release data is shown as below: ')
        print(data_show)
        return

    max = data_cluster['Total_number'].max()
    print('max cluster: ', max) 
    

    index = data_cluster[data_cluster.Total_number == max].index.tolist()[0]  
    print('index of max cluster number: ', index)

    if max < 2*K: # max < 2*K, it is apparent we can't further partition the data
        return


    global flag
    if flag == 0:
        data_cluster.loc[index,'Total_number'] = 0
        max = data_cluster['Total_number'].max()
        print('max cluster: ', max) 

        index = data_cluster[data_cluster.Total_number == max].index.tolist()[0]  
        print('index of max cluster number: ', index)

    
    ClusterAge = data_cluster.loc[index,'TempAge']
    ClusterEducationNumber = data_cluster.loc[index,'TempEducationNumber']

    AGE = []
    EDUNUMBER = []


    for i in range(30162):
        if data_copy.loc[i,'TempAge'] == ClusterAge and data_copy.loc[i,'TempEducationNumber'] == ClusterEducationNumber:
            AGE.append(data_copy.loc[i,'age'])
            EDUNUMBER.append(data_copy.loc[i,'education_num'])
        if i == 30161:
            AGE_array = np.array(AGE)
            EDUNUMBER_array = np.array(EDUNUMBER)
    
    FlipCoin = random.random()
    if (FlipCoin < 0.5):
        EduNumGeneralization(data_copy, EDUNUMBER_array, ClusterAge, ClusterEducationNumber)
    else:
        AgeGeneralization(data_copy, AGE_array, ClusterAge, ClusterEducationNumber)


    data_copy_cluster = Cluster(data_copy)
    
    if Satisfiable(data_copy_cluster) == 1:
        data = copy.deepcopy(data_copy)
        Mondrian(data)
    
    if Satisfiable(data_copy_cluster) == 0:
        flag = 0   # We tag the cluster to show that it can NOT be partitioned
        Mondrian(data)

begin = time.time()

Mondrian(data)

end = time.time()

Time = end - begin


print('Total calculation time is: ', Time)
