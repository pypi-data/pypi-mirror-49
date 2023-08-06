# Models Package

1- Ridge Regression: Extends SKLearns Ridge regression by adding p-values, featureSelection and alpha optimisation.

## Example Usage:

### Import
from model_arena.Regression import RidgeRegression

### Create a RidgeRegression object
rm = RidgeRegression()

### Run the feature selection method as above to limit to the most important variables. 
### Stores the order of variables to the object
rm.featureSelection(X,y)

### Find the value of alpha minimising MSE for these features
rm.findBestAlpha(X[rm.bestMeanCVModel],y)

### Print the alpha
print('Alpha = {}'.format(rm.alpha))

### Fit the model with the best features and the alpha
rm.fit(X[rm.bestMeanCVModel],y)

### Display a summary including p-values
rm.summary(X[rm.bestMeanCVModel],y)


## To Update PYPI

1- Clone from github

2- Make Changes

3- Update version number in setup.py

4- CD into the setup.py directory

5- Run the following in the CMD:
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
or
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel

6- Then the following in the CMD:
python3 -m pip install --user --upgrade twine
python3 -m twine upload dist/*
or
python -m pip install --user --upgrade twine
python -m twine upload dist/*

7- Test by pip install and importing





