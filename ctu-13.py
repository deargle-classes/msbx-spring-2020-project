# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 09:52:46 2020

@author: sethgrossman
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle as pkl
#%%
filename = 'capture20110810.binetflow'
try:
    # try to load the file from a local directory
    net_flows = pd.read_csv(filename)
    pass
except:
    # fetch it from the url
    net_flows = pd.read_csv('https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-42/detailed-bidirectional-flow-labels/{}'.format(filename))
    net_flows.to_csv(filename)
    pass

#%%
net_flows = net_flows.dropna()
X = net_flows.iloc[:,0:14]
y = net_flows['Target'] = net_flows['Label'].str.startswith('flow=From-Botnet').astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=42)


categorical_features = ['Proto','Dir','State']
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)])





clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('clf', RandomForestClassifier(min_samples_leaf = 10))])
pickle_it = clf.fit(X_train, y_train)

#%%
with open('{}.pkl'.format('pickle'), 'wb') as f:
    pkl.dump(pickle_it, f)
