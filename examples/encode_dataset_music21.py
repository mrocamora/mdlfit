# encoding: utf-8

"""
Quick encoding dataset


"""

from mdlfit.dataio import encode_dataset21

#dataset_name = 'airdsAirs'
dataset_name = 'oneills1850'
#dataset_name = 'EssenFolksong'

dataset, dataset_pre = encode_dataset21(dataset_name, signature='4/4', beat_subdivisions=2)

print(len(dataset_pre))

for piece in dataset_pre:
	print(piece["name"], len(piece["measures"]))


print(len(dataset))

for piece in dataset:
	print(piece["name"], len(piece["measures"]))


