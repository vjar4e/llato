# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %% is_executing=true
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn import tree 
import pandas as pd
import os

# %%
DEBUG = False
CSV_PATH = "../data/csv/"

# %%
dfs = {}
for filename in os.listdir(CSV_PATH):
    if filename.endswith(".csv"):
        dfs[filename[:-4]] = pd.read_csv(CSV_PATH + filename)
        if DEBUG:
            dfs[filename[:-4]] = dfs[filename[:-4]].sample(frac=0.1)

# %% [markdown]
# ## Case classification model

# %% [markdown]
# ### Training

# %%
MODEL_NAME = "case_classifier"

# %%
import numpy as np

def tokenize(s: str) -> [str]: 
    return [ord(i) for i in list(s.lower())]

def decode(l: [str]) -> str:
    return ''.join([chr(i) for i in l])


def pad(s: [int], max_len: int) -> [int]:
    return np.pad(s, (0, max_len - len(s)), 'constant', constant_values=(0, 0))


# %%
EXISTS = os.path.isfile(f'{MODEL_NAME}.skops')

if not EXISTS:
    dfs_w_cases = (
        dfs['adjectives'],
        dfs['halfparticiples'],
        dfs['nouns'],
        dfs['numerals'],
        dfs['pronoun'],
        dfs['subparticles'],
    )

    CASES = ['V.', 'K.', 'N.', 'G.', 'Įn.', 'Vt.']

    case_df = pd.concat(dfs_w_cases, ignore_index=True)
    case_df = case_df[["word", "case"]]
    case_df = case_df.dropna()
    case_df = case_df.drop_duplicates(subset=['word'])

    X = case_df['word']
    y = case_df['case']

    # pad each x

    X = X.apply(tokenize)
    global max_len
    max_len = max(X.apply(len))
    X = X.apply(lambda x: pad(x, max_len))
    y = y.apply(lambda x: CASES.index(x))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# %%
from sklearn.ensemble import RandomForestClassifier
from skops.io import dump, load


# Load case_classifier.skops if exists or train a new one
if EXISTS:
    case_classifier = load(f'{MODEL_NAME}.skops')
else:
    case_classifier = RandomForestClassifier()
    case_classifier.fit(X_train.tolist(), y_train.tolist())
    case_classifier.score(X_test.tolist(), y_test.tolist())
    dump(case_classifier, f'{MODEL_NAME}.skops')

# %% [markdown]
# ### Testing

# %%
from ipywidgets import interact, HTML


@interact
def predict_case(word: str = "") -> HTML:
    res = pd.DataFrame(columns=['case', 'probability'])
    for i, v in enumerate(case_classifier.predict_proba([pad(tokenize(word), max_len)])[0].tolist()):
        res.loc[i] = [CASES[i], v]
    return HTML(res.set_index("case").transpose().sort_values(by='probability', axis=1, ascending=False).to_html(index=False))
