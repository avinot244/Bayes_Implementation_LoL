import pandas as pd
from sklearn.datasets import load_iris
from factor_analyzer.factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

df = pd.read_csv("./bfi.csv")
df.drop(['gender', 'education', 'age'], axis=1, inplace=True)   # Dropping unnecessary columns
df.dropna(inplace=True)                                         # Dropping missing values rows

# print(df.info())

# Testing if we can use factor analysis on our dataset
chi_square_value,p_value=calculate_bartlett_sphericity(df)      # if p=0 we goood
print(chi_square_value, p_value)

kmo_all,kmo_model=calculate_kmo(df)                             # if kmo_model > 0.6 we good
print(kmo_model)


# Choosing the amount of factors
fa = FactorAnalyzer(rotation=None, n_factors=25)
fa.fit(df)

ev, v = fa.get_eigenvalues() # Count the amount of eigenvalues greater than one to know the amount of factor we will use why ?

plt.scatter(range(1,df.shape[1]+1),ev)
plt.plot(range(1,df.shape[1]+1),ev)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()
plt.savefig("screeplot.png")

# Performing factor analysis
fa = FactorAnalyzer(rotation="varimax", n_factors=5)
fa.fit(df)
print(fa.loadings_)
print(fa.get_factor_variance())