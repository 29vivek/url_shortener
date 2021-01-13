# URL shortener

A basic url shortener using Blake2B hash functions and Base64 encoding.

## Getting started

- Assuming you have anaconda/miniconda installed, run the following commands
```sh
$ conda env create -f environment.yml
$ conda activate flask
```
- Then, make necessary changes in *url_shortener/settings.py* and run
```sh
$ python setup.py
```
- All done! Run your factory setup flask app by doing
```sh
$ flask run
```
- Open [localhost](http://127.0.0.1:5000/) and voila!
