# Dune
REST interface for MirageOS unikernels

#### Running Dune locally on Ubuntu
###### Install required packages from Ubuntu repositories

```sh
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev python3-venv pylint
$ sudo apt-get install opam
```
**Note:** If you are running a version of Ubuntu older than 15.04, the package `python3-venv` may
not be available. Use `python3.4-venv` instead.

###### Create and activate a Python 3 virtual environment with `venv`
```sh
$ pyvenv ~/env
$ source ~/env/bin/activate
```
At this point, you should be able to see the `Python 3.4.3+` when you enter `python --version`.

###### Initialize OPAM and install MirageOS
```sh
$ opam init -a
$ eval `opam config env`
$ opam install mirage
```

###### Install Dune API requirements
```sh
$ git clone https://github.com/onyb/dune
$ cd dune
$ pip install -r requirements.txt
```

###### Launch Dune API server
```sh
$ python runapiserver.py
```
The webserver should now be running at `http://localhost:5000` with the API root at `http://localhost:5000/api`

#### Tech Stack
- [OCaml](http://ocaml.org)
- [Mirage](http://mirage.io)
- Python 3 (tested on 3.4)
- [Flask](http://flask.pocoo.org) for the web application and API
- [Jinja2](http://jinja.pocoo.org) for templating with Flask
- [MongoDB](https://docs.mongodb.org/manual) for the backend database
- [Flask-PyMongo](https://flask-pymongo.readthedocs.org/en/latest), a wrapper around the original [PyMongo](https://api.mongodb.org/python/current) driver.
- Test bench with [nose](https://nose.readthedocs.org/en/latest)
