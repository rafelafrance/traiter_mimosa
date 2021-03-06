#!/usr/bin/env bash

# #################################################################################
# Setup the virtual environment for development.
# You may need to "python -M pip install --user virtualenv" globally.
# This is not required but some form of project isolation (conda, virtual env, etc.) is strongly encouraged.
if [[ ! -z "$VIRTUAL_ENV" ]]; then
  echo "'deactivate' before running this script."
  exit 1
fi

rm -r .venv
python3.10 -m venv .venv
source ./.venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# ##############################################################################
# Install spacy and language libraries

python -m pip install -U spacy
python -m spacy download en_core_web_sm


# ##############################################################################
# Use the 2nd line if you don't have traiter installed locally

# pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
pip install -e ../traiter


# ##############################################################################
# Dev only installs (not required because they're personal preference)

python -m pip install -U neovim
python -m pip install -U 'python-lsp-server[all]'
python -m pip install -U pre-commit pre-commit-hooks
python -m pip install -U autopep8 flake8 isort pylint yapf pydocstyle black
python -m pip install -U bandit prospector pylama

python -m pip install -U jupyter jupyter_nbextensions_configurator ipyparallel
python -m pip install -U jupyterlab jupyterlab-drawio
python -m pip install -U jupyterlab-lsp jupyterlab-spellchecker
python -m pip install -U aquirdturtle-collapsible-headings
python -m pip install -U nbdime
python -m pip install -U jupyterlab-code-formatter==1.4.10
python -m pip install -U jupyterlab-git==0.36.0

jupyter labextension install jupyterlab_onedarkpro
jupyter server extension enable --py jupyterlab_git
jupyter serverextension enable --py jupyterlab_code_formatter

# ##############################################################################
# I Run pre-commit hooks (optional)

pre-commit install
