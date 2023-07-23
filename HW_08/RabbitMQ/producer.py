import pika
from faker import Faker
import model


def generate_messages(n):
    fake = Faker()
    messages = []
    for i in range(100):
        name = fake.name()
        messages.append(model.Messages(fullname=name,
                                       email=name + "@gmail.com",
                                       content=fake.text()).save())
    return messages


def main_():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='messages_mock', exchange_type='direct')
    channel.queue_declare(queue='messages_queue', durable=True)
    channel.queue_bind(exchange='messages_mock', queue='messages_queue')
    messages = generate_messages(3)

    for m in messages:
        msg = str(m.id)
        channel.basic_publish(exchange='messages_mock', routing_key='messages_queue', body=msg.encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
    print(" [x] Sent 'Hello World!'")
    connection.close()


if __name__ == '__main__':
    main_()
