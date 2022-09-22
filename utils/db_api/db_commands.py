from os import sync
from typing import List
from unicodedata import name
from django_project.usersmanage.models import User
from django_project.sales.models import Item
from asgiref.sync import sync_to_async

@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id,full_name,username):
    try:
        user = User(user_id=int(user_id), name=full_name, username=username)
        user.save()
        return user 
    except Exception:
        user = User.objects.filter(user_id=user_id).first()
        return user    
        

@sync_to_async
def get_categories():
   return Item.objects.distinct("group").all()         