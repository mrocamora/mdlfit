# encoding: utf-8

"""
Quick encoding dataset


"""
from mdlfit.dataio import encode_dataset21
from mdlfit.dataio import save_encoded_dataset


dataset_name = 'airdsAirs'
#dataset_name = 'oneills1850'
#dataset_name = 'EssenFolksong'

dataset = encode_dataset21(dataset_name, signature='4/4', beat_subdivisions=2)

print(len(dataset))

#for ind, piece in enumerate(dataset):
#	print(ind, piece["title"], len(piece["measures"]))

#save_encoded_dataset(dataset, dataset_name+"_44_2.pkl")