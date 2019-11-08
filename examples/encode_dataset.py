# encoding: utf-8

"""
Quick encoding dataset


"""

import sys 
sys.path.append('/home/veronica/Matemática/Articulos/Modelos_Ritmo_2019/mdlfit/')
import mdlfit
from mdlfit.dataio import encode_dataset
general_path = '/home/veronica/Matemática/Articulos/Modelos_Ritmo_2019/mdlfit/data/'
folder = 'tango_dataset_short/'
encode_dataset(general_path + folder)
