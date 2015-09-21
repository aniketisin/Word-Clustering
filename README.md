Description:
A python tool that clusters similar words according to their meaning, from a given data. The tool uses K-Means algorithm to do so after creating a co-occurrance matrix.
This expects tokenized input, one can use nltk (python module) to tokenize the data first then use the tool.


Usage:
Run kmeans.py, run the file without any arguments to get usage instructions.

Warning: 
The Sample Data provided is a large dataset.
Do not run on a very large dataset as algorithm is slow, for such uses use pypy (Just in Time compiler for python) to run the code, then it is fine to use on large dataset.
