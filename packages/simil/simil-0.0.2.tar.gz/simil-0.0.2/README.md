# Semantic String Similarity CLI

`simil` is a CLI interface to [`spacy`](https://spacy.io)'s string similarity engine. It uses the `en_vectors_web_lg` dataset to compare strings for their English semantic similarity. Given two words, phrases, or sentences, `simil` will tell you how similar their meanings are.

## Installation

First install `simil` itself:
```bash
$ pip3 install --user -U simil
```

Now install one of spacy's web_vector models:

```
$ python3 -m spacy download en_vectors_web_lg
```

You can choose between `en_vectors_web_lg`, `en_core_web_lg`, and `en_core_web_md`, (`en_core_web_sm` don't include word vectors at all, and can't be used with `simil`.) `simil` will use the largest model that you have installed, with preference for the `vectors` model over a `core` model.

I suggest using the large vectors model (`en_vectors_web_lg`), but you might want to use a smaller model in order to save on disk space or memory usage.

## Usage:
```bash
$ sim first_file.txt second_file.txt # compare two files
$ sim -s "first string" "second string" # compare two strings
```

The output is a number between 0 and 1, representing how similar the two strings are.

## Details:

`simil` uses Spacy's word vector models trained with [`GLoVe`](https://nlp.stanford.edu/projects/glove/), such as [`en_vectors_web_lg`](https://spacy.io/models/en#en_vectors_web_lg).

This can be a large dataset, which makes for long startup times. So `simil` spins off a process in the background to hold the model, and works under a client-server model with it. This means that if you run `simil` a number of times in a row, only the first run is slow.

This background process does take up a fair bit of memory, typically around 2GB (for the `en_vectors_web_lg` model). After 10 minutes of inactivity it will automatically be killed, in order not to take up memory indefinitely. You can change the length of this timeout with the `--timeout` flag.
