# encoding: utf-8

"""
Quick encoding dataset


"""

from mdlfit.dataio import encode_dataset
from mdlfit.dataio import save_encoded_dataset

general_path = '../data/'
#folder = 'tango_short'
folder = 'tango_songbook'

dataset = encode_dataset(general_path + folder + "/", signature='4/4', beat_subdivisions=2)

print(len(dataset))

for ind, piece in enumerate(dataset):
	print(ind, piece["dataset"], piece["title"], len(piece["measures"]))

save_encoded_dataset(dataset, folder+"_44_2.pkl")