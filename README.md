# K-anonymity
K-anonymity is a property possessed by certain anonymized data. The concept of k-anonymity was first introduced by Latanya Sweeney and Pierangela Samarati in a paper published in 1998 as an attempt to solve the problem: "Given person-specific field-structured data, produce a release of the data with scientific guarantees that the individuals who are the subjects of the data cannot be re-identified while the data remain practically useful." A release of data is said to have the k-anonymity property if the information for each person contained in the release cannot be distinguished from at least k - 1 individuals whose information also appear in the release(Cited from [Wikipedia](https://en.wikipedia.org/wiki/K-anonymity)). Here we implement k-anonymity via two algorithms: Samarati and Mondian and have further discussions about what difference does it make with different parameters, e.g., k and MaxSup.
## Introduction
Sweeney demonstrated that releasing a data table by simply removing identifiers can seriously breach the privacy of individuals whose data are in the table. By combinig a public voter registration list and a released medical database of health insurance information, she was able to identify the medical record of the governor of Massachusetts.  
We give the definition of k-anonymity as follows:

**Definition 1: _k-Anonymity_** : Given a set of QI attributes ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
, release candidate ![](http://latex.codecogs.com/svg.latex?D^{\ast}) is said to be k-anonymous with respect to ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
 if each unique tuple in the projection of ![](http://latex.codecogs.com/svg.latex?D^*)
 on ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
 occurs at least k times.  
 To implement _k-anonymity_, we have the following two algorithms proposed by Samarati, Mondrian. 
 
 ### Samarati
 For Algorithm 1 (Samarati) which deals with multiple categotical attributes, basic idea can be illustrated as follows:
 1. Define the hierarchy of generealization and Construct a Lattice.
 2. For instance, the distance vector corresponding to a generalized table with hierarchy <![](http://latex.codecogs.com/svg.latex?X_1), ![](http://latex.codecogs.com/svg.latex?Y_1)> is [1,1]
 3. Given the constraint that the generalized table must satisfy k-anonymity and that the deleted records is less than MaxSup, we need to set the sum of all the distance vectors as small as possible.

Consequently, we use bisection method to complete the process: For a lattice with its maximun height h, we determine whether the nodes with height h/2 is k-anonymous. If so, we proceed with the nodes with height h/4, otherwise we check the nodes with height 3h/4. We repeat the above process until the layer with minimun height satisfying k-anonymity is found.

We give specific generalizaiton hierarchy according to the generalization hierarchy given in adult_.txt as below.
![image](https://github.com/Hjh233/K-anonymity/blob/main/Image/2.PNG)



