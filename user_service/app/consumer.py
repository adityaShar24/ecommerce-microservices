import pika
import json
from . import create_app
from .models import db , User

app = create_app()

params = pika.URLParameters('amqps://xhpriczr:PHGniONLdwZjj4i4KrXTEvydiE4CSF9m@kebnekaise.lmq.cloudamqp.com/xhpriczr')

def callback(ch , method , properties, body):
    message = json.loads(body)
    print(" [x] Received:", message)
    
    if message.get("action") == "create_user":
        user_data = message["data"]
        print(f"Creating user in DB: {user_data}")
        with app.app_context():
            try:
                new_user = User(
                    id=user_data.get("user_id"),
                    full_name=user_data.get("full_name"),
                    email=user_data.get("email")
                )
                db.session.add(new_user)
                db.session.commit()
                print(f"✅ User {new_user.full_name} added successfully")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error inserting user: {e}")

    ch.basic_ack(delivery_tag=method.delivery_tag)
    
def start_consuming():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.exchange_declare(exchange='user_exchange', exchange_type='direct', durable=True)
    channel.queue_declare(queue='user_queue', durable=True)
    channel.queue_bind(exchange='user_exchange', queue='user_queue', routing_key='user.info')
    
    channel.basic_consume(queue='user_queue', on_message_callback=callback)
    print(" [*] Waiting for messages in user_service. Press CTRL+C to exit")
    channel.start_consuming()
    
if __name__ == '__main__':
    start_consuming()