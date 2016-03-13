# Dune
REST interface for MirageOS unikernels

#### Running Dune locally on Ubuntu
###### Install required packages from Ubuntu repositories

```sh
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev python3-virtualenv pylint
$ sudo apt-get install opam
```

###### Install and launch Redis Server

```sh
$ wget http://download.redis.io/redis-stable.tar.gz
$ tar xvzf redis-stable.tar.gz
$ cd redis-stable
$ make
$ sudo make install
$ redis-server
```

###### Create and activate a Python 3 virtual environment with `virtualenv`
```sh
$ virtualenv -p python3 ~/env
$ source ~/env/bin/activate
```

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
- Python 3
- [OCaml](http://ocaml.org)
- [Mirage](http://mirage.io)
- [Redis](http://redis.io) for acting as a broker
- [Flask](http://flask.pocoo.org) for the web application and API
- [Redis Queue](http://python-rq.org) for asynchronous task queueing
- [Jinja2](http://jinja.pocoo.org) for templating with Flask
- [MongoDB](https://docs.mongodb.org/manual) for the backend database
- [Flask-PyMongo](https://flask-pymongo.readthedocs.org/en/latest), a wrapper around the original [PyMongo](https://api.mongodb.org/python/current) driver.
- Test bench with [nose](https://nose.readthedocs.org/en/latest)
