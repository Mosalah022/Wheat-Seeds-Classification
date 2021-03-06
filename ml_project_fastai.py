# -*- coding: utf-8 -*-
"""ML_Project_FastAi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l97wSTs6bV8GfleYOqaWEtaR-xJyWq2L
"""

#hide
#skip
! [ -e /content ] && pip install -Uqq fastai  # upgrade fastai on colab
!gdown --id 1MbUWPsEZJ_Dana5RC07wUGTIgzN92Uld

#hide
from fastai.tabular.all import *

#hide
filename = "seeds.csv"
path = Path("/content/")

"""#Cover Page
### Developed by:
*   Mohamed Salah Eldin - 41810303
*   Fatma Mohamed - 41810121


"""





"""# Problem Definition
**This data was acquired from the 'UCI Center for Machine Learning' repository. It contains seven variables for three distinct types of wheat kernels: (Kama, Rosa, Canadian) designated as numerical variables 1, 2 & 3 respectively The last column is reserved for the Kernel type.**
"""

df = pd.read_csv(filename)
df.head()

"""# Method
In order to accomplish accurate classification easily and quickly, we've opted for the FastAI library as it has excellent support for tabular data and makes cutting edge mdoels and techniques readily available.

We use 20% of the dataset for validation, and the seed has been set to 123 to ensure that the dataset is split in the same way each time the code is run, to ensure repeatability.

We've set it to normalize any continuous data (All fields), fill any missing fields and to categorify our variables (Type).

We've identified which columns are discrete and which are continuous too.
"""

seed = 123
use_seed = True;

splits = RandomSplitter(valid_pct=0.4, seed=seed)(range_of(df))
procs=[Categorify, FillMissing, Normalize]

cat_names=["Type"]
cont_names = ['Area','Perimeter','Compactness','Kernel.Length',
           'Kernel.Width','Asymmetry.Coeff','Kernel.Groove']

cont,cat = cont_cat_split(df, 1, dep_var='Type')

to = TabularPandas(df, procs=procs, cont_names=cont, cat_names=cat,
                   y_names='Type', splits=splits)

if use_seed: set_seed(seed, True)

"""The batch size is set to 22. After experimentation we found that this batch size provided good accuracy after 10 epochs or so.

Decreasing the batch size leads to faster training and overfitting, but also gives over all lower accuracy.
"""

dls = to.dataloaders(bs=22)
if use_seed: dls.rng.seed(seed, True)

dls.show_batch()

"""# Experiment
A FastAI tabular learner object is instantiated. By default tabular learners have 2 hidden layers with 200 and 100 activations respectively, this was changed to 1000 and 00 activations respectively as that gave on average 1-2% better accuracy. Adding more hidden layers did not seem to provide any significant advantages.
"""

learn = tabular_learner(dls, metrics=accuracy_multi, layers=[1000,50])

"""lr_find does mock training over a large range of learning rates and graphs the loss for us. As per the recommendations in the fastai documentation for 1cycle, we pick a maximum learning rate that is an order of magnitude below the minima."""

learn.lr_find()

"""We're using the 1cycle technique to fit our model here, this is a relatively new technique that allows you to get convergence with less epochs. It works by varying the learning rate throughout the duration of the training."""

learn.fit_one_cycle(20, lr_max=1e-2)

"""We can see that overfitting starts happening after epoch 10~, though it is not significant."""

learn.recorder.plot_loss()

"""Below is a table that shows the predictions the trained model made on a few rows from the training dataset."""

learn.show_results()

"""Below some example code is provided that does inference on one row. Feel free to modify it."""

df.iloc[50]

df.iloc[50] = [15.26,14.84,0.871,5.763,3.312,2.221,5.22,3]

row, clas, probs = learn.predict(df.iloc[50])

row.show()

clas, probs