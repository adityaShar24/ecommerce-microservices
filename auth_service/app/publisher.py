import pika
import json

params = pika.URLParameters('amqps://xhpriczr:PHGniONLdwZjj4i4KrXTEvydiE4CSF9m@kebnekaise.lmq.cloudamqp.com/xhpriczr')

def publish_message(message: dict):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    # Declare exchange and queue
    channel.exchange_declare(exchange='user_exchange', exchange_type='direct', durable=True)
    channel.queue_declare(queue='user_queue', durable=True)
    channel.queue_bind(exchange='user_exchange', queue='user_queue', routing_key='user.info')

    # Publish message
    channel.basic_publish(
        exchange='user_exchange',
        routing_key='user.info',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )
    print(" [x] Sent message to user_service:", message)
    connection.close()
    
if __name__ == "__main__":
    publish_message({
        "action": "create_user",
        "data": {
            "user_id": 123,
            "email": "test@example.com"
        }
    })
