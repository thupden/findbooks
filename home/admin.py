from django.contrib import admin
from .models import Interface, ProductDetails, Category, Profile, Following
# Register your models here.
class ProductDetailsAdmin(admin.ModelAdmin):
    list_display = ('category','product', 'author','product_img1', 'product_price','address','district','state','contact_no','date')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'pro_img', 'bio', 'followers', 'following')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(ProductDetails, ProductDetailsAdmin)
admin.site.register(Interface)
admin.site.register(Category)
admin.site.register(Following)
