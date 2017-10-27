from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if (len(postData['first_name']) or len(postData['last_name']) or len(postData['email']) or len(postData['pass']) or len(postData['conf_pass'])) < 1:
            errors['field_empty'] = "Fields can not be empty!"   
    
        if (len(postData['first_name']) or len(postData['last_name'])) < 2:
            errors['name_length'] = "At least needs 2 characters for first name/last name!!"
        
        if (not NAME_REGEX.match(postData['first_name'])) or (not NAME_REGEX.match(postData['last_name'])):
            errors['name_type'] = "First Name/Last Name only contains letters!!"
        
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        
        if len(postData['pass']) < 8:
            errors['pass'] = "Password should be at least 8 characters long!"
        
        if postData['conf_pass'] != postData['pass']:
            errors['pass2'] = "Passwords didn't match!"
        return errors;

    def login_validator(self,postData):
        errors1 = {}
        if (len(postData['login_email']) or len(postData['login_pass'])) < 1:
            errors1['field_empty'] = "Fields can not be empty!"
        user_list = []
        user_list = User.objects.filter(email = postData['login_email'])
        if (user_list):
            login_pass = postData['login_pass']
            check = bcrypt.checkpw(login_pass.encode(),user_list[0].password.encode())
            if(check is False):
                errors1['wrong'] = "Wrong Username or Password!"
        else:
            errors1['wrong'] = "Wrong Username or Password!"
        return errors1;


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    
    objects = UserManager()

