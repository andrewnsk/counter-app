import os
import time
import redis
from flask import Flask

redis_hostname = os.environ.get('redis_hostname', 'redis')
test_env = os.environ.get('test_env', 'none')


app = Flask(__name__)
cache = redis.Redis(host=redis_hostname, port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def get_error_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('error_hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return "Big Ass hole counter: {} queries\n redis_hostname\n".format(count)


@app.route('/env')
def env():
    return 'Env is: {0}'.format(test_env)


@app.errorhandler(404)
def page_not_found(e):
    error_count = get_error_hit_count()
    return "error count: {0}".format(error_count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
