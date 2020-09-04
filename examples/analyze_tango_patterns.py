#!/usr/bin/env python3
# encoding: utf-8
# pylint: disable=C0103
'''
    __  __ _____  _      ______ _____ _______
   |  \/  |  __ \| |    |  ____|_   _|__   __|
   | \  / | |  | | |    | |__    | |    | |
   | |\/| | |  | | |    |  __|   | |    | |
   | |  | | |__| | |____| |     _| |_   | |
   |_|  |_|_____/|______|_|    |_____|  |_|

 music encodind using minimum description length


Load encoded dataset from a pickle file

'''

import sys
import argparse
from mdlfit.dataio import load_encoded_dataset

#load tango dataset

dataset = load_encoded_dataset('../data/encoded/' + 'tango_songbook_44_2.pkl')

#find measures [1,1,1,1,1,0,0,0] and [1,0,0,0,1,1,1,1]
#ref1 = [1,1,1,1,1,1,0,1]
#ref2 = [1,1,0,1,1,1,1,1]
ref1 = [1,0,1,0,1,0,0,0]
ref2 = [1,0,0,0,1,0,1,0]


count1 = 0
count2 = 0

for i in range(len(dataset)):
	for measure in dataset[i]['measures']:
		if sum(measure == ref1) == 8:
			count1 += 1
		elif sum(measure == ref2) == 8:
			count2 += 1

print("Cantidad de patrones:")  
print(ref1, count1)
print(ref2, count2)

