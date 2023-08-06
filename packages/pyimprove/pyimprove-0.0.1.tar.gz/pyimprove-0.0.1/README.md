# Pyimprove

This repository contains an implementation of Genetic Improvement that can be used to fix Python code.

## Setup

A virtual environment is used to ensure that all requirements are installed correctly without interference with the host environment.

```
brew install pyenv
brew install pyenv-virtualenv

nano ~/.bash_profile
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
source ~/.bash_profile

pyenv install 3.7.4
pyenv virtualenv 3.7.4 pyimprove

pyenv activate pyimprove

pip install --upgrade pip
pip install -r ./requirements.txt
pip install --editable .
```

```
python ./pyimprove/search.py ./bugs/custom/factorial.py ./bugs/custom/factorial_test.py
```
