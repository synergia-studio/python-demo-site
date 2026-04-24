from django.db import models
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class ContactUs(models.Model):

    db_table = 'contact_us'

    id = models.BigAutoField(primary_key=True, unique=True)
    client_ip = models.CharField(max_length=255, default='')
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')    
    email = models.CharField(max_length=255, default='') 
    subject = models.CharField(max_length=255, default='') 
    message = models.TextField(default='')
    created_at = models.DateTimeField(null=True, default='0000-00-00 00:00:00')
    updated_at = models.DateTimeField(null=True, default='0000-00-00 00:00:00')

    def __str__(self):
        return self.name