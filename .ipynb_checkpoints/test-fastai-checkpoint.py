import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

from fastai.data.all import *
from fastai.vision.all import *

print("fastai installed successfully!")


df = pd.read_csv('train.csv')
print(df.head())

cards = DataBlock(blocks=(ImageBlock, MultiCategoryBlock),
                  splitter=RandomSplitter(valid_pct=0.2, seed=42),
                  get_x=ColReader(0, pref=''),
                  get_y=(ColReader(1, label_delim=' ')),
                  item_tfms=Resize(224),
                  batch_tfms=aug_transforms())

dls = cards.dataloaders(df)
dls.show_batch()