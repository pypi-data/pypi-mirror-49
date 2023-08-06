import base64
try:
    from collections.abc import Iterable, Mapping
except ImportError:  # Python 2 compatibility
    from collections import Iterable, Mapping
import json
try:
    from json.decode import JSONDecodeError
except ImportError:  # Python 2 compatibility
    JSONDecodeError = ValueError
import logging
import os
import pickle
import six
import sys
import threading
import time
import traceback

from qualname import qualname
import requests

from .__version__ import __version__

PRODUCE_SNAP_URL = 'https://www.varsnap.com/api/snap/produce/'
CONSUME_SNAP_URL = 'https://www.varsnap.com/api/snap/consume/'

# Names of different environment variables used by varsnap
# See readme for descriptions
ENV_VARSNAP = 'VARSNAP'
ENV_ENV = 'ENV'
ENV_PRODUCER_TOKEN = 'VARSNAP_PRODUCER_TOKEN'
ENV_CONSUMER_TOKEN = 'VARSNAP_CONSUMER_TOKEN'

LOGGER = logging.getLogger('varsnap')
LOGGER.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
LOGGER.addHandler(handler)


def env_var(env):
    return os.environ.get(env, '').lower()


def get_signature(target_func):
    return 'python.%s.%s' % (__version__, qualname(target_func))


def equal(x, y):
    if not isinstance(x, y.__class__):
        return False
    if isinstance(x, six.string_types):
        return x == y
    if isinstance(x, Iterable):
        if len(x) != len(y):
            return False
        mapping = isinstance(x, Mapping)
        for v in zip(x, y):
            if not equal(v[0], v[1]):
                return False
            if mapping and not equal(x[v[0]], y[v[1]]):
                return False
        return True
    if hasattr(x, '__dict__'):
        return equal(x.__dict__, y.__dict__)
    return x == y


class Producer():
    def __init__(self, target_func):
        self.target_func = target_func

    @staticmethod
    def is_enabled():
        if env_var(ENV_VARSNAP) != 'true':
            return False
        if env_var(ENV_ENV) != 'production':
            return False
        if not env_var(ENV_PRODUCER_TOKEN):
            return False
        return True

    @staticmethod
    def serialize(data):
        data = base64.b64encode(pickle.dumps(data)).decode('utf-8')
        return data

    @staticmethod
    def get_globals():
        global_vars = {}
        for k, v in globals().items():
            if k[:2] == '__':
                continue
            try:
                pickle.dumps(v)
            except TypeError:
                continue
            global_vars[k] = v
        return global_vars

    def produce(self, args, kwargs, output):
        if not Producer.is_enabled():
            return
        LOGGER.info(
            'VarSnap producing call for %s' %
            qualname(self.target_func)
        )
        global_vars = Producer.get_globals()
        data = {
            'producer_token': env_var(ENV_PRODUCER_TOKEN),
            'signature': get_signature(self.target_func),
            'inputs': Producer.serialize([args, kwargs, global_vars]),
            'prod_outputs': Producer.serialize(output)
        }
        requests.post(PRODUCE_SNAP_URL, data=data)


class Consumer():
    def __init__(self, target_func):
        self.target_func = target_func

    @staticmethod
    def is_enabled():
        if env_var(ENV_VARSNAP) != 'true':
            return False
        if env_var(ENV_ENV) != 'development':
            return False
        if not env_var(ENV_CONSUMER_TOKEN):
            return False
        return True

    @staticmethod
    def deserialize(data):
        data = pickle.loads(base64.b64decode(data.encode('utf-8')))
        return data

    def consume(self):
        if not Consumer.is_enabled():
            return
        LOGGER.info(
            'VarSnap consuming calls to %s' %
            qualname(self.target_func)
        )
        last_snap_id = ''
        while True:
            data = {
                'consumer_token': env_var(ENV_CONSUMER_TOKEN),
                'signature': get_signature(self.target_func),
            }
            response = requests.post(CONSUME_SNAP_URL, data=data)
            try:
                response_data = json.loads(response.content)
            except JSONDecodeError:
                response_data = ''
            if (not response_data or
                    response_data['status'] != 'ok' or
                    len(response_data['results']) == 0):
                time.sleep(1)
                continue
            snap_data = response_data['results'][0]
            if snap_data['id'] == last_snap_id:
                time.sleep(1)
                continue

            last_snap_id = snap_data['id']
            LOGGER.info(
                'Receiving call from Varsnap uuid: ' + str(last_snap_id)
            )
            inputs = Consumer.deserialize(snap_data['inputs'])
            prod_outputs = Consumer.deserialize(snap_data['prod_outputs'])
            exception = ''
            try:
                if len(inputs) >= 3:
                    for k, v in inputs[2].items():
                        globals()[k] = v
                local_outputs = self.target_func(*inputs[0], **inputs[1])
            except Exception as e:
                local_outputs = e
                exception = traceback.format_exc()
            self.report(inputs, prod_outputs, local_outputs, exception)

    def report(self, inputs, prod_outputs, local_outputs, exception):
        function_name = qualname(self.target_func)
        LOGGER.info('Function:                         ' + function_name)
        LOGGER.info('Function input args:              ' + str(inputs[0]))
        LOGGER.info('Function input kwargs:            ' + str(inputs[1]))
        LOGGER.info('Production function outputs:      ' + str(prod_outputs))
        LOGGER.info('Your function outputs:            ' + str(local_outputs))
        if exception:
            LOGGER.info('Local exception:                  ' + str(exception))
        matches = equal(prod_outputs, local_outputs)
        LOGGER.info('Matching outputs:                 ' + str(matches))
        LOGGER.info('')


def varsnap(func):
    producer = Producer(func)
    consumer = Consumer(func)

    thread = threading.Thread(target=consumer.consume)
    thread.daemon = True
    thread.start()

    def magic(*args, **kwargs):
        try:
            output = func(*args, **kwargs)
        except Exception as e:
            threading.Thread(
                target=producer.produce,
                args=(args, kwargs, e),
            ).start()
            raise
        threading.Thread(
            target=producer.produce,
            args=(args, kwargs, output),
        ).start()
        return output
    LOGGER.info('Varsnap Loaded')
    # Reuse the original function name so it works with flask handlers
    magic.__name__ = func.__name__
    return magic
