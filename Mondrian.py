import copy
import numpy as np
import pandas as pd
import random

Attributes = ['age', 'work_class', 'final_weight', 'education',
            'education_num', 'marital_status', 'occupation', 'relationship',
            'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week',
            'native_country', 'class' ]
TempQI = ['TempAge', 'TempEducationNumber']
QI = ['age','education_num']
SV = ['occupation']

flag = 1
END = 0

K = 800

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

Native_country = data.pop('native_country')
data.insert(13, 'native_country', Native_country)

data['TempAge'] = Native_country
data.loc[:, 'TempAge'] = str((16,95))
data['TempEducationNumber'] = Native_country
data.loc[:, 'TempEducationNumber'] = str((1,20))

print(data)


def Cluster(data):
    data_temp = copy.deepcopy(data)
    Cluster = data_temp.groupby(TempQI, as_index=False).count()
    # We use groupby function to find TempQI clusters to further discuss whether they satisfy k-anonymity

    Cluster_show = Cluster[(TempQI + SV)]  
    Cluster_show.columns = ['TempAge', 'TempEducationNumber', 'Total_number']

    # We change the name of the last column to 'Total_number'
    print(Cluster_show)

    return Cluster_show
  

def AgeGeneralization(data, AGE_array, ClusterAge, ClusterEducationNumber):
    MinAge = np.min(AGE_array)
    MaxAge = np.max(AGE_array)
    MidAge = np.median(AGE_array)
    print('Maximun, Minimun, Midian of Age is:', MaxAge, MinAge, MidAge)

    for i in range(30162):
        if data.loc[i,'TempAge'] == ClusterAge and data.loc[i,'TempEducationNumber'] == ClusterEducationNumber:
            if data.loc[i,'age'] <= MidAge:
                data.loc[i,'TempAge'] = str((MinAge, MidAge))
            else:
                data.loc[i,'TempAge'] = str((MidAge, MaxAge))
    
    if MinAge == MidAge or MaxAge == MidAge:
        global END
        END = 1


def EduNumGeneralization(data, EDUNUMBER_array, ClusterAge, ClusterEducationNumber):

    MinEduNum = np.min(EDUNUMBER_array)
    MaxEduNum = np.max(EDUNUMBER_array)
    MidEduNum = np.median(EDUNUMBER_array)
    print('Maximun, Minimun, Midian of Education number is:', MaxEduNum, MinEduNum, MidEduNum)

    for i in range(30162):
        if data.loc[i,'TempAge'] == ClusterAge and data.loc[i,'TempEducationNumber'] == ClusterEducationNumber:
            if data.loc[i,'education_num'] <= MidEduNum:
                data.loc[i,'TempEducationNumber'] = str((MinEduNum, MidEduNum))
            else:
                data.loc[i,'TempEducationNumber'] = str((MidEduNum, MaxEduNum))
    
    if MinEduNum == MidEduNum or MaxEduNum == MidEduNum:
        END = 1


def Satisfiable(data):
    data_judge = data[(data['Total_number'] <= K)]
    Number_judge = data_judge['Total_number'].sum()
    if Number_judge > 0:
        return 0
    else:
        return 1


def Mondrian(data):
    data_temp = copy.deepcopy(data)
    data_copy = copy.deepcopy(data)

    data_cluster = Cluster(data_temp)
    max = data_cluster['Total_number'].max()
    print('max cluster: ', max) 
    
    if max == 0 or END == 1:
        exit()
    

    index = data_cluster[data_cluster.Total_number == max].index.tolist()[0]  
    print('index of max cluster number: ', index)


    global flag
    if flag == 0:
        data_cluster[index,'Total_number'] = 0
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
        flag = 0
        Mondrian(data)


Mondrian(data)
Cluster(data)
