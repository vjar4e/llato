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

## Sources

- [lietuviuzodynas.lt](https://lietuviuzodynas.lt/)
