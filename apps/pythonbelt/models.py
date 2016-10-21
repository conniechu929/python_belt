from __future__ import unicode_literals

from django.db import models

import datetime
import time
import bcrypt
import re

USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, **kwargs):
		errors = []
		if len(kwargs['name']) < 4:
			 errors.append('First name is not longer than 3 letters.')
		if not NAME_REGEX.match(kwargs['name']):
			errors.append('Name must be letters.')
		if len(kwargs['username']) < 4:
			errors.append('Username is too short.')
		if not USERNAME_REGEX.match(kwargs['username']):
			errors.append('Invalid username.')
		if User.objects.filter(username=kwargs["username"]):
			errors.append("Username already exists!")
		if len(kwargs['password']) < 8:
			errors.append('Password must be longer than 8 characters.')
		if kwargs['password'] != kwargs['confirm_pw']:
			errors.append('Password does not match.')
		if len(kwargs['date_hired']) == 0:
			errors.append('Please enter hired date.')
		if kwargs['date_hired'] < time.strftime("%m/%d/%Y"):
			errors.append('Invalid hire date.')
		if len(errors) is not 0:
			return (False, errors)
		else:
			hashed = bcrypt.hashpw((kwargs['password']).encode(), bcrypt.gensalt())
			info = User.objects.create(name=kwargs['name'], username=kwargs['username'], date_hired=kwargs['date_hired'], password=hashed)
			info.save()
			print info
			return (True, info)

	def login(self, **kwargs):
		try:
			user = User.objects.get(username=kwargs['username'])
		except:
			return (False, "Login fields are invalid.")

		if User.objects.get(username=kwargs['username']):
			hashed = bcrypt.hashpw((kwargs['password']).encode(), User.objects.get(username=kwargs['username']).password.encode())
			if User.objects.get(username=kwargs['username']).password == hashed: 
				info = User.objects.get(username=kwargs['username'])
				return (True, info)
			else:
				return (False, 'Password does not match.')
		else:
			return (False, 'Username does not exist.')

class ItemManager(models.Manager):
	def add(self, **items):
		errors = []
		if len(items['item_name']) < 4:
			errors.append('Fill in item/product name.')
		if len(errors) is not 0:
			return (False, errors)
		else:
			user = User.objects.get(id=items['user_id'])
			newItem = Item.objects.create(user_id=user, item_name=items['item_name'])
			newItem.save()
			return (True, newItem)

class WishlistManager(models.Manager):
	def newItem(self, **items):
		if len(items['item_name']) > 1:
			user = User.objects.get(id=items['user_id'])
			item = Item.objects.get(id=items['item_id'])
			new_item = Wishlist.objects.create(user_id=user, item_id=item)
			new_item.save()
			return (True, new_item)

class User(models.Model):
	name = models.CharField(max_length=45)
	username = models.CharField(max_length=45)
	password = models.CharField(max_length=255)
	date_hired = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Item(models.Model):
	item_name = models.CharField(max_length=45)
	user_id = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ItemManager()

class Wishlist(models.Model):
	item_id = models.ForeignKey(Item)
	user_id = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = WishlistManager()