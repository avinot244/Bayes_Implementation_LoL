import pandas as pd
from factor_analyzer.factor_analyzer import FactorAnalyzer
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np

from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

factorsPerRole : dict = {"Top" : 7,
                         "Jungle" : 7,
                         "Mid" : 9,
                         "ADC" : 5,
                         "Support" : 8}


role = "Jungle"
title = "Loading oblique rotation {}".format(role)
factors = factorsPerRole[role]

df = pd.read_csv("./behavior_{}.csv".format(role), sep=";")
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(axis=0, how='any', inplace=True)

header = [column for column in df.columns[2:]]

behavior = df[header]
# X = StandardScaler().fit_transform(behavior)
X = behavior

# Testing if we can use factor analysis on our dataset
chi_square_value,p_value=calculate_bartlett_sphericity(X)      # if p=0 we goood
print(chi_square_value, p_value)

kmo_all,kmo_model=calculate_kmo(X)                             # if kmo_model > 0.6 we good
print(kmo_model)


fa =  FactorAnalyzer(n_factors=factors, rotation="promax")



#  Let's prepare some plots on one canvas (subplots)
fig, axes = plt.subplots(ncols=1, figsize=(12, 7))

#  Fit the model to the standardized food data
fa = fa.fit(X)

#  and transpose the component (loading) matrix
factor_matrix = fa.loadings_
scaled_factor_matrix = []
for line in factor_matrix:
    scaler : MinMaxScaler = MinMaxScaler().fit(np.abs(line).reshape(-1, 1))
    scaledLine = scaler.transform(np.abs(line).reshape(-1, 1))
    scaled_factor_matrix.append(scaledLine.reshape(1, -1).tolist()[0])

scaled_factor_matrix = np.array(scaled_factor_matrix)


#  Plot the data as a heat map
im = axes.imshow(factor_matrix, cmap="RdBu_r", vmax=1, vmin=-1, aspect='auto')
#  and add the corresponding value to the center of each cell
for (i,j), z in np.ndenumerate(factor_matrix):
    
    axes.text(j, i, str(z.round(factors)), ha="center", va="center")
#  Tell matplotlib about the metadata of the plot
axes.set_yticks(np.arange(len(behavior.columns)))
if axes.get_subplotspec().is_first_col():
    axes.set_yticklabels(behavior.columns)
else:
    axes.set_yticklabels([])
axes.set_title(title)
axes.set_xticks(np.arange(factors))
axes.set_xticklabels(["Factor {}".format(i+1) for i in range(factors)])
#  and squeeze the axes tight, to save space
plt.tight_layout()
    
#  and add a colorbar
cb = fig.colorbar(im, ax=axes, location='right', label="loadings")
plt.savefig("./results/results_{}.png".format(role))

plt.clf()

#  Let's prepare some plots on one canvas (subplots)
fig, axes = plt.subplots(ncols=1, figsize=(12, 7))

#  Plot the data as a heat map
im = axes.imshow(scaled_factor_matrix, cmap="RdBu_r", vmax=1, vmin=0, aspect='auto')
#  and add the corresponding value to the center of each cell
for (i,j), z in np.ndenumerate(scaled_factor_matrix):
    
    axes.text(j, i, str(z.round(factors)), ha="center", va="center")
#  Tell matplotlib about the metadata of the plot
axes.set_yticks(np.arange(len(behavior.columns)))
if axes.get_subplotspec().is_first_col():
    axes.set_yticklabels(behavior.columns)
else:
    axes.set_yticklabels([])
axes.set_title(title)
axes.set_xticks(np.arange(factors))
axes.set_xticklabels(["Factor {}".format(i+1) for i in range(factors)])
#  and squeeze the axes tight, to save space
plt.tight_layout()
    
#  and add a colorbar
cb = fig.colorbar(im, ax=axes, location='right', label="loadings")
plt.savefig("./results/results_{}_scaled.png".format(role))

plt.clf()


# #  Plot the data as a heat map
# im = axes.imshow(factor_matrix, cmap="RdBu_r", vmax=1, vmin=-1, aspect='auto')
# #  and add the corresponding value to the center of each cell
# for (i,j), z in np.ndenumerate(factor_matrix):
    
#     axes.text(j, i, str(z.round(factors)), ha="center", va="center")
# #  Tell matplotlib about the metadata of the plot
# axes.set_yticks(np.arange(len(behavior.columns)))
# if axes.get_subplotspec().is_first_col():
#     axes.set_yticklabels(behavior.columns)
# else:
#     axes.set_yticklabels([])
# axes.set_title(title)
# axes.set_xticks(np.arange(factors))
# axes.set_xticklabels(["Factor {}".format(i+1) for i in range(factors)])
# #  and squeeze the axes tight, to save space
# plt.tight_layout()
    
# #  and add a colorbar
# cb = fig.colorbar(im, ax=axes, location='right', label="loadings")
# plt.savefig("results_{}.png".format(role))

# plt.clf()


#  Let's prepare some plots on one canvas (subplots)

# #  Fit the model to the standardized food data
# fa = fa.fit(X)

# plt.barh(y=behavior.columns, width=fa.get_communalities())
# plt.savefig("communalities{}.png".format(role))
# plt.clf()

# plt.barh(y=behavior.columns, width=1-fa.get_communalities())
# plt.savefig("uniqueness{}.png".format(role))
# plt.clf()

ev, v = fa.get_eigenvalues()
plt.scatter(range(1, X.shape[1]+1),ev)
plt.plot(range(1, X.shape[1]+1),ev)
plt.title('Scree Plot {}'.format(role))
plt.xlabel('Factors')
plt.ylabel('Eigenvalue')
plt.grid()
plt.savefig("./results/Scree Plot {}".format(role))
plt.clf()

