# encoding: utf-8

"""
Quick encoding dataset


"""
import mdlfit as mf

# dataset parameters
dataset_folder = '../data/tango_songbook/'
# dataset signature
signature = '4/4'
# subdivision per beat
beat_subdivisions = 2

dataset = mf.dataio.encode_dataset(dataset_folder, signature=signature,
                                   beat_subdivisions=beat_subdivisions)

# fit Bernoulli model
model1 = mf.models.Bernoulli(dataset)
# fit Bernoulli model
model1 = mf.models.Bernoulli(dataset, d=2**6)
# fit Postion model
model2 = mf.models.Position(dataset, signature, beat_subdivisions)
# fit Postion model
model2 = mf.models.Position(dataset, signature, beat_subdivisions, d=2**6)
# fit Refined Postion model
model3 = mf.models.RefinedPosition(dataset)
# fit Refined Postion model
model3 = mf.models.RefinedPosition(dataset, d=2**6)
# fit Hierarchical model
model4 = mf.models.Hierarchical(dataset, signature, beat_subdivisions)
# fit Hierarchical model
model4 = mf.models.Hierarchical(dataset, signature, beat_subdivisions, d=2**6)
# fit Refined Hierarchical model
model5 = mf.models.RefinedHierarchical(dataset, signature, beat_subdivisions)
# fit Refined Hierarchical model
model5 = mf.models.RefinedHierarchical(dataset, signature, beat_subdivisions, d=2**6)


print("="*10)
model1.show()
print("="*10)
model2.show()
print("="*10)
model3.show()
print("="*10)
model4.show()
print("="*10)
model5.show()
print("="*10)