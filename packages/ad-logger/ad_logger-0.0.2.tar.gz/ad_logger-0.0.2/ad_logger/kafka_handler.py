import logging
import os
import threading
from datetime import datetime, date, time, timedelta, timezone
import json
import time as tim
import socket
import queue
from enum import Enum

from kafka import KafkaProducer

default_datetime_format_json = '%Y-%m-%d %H:%M:%S%z'
default_date_format = '%Y-%m-%d'
default_time_format = '%H:%M:%S'

datetime_format_simple = '%Y-%m-%d %H:%M:%S'
time_format_short = '%H:%M'


def get_sys_timezone():
    tz = os.environ.get("TZ")
    if tz is not None:
        return timezone(timedelta(hours=int(tz)))
    return timezone(timedelta(hours=-tim.timezone // 3600))


SYSTEM_TIMEZONE = get_sys_timezone()


def datetime_fn(obj: datetime, dt_format=None):
    if obj.tzinfo is not None:
        return obj.replace(tzinfo=SYSTEM_TIMEZONE).strftime(dt_format or default_datetime_format_json)
    else:
        return obj.strftime(dt_format or default_datetime_format_json)


class JSONEncoder(json.JSONEncoder):
    def __init__(self, with_tz=None, datetime_format=None, date_format=None, time_format=None, converters=None, *args,
                 **kwargs):
        self.with_tz = with_tz
        self.datetime_format = datetime_format or datetime_format_simple
        self.date_format = date_format or default_date_format
        self.time_format = time_format or default_time_format
        self.converters = converters
        super(JSONEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):

        typ = type(obj)
        if self.converters:
            if typ in self.converters:
                return self.converters[typ](obj)
            for t, fn in self.converters.items():
                if isinstance(obj, t):
                    return fn(obj)

        if isinstance(obj, datetime):
            return datetime_fn(obj)
        if isinstance(obj, date):
            return obj.strftime(self.date_format)
        if isinstance(obj, time):
            return obj.strftime(self.time_format)

        if isinstance(obj, Enum):
            return obj.name,

        return super(JSONEncoder, self).default(obj)


def dumps(obj, cls=JSONEncoder, **kwargs):
    """
    :param datetime_format: default "%Y-%m-%d %H:%M:%S"
    :param date_format: default "%Y-%m-%d"
    :param time_format: default "%H:%M:%S"
    :param with_tz: bool or str. with timezone, default format "%Y-%m-%dT%H:%M:%S%z"
    """
    return json.dumps(obj, cls=cls, **kwargs)


class KafkaMessage:
    # ID:str
    msg: str
    # create at
    at: str
    # timestamp
    ts: float
    level: str
    # application name
    app: str
    filename: str
    module: str
    func: str
    process: str
    thread: str
    args: dict
    lineno: int = None
    exe_text: str = None
    stack: str = None
    pathname: str
    ip: str


class KafkaHandler(logging.Handler):

    def __init__(self, app: str, topic: str, kafka_producer: {}, kafka_producer_sender: {} = {},
                 json_dump: {} = None, use_queue=True, level=logging.NOTSET,send_timeout:float=3):
        super(KafkaHandler, self).__init__(level=level)
        self.kafka_producer_send_arg = kafka_producer_sender
        self.topic = topic
        self.use_queue = use_queue
        if 'value_serializer' not in kafka_producer :
            kafka_producer['value_serializer'] = lambda x: dumps(x, cls=JSONEncoder).encode("utf-8")
        self.kafka_producer_args = kafka_producer
        if 'max_block_ms' not in self.kafka_producer_args :
            self.kafka_producer_args['max_block_ms'] = send_timeout * 1000
        self.json_dump_args = json_dump
        self.app = app
        self.ip = ','.join(
            [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1])
        self.kafka_producer = self.new_producer()
        self.send_timeout = send_timeout
        if use_queue:
            self.q = queue.Queue()
            self.sender_thread = threading.Thread(target=self.send_with_queue, daemon=True)
            self.sender_thread.start()

    def new_producer(self):
        return KafkaProducer(
            **self.kafka_producer_args
        )

    def send_with_queue(self):
        while True:
            try:
                item = self.q.get(True, 3)
                if not item:
                    continue
                self.send(item)
                self.q.task_done()
            except Exception as e:
                print(e)

    def send(self , msg):
        try:
            self.kafka_producer.send(self.topic, msg.__dict__, **self.kafka_producer_send_arg)
            self.kafka_producer.flush(timeout=self.send_timeout)
        except Exception as e:
            print(e)

    def handle(self, record: logging.LogRecord):
        km = KafkaMessage()
        # km.ID = ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase + string.digits) for _ in range(20))
        km.msg = record.msg
        km.at = datetime_fn(datetime.fromtimestamp(record.created))
        km.ts = int(record.created)
        km.level = record.levelname
        km.app = self.app
        km.filename = record.filename
        km.module = record.module
        km.func = record.funcName
        km.process = record.processName
        km.thread = record.threadName
        km.lineno = record.lineno
        km.args = dumps(record.extra)
        # km.exe_text = record.exc_text
        # km.stack = record.stack_info
        km.pathname = record.pathname
        km.ip = self.ip
        if self.use_queue:
            self.q.put(km, True, 3)
        else:
            self.send(km)

    def join(self):
        if self.use_queue:
            self.sender_thread.join()
        self.kafka_producer.close()
