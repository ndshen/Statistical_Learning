#%%
import numpy as np
import pandas as pd

df = pd.read_csv('cwb.csv')
df.head()

#%%
df = df.replace({'...':np.nan})
df = df.dropna(axis=0)
df.head()

#%%
df = df.replace({'...':0})
#%%
df['GloblRad'] = pd.to_numeric(df['GloblRad'])
df['Cloud Amount'] = pd.to_numeric(df['Cloud Amount'])

df['GloblRad'].corr(df['Cloud Amount'])

#%%
df2 = pd.read_csv('final_project_pre/res.csv')
df2.head()

#%%
df['Month'] = pd.to_numeric(df['Month'])
df['Day'] = pd.to_numeric(df['Day'])
df['ObsTime'] = pd.to_numeric(df['ObsTime'])

obsTime = []
for index, row in df.iterrows():
    time = "{}{:02d}{:02d}{:02d}".format(row["Year"], row["Month"], row["Day"], row["ObsTime"]-1)
    obsTime.append(time)

obsTime


#%%
df2

#%%
df["obsTime"] = pd.to_numeric(df['obsTime'])
merge_df = pd.merge(df2, df, on='obsTime', how='left')
merge_df

#%%
merge_df.to_csv("merge_df.csv")

#%%
merge_df['TEMP'].corr(merge_df['Temperature'])

#%%
import statsmodels.formula.api as sm
X_train = merge_df[["SunShine", "GloblRad","Cloud Amount","UVI"]]
X_train = X_train.replace({"...":0})

Y_train = merge_df['kwh']
result = sm.OLS(Y_train.astype(float), X_train.astype(float)).fit()
print(result.summary())