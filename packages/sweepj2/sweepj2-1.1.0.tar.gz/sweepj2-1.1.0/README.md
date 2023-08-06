# Jinja2-based parameter sweep generation

[![Build Status](https://travis-ci.org/ivotron/sweepj2.svg?branch=master)](https://travis-ci.org/ivotron/sweepj2)

Utilities for running parameter sweeps by providing a Jinja2 template and a parameter space (in YAML).


## Installation
```bash
pip install sweepj2
```

## Usage
Here's is an example script with three variables, viz. `wn_grams`, `learning_rate` and `epoch`.

```bash
# script.sh
./fasttext supervised -input cooking.train -output model_cooking \
    -wordNgrams {{ wn_grams }} \
    -lr {{ learning_rate }} \
    -epoch {{ epoch }}
```

To do a parameter sweep over some parameter space, create a **YAML** file with the list of all the values corresponding to each variable in the script. 

e.g. `space.yml`
```yaml
learning_rate: [ 0.3, 0.5, 0.8 ]
epoch: [ 20, 30 ]
wn_grams: [1, 2, 3, 4, 5 ]
```

You can generate the scripts with all the possible combinations from the YAML file by doing:
```bash 
sweepj2 --template path/to/script.sh --space path/to/space.yml
```

You will find the generated scripts in `./sweepj2-output` directory, or you could mention the directory to save the files by using `--output` flag.