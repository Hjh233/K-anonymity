# K-anonymity
K-anonymity is a property possessed by certain anonymized data. The concept of k-anonymity was first introduced by Latanya Sweeney and Pierangela Samarati in a paper published in 1998 as an attempt to solve the problem: "Given person-specific field-structured data, produce a release of the data with scientific guarantees that the individuals who are the subjects of the data cannot be re-identified while the data remain practically useful." A release of data is said to have the k-anonymity property if the information for each person contained in the release cannot be distinguished from at least k - 1 individuals whose information also appear in the release.\footnote{Quote from Wikipedia} Here we implement k-anonymity via two algorithms: Samarati and Mondian and have further discussions about what difference does it make with different parameters, e.g., k and MaxSup.
## Introduction
Sweeney demonstrated that releasing a data table by simply removing identifiers can seriously breach the privacy of individuals whose data are in the table. By combinig a public voter registration list and a released medical database of health insurance information, she was able to identify the medical record of the governor of Massachusetts.  
We give the definition of k-anonymity as follows:  
**_k-Anonymity_** : Given a set of QI attributes ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
, release candidate ![](http://latex.codecogs.com/svg.latex? D^*)
 is said to be k-anonymous with respect to ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
 if each unique tuple in the projection of ![](http://latex.codecogs.com/svg.latex? D^*)
 on ![](http://latex.codecogs.com/svg.latex?Q_1), ![](http://latex.codecogs.com/svg.latex?\dots), ![](http://latex.codecogs.com/svg.latex?Q_d)
 occurs at least k times.
![](http://latex.codecogs.com/svg.latex? D^{\ast})


