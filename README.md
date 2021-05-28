# K-anonymity
K-anonymity is a property possessed by certain anonymized data. The concept of k-anonymity was first introduced by Latanya Sweeney and Pierangela Samarati in a paper published in 1998 as an attempt to solve the problem: "Given person-specific field-structured data, produce a release of the data with scientific guarantees that the individuals who are the subjects of the data cannot be re-identified while the data remain practically useful." A release of data is said to have the k-anonymity property if the information for each person contained in the release cannot be distinguished from at least k - 1 individuals whose information also appear in the release(Cited from [Wikipedia](https://en.wikipedia.org/wiki/K-anonymity)). Here we implement k-anonymity via two algorithms: Samarati and Mondian and have further discussions about what difference does it make with different parameters, e.g., k and MaxSup.
## Introduction
Sweeney[1] demonstrated that releasing a data table by simply removing identifiers can seriously breach the privacy of individuals whose data are in the table. By combinig a public voter registration list and a released medical database of health insurance information, she was able to identify the medical record of the governor of Massachusetts. This kind of attack is called _linking attack_. To protect data from linking attacks, Samaratia and Sweeney proposed _k-anonymity_ [1,2]. 

We give the definition of k-anonymity as follows:

**Definition 1: _k-Anonymity_** : Given a set of QI attributes ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
, release candidate ![](http://latex.codecogs.com/svg.latex?D^{\ast}) is said to be k-anonymous with respect to ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
 if each unique tuple in the projection of ![](http://latex.codecogs.com/svg.latex?D^*)
 on ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
 occurs at least k times.  
 
 To implement _k-anonymity_, we have the following two algorithms proposed by Samarati[2], Mondrian[3]. 
 
 ## Data
 There are 32561 rows in the original data which may contain missing items. After cleaning, there are 30162 rows in total.
 
 You can find original source via https://archive.ics.uci.edu/ml/datasets/adult.

 ## Algorithm
 ### Samarati
 For Algorithm 1 (Samarati) which deals with multiple categotical attributes, basic idea can be illustrated as follows:
 1. Define the hierarchy of generealization and Construct a Lattice.
 2. For instance, the distance vector corresponding to a generalized table with hierarchy <![](http://latex.codecogs.com/svg.latex?X_1), ![](http://latex.codecogs.com/svg.latex?Y_1)> is [1,1]
 3. Given the constraint that the generalized table must satisfy k-anonymity and that the deleted records is less than MaxSup, we need to set the sum of all the distance vectors as small as possible.

Consequently, we use bisection method to complete the process: For a lattice with its maximun height h, we determine whether the nodes with height h/2 is k-anonymous. If so, we proceed with the nodes with height h/4, otherwise we check the nodes with height 3h/4. We repeat the above process until the layer with minimun height satisfying k-anonymity is found.

We give specific generalizaiton hierarchy according to the generalization hierarchy given in adult_.txt as below.
![image](https://github.com/Hjh233/K-anonymity/blob/main/Image/1.PNG)
![image](https://github.com/Hjh233/K-anonymity/blob/main/Image/2.PNG)

### Mondrian
For algorithm 2 (Mondrian) which deals with multiple numerical attributes, basic idea can be illustrated as folllows:
1. Choose one attribute for every partition, you can choose the attribute with maximum range or just randomly pick one.
2. Find the median of the selected attribute and split the partition. There are 2 ways of doing partitioning, strict partitioning and relax partitioning respectively.
   * Say we set k = 2, and we have a dataset = [1,2,3,3,4,5]
   * For strict partitioning, we have the split dataset as [1,2,3,3],[4,5]. That is, we place all the median to one bucket.
   * For relax partitioning, we have the split dataset as [1,2,3],[3,4,5]. That is, we try to make the partitioned dataset as even as possible.
3. Repeat the process above until every cluster is k-anonymous and no more partitioning is allowed.  

There are still some details to be illustrated: After partitioning the maximum cluster, we need to judge whether the partitioned ones are k-anonymous or not. If so, we proceed. If not, we set the table the way it used to be before partitioning and tag the maximum cluster to show that the cluster cannot be partitioned.  

You can find quite detailed information about Mondrian from https://github.com/qiyuangong/Mondrian

## Utility
We now discuss how to use loss metric to measure the utility of data after sanitization (here we use generlization). Normally, we would like the utility of sanitized data to be as big as possible so long as the release data meets relevant privacy criterion.  

We give the definition of Loss Metric as follows:

**Definition 2: _Loss metric_** : LM is defined in terms of a normalized loss for each attribute of every tuple. For a tuple t and categorical attribute A, suppose the value of t[A] has been generalized to x. Letting |A| represent the size of the domain of attribute A and letting M represent the number of values in this domain that could have been generalized to x, then the loss for t[A] is (M − 1)/(|A| − 1). The loss for attribute A is defined as the average of the loss t[A] for all tuples t. The LM for the entire data set is defined as the sum of the losses for each attribute.

Samarati guarantees that we find the final hierarchy with its height minimized. Under such constraint, however, there may still be multiple solutions. Now we seek to find the 'optimal' output with its utility maximized, that is, its loss metric minimized (here we consider it a proper method to evaluate the output). We give our way to find the optimal output as follows:

We initialize 2 lists: HierarchyVector = [], LMHV = [] , to record the hierarchy vectors that can be used to generalize the data satisfying k-anonymity and their loss metric respectively. We only need to find the index of minimum in LMHV, and then we can find the hierarchy that minimize the loss metric simply by getting the value of HierarchyVector[index]. Relevent code is shown as below.

```
def Samarati(data,Lattice,LM,HV): # Hierarchy Vector
    low = 0
    high = 8
    while (low < high):
        mid = int((low + high)/2)
        for VECTOR in Lattice[mid]:
            GTC = Generalize(data, VECTOR)  # Generalized table candidate
            if Releasable(Cluster(GTC)) == 0:
                low = mid + 1
            else:
                ReleaseVector = copy.deepcopy(VECTOR)
                HV.append(ReleaseVector) # NEW!
                SupNum = Cluster(data) # NEW!
                LM.append(LossMetric(ReleaseVector, SupNum)) # NEW!
                high = mid

    Min = min(LM) # NEW!
    MinIndex = LM.index(Min) # NEW!

    ReleaseVector = HV[MinIndex] # NEW!

    return ReleaseVector 
 ```
    
   
## More Information
 [1] Sweeney, Latanya. “Datafly: A System for Providing Anonymity in Medical Data.” Proceedings of the IFIP TC11 WG11.3 Eleventh International Conference on Database Securty XI: Status and Prospects, 1997, pp. 356–381.  
 [2] Samarati, P. “Protecting Respondents Identities in Microdata Release.” IEEE Transactions on Knowledge and Data Engineering, vol. 13, no. 6, 2001, pp. 1010–1027.  
 [3] LeFevre, K., et al. “Mondrian Multidimensional K-Anonymity.” 22nd International Conference on Data Engineering (ICDE’06), 2006, pp. 25–25.
 
## Support
 Since this is the first time I learned how to tackle with literally large amount of data, I did not consider how to improve the performance of the code. The code I provide is quite slow. I would be very much appreciated if you can make improvements on the code.
 
 Contribution via [Pull Requests](https://github.com/Hjh233/K-anonymity/pulls) is appreciated!
 
