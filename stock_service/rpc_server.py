import json
from  threading import Thread
import pika
from stock_service.api.v_1_0.schemas import StockSchema
from stock_service.services import Stooq


class RPCService(Thread):

    def __init__(self):
        Thread.__init__(self, target=self.init_rpc_server)

    def init_rpc_server(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue='rpc_queue')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='rpc_queue', on_message_callback=self.on_request)

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


def main():
    th = RPCService()
    th.setDaemon(True)
    th.start()

main()