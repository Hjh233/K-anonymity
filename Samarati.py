import numpy as np
import pandas as pd
import time
import copy

Attributes = ['age', 'work_class', 'final_weight', 'education',
            'education_num', 'marital_status', 'occupation', 'relationship',
            'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week',
            'native_country', 'class' ]
QI = ['age', 'marital_status', 'race', 'sex']
SV = ['occupation']
K = 10
MaxSup = 10
Work_class = ['work_class']

star = '*'

Sex = ['*']

Race = ['*']

Marital_status = ['Married-spouse-absent','Widowed','Separated','Divorced',
                  'Married-civ-spouse','Married-AF-spouse','Never-married']

Marital_status_G1 = ['Alone','Leave','Married','NM']

Marital_status_G2 = ['*']

# print(data.loc[:,"age"].max())   # age_max: 90 
# print(data.loc[:,"age"].min())   # age_min: 17 

Age = [{(16,20),(21,25),(26,30),(31,35),(36,40),(41,45),(46,50),(51,55),
        (56,60),(61,65),(66,70),(71,75),(76,80),(81,85),(86,90),(91,95)},
        {(16,25),(26,35),(36,45),(46,55),(56,65),(66,75),(76,85),(86,95)},
        {(16,35),(36,55),(56,75),(76,95)}]

LM = np.zeros(50)

### Lattice Construction

''' 
    We store the Lattice in the form of list, each item (distance) in the form of a vector
    Initialization of Lattice 
    without which the list is empty and we can NOT add elements to the list due to 'list index out of range'
'''
Lattice = [{(0,0,0,0)},{(0,0,0,0)},{(0,0,0,0)},
    {(0,0,0,0)},{(0,0,0,0)},{(0,0,0,0)},
    {(0,0,0,0)},{(0,0,0,0)},{(0,0,0,0)}]

'''
    Note that each element in the tuple is set in the formulation of 
    (Layer_sex,Layer_race,Layer_marital_status,Layer_age)
    each with the layer of 0-1, 0-1, 0-2, 0-4 
    layer = 0 means data is not generalized, layer = top means the attribute is generalized to *
'''
for Layer_sex in range(2):
    for Layer_race in range(2):
        for Layer_marital_status in range(3):
            for Layer_age in range(5):
                Lattice[Layer_age + Layer_marital_status + Layer_race + Layer_sex].add((Layer_sex,Layer_race,Layer_marital_status,Layer_age))

'''
    We delete (0,0,0,0) of Lattice[1:9], which was introduced just to make the initialization job
    and by doing so we have the final Lattice
 '''
for i in range(8):
    Lattice[i + 1].remove((0,0,0,0))

# print(Lattice)

'''
    We proceed to traverse every set (element of Lattice)
    Note: There is no index of set in Python
'''

# for vector in Lattice[3]:
#     print(vector[1])

### Loading data
def load_data(data_path = "C:\\Users\\82581\\Desktop\\adult.data"):

    data_original = pd.read_csv(data_path, sep = ', ', engine = 'python', header = None, names = Attributes)

    '''
    ParserWarning: Falling back to the 'python' engine 
    because the 'c' engine does not support regex separators
    (separators > 1 char and different from '\s+' are interpreted as regex); 
    you can avoid this warning by specifying engine='python'.
    We therefore add engine = 'python' 
    '''

    print('Original data is shown as below')
    print(data_original)   # 32561 x 15

    data_nan = data_original.replace('?', np.nan)
    # We replace ? with np.nan, which can be detected and deleted automatically via dropna

    data_cleaned = data_nan.dropna().reset_index(drop = True)
    # We create a new datafram from index 0 to index 30161
    print('Data after cleaning is shown as below')
    print(data_cleaned)  # 30162 x 15
    return data_cleaned


def GeneralizeAge(i,G):
    if G != 4:
        for vector in Age[G-1]:
            if vector[0] <= i and vector[1] >= i:
                break
        return str(vector)  
        '''
        Should we directly return vector, which is in the form of tuple, 
        we can NOT replace 'age' column of the original datafram (dtype: object)
        and we will have system error: Must have equal len keys and value when setting with an iterable
        Yet, by converting tuple to str, we can complete the aforementioned job
        '''
    else:
        return star

def GeneralizeSex(str,G):
    if G == 1:
        return star
    else:
        return str

def GeneralizeRace(str,G):
    if G == 1:
        return star
    else:
        return str


def LocMaritalStatus(str):
    for index in range(7):
        if str == Marital_status[index]:
            break
        else:
            index = index + 1
    return index    

def GeneralizeMarital(str,G):
    if G == 2:
        return star
    if G == 1:
        index = LocMaritalStatus(str)
        return Marital_status_G1[int(index/2)]
    else:
        return str


def Generalize(Table_original,hierarchy):
    # The contents of hierarchy is Sex, Race, Marital status, Age respectively
    Table = copy.deepcopy(Table_original)

    '''
        Note!!!
        In python, when applying '=', e.g. a = b, we will change the value of b if we change a
        That is, if we do nothing about it, the table will change after one generalization, 
        which will cause LOTS OF trouble.
        Therefore, we use copy.deepcopy() to avoid things like that from happening.
    '''

    # Generaliaztion of Sex
    if hierarchy[0] != 0:
        Table.loc[:,'sex'] = GeneralizeSex(Table.loc[:,'sex'],hierarchy[0])

    '''
        Compared with the process of marital status and age, 
        where we proceed via traversal with i ranging from 0 to 30161,
        we can achieve much faster speed via [:,'sex'].
        Yet, because there are more than one hierarchy w.r.t. marital status and age,
        and the fact that we only deal with one variable in the function,
        we have to process the data one by one, slowing down the speed dramatically.
    '''

    # Generaliaztion of Race
    if hierarchy[1] != 0:
        Table.loc[:,'race'] = GeneralizeRace(Table.loc[:,'race'],hierarchy[1])

    # Generaliaztion of Marital Status
    if hierarchy[2] != 0:
        for i in range(30162):
            Table.loc[i,'marital_status'] = GeneralizeMarital(Table.loc[i,'marital_status'],hierarchy[2])

    # Generalization of Age
    if hierarchy[3] != 0:
        for i in range(30162):
            Table.loc[i,'age'] = GeneralizeAge(Table.loc[i,'age'],hierarchy[3])
    
    return Table

### Clustering

def Cluster(data):
    data_generalized = copy.deepcopy(data)
    Cluster_generalized = data_generalized.groupby(QI, as_index=False).count()
    # We use groupby function to find QI clusters to further discuss whether they satisfy k-anonymity
    Cluster_generalized_show = Cluster_generalized[(QI + Work_class)]  

    Cluster_generalized_show.columns = ['age', 'marital_status', 'race', 'sex', 'Total_number']
    # We change the name of the last column to 'Total_number'
    print(Cluster_generalized_show)
    Number_generalized_total = Cluster_generalized_show['Total_number'].sum() 
    print('Total number of the data after generaliation is : %d' % Number_generalized_total)

    Cluster_generalized_suppress = Cluster_generalized_show[(Cluster_generalized_show['Total_number']<=K)]
    Number_generalized_suppress = Cluster_generalized_suppress['Total_number'].sum()
    print('Total number of QI clusters after generalization that do NOT satisfy k-anonymity: %d' % Number_generalized_suppress)

    return Number_generalized_suppress


def Releasable(num):
    if num <= MaxSup:
        print('The generalized table is releasable!')
        return 1
    else:
        print('We can NOT release current table.')
        return 0


def LossMetric(hierarchy):
    # Loss when generalizing sex
    if hierarchy[0] == 0:
        LossSex = 0
    else:
        LossSex = 1

    # Loss when generalizing race
    if hierarchy[1] == 0:
        LossRace = 0
    else:
        LossRace = 1

    # Loss when generalizing marital status
    if hierarchy[2] == 0:
        LossMarital = 0
    if hierarchy[2] == 2:
        LossMarital = 1
    if hierarchy[2] == 1:
        LossMarital = (1/6) * ((30162 - 9726)/30162)  
        # Never-married is generalized to NM, which does not lose any information, meaning loss = 0

    # Loss when generalizing age
    if hierarchy[3] == 0:
        LossAge = 0
    if hierarchy[3] == 1:
        LossAge = 1/16
    if hierarchy[3] == 2:
        LossAge = 1/8
    if hierarchy[3] == 3:
        LossAge = 1/4
    if hierarchy[3] == 4:
        LossAge = 1
    
    LossTotal = LossSex + LossRace + LossMarital + LossAge

    return LossTotal


def Samarati(data,Lattice,LMRV):
    low = 0
    high = 8
    ReleaseNum = 0
    while (low < high):
        mid = int((low + high)/2)
        for VECTOR in Lattice[mid]:
            GTC = Generalize(data, VECTOR)  # Generalized table candidate
            if Releasable(Cluster(GTC)) == 0:
                low = mid + 1
            else:
                ReleaseVector = copy.deepcopy(VECTOR)
                # LMRV[ReleaseNum] = LossMetric(ReleaseVector)
                # ReleaseNum = ReleaseNum + 1
                high = mid

    return ReleaseVector



if __name__ == '__main__':
    data = load_data()
    # for key, value in data.items():
    #     print(f"{key} shape: {value.shape}")


begin = time.time()

VectorCandidate = Samarati(data, Lattice, LM)
print('One possible hierarchy is given below: ')
print(VectorCandidate)

LossVC = LossMetric(VectorCandidate)
print('The loss metric of it is: %.5f' %LossVC)

GT = Generalize(data,VectorCandidate)  # Generalized Table
print('Table with quasi-indentifiers after generalization is shown as below: ')
print(GT.loc[:,QI])
print('Full table after generalization is shown as below')
print(GT)

end = time.time()

print('Total generalization time:', end - begin)

LocSup = Cluster(GT)  # Local Suppression
print('MAX SUPPRESSION NUMBER: ', LocSup)

Releasable(LocSup)



