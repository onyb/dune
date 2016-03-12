from redis import Redis
from rq import Queue

Q = Queue(connection=Redis())