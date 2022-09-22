from tabnanny import verbose
from django.db import models

class TimeBaseModel(models.Model):
    
    class Meta:
        abstract=True

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)    

class User(TimeBaseModel):

    class Meta:
        verbose_name="Пользовател"
        verbose_name_plural="Пользователи"

    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True,default=1,verbose_name="Id пользователя")
    name = models.CharField(max_length=100,verbose_name="Имя пользователя")
    username = models.CharField(max_length=50,null=True)
    access = models.BooleanField(default=False, verbose_name="Доступ")

    def __str__(self) -> str:
        return f"№{self.id} ({self.user_id} - {self.name})"

        