.ONESHELL:
SHELL = /bin/bash

.PHONY : env
env:
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml 
	conda activate notebook
	conda install ipykernel
	python -m ipykernel install --user --name make-env --display-name "IPython - group22_project"

.PHONY : html
html:
	jupyter-book build .


.PHONY : all
all:
	jupyter execute main.ipynb