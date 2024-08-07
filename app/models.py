from mongoengine import (BooleanField, Document, EmailField, ImageField,
                         IntField, StringField)


class User(Document):
    name = StringField(max_length=100, required=True)
    nickname = StringField(max_length=100, required=True, unique=True)
    age = IntField(min_value=18)
    email = EmailField()
    self_image = ImageField()
    is_active = BooleanField(default=True)
