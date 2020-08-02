from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Interface(models.Model):
    site_name = models.CharField(max_length = 50)
    img_1 = models.ImageField(upload_to = "slideimage")
    img_2 = models.ImageField(upload_to="slideimage")
    img_3 = models.ImageField(upload_to = "slideimage")

    def __str__(self):
        return str(self.site_name)

class Category(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        ordering = ('name',)
    def __str__(self):
        return str(self.name)



class ProductDetails(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField(max_length=50)
    author = models.CharField(max_length=50,default='')
    product_img1 = models.ImageField(upload_to = 'product_image')
    product_img2 = models.ImageField(upload_to = 'product_image', blank=True)
    product_img3 = models.ImageField(upload_to = 'product_image',blank=True)
    product_img4 = models.ImageField(upload_to = 'product_image',blank=True)
    product_img5 = models.ImageField(upload_to = 'product_image', blank=True)
    product_price = models.IntegerField()
    address = models.CharField(max_length = 50, default='')
    district = models.CharField(max_length=50,default='')
    state = models.CharField(max_length=50,default='')
    contact_no = models.CharField(max_length = 15, default='')
    product_description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

class Profile(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   name = models.CharField(max_length=50, default="")
   pro_img = models.ImageField(upload_to = 'profile_img', default='default/default.jpg')
   bio = models.CharField(max_length=200)
   contact_no = models.CharField(max_length=15, default="")
   email = models.CharField(max_length=50,default="")
   following = models.IntegerField(default=0)
   followers = models.IntegerField(default=0)

   def __str__(self):
       return str(self.user)
class Following(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    followed = models.ManyToManyField(User, related_name = 'followed')
    follower = models.ManyToManyField(User, related_name = 'follower')

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)
    
    @classmethod
    def unFollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.remove(another_account)

    def __str__(self):
        return str(self.user)