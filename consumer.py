import pika, sys, os

import connect
from models import Contact

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# channel.queue_declare(queue='hello')
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def send_email(contact_id):
  print(f' [x] email sent to {contact_id} ')


def update_flag(contact_id):
  _id = contact_id
  contact = Contact.objects(id=_id)
  contact.update(isSent=True)
  print(f'flag: True')
  
       

def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {message}")
    print(f" [x] Done: {method.delivery_tag}")
    send_email(message)
    update_flag(message)
  
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)  

if __name__ == '__main__':
  channel.start_consuming()