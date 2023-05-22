from models import Author, Qoute
import connect
import json
import os


def find_by_name_qoute(tag):
    tag_list = tag.split(',')
    
    qoutes = Qoute.objects(tags__in = tag_list)
    res = []
    for qt in qoutes:
        res.append(qt.quote)
    print(res)
    
    
def find_by_author(author_name):
    authors = Author.objects(fullname = author_name)
    for author in authors:
        authors_id = author.id
    qoutes = Qoute.objects(author = authors_id)
    for qt in qoutes:
        print(qt.quote)


def main():    
    os.system('cls')
    print('Qoute finder comand:')
    print('name:<author name> - find by name')
    print('tag:<tag1,tag2> - find by tag')
    print('exit- exit')
    print('--------------')
    
    query_str = ''
    
    while query_str != 'exit':
        query_str = input('Input your command:')
        if query_str != 'exit':
            query_list = query_str.split(':') 
            if query_list[0] == 'name':
                find_by_author(query_list[1])
            elif query_list[0] == 'tag' or  query_list[0] == 'tags':
                find_by_name_qoute(query_list[1])
            else:
                print('Wrong command. Try again.')
                
        
main()    





    
    