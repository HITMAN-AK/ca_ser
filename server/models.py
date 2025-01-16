from django.db import models

class User(models.Model):
    name=models.CharField(max_length=100,null=True)
    uname=models.CharField(max_length=100,null=True)
    pas=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name
    
class Chat(models.Model):
    sen=models.CharField(max_length=100,null=True)
    rec=models.CharField(max_length=100,null=True)
    mess=models.TextField(null=True)
    time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.time
