# LLATO 

> Lithuanian Language Tools

## Description

A set of tools for Lithuanian language processing.

## Development

### Setup

```bash
git clone https://github.com/4evj/llato
cd llato
poetry install
``` 

### Updating dictionary

```bash
cd llato/dictionary
poetry run ./scrap_raw.py     # get list of words  (raw.csv)
poetry run ./scrap_grammes.py # get grammes of words from raw.csv
poetry run ./cleansing.py     # process grammes and save to dictionary/
```

### Updating scripts
Most of python files are generated from jupyter notebooks. If it's needed to convert them back for further development, run:

```bash
poetry run python -m jupytext --sync **/*_jt.py
```

And to convert them back to notebooks:

```bash
poetry run python -m jupytext --sync **/*_jt.ipynb
```

## Sources

- [lietuviuzodynas.lt](https://lietuviuzodynas.lt/)
