# Models Package

1- Ridge Regression: Extends SKLearns Ridge regression by adding p-values, featureSelection and alpha optimisation.

Example Usage:

# Import
from model_arena.Regression import RidgeRegression

# Create a RidgeRegression object
rm = RidgeRegression()

# Run the feature selection method as above to limit to the most important variables. 
# Stores the order of variables to the object
rm.featureSelection(X,y)

# Find the value of alpha minimising MSE for these features
rm.findBestAlpha(X[rm.bestMeanCVModel],y)

# Print the alpha
print('Alpha = {}'.format(rm.alpha))

# Fit the model with the best features and the alpha
rm.fit(X[rm.bestMeanCVModel],y)

# Display a summary including p-values
rm.summary(X[rm.bestMeanCVModel],y)