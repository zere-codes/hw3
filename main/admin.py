
# Register your models here.
from django.contrib import admin
from .models import Category, App, Review, ShoppingCart

admin.site.register(Category)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'created_at', 'weight_kb', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)
    exclude = ('created_at','favorited_by',)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('app', 'username', 'comment', 'stars','recommended', 'created_at')
    search_fields = ('username', 'app')
    list_filter = ('stars',)

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'app', 'price_when_added', 'add_time')
    list_filter = ('app',)