from models import Author, Qoute
import connect
import json


file_name_authors = 'authors.json'
file_name_qoute ='quotes.json'

def read_json(file_name): #--> list 
    with open(file_name, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object



record_list = read_json(file_name_authors)
qoute_list =read_json('quotes.json')

delete_author = Author.objects.delete({})
delete_qoute = Qoute.objects.delete({})
 
length = len(record_list)

for i in range(length):
    fullname = record_list[i]['fullname']
    born_date = record_list[i]['born_date']
    born_location = record_list[i]['born_location']
    description = record_list[i]['description']
    a = Author(fullname=fullname, born_date=born_date, born_location=born_location, description=description).save()
    
    tags = qoute_list[i]['tags']
    author = a.id
    quote = qoute_list[i]['quote']
    q = Qoute(tags= tags, author=author, quote=quote).save()

           

    


