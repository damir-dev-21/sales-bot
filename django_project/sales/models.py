from tabnanny import verbose
from django.db import models
from django_project.usersmanage.models import User


class TimeBaseModel(models.Model):
    class Meta:
        abstract=True

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)   


class Item(TimeBaseModel):
    
    class Meta:
        verbose_name="Товар"    
        verbose_name_plural="Товары"    

    id = models.AutoField(primary_key=True)
    uuid_id = models.CharField(max_length=255)
    name = models.CharField(verbose_name="Название товара", max_length=255)
    photo = models.CharField(verbose_name="Фото file_id", max_length=200)
    remind = models.IntegerField(verbose_name="Остаток",default=0)
    price = models.IntegerField(verbose_name="Цена")

    group = models.CharField(verbose_name="Группа товара", max_length=50)
    type = models.CharField(verbose_name="Вид товара", max_length=50)
        

    def __str__(self) -> str:
        return f"№{self.id} - {self.name}"   


class Order(TimeBaseModel):
    class Meta:
        verbose_name="Заказ"        
        verbose_name_plural="Заказы"  

    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, verbose_name="Покупатель",on_delete=models.SET(0))
    total = models.IntegerField(verbose_name="Сумма",max_length=255)
    phone_number = models.CharField(verbose_name="Номер телефона",max_length=300)
    purchase_time=models.DateTimeField(verbose_name="Время покупки",auto_now_add=True)
    success=models.BooleanField(verbose_name="Оплата", default=False)

  

class OrderItem(TimeBaseModel):
    class Meta:
        verbose_name="Товары в заказе"
        verbose_name_plural="Список товаров"

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Стоимость",max_length=200)
    quantity=models.IntegerField(verbose_name="Количество")
