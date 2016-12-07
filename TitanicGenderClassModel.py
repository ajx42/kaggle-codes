# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:03:05 2016

@author: Aditya
"""

'''
gender, class and price bracket based model for Titanic Sinking Problem - Kaggle
'''

import numpy as np
import csv

cfo = csv.reader(open('train.csv','rt'))
header = next(cfo)

data = []
for row in cfo:
    data.append(row)
data = np.array(data)

fare_ceiling = 40
data[data[0::,9].astype(np.float) >= fare_ceiling, 9] = 39.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling/fare_bracket_size

number_of_classes = len(np.unique(data[0::,2]))

survival_table = np.zeros((2,number_of_classes, number_of_price_brackets))

for i in range(number_of_classes):
    for j in range(int(number_of_price_brackets)):
        women_only_stats = data[\
        (data[0::,4]=="female")&\
        (data[0::,2].astype(np.float) == i+1)&\
        (data[0:,9].astype(np.float) >= j*fare_bracket_size)&\
        (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size),1]
        men_only_stats = data[\
        (data[0::,4]=="male")&\
        (data[0::,2].astype(np.float) == i+1)&\
        (data[0:,9].astype(np.float) >= j*fare_bracket_size)&\
        (data[0:,9].astype(np.float) < (j+1)*fare_bracket_size),1]
        survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))
        survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float))

survival_table[survival_table!=survival_table] = 0
survival_table[survival_table < 0.5] = 0
survival_table[survival_table >= 0.5] = 1

tfo = csv.reader(open('test.csv','rt'))
pfile = open('GCM.csv','wt')
pfo = csv.writer(pfile)
pfo.writerow(['PassengerId', 'Survived'])
header2 = next(tfo)

testdata = []
for row in tfo:
    testdata.append(row)

testdata = np.array(testdata)

for row in testdata:
    k = -1
    try: k = float(row[8])
    except:
        bf = 3 - float(row[1])
    if k!=-1:    
        if k > 40:
            k = 39
            bf = 3
        else:
            if k >= 0 and k < 10:
                bf = 0
            if k >= 10 and k < 20:
                bf = 1
            if k >= 20 and k < 30:
                bf = 2
            if k >= 30:
                bf = 3
    if row[3] == "female":
        gender = 0
    else:
        gender = 1
    clss = float(row[1]) - 1
    pfo.writerow([row[0], int(survival_table[gender, clss, bf])])

pfile.close()