
import json


file_name_authors = 'authors.json'
file_name_qoute ='quotes.json'

def read_json(file_name): #--> list 
    with open(file_name, 'r') as openfile:
        json_objecct = json.load(openfile)
    return json_objecct

file_name = 'authors.json'

print(read_json(file_name))
print(type(read_json(file_name)))