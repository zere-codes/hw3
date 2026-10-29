from decimal import ROUND_HALF_UP

from django.contrib.auth.models import User
from django.core.mail import message
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction


# Create your models here.




class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class AppQuerySet(models.QuerySet):

    def paid(self):
        return self.filter(price__gt=0)
    def cheap(self, max_price):
        return self.paid().filter(price__lt=max_price)

    def expensive(self, min_price):
        return self.paid().filter(price__gt=min_price)

    def new(self):
        return self.order_by('-created_at')

    def free(self):
        return self.filter(price=0)

    def category(self, category):
        return self.filter(category=category)

    def move_to_category(self, source, target):
        if source.pk is None or target.pk is None or source.pk == target.pk:
            raise ValueError('Нельзя перенести приложения в ту же категорию')
        with transaction.atomic():
            move = self.model.objects.category(source).update(category=target)
            source.delete()
        return move



class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[ MinValueValidator(0, message='Цена не может быть отрицательной')])
    created_at = models.DateTimeField(auto_now_add=True)
    weight_kb = models.IntegerField(blank=False, validators=[MinValueValidator(100,  message='Размер приложения должен быть минимум 100кб'), MaxValueValidator(30000000, message='Размер приложения должен быть максимум 30000000 кб(30 гб)')])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    icon = models.ImageField(upload_to='icons/', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='apps')
    favorited_by=models.ManyToManyField(User, related_name='favorite_apps', blank=True)
    average_rating = models.DecimalField(default=0, editable=False, max_digits=2, decimal_places=1)
    count_rating = models.IntegerField(default=0, editable=False)
    objects = AppQuerySet.as_manager()

    def __str__(self):
        return self.name




    def weight_unit(self):
        if self.weight_kb >= 1000000:
            return f"{self.weight_kb/1000000} GB"
        elif self.weight_kb >= 1000:
            return f"{self.weight_kb / 1000} MB"
        else:
            return f"{self.weight_kb} KB"

    def get_absolute_url(self):
        return reverse('main:app_detail', kwargs={'app_id': self.pk, 'app_name': self.name})

    def price_text(self):
        if self.price==0:
            return "Бесплатно"
        else:
            return self.price

    def author_text(self):
        if self.author:
            return self.author.username
        else:
            return "Не указан"

    @classmethod
    def discount_incategory(cls, category_id, percentage):
        if type(percentage) is not int:
            raise ValueError('Скидка должна быть целым числом')
        if not 1 <= percentage <= 70:
            raise ValueError('Скидка должна быть не меньше 1% и не больше 70%')

        paid_apps_incategory = list(cls.objects.filter(price__gt=0, category_id=category_id))
        for app in paid_apps_incategory:
            app.price=(app.price * (Decimal("100") - Decimal(percentage))/ Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return cls.objects.bulk_update(paid_apps_incategory, ['price'])






class Review(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    stars = models.IntegerField(default=5, validators=[MinValueValidator(1, message='Рейтинг не может быть меньше 1'), MaxValueValidator(5, message='Рейтинг не может превышать 5')])
    recommended=models.CharField(max_length=3, default='да')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} -> {self.app.name}"






