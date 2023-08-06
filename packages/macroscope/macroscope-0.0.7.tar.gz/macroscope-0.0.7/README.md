# Macroscope-cli

Macroscope cli written in python3.

## Usage

Install using pip

```shell
pip3 install macroscope
```

To verify install, run the command

```shell
macroscope --help
```

This should output help text about the available commands.

## Development

### Setup

To setup the project environment and install the required packages, run the command

```shell
make install
```

Then make sure to activate the ```venv``` environment. Instructions to do so are given below.

TODO: currently the python data must be copied into a data directory.

### Venv

Venv is a tool to create a virtual python environment for a project.

#### Create environment

```shell
make create-venv
```

This will create a ```venv``` directory which should not be committed to source control.

#### Activate environment

```shell
source ./venv/bin/activate
```

or equivalently

```shell
. ./venv/bin/activate
```

When the environment is activated, the prefix ```./venv/bin/``` used for commands can be dropped.

For example
* ```./venv/bin/pip3 install package-name``` becomes ```pip3 install package-name```

#### Deactivate environment

```shell
deactivate
```

### Installing new packages

Install new packages with ```pip```

```shell
./venv/bin/pip3 install package-name
```

When new packages are installed, the following command must be run to output installed packages to ```requirements.txt```

```shell
./venv/bin/pip3 freeze > requirements.txt
```

### Publishing package to PyPI

First, make sure ```wheel``` is installed.

```shell
pip install wheel
```

Build package

```shell
python setup.py sdist bdist_wheel
```

Check package is OK to upload

```shell
twine check dist/*
```

Use ```twine``` to upload package

```shell
twine upload dist/*
```

## Possible errors

### Vscode linter doesn't recognise imported packages in venv environment

* Use ```flake8``` linter
* Open ```vscode``` from activated ```venv``` terminal using the command 
```shell
code .
```

<!-- 
### Modules not importing correctly when executing code from command line

* In activated venv environment, execute the command ```python setup.py develop``` -->

## Blogs

* [Why I hate virtualenv and pip](https://pythonrants.wordpress.com/2013/12/06/why-i-hate-virtualenv-and-pip/)
* [Things you are probably not using in python3 but should](https://datawhatnow.com/things-you-are-probably-not-using-in-python-3-but-should/)
* [Installing python on debian](https://matthew-brett.github.io/pydagogue/installing_on_debian.html)
* [Publishing python packages](https://realpython.com/pypi-publish-python-package/)

### Package management

* [reference blog](https://chriswarrick.com/blog/2018/09/04/python-virtual-environments/)

## Possible tools

* https://github.com/jazzband/pip-tools
* https://github.com/sdispater/poetry
* https://github.com/conda/conda
* https://github.com/ofek/hatch
* https://github.com/takluyver/flit
* https://github.com/buildout/buildout

## Notes

* [Public, Private, and Protected in python](https://radek.io/2011/07/21/private-protected-and-public-in-python/)
* [MakeFiles](https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html)
* [Example type hinting](https://github.com/ActivityWatch/aw-core/blob/master/aw_core/models.py)

* [Possible existing python package](https://github.com/williamleif/histwords) - [Blog outlining method](https://aryamccarthy.github.io/hamilton2016diachronic/) - [Another paper](https://www.aclweb.org/anthology/C18-1117)

### Method acronyms

* [SGNS](https://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/)
* [SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition)

## TODO:

* Rename functions after they are verified to be working

* Add MANIFEST.in file
* figure out what to do with data directory
    * Download data using wget and add command to build and dev process - host zipped data file online - use https and all
* sgns-hamilton doesn't have a year 2000 file

* Look into running python in a virtual machine
* Use a MakeFile
* Logging?
* use tox?

* Dev requirements.txt - https://stackoverflow.com/questions/17803829/how-to-customize-a-requirements-txt-for-multiple-environments


* Add setup.py? [Example setup.py](https://github.com/kennethreitz/setup.py/blob/master/setup.py)

* use [mypy](https://github.com/python/mypy)?

* Make python package?
    * https://github.com/johnthagen/python-blueprint
    * https://github.com/audreyr/cookiecutter-pypackage

* use self as first parameter of function? good for memory and encapsulation?
* put suffix variable in one place
* Start of context change function looks very similar to plotCooccurrence function

## To mention

* ```wrapper_freq``` - not sure what start middle and end is?
* Discuss LICENSE
