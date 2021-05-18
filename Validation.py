import pandas as pd
import numpy as np
import time

tuple = (1,1,2,2)

star = '*'

Sex = [('*')]

Race = [('*')]

Marital_Status = [{('Alone'),('Leave'),('Married'),('NM')},{('*')}]

Age = [{(16,20),(21,25),(26,30),(31,35),(36,40),(41,45),(46,50),(51,55),
        (56,60),(61,65),(66,70),(71,75),(76,80),(81,85),(86,90),(91,95)},
        {(16,25),(26,35),(36,45),(46,55),(56,65),(66,75),(76,85),(86,95)},
        {(16,35),(36,55),(56,75),(76,95)}]


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


def Generalize(Table,hierarchy):
    # The contents of hierarchy is Sex, Race, Marital status, Age respectively

    # Generaliaztion of Sex
    if hierarchy[0] != 0:
        for i in range(30162):
            Table.loc[i,'sex'] = GeneralizeSex(Table.loc[i,'sex'],hierarchy[0])

    # Generaliaztion of Race
    if hierarchy[1] != 0:
        for i in range(30162):
            Table.loc[i,'race'] = GeneralizeRace(Table.loc[i,'race'],hierarchy[1])

    # Generalization of Age
    if hierarchy[3] != 0:
        for i in range(30162):
            Table.loc[i,'age'] = GeneralizeAge(Table.loc[i,'age'],hierarchy[3])
    
    return Table


Attributes = ['age', 'work_class', 'final_weight', 'education',
            'education_num', 'marital_status', 'occupation', 'relationship',
            'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week',
            'native_country', 'class' ]
QI = ['age', 'marital_status', 'race', 'sex']
SV = ['occupation']
K = 10
MaxSup = 20
Work_class = ['work_class']
Race = ['race']

### Loading data
def load_data(data_path = "C:\\Users\\82581\\Desktop\\adult.data"):

    data_original = pd.read_csv(data_path, sep = ', ', engine = 'python', header = None, names = Attributes)

    print('Original data is shown as below')
    print(data_original)   # 32561 x 15

    data_nan = data_original.replace('?', np.nan)
    # We replace ? with np.nan, which can be detected and deleted automatically via dropna

    data_cleaned = data_nan.dropna().reset_index(drop = True)
    print('Data after cleaning is shown as below')
    print(data_cleaned)  # 30162 x 15
    return data_cleaned

if __name__ == '__main__':
    data = load_data()
    for key, value in data.items():
        print(f"{key} shape: {value.shape}")


begin = time.time()

GT = Generalize(data,tuple)
print(GT.loc[:,QI])

end = time.time()

print('Total generalization time:', end - begin)
