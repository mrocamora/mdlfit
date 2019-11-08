# encoding: utf-8

"""
Quick reading  dataset


"""



import sys 
sys.path.append('/home/veronica/Matemática/Articulos/Modelos_Ritmo_2019/mdlfit/')
import mdlfit
from mdlfit.dataio import load_encoded_dataset
filename = '/home/veronica/Matemática/Articulos/Modelos_Ritmo_2019/mdlfit/data/encoded/tango_dataset_24_2.pkl'
load_encoded_dataset(filename)

