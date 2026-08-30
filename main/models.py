from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    weight_kb = models.IntegerField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def weight_unit(self):
        if self.weight_kb >= 1000000:
            return f"{self.weight_kb/1000000} GB"
        elif self.weight_kb >= 1000:
            return f"{self.weight_kb / 1000} MB"
        else:
            return f"{self.weight_kb} KB"


class Review(models.Model):
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    stars = models.IntegerField(default=5)
    recommended=models.CharField(max_length=3, default='да')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} -> {self.app.name}"





