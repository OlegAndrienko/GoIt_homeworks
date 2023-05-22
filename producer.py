import pika
from faker import Faker
import faker
from random import randint

import connect
from models import Contact



SUBSCRIBER_NUMBER = 10

# credential = pika.PlainCredentials("gest", "gest")
# connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5671, credentials=credential))
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# channel.queue_declare(queue='hw_9')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
# channel = connection.channel()
# channel.queue_declare(queue="hello")

#визначаємо біржу
channel.exchange_declare(exchange='email_mock', exchange_type='direct')
#Декларуємо чергу email  та зв'язуємо її з нашою біржею email
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='email_mock', queue='email_queue')



#generation fake data 
def insert_data_db(number):
    fake = Faker("uk_UA")
    delete_contact = Contact.objects.delete({})
    for i in range(1, number+1):
        fullname =  fake.name()
        email = fake.email()
        isSent = False
        contact = Contact(fullname=fullname, email=email, isSent = isSent).save()
        
def main():
    
    contacts = Contact.objects()
    lenght = len(contacts)
    
    for el in contacts:
        # channel.basic_publish(exchange='', routing_key='hello_world', body=str(el.id))
        
        channel.basic_publish(
            exchange='email_mock',
            routing_key='email_queue',
            body=str(el.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f" [x] Sent {el.id}")
    connection.close()  
        
        
        
        

if __name__ == '__main__':
    
    insert_data_db(SUBSCRIBER_NUMBER)
    main()
