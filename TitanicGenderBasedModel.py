# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:25:16 2016

@author: Aditya
"""

'''
gender based model for Titanic Sinking Problem - Kaggle
'''

import numpy as np
import csv

#read training data
cfo = csv.reader(open('train.csv','rt'))
header = next(cfo)
data = []

#get the data in numpy arrays
for row in cfo:
    data.append(row)

data = np.array(data)

number_passengers = np.size(data[0::,1].astype(float))
number_survived = np.sum(data[0::,1].astype(float))
proportion_survivors = number_survived/number_passengers
#0.38383838383838381

#gender based division
women_only_stats = data[0::,4]=="female"
men_only_stats = data[0::,4]=="male"

women_onboard = data[women_only_stats,1]
men_onboard = data[men_only_stats,1]

number_women = women_onboard.size
number_men = men_onboard.size

women_survived = np.sum(women_onboard.astype(float))
men_survived = np.sum(men_onboard.astype(float))

proportion_men_survived = men_survived/number_men 
#0.18890814558058924
proportion_women_survived = women_survived/number_women
#0.7420382165605095

#read training data
tfo = csv.reader(open('test.csv','rt'))
header2 = next(tfo)

#write results as csv file
pfile = open("GBM.csv",'wt')
pfo = csv.writer(pfile)

pfo.writerow(["PassengerId", "Survived"])

for row in tfo:    
    if row[3] == "female":
        pfo.writerow([row[0],1])
    else:
        pfo.writerow([row[0],0])

pfile.close()