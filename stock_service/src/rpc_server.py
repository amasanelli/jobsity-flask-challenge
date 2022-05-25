# encoding: utf-8

import json
import pika
import os

from .api.v_1_0.schemas import StockSchema
from .services import Stooq


class RPCService():

    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'rabbitmq-server'))
        )

        channel = connection.channel()
        channel.queue_declare(queue='rpc_queue')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue='rpc_queue', on_message_callback=self.on_request
        )

        print("RPC server listening")

        channel.start_consuming()

    def on_request(self, ch, method, props, body):
        stock_code = body.decode('utf-8')
        schema = StockSchema()

        try:
            stock_data_obj = Stooq.get_data(stock_code)
            response = json.dumps({"data": schema.dump(stock_data_obj)})
        except Exception as e:
            response = json.dumps({"err": e.args[0]})

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=response
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
