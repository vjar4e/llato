# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
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

# %%
import pandas as pd

grammes_raw = pd.read_csv('grammes_raw.csv', sep=',')

code_to_letter = {
    "%C4%85": "ą",
    "%C4%97": "ę",
    "%C4%AF": "į",
    "%C5%B3": "ų",
    "%C5%AB": "ū",
    "%C4%8D": "č",
    "%C5%A1": "š",
    "%C5%BE": "ž"
}

# Remove duplicates
grammes_raw = grammes_raw.drop_duplicates()

# Replace codes above with letters
grammes_raw['word'] = grammes_raw['word'].replace(code_to_letter, regex=True)

# %%
# Get gramme and split it. Separators are dash, arrow and comma
# Skip if gramme is nan

grammes_raw['gramme'] = grammes_raw['gramme'].str.replace('└*', '', regex=True).str.strip()
grammes_raw['gramme_split'] = grammes_raw['gramme'].str.split('–|→ ,|,', regex=True)

# %%
pd.set_option('display.max_colwidth', None)
grammes_raw.head()

# %%
gramme_types = grammes_raw['gramme_split'].apply(lambda x: x[2].strip()).unique()


grammes_dfs = {}

# put each gramme type into separate dataframe and save it to dictionary grammes_dfs 
for gramme_type in gramme_types:
    # append grammes_dfs with removed gramme column and renamed gramme_split to gramme columns
    grammes_dfs[gramme_type] = grammes_raw[grammes_raw['gramme_split'].apply(lambda x: x[2].strip()) == gramme_type].drop(
        columns=['gramme']).rename(columns={'gramme_split': 'gramme'})
    # grammes_dfs[gramme_type] = grammes_raw[grammes_raw['gramme_split'].apply(lambda x: x[2]) == gramme_type]

# Rename ivard-daikt to įvardžiai
grammes_dfs['įvardžiai'] = grammes_dfs.pop('įvard.-daikt.')

# %%
import plotly.express as px

grammes_count = pd.DataFrame()
grammes_count['type'] = grammes_dfs.keys()
grammes_count['type'] = grammes_count['type'].apply(lambda x: x.capitalize())
grammes_count['count'] = [len(grammes_dfs[key]) for key in grammes_dfs.keys()]
grammes_count = grammes_count.sort_values(by=['count'], ascending=True)

px.bar(grammes_count, x='count', y='type', orientation='h', labels={'count': '', 'type': ''}, log_x=True, text_auto=True)

# %%
# Shortcuts
CASES = ["V.", "K.", "N.", "G.", "Vt.", "Įn."]
GENDERS = ["vyr. g.", "mot. g."]
NUMBERS = ["vns.", "dgs."]
PERSON = ['aš', 'mes', 'tu', 'jūs', 'jis', '1 asm.', '2 asm.', '3 asm.']
TYPE = ['daiktavardis',
        'būdvardis',
        'veiksmažodis',
        'jungtukas',
        'jaustukas',
        'dalyvis',
        'dalelytė',
        'prieveiksmis',
        'įvard.-daikt.',
        'padalyvis',
        'prielinksnis',
        'pusdalyvis',
        'skaitvardis']
TENSE = ['es. l.', 'būt. k. l.', 'bus. l.', 'būt. d. l.']
VARIANT = ['trump.', "ilg."]
MOOD = ['ties. nuos.', 'tar. nuos.', 'liep. nuos.']
COMPARISON_DEGREES = ['nelyg. l.', 'aukšt. l.', 'aukšč. l.']
# Write function that accepts list and list of possible values. If possible value appears in list, return it. Else return None


def get_value_from_list(values, possible_values, default=None):
    for value in values:
        for possible_value in possible_values:
            if possible_value in value:
                return value.strip()
    return default


# %%
nouns = pd.DataFrame()
nouns_mask = grammes_dfs['daiktavardis']['gramme']
nouns['word'] = grammes_dfs['daiktavardis']['word']
nouns['initial_form'] = nouns_mask.apply(lambda x: x[0].strip())
nouns['gender'] = nouns_mask.apply(lambda x: get_value_from_list(x, GENDERS))
nouns['case'] = nouns_mask.apply(lambda x: get_value_from_list(x, CASES))
nouns['number'] = nouns_mask.apply(
    lambda x: get_value_from_list(x, NUMBERS))
nouns.to_csv('csv/nouns.csv', index=False)
nouns.head()

# %%
# Count budvardis in grammes_raw
grammes_raw['gramme_split'].apply(lambda x: x[2]).value_counts()

# %%
verbs = pd.DataFrame()
verb_mask = grammes_dfs['veiksmažodis']['gramme']
verbs['word'] = grammes_dfs['veiksmažodis']['word']
verbs['initial_form'] = verb_mask.apply(lambda x: x[0].strip())
verbs['person'] = verb_mask.apply(lambda x: get_value_from_list(x, PERSON))
verbs['tense'] = verb_mask.apply(lambda x: get_value_from_list(x, TENSE, "es. l."))
verbs['mood'] = verb_mask.apply(
    lambda x: get_value_from_list(x, MOOD, "ties. nuos."))
verbs['variant'] = verb_mask.apply(lambda x: get_value_from_list(x, VARIANT, "ilg."))

# Remove anomalies
verbs['initial_form'] = verbs['initial_form'].replace('būnti', 'būti', regex=True)

verbs.to_csv('csv/verbs.csv', sep=',', index=False)
verbs.head()

# %%
conjunctions = pd.DataFrame()
conjunctions['word'] = grammes_dfs['jungtukas']['word'].str.strip()
conjunctions.to_csv('csv/conjunctions.csv', sep=',', index=False)
conjunctions.sort_values(by=['word']).head()

# %%
adjectives = pd.DataFrame()
adjectives_mask = grammes_dfs['būdvardis']['gramme']
adjectives['word'] = grammes_dfs['būdvardis']['word']
adjectives['initial_form'] = adjectives_mask.apply(
    lambda x: x[0].strip())
adjectives['gender'] = adjectives_mask.apply(lambda x: get_value_from_list(x, GENDERS))
adjectives['case'] = adjectives_mask.apply(lambda x: get_value_from_list(x, CASES))
adjectives['number'] = adjectives_mask.apply(lambda x: get_value_from_list(x, NUMBERS, "vns."))
adjectives.to_csv('csv/adjectives.csv', sep=',', index=False)
adjectives.head()

# %%
halfparticiples = pd.DataFrame()
halfparticiples_mask = grammes_dfs['pusdalyvis']['gramme']
halfparticiples['word'] = grammes_dfs['pusdalyvis']['word']
halfparticiples['initial_form'] = halfparticiples_mask.apply(
    lambda x: x[0].strip())
halfparticiples['case'] = halfparticiples_mask.apply(
    lambda x: get_value_from_list(x, CASES))
halfparticiples['number'] = halfparticiples_mask.apply(
    lambda x: get_value_from_list(x, NUMBERS))
halfparticiples['gender'] = halfparticiples_mask.apply(
    lambda x: get_value_from_list(x, GENDERS))
halfparticiples.to_csv('csv/halfparticiples.csv', sep=',', index=False)
halfparticiples.head()

# %%
particles = grammes_dfs['dalelytė']['word']
particles.to_csv('csv/particles.csv', sep=',', index=False)

# %%
interjections = grammes_dfs['jaustukas']['word']
interjections.to_csv('csv/interjections.csv', sep=',', index=False)

# %%
subparticles = pd.DataFrame()
subparticles_mask = grammes_dfs['padalyvis']['gramme']
subparticles['initial_form'] = grammes_dfs['padalyvis']['word']
subparticles['case'] = subparticles_mask.apply(
    lambda x: get_value_from_list(x, CASES))
subparticles['number'] = subparticles_mask.apply(
    lambda x: get_value_from_list(x, NUMBERS))
subparticles['tense'] = subparticles_mask.apply(
    lambda x: get_value_from_list(x, TENSE))
subparticles.to_csv('csv/subparticles.csv', sep=',', index=False)
subparticles.head()

# %%
prepositions = grammes_dfs['prielinksnis']['word']
prepositions.to_csv('csv/prepositions.csv', sep=',', index=False)
prepositions.head()

# %%
grammes_dfs['skaitvardis'].head()

# %%
numerals = pd.DataFrame()
numerals_mask = grammes_dfs['skaitvardis']['gramme']
numerals['word'] = grammes_dfs['skaitvardis']['word']
numerals['initial_form'] = numerals_mask.apply(
    lambda x: x[0].strip())
numerals['case'] = numerals_mask.apply(
    lambda x: get_value_from_list(x, CASES))
numerals['number'] = numerals_mask.apply(
    lambda x: get_value_from_list(x, NUMBERS))
numerals['gender'] = numerals_mask.apply(
    lambda x: get_value_from_list(x, GENDERS))
numerals.to_csv('csv/numerals.csv', sep=',', index=False)
numerals.head()

# %%
pronoun = pd.DataFrame()
pronoun_mask = grammes_dfs['įvardžiai']['gramme']
pronoun['word'] = grammes_dfs['įvardžiai']['word']
pronoun['initial_form'] = pronoun_mask.apply(lambda x: x[0].strip())
pronoun['case'] = pronoun_mask.apply(lambda x: get_value_from_list(x, CASES))
pronoun['number'] = pronoun_mask.apply(lambda x: get_value_from_list(x, NUMBERS))

# Fix anomalies
pronoun.loc[pronoun['word'] == 'mano', 'initial_form'] = 'aš'

pronoun.to_csv('csv/pronoun.csv', sep=',', index=False)
pronoun.head()

# %%
adverbs = pd.DataFrame()
adverbs_mask = grammes_dfs['prieveiksmis']['gramme']
adverbs['word'] = grammes_dfs['prieveiksmis']['word']
adverbs['form'] = adverbs_mask.apply(lambda x: 'neįv. f.' if x[0].strip() in x else 'ties. nuos.')
adverbs['comparison_degree'] = adverbs_mask.apply(
    lambda x: x[-1].strip() if x[-1].strip() in COMPARISON_DEGREES else "nelyg. l.")
adverbs.to_csv('csv/adverbs.csv', sep=',', index=False)
adverbs.head()

# %%
participles = pd.DataFrame()
participles_mask = grammes_dfs['dalyvis']['gramme']
participles['word'] = grammes_dfs['dalyvis']['word']
particles['case'] = participles_mask.apply(lambda x: get_value_from_list(x, CASES))
participles['number'] = participles_mask.apply(lambda x: get_value_from_list(x, NUMBERS))
participles['tense'] = participles_mask.apply(lambda x: get_value_from_list(x, TENSE))
participles['form'] = participles_mask.apply(lambda x: get_value_from_list(x, ['neįv. f.', 'ties. nuos.', 'įv. f.']))
participles['gender'] = participles_mask.apply(lambda x: get_value_from_list(x, GENDERS))
participles.to_csv('csv/participles.csv', sep=',', index=False)
participles.head()
