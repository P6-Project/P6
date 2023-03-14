# P6

## Converting data

```sh
pwd
path/to/this/repo
python ./src/extractor.py PATH-TO-DATA-DIR SAMPLE-SIZE FILE.pkl
```

## Running tests

```sh
python -m unittest discover -s ./test
```

## Creating graphs

```sh
python .\src\histogram.py picklefile outputpath
```

## Creating model data

```sh
python3 ./src/graphplot.py ./src/loxam.pkl ./src/graphs/ ./src/data.pkl
```
After this, you can run the model
```sh
python ./src/patternRecognizer.py picklefile
```