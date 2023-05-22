from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField




class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    

class Qoute(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Author)
    quote = StringField()
      
      
class Contact(Document):
    fullname = StringField()
    email = StringField()
    isSent = BooleanField(default=False)