import pandas as pd
from factor_analyzer.factor_analyzer import FactorAnalyzer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

factors = 6
df = pd.read_csv("./behavior_Jungle.csv", sep=";")
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(axis=0, how='any', inplace=True)

behavior = df[["XPD@15","GD@15","Kills","Deaths","Assists","WardPlaced","WardKilled","TotalDamageShieldedOnTeammates","TotalDamageDealtToBuilding","TotalDamageDealtToObjectives","TotalTimeCrowdControlDealt","TotalTimeCCOthers","JungleProximity","midLanePresence","topLanePresence","botLanePresence","jungleBlueEntryPresence","jungleRedEntryPresence"]]
# X = StandardScaler().fit_transform(behavior)
X = behavior

print(X)


# Testing if we can use factor analysis on our dataset
chi_square_value,p_value=calculate_bartlett_sphericity(X)      # if p=0 we goood
print(chi_square_value, p_value)

kmo_all,kmo_model=calculate_kmo(X)                             # if kmo_model > 0.6 we good
print(kmo_model)


fas = [
    ("FA oblique rotation", FactorAnalyzer(n_factors=factors, rotation="promax")),
    ("FA orthogonal rotation", FactorAnalyzer(n_factors=factors, rotation="varimax")),
]  

#  Let's prepare some plots on one canvas (subplots)
fig, axes = plt.subplots(ncols=len(fas), figsize=(20, 15))
for ax, (title, fa) in zip(axes, fas):
    #  Fit the model to the standardized food data
    fa = fa.fit(X)

    #  and transpose the component (loading) matrix
    factor_matrix = fa.loadings_
    #  Plot the data as a heat map
    im = ax.imshow(factor_matrix, cmap="RdBu_r", vmax=1, vmin=-1, aspect='auto')
    #  and add the corresponding value to the center of each cell
    for (i,j), z in np.ndenumerate(factor_matrix):
        ax.text(j, i, str(z.round(factors)), ha="center", va="center")
    #  Tell matplotlib about the metadata of the plot
    ax.set_yticks(np.arange(len(behavior.columns)))
    if ax.get_subplotspec().is_first_col():
        ax.set_yticklabels(behavior.columns)
    else:
        ax.set_yticklabels([])
    ax.set_title(title)
    ax.set_xticks(np.arange(factors))
    ax.set_xticklabels(["Factor {}".format(i+1) for i in range(factors)])
    #  and squeeze the axes tight, to save space
    plt.tight_layout()
    
#  and add a colorbar
cb = fig.colorbar(im, ax=axes, location='right', label="loadings")
plt.savefig("results.png")

plt.clf()


#  Let's prepare some plots on one canvas (subplots)
for title, fa in fas:
    #  Fit the model to the standardized food data
    fa = fa.fit(X)
    
    plt.barh(y=behavior.columns, width=fa.get_communalities())
    plt.savefig("communalities{}.png".format(title))
    plt.clf()

    plt.barh(y=behavior.columns, width=1-fa.get_communalities())
    plt.savefig("uniqueness{}.png".format(title))
    plt.clf()

for title, fa in fas:
    ev, v = fa.get_eigenvalues()
    plt.scatter(range(1, X.shape[1]+1),ev)
    plt.plot(range(1, X.shape[1]+1),ev)
    plt.title('Scree Plot {}'.format(title))
    plt.xlabel('Factors')
    plt.ylabel('Eigenvalue')
    plt.grid()
    plt.savefig("Scree Plot {}".format(title))
    plt.clf()

