# encoding: utf-8

import json
import pika
import uuid
import requests


class StockRPCService(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq-server')
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def get_data(self, stock_code: str):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=stock_code
        )

        while self.response is None:
            self.connection.process_data_events()

        if self.response.get('err') is not None:
            raise Exception(self.response.get('err'))

        return self.response.get('data')


class StockHTTPService(object):

    url = 'http://127.0.0.1:5001/api/v1/stock?stockCode={}'

    @classmethod
    def get_data(cls, stock_code: str):
        res = requests.get(cls.url.format(stock_code))

        if res.status_code != 200:
            raise Exception(res.text)

        return res.json()
