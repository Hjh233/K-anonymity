import pandas as pd
import numpy as np

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

    data_cleaned = data_nan.dropna()
    print('Data after cleaning is shown as below')
    print(data_cleaned)  # 30162 x 15
    return data_cleaned


if __name__ == '__main__':
    data = load_data()
    for key, value in data.items():
        print(f"{key} shape: {value.shape}")


# We use groupby function to find QI clusters to further discuss whether they satisfy k-anonymity
Cluster = data.groupby(QI, as_index=False).count()
Cluster_show = Cluster[(QI + Work_class)]  
''' 
    We only want to show the data with their quasi identifiers
    The last column shows the number of each QI clusters, 
    so we choose work_class which is IN the index and is a categorical attribute to expand the datafram
    Should we choose a numerical attribute, e.g. age, 
    the number of each QI clusters may be erased and replaced by it
''' 
Cluster_show.columns = ['age', 'marital_status', 'race', 'sex', 'Total_number']
# We change the name of the last column to 'Total_number'
print(Cluster_show)
Number_total = Cluster_show['Total_number'].sum() 
print('Total number of the data is : %d' % Number_total)

Cluster_suppress = Cluster_show[(Cluster_show['Total_number']<=K)]
Number_suppress = Cluster_suppress['Total_number'].sum()
print('Total number of QI clusters that do NOT satisfy k-anonymity: %d' % Number_suppress)


### Generalization

data_generalized = data

data_generalized.loc[:,'sex'] = '*'
print(data_generalized.loc[:,'sex'])


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

# print(data.loc[:,"education_num"].max())   # age: 90 education_num: 16
# print(data.loc[:,"education_num"].min())   # age: 17 education_num: 1